import 'package:flutter/material.dart';

import 'services/auth_service.dart';
import 'login_screen.dart';

class RegisterScreen extends StatefulWidget {
  const RegisterScreen({super.key});

  @override
  State<RegisterScreen> createState() => _RegisterScreenState();
}

class _RegisterScreenState extends State<RegisterScreen> {
  final nameController = TextEditingController();

  final emailController = TextEditingController();

  final phoneController = TextEditingController();

  final passwordController = TextEditingController();

  String role = "PARENT";

  final AuthService authService = AuthService();

  bool loading = false;

  @override
  void dispose() {
    nameController.dispose();

    emailController.dispose();

    phoneController.dispose();

    passwordController.dispose();

    super.dispose();
  }

  Future<void> register() async {
    if (nameController.text.trim().isEmpty ||
        emailController.text.trim().isEmpty ||
        phoneController.text.trim().isEmpty ||
        passwordController.text.isEmpty) {
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(const SnackBar(content: Text("Fill all fields")));

      return;
    }

    setState(() {
      loading = true;
    });

    try {
      await authService.register(
        name: nameController.text.trim(),

        email: emailController.text.trim(),

        phone: phoneController.text.trim(),

        password: passwordController.text,

        role: role,
      );

      if (!mounted) return;

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text("Registration successful"),

          backgroundColor: Colors.green,
        ),
      );

      Navigator.pushReplacement(
        context,

        MaterialPageRoute(builder: (_) => const LoginScreen()),
      );
    } catch (e) {
      print("REGISTER ERROR: $e");

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(e.toString()), backgroundColor: Colors.red),
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

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Vaa · Create account")),

      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),

        child: Column(
          children: [
            TextField(
              controller: nameController,

              decoration: const InputDecoration(
                labelText: "Name",

                border: OutlineInputBorder(),
              ),
            ),

            const SizedBox(height: 15),

            TextField(
              controller: emailController,

              keyboardType: TextInputType.emailAddress,

              decoration: const InputDecoration(
                labelText: "Email",

                border: OutlineInputBorder(),
              ),
            ),

            const SizedBox(height: 15),

            TextField(
              controller: phoneController,

              keyboardType: TextInputType.phone,

              decoration: const InputDecoration(
                labelText: "Phone",

                border: OutlineInputBorder(),
              ),
            ),

            const SizedBox(height: 15),

            TextField(
              controller: passwordController,

              obscureText: true,

              decoration: const InputDecoration(
                labelText: "Password",

                border: OutlineInputBorder(),
              ),
            ),

            const SizedBox(height: 15),

            DropdownButtonFormField<String>(
              value: role,

              items: const [
                DropdownMenuItem(value: "PARENT", child: Text("Parent")),

                DropdownMenuItem(value: "THERAPIST", child: Text("Therapist")),

                DropdownMenuItem(value: "ADMIN", child: Text("Admin")),
              ],

              onChanged: (value) {
                if (value != null) {
                  setState(() {
                    role = value;
                  });
                }
              },

              decoration: const InputDecoration(
                labelText: "Role",

                border: OutlineInputBorder(),
              ),
            ),

            const SizedBox(height: 30),

            SizedBox(
              width: double.infinity,

              height: 50,

              child: ElevatedButton(
                onPressed: loading ? null : register,

                child: loading
                    ? const SizedBox(
                        width: 22,

                        height: 22,

                        child: CircularProgressIndicator(strokeWidth: 2),
                      )
                    : const Text("Register"),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
