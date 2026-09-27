import 'package:flutter/material.dart';

import '../models/recommendation_model.dart';

import '../services/recommendation_service.dart';

class RecommendationScreen extends StatefulWidget {
  final int childId;

  const RecommendationScreen({super.key, required this.childId});

  @override
  State<RecommendationScreen> createState() => _RecommendationScreenState();
}

class _RecommendationScreenState extends State<RecommendationScreen> {
  final RecommendationService service = RecommendationService();

  Recommendation? recommendation;

  bool loading = true;

  @override
  void initState() {
    super.initState();

    loadRecommendation();
  }

  Future<void> loadRecommendation() async {
    try {
      recommendation = await service.getRecommendation(widget.childId);
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

  Color riskColor(String risk) {
    switch (risk.toUpperCase()) {
      case "LOW":
        return Colors.green;

      case "MEDIUM":
        return Colors.orange;

      case "HIGH":
        return Colors.red;

      default:
        return Colors.grey;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Development Recommendations")),

      body: loading
          ? const Center(child: CircularProgressIndicator())
          : recommendation == null
          ? const Center(child: Text("No recommendation found"))
          : Padding(
              padding: const EdgeInsets.all(20),

              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,

                children: [
                  Card(
                    child: Padding(
                      padding: const EdgeInsets.all(20),

                      child: Column(
                        children: [
                          const Text(
                            "Risk Level",

                            style: TextStyle(
                              fontSize: 18,

                              fontWeight: FontWeight.bold,
                            ),
                          ),

                          const SizedBox(height: 10),

                          Text(
                            "Available",

                            style: TextStyle(
                              fontSize: 28,

                              fontWeight: FontWeight.bold,

                              color: riskColor("LOW"),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),

                  const SizedBox(height: 20),

                  Text(
                    "Active goals: ${recommendation!.activeGoals}",

                    style: const TextStyle(fontSize: 18),
                  ),

                  Text(
                    recommendation!.progressPercentage == null
                        ? "No milestone progress recorded yet."
                        : "Recorded milestone progress: ${recommendation!.progressPercentage!.toStringAsFixed(1)}%",
                    style: const TextStyle(fontSize: 16),
                  ),

                  const SizedBox(height: 20),

                  const Text(
                    "Recommendations",

                    style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                  ),

                  Expanded(
                    child: ListView.builder(
                      itemCount: recommendation!.recommendations.length,

                      itemBuilder: (_, index) {
                        return Card(
                          child: ListTile(
                            leading: const Icon(Icons.check_circle),

                            title: Text(recommendation!.recommendations[index]),
                          ),
                        );
                      },
                    ),
                  ),
                ],
              ),
            ),
    );
  }
}
