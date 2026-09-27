import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree

from app.database.session import SessionLocal
from app.models.assessment import Assessment
from app.models.assessment_question import AssessmentQuestion
from app.models.milestone import Milestone
from app.models.user import User


WORD_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
AGE_HEADING = re.compile(r"LDST\s*[–-]\s*(\d+)\s*MONTHS", re.IGNORECASE)
QUESTION = re.compile(r"^(GM|FM|SL|CG|SE|AD)(\d+)-(\d+)\.\s*(.+)$")
DOMAIN_NAMES = {
    "GM": "Gross Motor",
    "FM": "Fine Motor",
    "SL": "Speech & Language",
    "CG": "Cognition",
    "SE": "Social & Emotional",
    "AD": "Adaptive / Self-Help",
}


def read_paragraphs(path: Path) -> list[str]:
    with zipfile.ZipFile(path) as archive:
        root = ElementTree.fromstring(archive.read("word/document.xml"))
    paragraphs = []
    for paragraph in root.iter(f"{WORD_NS}p"):
        text = "".join(node.text or "" for node in paragraph.iter(f"{WORD_NS}t"))
        if text.strip():
            paragraphs.append(text.strip())
    return paragraphs


def parse_questions(path: Path) -> dict[int, list[dict[str, str]]]:
    current_month = None
    current_question = None
    parsed: dict[int, list[dict[str, str]]] = {}
    for paragraph in read_paragraphs(path):
        heading = AGE_HEADING.search(paragraph)
        if heading:
            current_month = int(heading.group(1))
            parsed.setdefault(current_month, [])
            current_question = None
            continue
        match = QUESTION.match(paragraph)
        if match and current_month is not None:
            code, _, number, text = match.groups()
            current_question = {
                "code": f"{code}{current_month}-{number}",
                "domain": DOMAIN_NAMES[code],
                "question": text,
                "text": text,
            }
            parsed[current_month].append(current_question)
            continue

        if current_question is not None and paragraph.lower().startswith(
            ("example:", "for example:", "details:")
        ):
            current_question["text"] += f"\n{paragraph}"
        elif paragraph.lower().startswith("response:"):
            current_question = None
    return parsed


def import_assessments(path: Path) -> tuple[int, int]:
    parsed = parse_questions(path)
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.role == "ADMIN").first()
        if not admin:
            raise RuntimeError("Create an ADMIN user before importing assessments")

        assessment_count = 0
        question_count = 0
        for month, questions in sorted(parsed.items()):
            name = f"LDST Parent Screening - {month} Months"
            assessment = db.query(Assessment).filter(Assessment.name == name).first()
            if not assessment:
                assessment = Assessment(
                    name=name,
                    description=f"Parent-friendly developmental screening for {month} months.",
                    assessment_type="PARENT_SCREENING",
                    age_group=f"{month} months",
                    domain="Multiple",
                    created_by=admin.id,
                    status="PUBLISHED",
                    version=1,
                )
                db.add(assessment)
                db.flush()
                assessment_count += 1

            existing_questions = (
                db.query(AssessmentQuestion)
                .filter(AssessmentQuestion.assessment_id == assessment.id)
                .all()
            )
            existing_by_code = {
                str(question.milestone.title): question
                for question in existing_questions
                if question.milestone is not None
            }
            existing_text = {question.question for question in existing_questions}
            order = len(existing_questions) + 1
            for item in questions:
                existing = existing_by_code.get(item["code"])
                if existing is not None:
                    # Enrich legacy imported rows with the document's explanation
                    # while preserving their IDs and any linked responses.
                    if existing.question.splitlines()[0] == item["question"]:
                        existing.question = item["text"]
                        existing.milestone.description = item["text"]
                    continue
                if item["question"] in existing_text:
                    continue
                milestone = Milestone(
                    age_group=f"{month} months",
                    expected_month=month,
                    domain=item["domain"],
                    title=item["code"],
                    description=item["text"],
                )
                db.add(milestone)
                db.flush()
                db.add(AssessmentQuestion(
                    assessment_id=assessment.id,
                    milestone_id=milestone.id,
                    question=item["text"],
                    order=order,
                ))
                order += 1
                question_count += 1
                existing_text.add(item["text"])
        db.commit()
        return assessment_count, question_count
    finally:
        db.close()


if __name__ == "__main__":
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("001 Assessment - initial.docx")
    created_assessments, created_questions = import_assessments(source)
    print(f"Imported {created_assessments} assessments and {created_questions} questions")
