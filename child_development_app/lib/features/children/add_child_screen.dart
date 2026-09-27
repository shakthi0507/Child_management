import 'package:flutter/material.dart';

import 'children_service.dart';

class AddChildScreen extends StatefulWidget {
  const AddChildScreen({super.key});

  @override
  State<AddChildScreen> createState() =>
      _AddChildScreenState();
}

class _AddChildScreenState
    extends State<AddChildScreen> {
  final service = ChildrenService();

  final nameController =
      TextEditingController();

  final dobController =
      TextEditingController();

  final heightController =
      TextEditingController();

  final weightController =
      TextEditingController();

  String gender = "Male";

  bool loading = false;

  Future<void> save() async {
    if (nameController.text.isEmpty ||
        dobController.text.isEmpty ||
        heightController.text.isEmpty ||
        weightController.text.isEmpty) {
      ScaffoldMessenger.of(context)
          .showSnackBar(
        const SnackBar(
          content: Text(
              "Please fill all fields"),
        ),
      );
      return;
    }

    setState(() {
      loading = true;
    });

    final success =
        await service.addChild(
      name: nameController.text,
      gender: gender,
      dob: dobController.text,
      height: double.parse(
        heightController.text,
      ),
      weight: double.parse(
        weightController.text,
      ),
    );

    setState(() {
      loading = false;
    });

    if (!mounted) return;

    if (success) {
      ScaffoldMessenger.of(context)
          .showSnackBar(
        const SnackBar(
          content:
              Text("Child Added Successfully"),
        ),
      );

      Navigator.pop(context);
    } else {
      ScaffoldMessenger.of(context)
          .showSnackBar(
        const SnackBar(
          content: Text(
              "Failed to add child"),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(
          "Add Child",
        ),
      ),
      body: SingleChildScrollView(
        padding:
            const EdgeInsets.all(20),
        child: Column(
          children: [

            TextField(
              controller:
                  nameController,
              decoration:
                  const InputDecoration(
                labelText: "Name",
                border:
                    OutlineInputBorder(),
              ),
            ),

            const SizedBox(height: 16),

            DropdownButtonFormField<String>(
              initialValue: gender,
              decoration:
                  const InputDecoration(
                labelText: "Gender",
                border:
                    OutlineInputBorder(),
              ),
              items: const [

                DropdownMenuItem(
                  value: "Male",
                  child: Text("Male"),
                ),

                DropdownMenuItem(
                  value: "Female",
                  child: Text("Female"),
                ),

                DropdownMenuItem(
                  value: "Other",
                  child: Text("Other"),
                ),
              ],
              onChanged: (value) {
                setState(() {
                  gender = value!;
                });
              },
            ),

            const SizedBox(height: 16),

            TextField(
              controller:
                  dobController,
              readOnly: true,
              decoration:
                  const InputDecoration(
                labelText:
                    "Date of Birth",
                border:
                    OutlineInputBorder(),
                suffixIcon: Icon(
                  Icons.calendar_today,
                ),
              ),
              onTap: () async {

                final picked =
                    await showDatePicker(
                  context: context,
                  firstDate:
                      DateTime(2000),
                  lastDate:
                      DateTime.now(),
                  initialDate:
                      DateTime.now(),
                );

                if (picked != null) {
                  dobController.text =
                      picked
                          .toIso8601String()
                          .split("T")[0];
                }
              },
            ),

            const SizedBox(height: 16),

            TextField(
              controller:
                  heightController,
              keyboardType:
                  TextInputType.number,
              decoration:
                  const InputDecoration(
                labelText:
                    "Height (cm)",
                border:
                    OutlineInputBorder(),
              ),
            ),

            const SizedBox(height: 16),

            TextField(
              controller:
                  weightController,
              keyboardType:
                  TextInputType.number,
              decoration:
                  const InputDecoration(
                labelText:
                    "Weight (kg)",
                border:
                    OutlineInputBorder(),
              ),
            ),

            const SizedBox(height: 30),

            SizedBox(
              width: double.infinity,
              height: 55,
              child:
                  ElevatedButton.icon(
                icon:
                    const Icon(Icons.save),
                label: loading
                    ? const CircularProgressIndicator(
                        color:
                            Colors.white,
                      )
                    : const Text(
                        "Save Child",
                        style: TextStyle(
                          fontSize: 18,
                        ),
                      ),
                onPressed: loading
                    ? null
                    : save,
              ),
            ),
          ],
        ),
      ),
    );
  }
}