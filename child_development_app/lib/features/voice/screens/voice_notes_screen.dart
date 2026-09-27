import 'dart:io';

import 'package:flutter/material.dart';
import 'package:path_provider/path_provider.dart';
import 'package:record/record.dart';

import '../services/voice_service.dart';
import '../models/voice_note_model.dart';
import '../widgets/voice_note_audio_player.dart';

class VoiceNotesScreen extends StatefulWidget {
  final int childId;

  final bool isTherapist;

  const VoiceNotesScreen({
    super.key,

    required this.childId,

    required this.isTherapist,
  });

  @override
  State<VoiceNotesScreen> createState() => _VoiceNotesScreenState();
}

class _VoiceNotesScreenState extends State<VoiceNotesScreen> {
  final VoiceService service = VoiceService();

  final AudioRecorder recorder = AudioRecorder();

  List<VoiceNote> notes = [];

  bool recording = false;

  bool uploading = false;

  bool loading = true;

  String? audioPath;

  String transcription = "";

  DateTime? recordingTime;

  @override
  void initState() {
    super.initState();

    loadNotes();
  }

  @override
  void dispose() {
    recorder.dispose();

    super.dispose();
  }

  Future<void> loadNotes() async {
    try {
      final result = await service.getChildVoiceNotes(widget.childId);

      if (!mounted) return;

      setState(() {
        notes = result;

        loading = false;
      });
    } catch (e) {
      if (mounted) {
        setState(() {
          loading = false;
        });
      }

      debugPrint(e.toString());
    }
  }

  Future<void> startRecording() async {
    final permission = await recorder.hasPermission();
    if (!mounted) return;

    if (!permission) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Microphone permission required")),
      );

