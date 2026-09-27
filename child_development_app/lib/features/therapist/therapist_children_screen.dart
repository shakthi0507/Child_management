import 'package:flutter/material.dart';

import '../../shared/models/child_model.dart';
import '../children/child_details_screen.dart';
import '../children/children_service.dart';

class TherapistChildrenScreen extends StatefulWidget {
  final int therapistId;

  const TherapistChildrenScreen({super.key, required this.therapistId});

  @override
  State<TherapistChildrenScreen> createState() =>
      _TherapistChildrenScreenState();
}

class _TherapistChildrenScreenState extends State<TherapistChildrenScreen> {
  final ChildrenService service = ChildrenService();
  late Future<List<ChildModel>> childrenFuture;

  @override
  void initState() {
    super.initState();
    childrenFuture = service.getAssignedChildren();
  }

  Future<void> refreshChildren() async {
    setState(() => childrenFuture = service.getAssignedChildren());
    await childrenFuture;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Assigned Children')),
      body: FutureBuilder<List<ChildModel>>(
        future: childrenFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }

          if (snapshot.hasError) {
            return Center(
              child: Padding(
                padding: const EdgeInsets.all(24),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Icon(
                      Icons.cloud_off_rounded,
                      size: 42,
                      color: Theme.of(context).colorScheme.error,
                    ),
                    const SizedBox(height: 12),
                    Text(
                      'Assigned children could not be loaded.',
                      style: Theme.of(context).textTheme.titleMedium,
                    ),
                    const SizedBox(height: 4),
                    const Text(
                      'Check your connection and try again.',
                      textAlign: TextAlign.center,
                    ),
                    const SizedBox(height: 12),
                    FilledButton.icon(
                      onPressed: refreshChildren,
                      icon: const Icon(Icons.refresh_rounded),
                      label: const Text('Try again'),
                    ),
                  ],
                ),
              ),
            );
          }

          final children = snapshot.data ?? [];
          if (children.isEmpty) {
            return Center(
              child: Padding(
                padding: const EdgeInsets.all(24),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Icon(
                      Icons.child_care_rounded,
                      size: 48,
                      color: Theme.of(context).colorScheme.primary,
                    ),
                    const SizedBox(height: 12),
                    Text(
                      'No assigned children',
                      style: Theme.of(context).textTheme.titleMedium,
                    ),
                    const SizedBox(height: 4),
                    const Text(
                      'Children assigned to you will appear here.',
                      textAlign: TextAlign.center,
                    ),
                  ],
                ),
              ),
            );
          }

          return RefreshIndicator(
            onRefresh: refreshChildren,
            child: Center(
              child: ConstrainedBox(
                constraints: const BoxConstraints(maxWidth: 720),
                child: ListView.builder(
                  padding: const EdgeInsets.fromLTRB(16, 10, 16, 24),
                  itemCount: children.length,
                  itemBuilder: (context, index) {
                    final child = children[index];
                    return Card(
                      child: ListTile(
                        contentPadding: const EdgeInsets.symmetric(
                          horizontal: 16,
                          vertical: 8,
                        ),
                        leading: CircleAvatar(
                          backgroundColor: Theme.of(
                            context,
                          ).colorScheme.primaryContainer,
                          child: Icon(
                            Icons.child_care_rounded,
                            color: Theme.of(context).colorScheme.primary,
                          ),
                        ),
                        title: Text(child.name),
                        subtitle: const Text('Open child profile'),
                        trailing: const Icon(
                          Icons.arrow_forward_ios_rounded,
                          size: 16,
                        ),
                        onTap: () => Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (_) => ChildDetailsScreen(
                              child: child,
                              therapistId: widget.therapistId,
                            ),
                          ),
                        ),
                      ),
                    );
                  },
                ),
              ),
            ),
          );
        },
      ),
    );
  }
}
