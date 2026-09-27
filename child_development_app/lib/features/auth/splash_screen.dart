import 'package:flutter/material.dart';

import '../../core/api/api_service.dart';
import '../../shared/widgets/vaa_branding.dart';
import '../dashboard/role_router.dart';
import 'login_screen.dart';

class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  @override
  void initState() {
    super.initState();
    checkLogin();
  }

  Future<void> checkLogin() async {
    await Future.delayed(const Duration(seconds: 2));
    final token = await ApiService.getToken();

    if (!mounted) return;

    Map<String, dynamic>? user;
    if (token != null && token.isNotEmpty) {
      user = await ApiService.getCurrentUser();
    }

    if (!mounted) return;

    if (user != null && user['role'] != null && user['id'] != null) {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(
          builder: (_) => RoleRouter.getScreen(user!['role'], user['id']),
        ),
      );
      return;
    }

    await ApiService.clearToken();
    if (!mounted) return;
    Navigator.pushReplacement(
      context,
      MaterialPageRoute(builder: (_) => const LoginScreen()),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const VaaLogo(size: 220),
            const SizedBox(height: 24),
            Text(
              'Vaa',
              style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                fontWeight: FontWeight.w800,
                color: Theme.of(context).colorScheme.primary,
                letterSpacing: 1.2,
              ),
            ),
            const SizedBox(height: 24),
            const SizedBox(
              width: 24,
              height: 24,
              child: CircularProgressIndicator(strokeWidth: 2.5),
            ),
          ],
        ),
      ),
    );
  }
}
