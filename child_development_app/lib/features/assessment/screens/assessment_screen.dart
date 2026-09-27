import 'package:flutter/material.dart';

import '../assessment_model.dart';
import '../services/assessment_service.dart';
import 'assessment_question_screen.dart';
import 'assessment_result_screen.dart';
import 'parent_assessment_review_screen.dart';

class AssessmentScreen extends StatefulWidget {
  final int childId;
  final bool isTherapist;

  const AssessmentScreen({
    super.key,
    required this.childId,
    this.isTherapist = false,
  });

  @override
  State<AssessmentScreen> createState() => _AssessmentScreenState();
}

class _AssessmentScreenState extends State<AssessmentScreen> {
  final AssessmentService _service = AssessmentService();
  List<Assessment> assessments = [];
  List<Map<String, dynamic>> assessmentHistory = [];
  final Map<int, List<AssessmentQuestion>> questionsByAssessment = {};
  String? selectedDomain;
  String? loadError;
  bool loading = true;

  List<String> get availableDomains =>
      questionsByAssessment.values
          .expand((questions) => questions)
          .map((question) => question.domain)
          .whereType<String>()
          .where((domain) => domain.isNotEmpty)
          .toSet()
          .toList()
        ..sort();

  List<Assessment> get visibleAssessments {
    if (!widget.isTherapist || selectedDomain == null) return assessments;
    return assessments.where((assessment) {
      final id = assessment.id;
      return id != null &&
          (questionsByAssessment[id] ?? []).any(
            (question) => question.domain == selectedDomain,
          );
    }).toList();
  }

  List<Map<String, dynamic>> get parentSessions => assessmentHistory
      .where((session) => session["assessment_type"] == "PARENT_SCREENING")
      .toList();

  List<Map<String, dynamic>> get therapistSessions => assessmentHistory
      .where((session) => session["assessment_type"] == "THERAPIST_ASSESSMENT")
      .toList();

  @override
  void initState() {
    super.initState();
    loadAssessments();
  }

  Future<void> loadAssessments() async {
    if (!mounted) return;
    setState(() {
      loading = true;
      loadError = null;
    });

    try {
      final loaded = await _service.getChildAssessments(widget.childId);
      final history = await _service.getChildAssessmentHistory(widget.childId);
      final questionMap = <int, List<AssessmentQuestion>>{};
      if (widget.isTherapist) {
        final assessmentsWithIds = loaded.where((item) => item.id != null);
        final results = await Future.wait(
          assessmentsWithIds.map(
            (assessment) =>
                _service.getQuestions(assessment.id!, childId: widget.childId),
          ),
        );
        var index = 0;
        for (final assessment in assessmentsWithIds) {
          questionMap[assessment.id!] = results[index++];
        }
      }

      if (!mounted) return;
      setState(() {
        assessments = loaded;
        assessmentHistory = history;
        questionsByAssessment
          ..clear()
          ..addAll(questionMap);
        if (selectedDomain != null &&
            !availableDomains.contains(selectedDomain)) {
          selectedDomain = null;
        }
      });
    } catch (_) {
      if (!mounted) return;
      setState(
        () => loadError = 'Assessments could not be loaded. Please retry.',
      );
    } finally {
      if (mounted) setState(() => loading = false);
    }
  }

