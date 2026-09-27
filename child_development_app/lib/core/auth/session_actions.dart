import 'package:flutter/material.dart';

import '../api/api_service.dart';
import '../storage/session_manager.dart';
import '../../features/auth/login_screen.dart';


Future<void> logoutAndShowLogin(BuildContext context) async {
  await ApiService.clearToken();
  await SessionManager.clear();
  if (!context.mounted) return;

  Navigator.of(context).pushAndRemoveUntil(
    MaterialPageRoute(builder: (_) => const LoginScreen()),
    (_) => false,
  );
}
