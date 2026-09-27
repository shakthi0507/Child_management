import 'dart:io';

import 'package:dio/dio.dart';
import 'package:flutter/foundation.dart';

import '../../../core/api/api_service.dart';
import '../models/voice_note_model.dart';

class VoiceService {
  final Dio _dio = ApiService.dio;

  // =====================================================
  // Get all voice notes of a child
  //
  // Backend:
  // GET /voice-notes/child/{child_id}
  //
  // =====================================================

  Future<List<VoiceNote>> getChildVoiceNotes(int childId) async {
    await ApiService.setToken();

    try {
      final response = await _dio.get("/voice-notes/child/$childId");

      return (response.data as List)
          .map((json) => VoiceNote.fromJson(json))
          .toList();
    } on DioException catch (e) {
      debugPrint(
        'Loading voice notes failed (HTTP ${e.response?.statusCode ?? "network"})',
      );

      throw Exception(
        e.response?.statusCode == 403
            ? "You are not allowed to view these voice notes."
            : "Failed to load voice notes",
      );
    }
  }

  // =====================================================
  // Upload voice note
  //
  // Backend:
  // POST /voice-notes/upload
  //
  // Form Data:
  // child_id
  // file
  //
  // =====================================================

  Future<VoiceNote> uploadVoice({
    required int childId,

    required File audioFile,
  }) async {
    await ApiService.setToken();

    try {
      final fileName = audioFile.path.split("/").last;

      final formData = FormData.fromMap({
        "child_id": childId,

        "file": await MultipartFile.fromFile(
          audioFile.path,

          filename: fileName,
        ),
      });

      final response = await _dio.post(
        "/voice-notes/upload",

        data: formData,

        options: Options(contentType: "multipart/form-data"),
      );

      return VoiceNote.fromJson(response.data);
    } on DioException catch (e) {
      debugPrint(
        'Voice upload failed (HTTP ${e.response?.statusCode ?? "network"})',
      );

      throw Exception("Voice upload failed");
    }
  }

  // =====================================================
  // Delete voice note
  //
  // Backend needs:
  // DELETE /voice-notes/{id}
  //
  // =====================================================

  Future<bool> deleteVoiceNote(int id) async {
    await ApiService.setToken();

    try {
      final response = await _dio.delete("/voice-notes/$id");

      return response.statusCode == 200;
    } on DioException catch (e) {
      debugPrint(
        'Voice-note delete failed (HTTP ${e.response?.statusCode ?? "network"})',
      );

      return false;
    }
  }

  Future<VoiceNote> reviewVoiceNote({
    required int id,
    required String comment,
    String status = "REVIEWED",
  }) async {
    await ApiService.setToken();
    final response = await _dio.put(
      "/voice-notes/$id/review",
      data: {"therapist_comment": comment, "review_status": status},
    );
    return VoiceNote.fromJson(response.data as Map<String, dynamic>);
  }
}
