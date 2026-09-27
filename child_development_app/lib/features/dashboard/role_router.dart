import 'package:flutter/material.dart';

import 'dashboard_screen.dart';

import '../admin/admin_dashboard.dart';
import '../therapist/therapist_dashboard.dart';
import '../parent/parent_dashboard.dart';



class RoleRouter {


  static Widget getScreen(

    String role,

    int userId,

  ) {



    switch(role.toUpperCase()) {



      case "ADMIN":

        return const AdminDashboard();




      case "THERAPIST":

        return TherapistDashboard(

          therapistId:
              userId,

        );




      case "PARENT":

        return const ParentDashboard();




      default:

        return const DashboardScreen();


    }


  }


}