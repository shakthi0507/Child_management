import 'package:shared_preferences/shared_preferences.dart';


class SessionManager {


  static Future<void> saveUser({
    required String email,
    required String role,
  }) async {

    final prefs =
        await SharedPreferences.getInstance();


    await prefs.setString(
      "email",
      email,
    );


    await prefs.setString(
      "role",
      role,
    );

  }



  static Future<String?> getEmail() async {

    final prefs =
        await SharedPreferences.getInstance();

    return prefs.getString(
      "email",
    );

  }



  static Future<String?> getRole() async {

    final prefs =
        await SharedPreferences.getInstance();

    return prefs.getString(
      "role",
    );

  }



  static Future<void> clear() async {

    final prefs =
        await SharedPreferences.getInstance();


    await prefs.clear();

  }

}