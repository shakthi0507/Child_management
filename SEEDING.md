# Development Database Setup

`seed.py` is a reset seed. It recreates the development database and inserts the stable relational fixture: users, parents, children, therapists, assignments, milestones, the existing assessment definitions, sessions, responses, profiles, recommendations, goals, milestones, and progress.

Run the two steps below from the backend directory after configuring the virtual environment:

```powershell
.\venv\Scripts\python.exe seed.py
.\venv\Scripts\python.exe -m app.database.import_assessment_docx "001 Assessment - initial.docx"
```

The second command is idempotent. It imports the documented LDST parent-screening assessments for 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, and 36 months, and skips assessments/questions already present.

This two-step process keeps the stable application fixture separate from the external assessment document import. Do not run `seed.py` against a production database: it drops and recreates all tables.

Start the API after setup:

```powershell
uvicorn main:app --host 0.0.0.0 --port 8000
```
