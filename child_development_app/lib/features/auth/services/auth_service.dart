import 'package:dio/dio.dart';
import 'package:flutter/foundation.dart';

import '../../../core/api/api_service.dart';
import '../../../core/storage/session_manager.dart';

class AuthService {
  final Dio _dio = ApiService.dio;

  Future<void> register({
    required String name,

    required String email,

    required String phone,

    required String password,

    required String role,
  }) async {
    await _dio.post(
      "/auth/register",

      data: {
        "username": name,

        "email": email,

        "password": password,

        "role": role,
      },
    );
  }

  Future<String> login({
    required String email,

    required String password,
  }) async {
    final response = await _dio.post(
      "/auth/login",

      data: {"username": email, "password": password},

      options: Options(contentType: Headers.formUrlEncodedContentType),
    );

    final token = response.data["access_token"];

    if (token == null || token.isEmpty) {
      throw Exception("Login failed: token missing");
    }

    await ApiService.saveToken(token);

    // Fetch user details after token save

    final user = await getCurrentUser();

    if (user != null) {
      await SessionManager.saveUser(
        email: user["email"] ?? email,

        role: user["role"] ?? "",
      );
    }

    return token;
  }

  Future<Map<String, dynamic>?> getCurrentUser() async {
    try {
      await ApiService.setToken();

      final response = await _dio.get("/auth/me");

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

  Future<List<dynamic>> getUsers() async {
    await ApiService.setToken();

    final response = await _dio.get("/auth/users");

    return response.data;
  }
}