      return;
    }

    final directory = await getApplicationDocumentsDirectory();
    if (!mounted) return;

    audioPath =
        "${directory.path}/voice_${DateTime.now().millisecondsSinceEpoch}.m4a";

    await recorder.start(
      const RecordConfig(encoder: AudioEncoder.aacLc),

      path: audioPath!,
    );
    if (!mounted) return;

    setState(() {
      recording = true;

      transcription = "";
    });
  }

  Future<void> stopRecording() async {
    final path = await recorder.stop();
    if (!mounted) return;

    setState(() {
      recording = false;

      audioPath = path;

      recordingTime = DateTime.now();
    });
  }

  Future<void> uploadVoice() async {
    if (audioPath == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Please record voice first")),
      );

      return;
    }

    setState(() {
      uploading = true;
    });

    try {
      final result = await service.uploadVoice(
        childId: widget.childId,

        audioFile: File(audioPath!),
      );

      if (!mounted) return;

      setState(() {
        transcription = result.transcription;
      });

      await loadNotes();
      if (!mounted) return;

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text("Voice uploaded successfully"),

          backgroundColor: Colors.green,
        ),
      );
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(e.toString()), backgroundColor: Colors.red),
      );
    }

    if (mounted) {
      setState(() {
        uploading = false;
      });
    }
  }

  Widget recordingCard() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),

        child: Column(
          children: [
            Row(
              children: [
                Icon(
                  recording ? Icons.fiber_manual_record : Icons.mic,

                  color: recording ? Colors.red : Colors.blue,
                ),

                const SizedBox(width: 10),

                Text(
                  recording
                      ? "Recording..."
                      : audioPath != null
                      ? "Recording Ready"
                      : "No Recording",

                  style: const TextStyle(fontWeight: FontWeight.bold),
                ),
              ],
            ),

            if (audioPath != null)
              Padding(
                padding: const EdgeInsets.only(top: 10),

                child: Text(audioPath!.split("/").last),
              ),

            const SizedBox(height: 15),

            ElevatedButton.icon(
              onPressed: recording ? stopRecording : startRecording,

              icon: Icon(recording ? Icons.stop : Icons.mic),

              label: Text(recording ? "Stop Recording" : "Start Recording"),
            ),

            if (audioPath != null && !recording)
              ElevatedButton.icon(
                onPressed: uploading ? null : uploadVoice,

                icon: uploading
                    ? const SizedBox(
                        width: 18,

                        height: 18,

                        child: CircularProgressIndicator(strokeWidth: 2),
                      )
                    : const Icon(Icons.upload),

                label: Text(uploading ? "Uploading..." : "Upload Voice"),
              ),
          ],
        ),
      ),
    );
  }

  Widget latestResult() {
    if (transcription.isEmpty) {
      return const SizedBox();
    }

    return Card(
      color: Colors.green.shade50,

      child: Padding(
        padding: const EdgeInsets.all(16),

        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,

          children: [
            const Text(
              "Latest AI Result",

              style: TextStyle(fontWeight: FontWeight.bold),
            ),

            const SizedBox(height: 10),

            Text("Transcription:\n$transcription"),
          ],
        ),
      ),
    );
  }

  Future<void> reviewNote(VoiceNote note) async {
    final controller = TextEditingController(text: note.therapistReview ?? "");
    final comment = await showDialog<String>(
      context: context,
      builder: (dialogContext) => AlertDialog(
        title: const Text("Therapist comment"),
        content: TextField(
          controller: controller,
          maxLines: 4,
          decoration: const InputDecoration(hintText: "Add review comment"),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(dialogContext),
            child: const Text("Cancel"),
          ),
          FilledButton(
            onPressed: () =>
                Navigator.pop(dialogContext, controller.text.trim()),
            child: const Text("Save"),
          ),
        ],
      ),
    );
    controller.dispose();
    if (comment == null || comment.isEmpty || note.id == null) return;
    try {
      await service.reviewVoiceNote(id: note.id!, comment: comment);
      await loadNotes();
    } catch (error) {
      if (!mounted) return;
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text("Voice review failed: $error")));
    }
  }

  Widget voiceHistory() {
    if (notes.isEmpty) {
      return const Center(child: Text("No uploaded voice notes"));
    }

    return ListView.builder(
      itemCount: notes.length,

      itemBuilder: (_, index) {
        final note = notes[index];

        return Card(
          margin: const EdgeInsets.only(bottom: 12),

          child: Padding(
            padding: const EdgeInsets.all(15),

            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,

              children: [
                Row(
                  children: [
                    const Icon(Icons.mic),

                    const SizedBox(width: 10),

                    const Text(
                      "Voice Note",

                      style: TextStyle(fontWeight: FontWeight.bold),
                    ),
                  ],
                ),

                const SizedBox(height: 10),

                if (note.id != null)
                              VoiceNoteAudioPlayer(
                                key: ValueKey(note.id),
                                voiceNoteId: note.id!,
                              ),

                const SizedBox(height: 8),

                Text(
                  note.transcription.isEmpty
                      ? "Transcription unavailable. You can listen to the original recording."
                      : note.transcription,
                ),

                const SizedBox(height: 8),

                Text("Language: ${note.language}"),

                if (note.domain != null) Text("Domain: ${note.domain}"),

                if (note.aiMatchStatus != null)
                  Text("AI Status: ${note.aiMatchStatus}"),

                if (note.confidence != null)
                  Text("Match confidence: ${note.confidence}%"),

                if (note.aiSummary != null)
                  Text("AI summary: ${note.aiSummary}"),

                if (note.aiSuggestion != null)
                  Text("AI suggestion: ${note.aiSuggestion}"),

                if (note.therapistReview != null)
                  Text("Therapist comment: ${note.therapistReview}"),

                if (widget.isTherapist && note.id != null)
                  Align(
                    alignment: Alignment.centerRight,
                    child: TextButton.icon(
                      onPressed: () => reviewNote(note),
                      icon: const Icon(Icons.rate_review),
                      label: const Text("Review"),
                    ),
                  ),
              ],
            ),
          ),
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Voice Notes")),

      body: loading
          ? const Center(child: CircularProgressIndicator())
          : Padding(
              padding: const EdgeInsets.all(16),

              child: Column(
                children: [
                  if (!widget.isTherapist) recordingCard(),

                  latestResult(),

                  const SizedBox(height: 10),

                  Expanded(child: voiceHistory()),
                ],
              ),
            ),
    );
  }
}
