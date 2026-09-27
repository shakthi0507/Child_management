import 'package:dio/dio.dart';

import '../../../core/api/api_service.dart';
import '../models/current_user_model.dart';


class UserService {


  final Dio _dio =
      ApiService.dio;



  Future<CurrentUserModel> getCurrentUser() async {


    await ApiService.setToken();


    final response =
        await _dio.get(
      "/auth/me",
    );


    return CurrentUserModel.fromJson(
      response.data,
    );


  }


}
