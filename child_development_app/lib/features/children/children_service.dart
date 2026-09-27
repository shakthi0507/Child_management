import 'package:dio/dio.dart';

import '../../core/api/api_service.dart';
import '../../shared/models/child_model.dart';



class ChildrenService {


  final Dio _dio =
      ApiService.dio;



  /// Parent: Get own children
  Future<List<ChildModel>> getChildren() async {


    await ApiService.setToken();



    final response =
        await _dio.get(
      "/children/",
    );



    return (response.data as List)

        .map(
          (e) => ChildModel.fromJson(e),
        )

        .toList();

  }





  /// Therapist: Get assigned children
  ///
  /// Uses logged-in therapist token.
  /// Backend:
  /// GET /assignments/my-children
  Future<List<ChildModel>> getAssignedChildren() async {


    await ApiService.setToken();



    final response =
        await _dio.get(
      "/assignments/my-children",
    );



    return (response.data as List)

        .map(
          (e) => ChildModel.fromJson(e),
        )

        .toList();

  }





  /// Add Child
  Future<bool> addChild({

    required String name,

    required String gender,

    required String dob,

    required double height,

    required double weight,

  }) async {


    try {


      await ApiService.setToken();



      final response =
          await _dio.post(

        "/children/",


        data: {


          "name":
              name,


          "gender":
              gender,


          "dob":
              dob,


          "height":
              height,


          "weight":
              weight,


        },

      );



      print(
        "ADD CHILD SUCCESS: ${response.data}",
      );



      return true;



    } on DioException catch(e) {


      print(
        "Status Code: ${e.response?.statusCode}",
      );


      print(
        "Response: ${e.response?.data}",
      );


      return false;



    } catch(e) {


      print(
        "Unknown Error: $e",
      );


      return false;

    }


  }







  /// Update Child
  Future<bool> updateChild({

    required int id,

    required String name,

    required String gender,

    required String dob,

    required double height,

    required double weight,

  }) async {


    try {


      await ApiService.setToken();



      await _dio.put(

        "/children/$id",


        data: {


          "name":
              name,


          "gender":
              gender,


          "dob":
              dob,


          "height":
              height,


          "weight":
              weight,


        },

      );



      return true;



    } on DioException catch(e) {


      print(
        e.response?.data,
      );


      return false;


    }


  }







  /// Delete Child
  Future<bool> deleteChild(
      int id) async {


    try {


      await ApiService.setToken();



      await _dio.delete(

        "/children/$id",

      );



      return true;



    } on DioException catch(e) {


      print(
        e.response?.data,
      );


      return false;


    }


  }


}