import 'package:dio/dio.dart';

import '../../../core/api/api_service.dart';

class DevelopmentProfileService {
  final Dio _dio = ApiService.dio;

  Future<dynamic> generateProfile(int sessionId) async {
    await ApiService.setToken();

    final response = await _dio.post(
      "/development-profile/generate/$sessionId",
    );

    return response.data;
  }

  Future<dynamic> confirmProfile({
    required int profileId,
    bool confirmed = true,
    String? therapistLevel,
    String? clinicalInterpretation,
  }) async {
    await ApiService.setToken();

    final response = await _dio.put(
      "/development-profile/$profileId/confirm",
      data: {
        "confirmed": confirmed,
        if (therapistLevel != null && therapistLevel.isNotEmpty)
          "therapist_level": therapistLevel,
        if (clinicalInterpretation != null && clinicalInterpretation.isNotEmpty)
          "clinical_interpretation": clinicalInterpretation,
      },
    );

    return response.data;
  }

  Future<List<dynamic>> getSessionProfiles(
    int sessionId, {
    int? childId,
  }) async {
    await ApiService.setToken();
    final response = await _dio.get(
      "/development-profile/session/$sessionId",
      queryParameters: {if (childId != null) "child_id": childId},
    );
    return response.data as List<dynamic>;
  }
}
