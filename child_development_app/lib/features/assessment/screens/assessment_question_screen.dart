import 'package:flutter/material.dart';

import '../assessment_model.dart';
import '../services/assessment_service.dart';
import 'assessment_result_screen.dart';

class AssessmentQuestionScreen extends StatefulWidget {
  final Assessment assessment;
  final int childId;
  final bool isTherapist;
  final String? selectedDomain;

  const AssessmentQuestionScreen({
    super.key,
    required this.assessment,
    required this.childId,
    this.isTherapist = false,
    this.selectedDomain,
  });

  @override
  State<AssessmentQuestionScreen> createState() =>
      _AssessmentQuestionScreenState();
}

class _AssessmentQuestionScreenState extends State<AssessmentQuestionScreen> {
  final AssessmentService _service = AssessmentService();

  List<AssessmentQuestion> questions = [];

  Map<int, String> answers = {};
  Map<int, String> remarks = {};

  int? sessionId;
  bool loading = true;
  bool submitting = false;
  String? loadError;

  @override
  void initState() {
    super.initState();

    startAssessment();
  }

  Future<void> startAssessment() async {
    try {
      final result = await _service.startAssessment(
        childId: widget.childId,

        assessmentId: widget.assessment.id!,
      );

      sessionId = result["id"];

      await loadQuestions();
    } catch (e) {
      loadError = e.toString();
      if (mounted) {
        setState(() => loading = false);
        ScaffoldMessenger.of(
          context,
        ).showSnackBar(SnackBar(content: Text(e.toString())));
      }
    }
  }

  Future<void> loadQuestions() async {
    try {
      if (widget.assessment.id == null) {
        throw Exception("Assessment ID missing");
      }

      questions = await _service.getQuestions(
        widget.assessment.id!,
        childId: widget.childId,
        domain: widget.selectedDomain,
      );
    } catch (e) {
      loadError = e.toString();
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

  Future<void> retryLoad() async {
    if (sessionId == null) {
      await startAssessment();
    } else {
      setState(() {
        loading = true;
        loadError = null;
      });
      await loadQuestions();
    }
  }

  Future<void> submitAssessment() async {
    if (submitting || sessionId == null) return;

    if (answers.length != questions.length) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Please answer all questions")),
      );

      return;
    }

    try {
      setState(() => submitting = true);

      for (var question in questions) {
        await _service.submitResponse(
          sessionId: sessionId!,

          questionId: question.id!,

          answer: answers[question.id]!,

          therapistRemark: widget.isTherapist ? remarks[question.id] : null,
        );
      }

      await _service.completeAssessment(
        sessionId: sessionId!,
        childId: widget.childId,
      );

      if (!mounted) return;

      Navigator.pushReplacement(
        context,

        MaterialPageRoute(
          builder: (_) => AssessmentResultScreen(
            sessionId: sessionId!,

            childId: widget.childId,

            isTherapist: widget.isTherapist,
          ),
        ),
      );
    } catch (e) {
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text(e.toString())));
    }
    if (mounted) setState(() => submitting = false);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(widget.assessment.name)),

      body: loading
          ? const Center(child: CircularProgressIndicator())
          : questions.isEmpty
          ? Center(
              child: Padding(
                padding: const EdgeInsets.all(24),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Text(
                      loadError ??
                          "No questions are available for this assessment.",
                    ),
                    const SizedBox(height: 12),
                    FilledButton(
                      onPressed: retryLoad,
                      child: const Text("Retry"),
                    ),
                  ],
                ),
              ),
            )
          : ListView.builder(
              padding: const EdgeInsets.all(16),

              itemCount: questions.length + 1,

              itemBuilder: (_, index) {
                if (index == questions.length) {
                  return SizedBox(
                    width: double.infinity,

                    child: ElevatedButton(
                      onPressed: submitting ? null : submitAssessment,

                      child: Text(
                        submitting ? "Submitting..." : "Submit Assessment",
                      ),
                    ),
                  );
                }

                final question = questions[index];

                return Card(
                  margin: const EdgeInsets.only(bottom: 15),

                  child: Padding(
                    padding: const EdgeInsets.all(16),

                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,

                      children: [
                        Text(
                          question.question,

                          style: const TextStyle(
                            fontSize: 17,

                            fontWeight: FontWeight.bold,
                          ),
                        ),

                        const SizedBox(height: 15),

                        if (widget.assessment.assessmentType ==
                            "PARENT_SCREENING")
                          Wrap(
                            spacing: 8,
                            children: [
                              for (final answer in [
                                "YES",
                                "SOMETIMES/STARTING",
                                "NOT YET",
                              ])
                                ChoiceChip(
                                  label: Text(
                                    answer == "SOMETIMES/STARTING"
                                        ? "Sometimes / Starting"
                                        : answer == "NOT YET"
                                        ? "Not Yet"
                                        : "Yes",
                                  ),
                                  selected: answers[question.id] == answer,
                                  onSelected: (_) => setState(
                                    () => answers[question.id!] = answer,
                                  ),
                                ),
                            ],
                          )
                        else
                          Row(
                            children: [
                              Expanded(
                                child: ElevatedButton(
                                  style: ElevatedButton.styleFrom(
                                    backgroundColor:
                                        answers[question.id] == "YES"
                                        ? Colors.green
                                        : null,
                                  ),

                                  onPressed: () {
                                    setState(() {
                                      answers[question.id!] = "YES";
                                    });
                                  },

                                  child: const Text("YES"),
                                ),
                              ),

                              const SizedBox(width: 10),

                              Expanded(
                                child: ElevatedButton(
                                  style: ElevatedButton.styleFrom(
                                    backgroundColor:
                                        answers[question.id] == "NO"
                                        ? Colors.red
                                        : null,
                                  ),

                                  onPressed: () {
                                    setState(() {
                                      answers[question.id!] = "NO";
                                    });
                                  },

                                  child: const Text("NO"),
                                ),
                              ),
                            ],
                          ),

                        if (widget.isTherapist)
                          Padding(
                            padding: const EdgeInsets.only(top: 12),
                            child: TextField(
                              maxLines: 2,
                              decoration: const InputDecoration(
                                labelText: "Therapist remark",
                                border: OutlineInputBorder(),
                              ),
                              onChanged: (value) {
                                remarks[question.id!] = value;
                              },
                            ),
                          ),
                      ],
                    ),
                  ),
                );
              },
            ),
    );
  }
}
