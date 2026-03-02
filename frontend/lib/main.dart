import 'package:flutter/material.dart';

void main() {
  runApp(const UdraChallanApp());
}

class UdraChallanApp extends StatelessWidget {
  const UdraChallanApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Udra Challan Admin Portal',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blueGrey),
        useMaterial3: true,
      ),
      home: const LoginScreen(), // The very first screen users will see
    );
  }
}

class LoginScreen extends StatelessWidget {
  const LoginScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text('Udra Challan Secure Login', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
            const SizedBox(height: 20),
            const Text('Authentication Module goes here.'),
          ],
        ),
      ),
    );
  }
}
