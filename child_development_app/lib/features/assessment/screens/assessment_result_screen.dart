import 'package:flutter/material.dart';

import '../services/assessment_service.dart';
import '../../development_profile/services/development_profile_service.dart';

class AssessmentResultScreen extends StatefulWidget {
  final int sessionId;

  final int childId;
  final bool isTherapist;

  const AssessmentResultScreen({
    super.key,

    required this.sessionId,

    required this.childId,
    this.isTherapist = false,
  });

  @override
  State<AssessmentResultScreen> createState() => _AssessmentResultScreenState();
}

class _AssessmentResultScreenState extends State<AssessmentResultScreen> {
  final AssessmentService _service = AssessmentService();
  final DevelopmentProfileService _profileService = DevelopmentProfileService();

  Map<String, dynamic>? result;

  bool loading = true;
  List<dynamic> profiles = [];
  int? selectedProfileId;
  final therapistLevelController = TextEditingController();
  final interpretationController = TextEditingController();

  @override
  void initState() {
    super.initState();

    loadResult();
  }

  @override
  void dispose() {
    therapistLevelController.dispose();
    interpretationController.dispose();
    super.dispose();
  }

  Future<void> loadResult() async {
    try {
      result = await _service.getResult(
        widget.sessionId,
        childId: widget.childId,
      );
      profiles = await _profileService.getSessionProfiles(
        widget.sessionId,
        childId: widget.childId,
      );
      if (profiles.isNotEmpty) {
        selectedProfileId = profiles.first["id"] as int;
        therapistLevelController.text =
            profiles.first["therapist_level"]?.toString() ?? "";
        interpretationController.text =
            profiles.first["clinical_interpretation"]?.toString() ?? "";
      }
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

  Future<void> confirmProfile() async {
    if (!widget.isTherapist || selectedProfileId == null) return;
    await _profileService.confirmProfile(
      profileId: selectedProfileId!,
      therapistLevel: therapistLevelController.text.trim(),
      clinicalInterpretation: interpretationController.text.trim(),
    );
    if (!mounted) return;
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text("Clinical interpretation saved")),
    );
  }

  String getPerformanceMessage(double percentage) {
    return "Score is calculated from recorded answers. Review domain results with the therapist.";
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Assessment Result")),

      body: loading
          ? const Center(child: CircularProgressIndicator())
          : result == null
          ? const Center(child: Text("No result found"))
          : Padding(
              padding: const EdgeInsets.all(20),

              child: Card(
                elevation: 4,

                child: Padding(
                  padding: const EdgeInsets.all(25),

                  child: Column(
                    mainAxisSize: MainAxisSize.min,

                    children: [
                      const Icon(Icons.assessment, size: 70),

                      const SizedBox(height: 20),

                      Text(
                        "${result!["percentage"] ?? 0}%",

                        style: const TextStyle(
                          fontSize: 35,

                          fontWeight: FontWeight.bold,
                        ),
                      ),

                      if (profiles.isNotEmpty) ...[
                        const SizedBox(height: 16),
                        const Align(
                          alignment: Alignment.centerLeft,
                          child: Text(
                            "Development domains",
                            style: TextStyle(fontWeight: FontWeight.bold),
                          ),
                        ),
                        for (final profile in profiles)
                          ListTile(
                            contentPadding: EdgeInsets.zero,
                            title: Text(
                              profile["domain"]?.toString() ?? "Domain",
                            ),
                            subtitle: Text(
                              "System level: ${profile["system_level"] ?? "Not scored"}",
                            ),
                            trailing: Text(
                              "${profile["score_percentage"] ?? 0}%",
                            ),
                          ),
                      ],

                      if (widget.isTherapist && profiles.isNotEmpty) ...[
                        const SizedBox(height: 24),
                        DropdownButtonFormField<int>(
                          value: selectedProfileId,
                          decoration: const InputDecoration(
                            labelText: "Profile domain to interpret",
                            border: OutlineInputBorder(),
                          ),
                          items: profiles
                              .map<DropdownMenuItem<int>>(
                                (profile) => DropdownMenuItem<int>(
                                  value: profile["id"] as int,
                                  child: Text(
                                    profile["domain"]?.toString() ?? "Domain",
                                  ),
                                ),
                              )
                              .toList(),
                          onChanged: (id) {
                            final profile = profiles.firstWhere(
                              (item) => item["id"] == id,
                            );
                            setState(() {
                              selectedProfileId = id;
                              therapistLevelController.text =
                                  profile["therapist_level"]?.toString() ?? "";
                              interpretationController.text =
                                  profile["clinical_interpretation"]
                                      ?.toString() ??
                                  "";
                            });
                          },
                        ),
                        const SizedBox(height: 12),
                        TextField(
                          controller: therapistLevelController,
                          decoration: const InputDecoration(
                            labelText: "Therapist development level",
                            border: OutlineInputBorder(),
                          ),
                        ),
                        const SizedBox(height: 12),
                        TextField(
                          controller: interpretationController,
                          maxLines: 4,
                          decoration: const InputDecoration(
                            labelText: "Clinical interpretation",
                            border: OutlineInputBorder(),
                          ),
                        ),
                        const SizedBox(height: 12),
                        SizedBox(
                          width: double.infinity,
                          child: FilledButton.icon(
                            onPressed: confirmProfile,
                            icon: const Icon(Icons.check),
                            label: const Text("Confirm development profile"),
                          ),
                        ),
                      ],

                      const SizedBox(height: 20),

                      Text(
                        getPerformanceMessage(
                          (result!["percentage"] ?? 0).toDouble(),
                        ),

                        textAlign: TextAlign.center,

                        style: const TextStyle(fontSize: 16),
                      ),
                    ],
                  ),
                ),
              ),
            ),
    );
  }
}
