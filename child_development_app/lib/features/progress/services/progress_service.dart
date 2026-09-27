import 'package:dio/dio.dart';

import '../../../core/api/api_service.dart';
import '../progress_model.dart';


class ProgressService {


  final Dio _dio = ApiService.dio;



  Future<List<Progress>> getGoalProgress(
      int goalId) async {


    await ApiService.setToken();


    final response =
        await _dio.get(
      "/progress/goal/$goalId",
    );


    return (response.data as List)
        .map(
          (e) => Progress.fromJson(e),
        )
        .toList();

  }





  Future<Progress> createProgress(
      Progress progress) async {


    await ApiService.setToken();


    final response =
        await _dio.post(

      "/progress/",

      data: progress.toJson(),

    );


    return Progress.fromJson(
      response.data,
    );

  }

  Future<List<Map<String, dynamic>>> getGoalMilestones(int goalId) async {
    await ApiService.setToken();
    final response = await _dio.get(
      "/goal-milestones/goal/$goalId",
    );
    return (response.data as List)
        .map((item) => Map<String, dynamic>.from(item as Map))
        .toList();
  }


}