import 'package:flutter/material.dart';

import '../../core/auth/session_actions.dart';
import '../../shared/widgets/vaa_branding.dart';
import 'therapist_children_screen.dart';
import 'therapist_help_screen.dart';

class TherapistDashboard extends StatelessWidget {
  final int therapistId;

  const TherapistDashboard({super.key, required this.therapistId});

  void _openAssignedChildren(BuildContext context) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (_) => TherapistChildrenScreen(therapistId: therapistId),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Vaa · Therapist Dashboard'),
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
                title: 'Therapist workspace',
                subtitle: 'Review assigned children and continue their care.',
              ),
              const SizedBox(height: 24),
              Text(
                'Your workspace',
                style: Theme.of(
                  context,
                ).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.w800),
              ),
              const SizedBox(height: 8),
              VaaNavigationCard(
                icon: Icons.child_care_rounded,
                title: 'Assigned children',
                subtitle: 'Open children assigned to you',
                onTap: () => _openAssignedChildren(context),
              ),
              VaaNavigationCard(
                icon: Icons.assignment_rounded,
                title: 'Assessments',
                subtitle: 'Review parent and therapist assessments',
                onTap: () => _openAssignedChildren(context),
              ),
              VaaNavigationCard(
                icon: Icons.help_outline_rounded,
                title: 'Therapist Help / FAQ',
                subtitle: 'Watch the therapist training video',
                onTap: () => Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (_) => const TherapistHelpScreen(),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
