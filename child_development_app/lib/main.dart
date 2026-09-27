import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';

import 'core/constants/app_constants.dart';
import 'features/auth/splash_screen.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  if (kReleaseMode && !AppConstants.baseUrl.startsWith('https://')) {
    throw StateError(
      'Release builds require an HTTPS API_BASE_URL. Rebuild with '
      '--dart-define=API_BASE_URL=https://<your-api-domain>.',
    );
  }
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: "Vaa",

      themeMode: ThemeMode.light,

      theme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xff438FCB),
          primary: const Color(0xff17366F),
          secondary: const Color(0xff438FCB),
          surface: Colors.white,
        ),
        scaffoldBackgroundColor: const Color(0xffF4F7FB),
        appBarTheme: const AppBarTheme(
          centerTitle: false,
          elevation: 0,
          scrolledUnderElevation: 1,
          backgroundColor: Color(0xffF4F7FB),
          foregroundColor: Color(0xff17366F),
          titleTextStyle: TextStyle(
            color: Color(0xff17366F),
            fontSize: 20,
            fontWeight: FontWeight.w700,
          ),
        ),
        cardTheme: CardThemeData(
          elevation: 0,
          color: Colors.white,
          surfaceTintColor: Colors.transparent,
          margin: const EdgeInsets.symmetric(vertical: 7),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(18),
            side: const BorderSide(color: Color(0xffE5EAF2)),
          ),
        ),
        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
            minimumSize: const Size(double.infinity, 52),
            elevation: 0,
            backgroundColor: const Color(0xff17366F),
            foregroundColor: Colors.white,
            textStyle: const TextStyle(fontWeight: FontWeight.w700),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(14),
            ),
          ),
        ),
        inputDecorationTheme: InputDecorationTheme(
          filled: true,
          fillColor: const Color(0xffF8FAFD),
          contentPadding: const EdgeInsets.symmetric(
            horizontal: 16,
            vertical: 17,
          ),
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(14),
            borderSide: const BorderSide(color: Color(0xffDCE4EF)),
          ),
          enabledBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(14),
            borderSide: const BorderSide(color: Color(0xffDCE4EF)),
          ),
          focusedBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(14),
            borderSide: const BorderSide(color: Color(0xff438FCB), width: 1.5),
          ),
        ),
        snackBarTheme: SnackBarThemeData(
          behavior: SnackBarBehavior.floating,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
          ),
        ),
        textTheme: Typography.material2021().black.apply(
          bodyColor: const Color(0xff26354D),
          displayColor: const Color(0xff17366F),
        ),
      ),

      home: const SplashScreen(),
    );
  }
}
