import 'package:flutter/material.dart';
import 'package:video_player/video_player.dart';

import '../../../core/api/api_service.dart';
import '../../../core/constants/app_constants.dart';

class VoiceNoteAudioPlayer extends StatefulWidget {
  final int voiceNoteId;

  const VoiceNoteAudioPlayer({super.key, required this.voiceNoteId});

  @override
  State<VoiceNoteAudioPlayer> createState() => _VoiceNoteAudioPlayerState();
}

class _VoiceNoteAudioPlayerState extends State<VoiceNoteAudioPlayer> {
  VideoPlayerController? _controller;
  bool _loading = true;
  bool _failed = false;

  @override
  void initState() {
    super.initState();
    _load();
  }

  @override
  void didUpdateWidget(covariant VoiceNoteAudioPlayer oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.voiceNoteId != widget.voiceNoteId) {
      _controller?.dispose();
      _controller = null;
      _loading = true;
      _failed = false;
      _load();
    }
  }

  Future<void> _load() async {
    try {
      final token = await ApiService.getToken();
      if (token == null || token.isEmpty) throw StateError('No session');
      final controller = VideoPlayerController.networkUrl(
        Uri.parse(
          '${AppConstants.baseUrl}/voice-notes/${widget.voiceNoteId}/audio',
        ),
        httpHeaders: {'Authorization': 'Bearer $token'},
      );
      _controller = controller;
      await controller.initialize();
      if (!mounted) return;
      setState(() => _loading = false);
    } catch (_) {
      if (!mounted) return;
      setState(() {
        _loading = false;
        _failed = true;
      });
    }
  }

  @override
  void dispose() {
    _controller?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final controller = _controller;
    if (_loading) {
      return const Row(
        children: [
          SizedBox.square(
            dimension: 20,
            child: CircularProgressIndicator(strokeWidth: 2),
          ),
          SizedBox(width: 10),
          Text('Loading audio…'),
        ],
      );
    }
    if (_failed || controller == null) {
      return const Text('Original audio is unavailable.');
    }
    return Row(
      children: [
        IconButton(
          tooltip: controller.value.isPlaying
              ? 'Pause recording'
              : 'Play recording',
          onPressed: () {
            setState(() {
              controller.value.isPlaying
                  ? controller.pause()
                  : controller.play();
            });
          },
          icon: Icon(
            controller.value.isPlaying ? Icons.pause : Icons.play_arrow,
          ),
        ),
        const Text('Original audio'),
        const SizedBox(width: 12),
        Expanded(
          child: VideoProgressIndicator(controller, allowScrubbing: true),
        ),
      ],
    );
  }
}
