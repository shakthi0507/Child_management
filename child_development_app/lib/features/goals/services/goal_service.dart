import 'package:dio/dio.dart';

import '../../../core/api/api_service.dart';
import '../goal_model.dart';

class GoalService {
  final Dio _dio = ApiService.dio;

  // ============================
  // CREATE GOAL
  // POST /goals/
  // ============================

  Future<Goal> createGoal({
    required int childId,

    required int therapistId,

    int? assessmentSessionId,

    required String domain,

    required String currentLevel,

    required String shortTermGoal,

    required String longTermGoal,

    required int durationDays,
  }) async {
    await ApiService.setToken();

    final response = await _dio.post(
      "/goals/",

      data: {
        "child_id": childId,

        "therapist_id": therapistId,

        "assessment_session_id": assessmentSessionId,

        "domain": domain,

        "current_level": currentLevel,

        "short_term_goal": shortTermGoal,

        "long_term_goal": longTermGoal,

        "duration_days": durationDays,
      },
    );

    return Goal.fromJson(response.data as Map<String, dynamic>);
  }

  // ============================
  // GET GOALS BY CHILD
  // GET /goals/{child_id}
  // ============================

  Future<List<Goal>> getGoalsByChild(int childId) async {
    await ApiService.setToken();

    final response = await _dio.get("/goals/child/$childId");

    final List data = response.data;

    return data.map((json) => Goal.fromJson(json)).toList();
  }

  // ============================
  // UPDATE GOAL
  // PUT /goals/{goal_id}
  // ============================

  Future<bool> updateGoal({
    required int goalId,

    required String shortTermGoal,

    required String longTermGoal,

    required int durationDays,

    required String status,
  }) async {
    await ApiService.setToken();

    final response = await _dio.put(
      "/goals/$goalId",

      data: {
        "short_term_goal": shortTermGoal,

        "long_term_goal": longTermGoal,

        "duration_days": durationDays,

        "status": status,
      },
    );

    return response.statusCode == 200;
  }

  // ============================
  // DELETE GOAL
  // DELETE /goals/{goal_id}
  // ============================

  Future<bool> deleteGoal(int goalId) async {
    await ApiService.setToken();

    final response = await _dio.delete("/goals/$goalId");

    return response.statusCode == 200;
  }

  // ============================
  // CREATE MILESTONE
  // POST /goal-milestones/
  // ============================

  Future<dynamic> createMilestone({
    required int goalId,

    required String title,
  }) async {
    await ApiService.setToken();

    final response = await _dio.post(
      "/goal-milestones/",

      data: {"goal_id": goalId, "title": title},
    );

    return response.data;
  }
}
