class VoiceNote {


  final int? id;

  final int childId;

  final int parentId;

  final int? goalId;

  final String audioPath;

  final String language;

  final String transcription;

  final String? domain;

    final int? confidence;

  final String? aiMatchStatus;
    final String? therapistReview;

    final String? aiSummary;

    final String? aiSuggestion;

    final String? reviewStatus;

  final DateTime? createdAt;



  VoiceNote({

    this.id,

    required this.childId,

    required this.parentId,

    this.goalId,

    required this.audioPath,

    required this.language,

    required this.transcription,

    this.domain,
    this.confidence,

    this.aiMatchStatus,
    this.therapistReview,
    this.aiSummary,
    this.aiSuggestion,
    this.reviewStatus,

    this.createdAt,

  });





  factory VoiceNote.fromJson(
      Map<String, dynamic> json) {


    return VoiceNote(


      id:
          json["id"],


      childId:
          json["child_id"] ?? 0,


      parentId:
          json["parent_id"] ?? 0,


      goalId:
          json["goal_id"],


      audioPath:
          json["audio_path"] ?? "",


      language:
          json["language"] ?? "Unknown",


      transcription:
          json["transcribed_text"] ?? "",


      domain:
          json["domain"],

      confidence:
          json["confidence"],


      aiMatchStatus:
          json["ai_match_status"],

      therapistReview:
          json["therapist_review"],

        aiSummary:
          json["ai_summary"],

        aiSuggestion:
          json["ai_suggestion"],

        reviewStatus:
          json["review_status"],


      createdAt:

          json["created_at"] != null

              ? DateTime.tryParse(
                  json["created_at"],
                )

              : null,

    );


  }

}