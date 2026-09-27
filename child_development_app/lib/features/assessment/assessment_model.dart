class Assessment {
  final int? id;
  final String name;
  final String description;
  final String assessmentType;

  const Assessment({
    this.id,
    required this.name,
    required this.description,
    this.assessmentType = "",
  });

  factory Assessment.fromJson(Map<String, dynamic> json) {
    return Assessment(
      id: json["id"],
      name: json["name"] ?? "",
      description: json["description"] ?? "",
      assessmentType: json["assessment_type"] ?? "",
    );
  }

  Map<String, dynamic> toJson() {
    return {"name": name, "description": description};
  }
}

class AssessmentQuestion {
  final int? id;
  final int assessmentId;
  final String question;
  final String? domain;

  const AssessmentQuestion({
    this.id,
    required this.assessmentId,
    required this.question,
    this.domain,
  });

  factory AssessmentQuestion.fromJson(Map<String, dynamic> json) {
    return AssessmentQuestion(
      id: json["id"],

      assessmentId: json["assessment_id"],

      question: json["question"] ?? "",
      domain: json["domain"]?.toString(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      "assessment_id": assessmentId,
      "question": question,
      if (domain != null) "domain": domain,
    };
  }
}
