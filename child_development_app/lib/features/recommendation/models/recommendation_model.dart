class Recommendation {
  final int childId;

  final int activeGoals;

  final double? progressPercentage;

  final List<String> recommendations;

  Recommendation({
    required this.childId,

    required this.activeGoals,

    this.progressPercentage,

    required this.recommendations,
  });

  factory Recommendation.fromJson(Map<String, dynamic> json) {
    return Recommendation(
      childId: json["child_id"] ?? 0,

      activeGoals: json["active_goals"] ?? 0,

      progressPercentage: (json["progress_percentage"] as num?)?.toDouble(),

      recommendations: List<String>.from(json["recommendations"] ?? []),
    );
  }
}
