class ChildSummary {

  final ChildInfo child;

  final int totalGoals;

  final int completedGoals;

  final double successRate;

  final String riskLevel;

  final String summary;



  ChildSummary({

    required this.child,

    required this.totalGoals,

    required this.completedGoals,

    required this.successRate,

    required this.riskLevel,

    required this.summary,

  });




  factory ChildSummary.fromJson(
      Map<String, dynamic> json) {
    final goals = (json["goals"] as List<dynamic>? ?? [])
        .whereType<Map<String, dynamic>>()
        .toList();
    final domains = (json["development_domains"] as List<dynamic>? ?? [])
        .whereType<Map<String, dynamic>>()
        .toList();
    final totalMilestones = goals.fold<int>(
      0,
      (sum, goal) => sum + ((goal["total_milestones"] as num?)?.toInt() ?? 0),
    );
    final completedMilestones = goals.fold<int>(
      0,
      (sum, goal) => sum + ((goal["completed_progress_records"] as num?)?.toInt() ?? 0),
    );
    final successRate = totalMilestones == 0
        ? 0.0
        : completedMilestones / totalMilestones * 100;
    final delayedDomains = domains.where(
      (domain) => (domain["development_level"] ?? "").toString().toUpperCase() == "DELAYED",
    ).length;


    return ChildSummary(


      child:
          ChildInfo.fromJson(
            json["child"],
          ),



      totalGoals:
          goals.length,



      completedGoals:
          goals.where((goal) => (goal["progress"] as num? ?? 0) >= 100).length,



      successRate:
          successRate,



      riskLevel:
          delayedDomains > 1 ? "HIGH" : delayedDomains == 1 ? "MEDIUM" : "LOW",



      summary:
          json["summary"] ?? "",


    );


  }

}





class ChildInfo {


  final int id;

  final String name;

  final String gender;

  final String dob;

  final double height;

  final double weight;



  ChildInfo({

    required this.id,

    required this.name,

    required this.gender,

    required this.dob,

    required this.height,

    required this.weight,

  });




  factory ChildInfo.fromJson(
      Map<String,dynamic> json){


    return ChildInfo(

      id:
          json["id"],

      name:
          json["name"] ?? "",

      gender:
          json["gender"] ?? "",

      dob:
          json["dob"] ?? "",


      height:
          (json["height"] ?? 0)
              .toDouble(),


      weight:
          (json["weight"] ?? 0)
              .toDouble(),

    );


  }

}