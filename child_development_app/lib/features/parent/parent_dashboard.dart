import 'package:flutter/material.dart';

import '../../core/auth/session_actions.dart';
import '../../shared/widgets/vaa_branding.dart';
import '../children/children_screen.dart';

class ParentDashboard extends StatelessWidget {
  const ParentDashboard({super.key});

  void _openChildren(BuildContext context) {
    Navigator.push(
      context,
      MaterialPageRoute(builder: (_) => const ChildrenScreen()),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Vaa · Parent Dashboard'),
        actions: [
          IconButton(
            tooltip: 'Log out',
            icon: const Icon(Icons.logout_rounded),
            onPressed: () => logoutAndShowLogin(context),
          ),
        ],
      ),
      body: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 720),
          child: ListView(
            padding: const EdgeInsets.fromLTRB(18, 12, 18, 24),
            children: [
              const VaaWelcomeBanner(
                title: 'Welcome',
                subtitle: 'A clear place to follow your child’s development.',
              ),
              const SizedBox(height: 24),
              Text(
                'Your child’s care',
                style: Theme.of(
                  context,
                ).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.w800),
              ),
              const SizedBox(height: 8),
              VaaNavigationCard(
                icon: Icons.child_care_rounded,
                title: 'My Children',
                subtitle: 'View child details and activities',
                onTap: () => _openChildren(context),
              ),
              VaaNavigationCard(
                icon: Icons.flag_rounded,
                title: 'Goals',
                subtitle: 'Review your child’s development goals',
                onTap: () => _openChildren(context),
              ),
              VaaNavigationCard(
                icon: Icons.assignment_rounded,
                title: 'Assessments & recommendations',
                subtitle: 'See age-appropriate assessment information',
                onTap: () => _openChildren(context),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
