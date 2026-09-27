import 'package:dio/dio.dart';

import '../../../../core/api/api_service.dart';
import '../assessment_model.dart';

class AssessmentService {
  final Dio _dio = ApiService.dio;

  /// Get all assessments
  Future<List<Assessment>> getAssessments() async {
    await ApiService.setToken();

    final response = await _dio.get("/assessments/");

    return (response.data as List).map((e) => Assessment.fromJson(e)).toList();
  }

  /// Start assessment session
  Future<Map<String, dynamic>> startAssessment({
    required int childId,
    required int assessmentId,
  }) async {
    await ApiService.setToken();

    final response = await _dio.post(
      "/assessments/start",
      data: {"child_id": childId, "assessment_id": assessmentId},
    );

    return response.data;
  }

  /// Get questions for an assessment
  Future<List<AssessmentQuestion>> getQuestions(
    int assessmentId, {
    int? childId,
    String? domain,
  }) async {
    await ApiService.setToken();

    final response = await _dio.get(
      "/assessments/$assessmentId/questions",
      queryParameters: {
        if (childId != null) "child_id": childId,
        if (domain != null) "domain": domain,
      },
    );

    return (response.data as List)
        .map((e) => AssessmentQuestion.fromJson(e))
        .toList();
  }

  /// Get assessments for selected child

  Future<List<Assessment>> getChildAssessments(int childId) async {
    await ApiService.setToken();

    final response = await _dio.get("/assessments/child/$childId");

    return (response.data as List).map((e) => Assessment.fromJson(e)).toList();
  }

  /// Get completed and in-progress sessions visible to the signed-in role.
  Future<List<Map<String, dynamic>>> getChildAssessmentHistory(
    int childId,
  ) async {
    await ApiService.setToken();
    final response = await _dio.get("/assessments/child/$childId/sessions");
    return (response.data as List)
        .map((item) => Map<String, dynamic>.from(item as Map))
        .toList();
  }

  Future<List<Map<String, dynamic>>> getSessionResponses(
    int sessionId, {
    required int childId,
  }) async {
    await ApiService.setToken();
    final response = await _dio.get(
      "/assessments/sessions/$sessionId/responses",
      queryParameters: {"child_id": childId},
    );
    return (response.data as List)
        .map((item) => Map<String, dynamic>.from(item as Map))
        .toList();
  }

  /// Submit answer
  Future<void> submitResponse({
    required int sessionId,

    required int questionId,

    required String answer,

    String? therapistRemark,
  }) async {
    await ApiService.setToken();

    await _dio.post(
      "/assessments/responses",

      data: {
        "session_id": sessionId,

        "question_id": questionId,

        "answer": answer,

        if (therapistRemark != null && therapistRemark.trim().isNotEmpty)
          "therapist_remark": therapistRemark.trim(),
      },
    );
  }

  /// Complete assessment
  Future<Map<String, dynamic>> completeAssessment({
    required int sessionId,
    required int childId,
  }) async {
    await ApiService.setToken();

    final response = await _dio.post(
      "/assessments/$sessionId/complete",
      queryParameters: {"child_id": childId},
    );

    return response.data;
  }

  /// Get assessment result
  Future<Map<String, dynamic>> getResult(int sessionId, {int? childId}) async {
    await ApiService.setToken();

    final response = await _dio.get(
      "/assessment-result/$sessionId",
      queryParameters: {if (childId != null) "child_id": childId},
    );

    return response.data;
  }
}
