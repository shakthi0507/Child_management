import 'package:flutter/material.dart';

import '../services/assessment_service.dart';
import '../../development_profile/services/development_profile_service.dart';
import '../../voice/models/voice_note_model.dart';
import '../../voice/services/voice_service.dart';
import '../../voice/widgets/voice_note_audio_player.dart';

class ParentAssessmentReviewScreen extends StatefulWidget {
  final int sessionId;
  final int childId;

  const ParentAssessmentReviewScreen({
    super.key,
    required this.sessionId,
    required this.childId,
  });

  @override
  State<ParentAssessmentReviewScreen> createState() =>
      _ParentAssessmentReviewScreenState();
}

class _ParentAssessmentReviewScreenState
    extends State<ParentAssessmentReviewScreen> {
  final _assessmentService = AssessmentService();
  final _profileService = DevelopmentProfileService();
  Map<String, dynamic>? _result;
  List<Map<String, dynamic>> _responses = [];
  List<dynamic> _profiles = [];
  List<VoiceNote> _voiceNotes = [];
  bool _loading = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      final result = await _assessmentService.getResult(
        widget.sessionId,
        childId: widget.childId,
      );
      final responses = await _assessmentService.getSessionResponses(
        widget.sessionId,
        childId: widget.childId,
      );
      final profiles = await _profileService.getSessionProfiles(
        widget.sessionId,
        childId: widget.childId,
      );
      List<VoiceNote> voiceNotes = [];
      try {
        voiceNotes = await VoiceService().getChildVoiceNotes(widget.childId);
      } catch (_) {
        // Assessment results remain reviewable if voice notes are unavailable.
      }
      if (!mounted) return;
      setState(() {
        _result = result;
        _responses = responses;
        _profiles = profiles;
        _voiceNotes = voiceNotes;
        _loading = false;
      });
    } catch (_) {
      if (!mounted) return;
      setState(() {
        _error = 'Could not load this assessment. Please retry.';
        _loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Parent's Assessment Review")),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : _error != null
          ? Center(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Text(_error!),
                  const SizedBox(height: 12),
                  FilledButton(onPressed: _load, child: const Text('Retry')),
                ],
              ),
            )
          : ListView(
              padding: const EdgeInsets.all(16),
              children: [
                if (_result != null) ...[
                  Text('Session status: ${_result!["status"] ?? "Unknown"}'),
                  if (_result!["percentage"] != null)
                    Text('Recorded score: ${_result!["percentage"]}%'),
                  for (final domain in (_result!["domains"] as List? ?? []))
                    ListTile(
                      contentPadding: EdgeInsets.zero,
                      title: Text(domain["domain"]?.toString() ?? 'Domain'),
                      subtitle: Text(
                        'Result: ${domain["status"] ?? "Not available"} · ${domain["percentage"] ?? "—"}%',
                      ),
                    ),
                ],
                if (_profiles.isNotEmpty) ...[
                  const SizedBox(height: 16),
                  const Text(
                    'Development profile',
                    style: TextStyle(fontWeight: FontWeight.bold),
                  ),
                  for (final profile in _profiles)
                    ListTile(
                      contentPadding: EdgeInsets.zero,
                      title: Text(profile['domain']?.toString() ?? 'Domain'),
                      subtitle: Text(
                        'System level: ${profile['system_level'] ?? 'Not available'}'
                        '${profile['therapist_level'] == null ? '' : '\nTherapist level: ${profile['therapist_level']}'}'
                        '${profile['clinical_interpretation'] == null ? '' : '\nClinical interpretation: ${profile['clinical_interpretation']}'}',
                      ),
                    ),
                ],
                const SizedBox(height: 16),
                const Text(
                  "Parent's answers",
                  style: TextStyle(fontWeight: FontWeight.bold),
                ),
                if (_responses.isEmpty)
                  const Padding(
                    padding: EdgeInsets.symmetric(vertical: 12),
                    child: Text('No saved answers are available.'),
                  ),
                for (final response in _responses)
                  Card(
                    child: ListTile(
                      title: Text(
                        response['question']?.toString() ?? 'Question',
                      ),
                      subtitle: Text(
                        'Answer: ${response['answer'] ?? '—'}'
                        '${response['domain'] == null ? '' : '\nDomain: ${response['domain']}'}',
                      ),
                    ),
                  ),
                if (_voiceNotes.isNotEmpty) ...[
                  const SizedBox(height: 16),
                  const Text(
                    'Child voice notes',
                    style: TextStyle(fontWeight: FontWeight.bold),
                  ),
                  const Text(
                    'These notes are child-level records, not tied to this session.',
                  ),
                  for (final note in _voiceNotes)
                    Card(
                      child: Padding(
                        padding: const EdgeInsets.all(12),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            if (note.id != null)
                              VoiceNoteAudioPlayer(voiceNoteId: note.id!),
                            const SizedBox(height: 8),
                            Text(
                              note.transcription.isEmpty
                                  ? 'Transcription unavailable.'
                                  : note.transcription,
                            ),
                          ],
                        ),
                      ),
                    ),
                ],
                const Padding(
                  padding: EdgeInsets.only(top: 12),
                  child: Text(
                    'The child Voice section also contains these notes. They are not linked to individual assessment sessions in the current data model.',
                  ),
                ),
              ],
            ),
    );
  }
}
