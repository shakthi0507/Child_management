import 'package:flutter/material.dart';

import '../../shared/models/child_model.dart';
import 'children_service.dart';

class EditChildScreen extends StatefulWidget {
  final ChildModel child;

  const EditChildScreen({
    super.key,
    required this.child,
  });

  @override
  State<EditChildScreen> createState() => _EditChildScreenState();
}

class _EditChildScreenState extends State<EditChildScreen> {
  final _formKey = GlobalKey<FormState>();

  late TextEditingController _nameController;
  late TextEditingController _heightController;
  late TextEditingController _weightController;

  late String _gender;
  late DateTime _selectedDate;

  bool _isLoading = false;

  final ChildrenService _service = ChildrenService();

  @override
  void initState() {
    super.initState();

    _nameController =
        TextEditingController(text: widget.child.name);

    _heightController =
        TextEditingController(
      text: widget.child.height.toString(),
    );

    _weightController =
        TextEditingController(
      text: widget.child.weight.toString(),
    );

    _gender = widget.child.gender;

    _selectedDate = DateTime.parse(widget.child.dob);
  }

  @override
  void dispose() {
    _nameController.dispose();
    _heightController.dispose();
    _weightController.dispose();
    super.dispose();
  }

  Future<void> _pickDate() async {
    final picked = await showDatePicker(
      context: context,
      initialDate: _selectedDate,
      firstDate: DateTime(2000),
      lastDate: DateTime.now(),
    );

    if (picked != null) {
      setState(() {
        _selectedDate = picked;
      });
    }
  }

  Future<void> _updateChild() async {
    if (!_formKey.currentState!.validate()) {
      return;
    }

    setState(() {
      _isLoading = true;
    });

    final success = await _service.updateChild(
      id: widget.child.id,
      name: _nameController.text.trim(),
      gender: _gender,
      dob: _selectedDate.toIso8601String().split("T").first,
      height: double.parse(_heightController.text),
      weight: double.parse(_weightController.text),
    );

    setState(() {
      _isLoading = false;
    });

    if (!mounted) return;

    if (success) {
      final updatedChild = ChildModel(
        id: widget.child.id,
        name: _nameController.text.trim(),
        gender: _gender,
        dob: _selectedDate.toIso8601String().split("T").first,
        height: double.parse(_heightController.text),
        weight: double.parse(_weightController.text),
      );

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text(
            "Child updated successfully",
          ),
          backgroundColor: Colors.green,
        ),
      );

      Navigator.pop(context, updatedChild);
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text(
            "Failed to update child",
          ),
          backgroundColor: Colors.red,
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Edit Child"),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Form(
          key: _formKey,
          child: Column(
            children: [
              TextFormField(
                controller: _nameController,
                decoration: const InputDecoration(
                  labelText: "Name",
                  border: OutlineInputBorder(),
                ),
                validator: (value) {
                  if (value == null ||
                      value.trim().isEmpty) {
                    return "Enter child's name";
                  }
                  return null;
                },
              ),

              const SizedBox(height: 20),

              DropdownButtonFormField<String>(
                initialValue: _gender,
                decoration: const InputDecoration(
                  labelText: "Gender",
                  border: OutlineInputBorder(),
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
                ],
                onChanged: (value) {
                  setState(() {
                    _gender = value!;
                  });
                },
              ),

              const SizedBox(height: 20),

              InkWell(
                onTap: _pickDate,
                child: InputDecorator(
                  decoration: const InputDecoration(
                    labelText: "Date of Birth",
                    border: OutlineInputBorder(),
                  ),
                  child: Text(
                    _selectedDate
                        .toIso8601String()
                        .split("T")
                        .first,
                  ),
                ),
              ),

              const SizedBox(height: 20),

              TextFormField(
                controller: _heightController,
                keyboardType:
                    TextInputType.number,
                decoration: const InputDecoration(
                  labelText: "Height (cm)",
                  border: OutlineInputBorder(),
                ),
                validator: (value) {
                  if (value == null ||
                      value.isEmpty) {
                    return "Enter height";
                  }

                  final h =
                      double.tryParse(value);

                  if (h == null || h <= 0) {
                    return "Invalid height";
                  }

                  return null;
                },
              ),

              const SizedBox(height: 20),

              TextFormField(
                controller: _weightController,
                keyboardType:
                    TextInputType.number,
                decoration: const InputDecoration(
                  labelText: "Weight (kg)",
                  border: OutlineInputBorder(),
                ),
                validator: (value) {
                  if (value == null ||
                      value.isEmpty) {
                    return "Enter weight";
                  }

                  final w =
                      double.tryParse(value);

                  if (w == null || w <= 0) {
                    return "Invalid weight";
                  }

                  return null;
                },
              ),

              const SizedBox(height: 35),

              SizedBox(
                width: double.infinity,
                height: 50,
                child: ElevatedButton(
                  onPressed: _isLoading
                      ? null
                      : _updateChild,
                  child: _isLoading
                      ? const SizedBox(
                          height: 22,
                          width: 22,
                          child:
                              CircularProgressIndicator(
                            strokeWidth: 2,
                            color: Colors.white,
                          ),
                        )
                      : const Text(
                          "Update Child",
                        ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}