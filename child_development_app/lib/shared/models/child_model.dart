class ChildModel {
  final int id;
  final String name;
  final String gender;
  final String dob;
  final double height;
  final double weight;

  ChildModel({
    required this.id,
    required this.name,
    required this.gender,
    required this.dob,
    required this.height,
    required this.weight,
  });

  factory ChildModel.fromJson(
      Map<String, dynamic> json) {
    return ChildModel(
      id: json["id"],
      name: json["name"],
      gender: json["gender"],
      dob: json["dob"],
      height: ((json["height"] as num?) ?? 0).toDouble(),
      weight: ((json["weight"] as num?) ?? 0).toDouble(),
    );
  }
}