import 'package:dio/dio.dart';
import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../constants/app_constants.dart';

class ApiService {
  static final Dio dio =
      Dio(
          BaseOptions(
            baseUrl: AppConstants.baseUrl,

            connectTimeout: const Duration(seconds: 20),

            receiveTimeout: const Duration(seconds: 30),

            sendTimeout: const Duration(seconds: 30),

            headers: {"Content-Type": "application/json"},
          ),
        )
        ..interceptors.add(
          LogInterceptor(
            request: true,
            requestHeader: false,
            requestBody: false,
            responseHeader: false,
            responseBody: false,
            error: true,
          ),
        );

  static Future<void> saveToken(String token) async {
    final prefs = await SharedPreferences.getInstance();

    await prefs.setString("access_token", token);
  }

  static Future<String?> getToken() async {
    final prefs = await SharedPreferences.getInstance();

    return prefs.getString("access_token");
  }

  static Future<void> setToken() async {
    final token = await getToken();

    if (token != null && token.isNotEmpty) {
      dio.options.headers["Authorization"] = "Bearer $token";
    }
  }

  static Future<Map<String, dynamic>?> getCurrentUser() async {
    await setToken();

    try {
      final response = await dio.get("/auth/me");

      return response.data;
    } catch (e) {
      if (e is DioException) {
        debugPrint(
          'Current-user request failed (HTTP ${e.response?.statusCode ?? "network"})',
        );
      } else {
        debugPrint('Current-user request failed (${e.runtimeType})');
      }

      return null;
    }
  }

  static Future<void> clearToken() async {
    final prefs = await SharedPreferences.getInstance();

    await prefs.remove("access_token");

    dio.options.headers.remove("Authorization");
  }
}
