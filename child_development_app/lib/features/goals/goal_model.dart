class Goal {

  final int? id;

  final int childId;

  final int therapistId;

  final String domain;

  final String currentLevel;

  final String shortTermGoal;

  final String longTermGoal;

  final int durationDays;

  final String status;

  final DateTime? createdAt;


  const Goal({

    this.id,

    required this.childId,

    required this.therapistId,

    required this.domain,

    required this.currentLevel,

    required this.shortTermGoal,

    required this.longTermGoal,

    required this.durationDays,

    required this.status,

    this.createdAt,

  });



  factory Goal.fromJson(
      Map<String, dynamic> json
  ) {

    return Goal(

      id:
          json["id"],


      childId:
          json["child_id"] ?? 0,


      therapistId:
          json["therapist_id"] ?? 0,


      domain:
          json["domain"] ?? "",


      currentLevel:
          json["current_level"] ?? "",


      shortTermGoal:
          json["short_term_goal"] ?? "",


      longTermGoal:
          json["long_term_goal"] ?? "",


      durationDays:
          json["duration_days"] ?? 0,


      status:
          json["status"] ?? "ACTIVE",


      createdAt:
          json["created_at"] != null
              ? DateTime.tryParse(
                  json["created_at"],
                )
              : null,

    );

  }





  Map<String, dynamic> toJson() {

    return {


      "child_id":
          childId,


      "therapist_id":
          therapistId,


      "domain":
          domain,


      "current_level":
          currentLevel,


      "short_term_goal":
          shortTermGoal,


      "long_term_goal":
          longTermGoal,


      "duration_days":
          durationDays,


      "status":
          status,


    };

  }





  Goal copyWith({

    int? id,

    int? childId,

    int? therapistId,

    String? domain,

    String? currentLevel,

    String? shortTermGoal,

    String? longTermGoal,

    int? durationDays,

    String? status,

    DateTime? createdAt,

  }) {


    return Goal(


      id:
          id ?? this.id,


      childId:
          childId ?? this.childId,


      therapistId:
          therapistId ?? this.therapistId,


      domain:
          domain ?? this.domain,


      currentLevel:
          currentLevel ?? this.currentLevel,


      shortTermGoal:
          shortTermGoal ?? this.shortTermGoal,


      longTermGoal:
          longTermGoal ?? this.longTermGoal,


      durationDays:
          durationDays ?? this.durationDays,


      status:
          status ?? this.status,


      createdAt:
          createdAt ?? this.createdAt,


    );

  }





  @override
  String toString() {


    return 'Goal('

        'id: $id, '

        'domain: $domain, '

        'shortTermGoal: $shortTermGoal, '

        'status: $status'

        ')';


  }

}