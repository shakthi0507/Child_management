import 'package:flutter/foundation.dart';
import 'package:dio/dio.dart';

import '../../../core/api/api_service.dart';
import '../models/recommendation_model.dart';


class RecommendationService {

  final Dio _dio = ApiService.dio;


  Future<Recommendation> getRecommendation(int childId) async {

    await ApiService.setToken();

    final response = await _dio.get(
      "/recommendations/$childId",
    );

    debugPrint(
      "RECOMMENDATION RESPONSE: ${response.data}",
    );

    return Recommendation.fromJson(
      response.data,
    );

  }


}
