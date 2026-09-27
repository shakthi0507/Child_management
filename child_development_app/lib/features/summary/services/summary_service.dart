import 'package:dio/dio.dart';

import '../../../core/api/api_service.dart';

import '../models/child_summary_model.dart';



class SummaryService {


  final Dio _dio =
      ApiService.dio;



  Future<ChildSummary>
      getSummary(int childId) async {



    await ApiService.setToken();



    final response =
        await _dio.get(

      "/children/$childId/summary",

    );



    return ChildSummary.fromJson(
      response.data,
    );


  }


}