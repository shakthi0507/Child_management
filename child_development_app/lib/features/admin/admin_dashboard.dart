import 'package:flutter/material.dart';

import '../../core/auth/session_actions.dart';
import '../../shared/widgets/vaa_branding.dart';

class AdminDashboard extends StatelessWidget {
  const AdminDashboard({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Vaa · Admin Dashboard'),
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
                title: 'Administration',
                subtitle: 'Manage therapist accounts and child assignments.',
              ),
              const SizedBox(height: 24),
              Text(
                'Admin tools',
                style: Theme.of(
                  context,
                ).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.w800),
              ),
              const SizedBox(height: 8),
              Card(
                child: ListTile(
                  contentPadding: const EdgeInsets.all(16),
                  leading: const CircleAvatar(
                    child: Icon(Icons.person_add_alt_1_rounded),
                  ),
                  title: const Text('Create Therapist'),
                  subtitle: const Text('Add a new therapist account'),
                ),
              ),
              Card(
                child: ListTile(
                  contentPadding: const EdgeInsets.all(16),
                  leading: const CircleAvatar(
                    child: Icon(Icons.assignment_ind_rounded),
                  ),
                  title: const Text('Assign Child'),
                  subtitle: const Text('Assign a therapist to a child'),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
