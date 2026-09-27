import 'package:flutter/material.dart';
import 'package:video_player/video_player.dart';

import '../../core/api/api_service.dart';
import '../../core/constants/app_constants.dart';

class TherapistHelpScreen extends StatefulWidget {
  const TherapistHelpScreen({super.key});

  @override
  State<TherapistHelpScreen> createState() => _TherapistHelpScreenState();
}

class _TherapistHelpScreenState extends State<TherapistHelpScreen> {
  VideoPlayerController? _controller;
  bool _loading = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _initializeVideo();
  }

  Future<void> _initializeVideo() async {
    setState(() {
      _loading = true;
      _error = null;
    });
    await _controller?.dispose();
    _controller = null;
    try {
      final token = await ApiService.getToken();
      if (token == null || token.isEmpty) {
        throw Exception('Please sign in again to view therapist help.');
      }
      final controller = VideoPlayerController.networkUrl(
        Uri.parse('${AppConstants.baseUrl}/therapist/help-video'),
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
        _error = 'The therapist help video could not be loaded. Please retry.';
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
    return Scaffold(
      appBar: AppBar(title: const Text('Vaa · Therapist Help / FAQ')),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: _loading
              ? const CircularProgressIndicator()
              : _error != null || controller == null
              ? Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Text(_error ?? 'The video is unavailable.'),
                    const SizedBox(height: 12),
                    FilledButton.icon(
                      onPressed: _initializeVideo,
                      icon: const Icon(Icons.refresh),
                      label: const Text('Retry'),
                    ),
                  ],
                )
              : Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    AspectRatio(
                      aspectRatio: controller.value.aspectRatio,
                      child: VideoPlayer(controller),
                    ),
                    const SizedBox(height: 12),
                    IconButton.filled(
                      tooltip: controller.value.isPlaying ? 'Pause' : 'Play',
                      onPressed: () {
                        setState(() {
                          controller.value.isPlaying
                              ? controller.pause()
                              : controller.play();
                        });
                      },
                      icon: Icon(
                        controller.value.isPlaying
                            ? Icons.pause
                            : Icons.play_arrow,
                      ),
                    ),
                    VideoProgressIndicator(controller, allowScrubbing: true),
                  ],
                ),
        ),
      ),
    );
  }
}
