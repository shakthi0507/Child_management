class AppConstants {
  static const String baseUrl = String.fromEnvironment(
    "API_BASE_URL",
    defaultValue: "http://192.168.1.11:8000",
  );
}