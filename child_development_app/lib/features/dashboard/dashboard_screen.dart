import 'package:flutter/material.dart';

import '../../core/auth/session_actions.dart';
import '../../shared/widgets/vaa_branding.dart';
import '../auth/services/user_service.dart';
import '../children/children_screen.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  final UserService userService = UserService();
  String username = '';

  @override
  void initState() {
    super.initState();
    loadUser();
  }

  Future<void> loadUser() async {
    try {
      final user = await userService.getCurrentUser();
      if (!mounted) return;
      setState(() => username = user.name);
    } catch (error) {
      debugPrint('User loading failed: ${error.runtimeType}');
    }
  }

  void _openChildren() {
    Navigator.push(
      context,
      MaterialPageRoute(builder: (_) => const ChildrenScreen()),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Center(
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 720),
            child: ListView(
              padding: const EdgeInsets.fromLTRB(18, 18, 18, 24),
              children: [
                VaaWelcomeBanner(
                  title: username.isEmpty
                      ? 'Welcome to Vaa'
                      : 'Welcome, $username',
                  subtitle: 'Supporting child development with your care team.',
                ),
                const SizedBox(height: 24),
                Text(
                  'Explore',
                  style: Theme.of(
                    context,
                  ).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.w800),
                ),
                const SizedBox(height: 8),
                VaaNavigationCard(
                  icon: Icons.flag_rounded,
                  title: 'Goals',
                  subtitle: 'Open a child profile to view development goals',
                  onTap: _openChildren,
                ),
                VaaNavigationCard(
                  icon: Icons.show_chart_rounded,
                  title: 'Progress',
                  subtitle: 'Review progress in a child profile',
                  onTap: _openChildren,
                ),
                VaaNavigationCard(
                  icon: Icons.assignment_rounded,
                  title: 'Assessments',
                  subtitle: 'View assessments for a child',
                  onTap: _openChildren,
                ),
                VaaNavigationCard(
                  icon: Icons.mic_rounded,
                  title: 'Voice notes',
                  subtitle: 'Open voice notes from a child profile',
                  onTap: _openChildren,
                ),
                VaaNavigationCard(
                  icon: Icons.lightbulb_outline_rounded,
                  title: 'Recommendations',
                  subtitle: 'Review recommendations for a child',
                  onTap: _openChildren,
                ),
                VaaNavigationCard(
                  icon: Icons.analytics_outlined,
                  title: 'Child summary',
                  subtitle: 'Open a child profile to view their summary',
                  onTap: _openChildren,
                ),
                const SizedBox(height: 14),
                OutlinedButton.icon(
                  onPressed: () => logoutAndShowLogin(context),
                  icon: const Icon(Icons.logout_rounded),
                  label: const Text('Log out'),
                  style: OutlinedButton.styleFrom(
                    minimumSize: const Size(double.infinity, 50),
                    foregroundColor: Theme.of(context).colorScheme.primary,
                    side: BorderSide(
                      color: Theme.of(context).colorScheme.outline,
                    ),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(14),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