  void openAssessment(Assessment assessment) {
    if (assessment.id == null) return;
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (_) => AssessmentQuestionScreen(
          assessment: assessment,
          childId: widget.childId,
          isTherapist: widget.isTherapist,
          selectedDomain: widget.isTherapist ? selectedDomain : null,
        ),
      ),
    ).then((_) => loadAssessments());
  }

  void openSession(Map<String, dynamic> session) {
    final sessionId = (session["id"] as num?)?.toInt();
    if (sessionId == null) return;
    final isParentScreening = session["assessment_type"] == "PARENT_SCREENING";
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (_) => isParentScreening
            ? ParentAssessmentReviewScreen(
                sessionId: sessionId,
                childId: widget.childId,
              )
            : AssessmentResultScreen(
                sessionId: sessionId,
                childId: widget.childId,
                isTherapist: widget.isTherapist,
              ),
      ),
    );
  }

  Widget _historyList(List<Map<String, dynamic>> sessions) {
    if (sessions.isEmpty) {
      return const Center(child: Text('No completed assessments to review.'));
    }
    return RefreshIndicator(
      onRefresh: loadAssessments,
      child: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          for (final session in sessions)
            Card(
              child: ListTile(
                leading: const Icon(Icons.assignment_turned_in_outlined),
                title: Text(
                  session["assessment_name"]?.toString() ?? "Assessment",
                ),
                subtitle: Text(
                  '${session["status"] ?? "Unknown"} · ${session["created_at"] ?? ""}',
                ),
                trailing: const Icon(Icons.chevron_right),
                onTap: session["status"] == "COMPLETED"
                    ? () => openSession(session)
                    : null,
              ),
            ),
        ],
      ),
    );
  }

  Widget _parentAssessmentReview() => _historyList(parentSessions);

  Widget _therapistAssessmentTab() {
    final domains = availableDomains;
    final visible = visibleAssessments;
    return Column(
      children: [
        if (domains.isNotEmpty)
          Padding(
            padding: const EdgeInsets.fromLTRB(16, 16, 16, 8),
            child: DropdownButtonFormField<String>(
              initialValue: selectedDomain,
              decoration: const InputDecoration(
                labelText: "Assessment category",
                border: OutlineInputBorder(),
              ),
              items: domains
                  .map(
                    (domain) =>
                        DropdownMenuItem(value: domain, child: Text(domain)),
                  )
                  .toList(),
              onChanged: (value) => setState(() => selectedDomain = value),
            ),
          ),
        Expanded(
          child: RefreshIndicator(
            onRefresh: loadAssessments,
            child: ListView(
              padding: const EdgeInsets.all(16),
              children: [
                if (therapistSessions.isNotEmpty) ...[
                  const Text(
                    'Previous therapist assessments',
                    style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                  ),
                  ...therapistSessions.map(
                    (session) => Card(
                      child: ListTile(
                        title: Text(
                          session["assessment_name"]?.toString() ??
                              "Assessment",
                        ),
                        subtitle: Text(
                          '${session["status"]} · ${session["created_at"] ?? ""}',
                        ),
                        trailing: const Icon(Icons.chevron_right),
                        onTap: session["status"] == "COMPLETED"
                            ? () => openSession(session)
                            : null,
                      ),
                    ),
                  ),
                  const SizedBox(height: 16),
                ],
                if (assessments.isEmpty)
                  const Center(
                    child: Text('No therapist assessments available.'),
                  )
                else if (domains.isEmpty)
                  const Center(
                    child: Text(
                      'No therapist assessment categories have questions yet.',
                      textAlign: TextAlign.center,
                    ),
                  )
                else if (selectedDomain == null)
                  const Center(
                    child: Text('Select an assessment category to continue.'),
                  )
                else if (visible.isEmpty)
                  const Center(
                    child: Text(
                      'No assessment is available for this category.',
                    ),
                  )
                else
                  ...visible.map(
                    (assessment) => Card(
                      elevation: 3,
                      margin: const EdgeInsets.only(bottom: 16),
                      child: Padding(
                        padding: const EdgeInsets.all(18),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              assessment.name,
                              style: const TextStyle(
                                fontSize: 20,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            const SizedBox(height: 8),
                            Text(assessment.description),
                            const SizedBox(height: 15),
                            SizedBox(
                              width: double.infinity,
                              child: ElevatedButton.icon(
                                icon: const Icon(Icons.play_arrow),
                                label: const Text("Start Assessment"),
                                onPressed: () => openAssessment(assessment),
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                  ),
              ],
            ),
          ),
        ),
      ],
    );
  }

  Widget _parentAssessments() {
    final parentAssessmentList = assessmentHistory
        .where((session) => session["assessment_type"] == "PARENT_SCREENING")
        .toList();
    return RefreshIndicator(
      onRefresh: loadAssessments,
      child: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          if (parentAssessmentList.isNotEmpty) ...[
            const Text(
              'Previous assessments',
              style: TextStyle(fontWeight: FontWeight.bold),
            ),
            ...parentAssessmentList.map(
              (session) => Card(
                child: ListTile(
                  title: Text(
                    session["assessment_name"]?.toString() ?? "Assessment",
                  ),
                  subtitle: Text(
                    '${session["status"]} · ${session["created_at"] ?? ""}',
                  ),
                  onTap: session["status"] == "COMPLETED"
                      ? () => openSession(session)
                      : null,
                ),
              ),
            ),
            const SizedBox(height: 12),
          ],
          if (assessments.isEmpty)
            const Padding(
              padding: EdgeInsets.only(top: 80),
              child: Center(
                child: Text("No assessments available for this child's age."),
              ),
            )
          else
            ...assessments.map(
              (assessment) => Card(
                elevation: 3,
                margin: const EdgeInsets.only(bottom: 16),
                child: Padding(
                  padding: const EdgeInsets.all(18),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        assessment.name,
                        style: const TextStyle(
                          fontSize: 20,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 8),
                      Text(assessment.description),
                      const SizedBox(height: 15),
                      SizedBox(
                        width: double.infinity,
                        child: ElevatedButton.icon(
                          icon: const Icon(Icons.play_arrow),
                          label: const Text("Start Assessment"),
                          onPressed: () => openAssessment(assessment),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: widget.isTherapist ? 2 : 1,
      child: Scaffold(
        appBar: AppBar(
          title: const Text("Assessments"),
          bottom: widget.isTherapist
              ? const TabBar(
                  isScrollable: true,
                  tabs: [
                    Tab(text: "Parent's Assessment Review"),
                    Tab(text: "Therapist Assessment"),
                  ],
                )
              : null,
        ),
        body: loading
            ? const Center(child: CircularProgressIndicator())
            : loadError != null
            ? Center(
                child: Padding(
                  padding: const EdgeInsets.all(24),
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Text(loadError!),
                      const SizedBox(height: 12),
                      FilledButton(
                        onPressed: loadAssessments,
                        child: const Text("Retry"),
                      ),
                    ],
                  ),
                ),
              )
            : widget.isTherapist
            ? TabBarView(
                children: [
                  _parentAssessmentReview(),
                  _therapistAssessmentTab(),
                ],
              )
            : _parentAssessments(),
      ),
    );
  }
}
