import 'package:flutter/material.dart';
import 'package:dio/dio.dart';

import 'services/auth_service.dart';
import '../dashboard/role_router.dart';
import '../../core/api/api_service.dart';
import '../../shared/widgets/vaa_branding.dart';

import 'register_screen.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final TextEditingController emailController = TextEditingController();

  final TextEditingController passwordController = TextEditingController();

  final AuthService authService = AuthService();

  bool loading = false;

  @override
  void dispose() {
    emailController.dispose();

    passwordController.dispose();

    super.dispose();
  }

  Future<void> login() async {
    if (emailController.text.trim().isEmpty ||
        passwordController.text.isEmpty) {
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(const SnackBar(content: Text("Enter email and password")));

      return;
    }

    setState(() {
      loading = true;
    });

    try {
      final token = await authService.login(
        email: emailController.text.trim(),

        password: passwordController.text,
      );

      if (token.isEmpty) {
        throw Exception("Invalid credentials");
      }

      await ApiService.setToken();

      final user = await ApiService.getCurrentUser();

      if (user == null) {
        throw Exception("Unable to fetch user details");
      }

      if (!mounted) return;

      Navigator.pushReplacement(
        context,

        MaterialPageRoute(
          builder: (_) => RoleRouter.getScreen(user["role"], user["id"]),
        ),
      );
    } catch (e) {
      final message = _loginErrorMessage(e);
      if (e is DioException) {
        debugPrint(
          'Login request failed (HTTP ${e.response?.statusCode ?? "network"})',
        );
      } else {
        debugPrint('Login failed (${e.runtimeType})');
      }

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(message), backgroundColor: Colors.red),
        );
      }
    } finally {
      if (mounted) {
        setState(() {
          loading = false;
        });
      }
    }
  }

  String _loginErrorMessage(Object error) {
    if (error is DioException) {
      final status = error.response?.statusCode;
      if (status == 401) return 'Invalid username or password';
      if (status == 403) return 'You are not permitted to sign in.';
      if (error.response == null) {
        return 'Unable to connect. Check your connection and try again.';
      }
    }
    return 'Unable to sign in. Please try again.';
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: LayoutBuilder(
          builder: (context, constraints) => SingleChildScrollView(
            padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 20),
            child: ConstrainedBox(
              constraints: BoxConstraints(
                minHeight: constraints.maxHeight - 40,
              ),
              child: Center(
                child: ConstrainedBox(
                  constraints: const BoxConstraints(maxWidth: 440),
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      const VaaLogo(size: 184),
                      const SizedBox(height: 12),
                      Text(
                        'Welcome to Vaa',
                        style: Theme.of(context).textTheme.headlineSmall
                            ?.copyWith(
                              fontWeight: FontWeight.w800,
                              color: Theme.of(context).colorScheme.primary,
                            ),
                      ),
                      const SizedBox(height: 6),
                      Text(
                        'Sign in to continue your child’s development journey.',
                        textAlign: TextAlign.center,
                        style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                          color: Theme.of(context).colorScheme.onSurfaceVariant,
                        ),
                      ),
                      const SizedBox(height: 28),
                      Card(
                        child: Padding(
                          padding: const EdgeInsets.all(20),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.stretch,
                            children: [
                              TextField(
                                controller: emailController,
                                keyboardType: TextInputType.emailAddress,
                                textInputAction: TextInputAction.next,
                                autofillHints: const [AutofillHints.username],
                                decoration: const InputDecoration(
                                  labelText: 'Email',
                                  prefixIcon: Icon(Icons.mail_outline_rounded),
                                ),
                              ),
                              const SizedBox(height: 16),
                              TextField(
                                controller: passwordController,
                                obscureText: true,
                                textInputAction: TextInputAction.done,
                                autofillHints: const [AutofillHints.password],
                                onSubmitted: (_) => loading ? null : login(),
                                decoration: const InputDecoration(
                                  labelText: 'Password',
                                  prefixIcon: Icon(Icons.lock_outline_rounded),
                                ),
                              ),
                              const SizedBox(height: 22),
                              ElevatedButton(
                                onPressed: loading ? null : login,
                                child: loading
                                    ? const SizedBox(
                                        width: 22,
                                        height: 22,
                                        child: CircularProgressIndicator(
                                          strokeWidth: 2,
                                          color: Colors.white,
                                        ),
                                      )
                                    : const Text('Sign in'),
                              ),
                              const SizedBox(height: 8),
                              TextButton(
                                onPressed: () => Navigator.push(
                                  context,
                                  MaterialPageRoute(
                                    builder: (_) => const RegisterScreen(),
                                  ),
                                ),
                                child: const Text('Create new account'),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
