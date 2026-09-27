class Progress {

  final int? id;

  final int goalId;

  final int milestoneId;

  final int? updatedBy;

  final String status;

  final String? notes;

  final DateTime? createdAt;


  const Progress({

    this.id,

    required this.goalId,

    required this.milestoneId,

    this.updatedBy,

    required this.status,

    this.notes,

    this.createdAt,

  });



  factory Progress.fromJson(
      Map<String,dynamic> json) {

    return Progress(

      id: json["id"],

      goalId: json["goal_id"],

      milestoneId: json["milestone_id"],

      updatedBy: json["updated_by"],

      status: json["status"] ?? "PENDING",

      notes: json["notes"],

      createdAt:
          json["created_at"] != null
              ? DateTime.tryParse(
                  json["created_at"]
                )
              : null,

    );

  }



  Map<String,dynamic> toJson(){

    return {

      "goal_id": goalId,

      "milestone_id": milestoneId,

      "status": status,

      "notes": notes,

    };

  }

}