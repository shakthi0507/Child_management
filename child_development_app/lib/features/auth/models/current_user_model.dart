class CurrentUserModel {

  final int id;
  final String name;
  final String email;
  final String phone;
  final String role;


  CurrentUserModel({

    required this.id,
    required this.name,
    required this.email,
    required this.phone,
    required this.role,

  });



  factory CurrentUserModel.fromJson(
      Map<String, dynamic> json) {

    return CurrentUserModel(

      id: json["id"],

      name: json["name"] ?? json["username"] ?? "",

      email: json["email"],

      phone: json["phone"] ?? "",

      role: json["role"],

    );

  }

}