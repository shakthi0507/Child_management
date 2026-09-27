import 'package:flutter/material.dart';

import '../services/goal_service.dart';

class AddGoalScreen extends StatefulWidget {
  final int childId;
  final int therapistId;
  final int? assessmentSessionId;

  const AddGoalScreen({
    super.key,
    required this.childId,
    required this.therapistId,
    this.assessmentSessionId,
  });

  @override
  State<AddGoalScreen> createState() => _AddGoalScreenState();
}

class _AddGoalScreenState extends State<AddGoalScreen> {
  final _formKey = GlobalKey<FormState>();

  final shortTermController = TextEditingController();

  final longTermController = TextEditingController();

  final durationController = TextEditingController();

  final currentLevelController = TextEditingController();

  String? selectedDomain;

  final GoalService service = GoalService();

  bool loading = false;

  @override
  void dispose() {
    shortTermController.dispose();

    longTermController.dispose();

    durationController.dispose();

    currentLevelController.dispose();

    super.dispose();
  }

  Future<void> saveGoal() async {
    if (!_formKey.currentState!.validate()) {
      return;
    }

    if (selectedDomain == null) return;

    setState(() {
      loading = true;
    });

    try {
      await service.createGoal(
        childId: widget.childId,

        therapistId: widget.therapistId,

        assessmentSessionId: widget.assessmentSessionId,

        domain: selectedDomain!,

        currentLevel: currentLevelController.text.trim(),

        shortTermGoal: shortTermController.text.trim(),

        longTermGoal: longTermController.text.trim(),

        durationDays: int.parse(durationController.text.trim()),
      );

      if (!mounted) return;

      Navigator.pop(context, true);
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(
          context,
        ).showSnackBar(SnackBar(content: Text(e.toString())));
      }
    }

    if (mounted) {
      setState(() {
        loading = false;
      });
    }
  }

  Widget buildField(TextEditingController controller, String label) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 18),

      child: TextFormField(
        controller: controller,

        validator: (value) {
          if (value == null || value.trim().isEmpty) {
            return "$label is required";
          }

          return null;
        },

        decoration: InputDecoration(
          labelText: label,

          border: OutlineInputBorder(borderRadius: BorderRadius.circular(15)),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Add Goal")),

      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),

        child: Form(
          key: _formKey,

          child: Column(
            children: [
              buildField(shortTermController, "Short Term Goal"),

              DropdownButtonFormField<String>(
                value: selectedDomain,
                validator: (value) =>
                    value == null ? "Select a development domain" : null,
                decoration: const InputDecoration(
                  labelText: "Development domain",
                  border: OutlineInputBorder(),
                ),
                items:
                    const [
                          "Gross Motor",
                          "Fine Motor",
                          "Speech & Language",
                          "Cognition",
                          "Social & Emotional",
                          "Adaptive / Self-Help",
                        ]
                        .map(
                          (domain) => DropdownMenuItem<String>(
                            value: domain,
                            child: Text(domain),
                          ),
                        )
                        .toList(),
                onChanged: (value) {
                  if (value != null) {
                    setState(() => selectedDomain = value);
                  }
                },
              ),

              const SizedBox(height: 18),

              buildField(
                currentLevelController,
                "Current Level / Therapist Interpretation",
              ),

              buildField(longTermController, "Long Term Goal"),

              buildField(durationController, "Duration Days"),

              const SizedBox(height: 30),

              SizedBox(
                width: double.infinity,

                height: 55,

                child: ElevatedButton(
                  onPressed: loading ? null : saveGoal,

                  child: loading
                      ? const CircularProgressIndicator()
                      : const Text("Save Goal"),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
