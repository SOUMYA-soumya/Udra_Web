import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dashboard.dart'; // Added the dashboard import

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
        // Using a professional corporate blue theme for the web portal
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF1E3A8A)),
        useMaterial3: true,
      ),
      home: const LoginScreen(),
    );
  }
}

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final TextEditingController _usernameController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  bool _isLoading = false;

  Future<void> _attemptLogin() async {
    setState(() {
      _isLoading = true;
    });

    // Development endpoint matching your local Flask setup
    final url = Uri.parse('https://udra-web-api.onrender.com/api/login');
    
    try {
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'username': _usernameController.text,
          'password': _passwordController.text,
        }),
      );

      final responseData = jsonDecode(response.body);

      // Handle the API Response based on our strict architecture rules
      if (response.statusCode == 200) {
        // Success: Audit log recorded in DB, proceed to dashboard
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Welcome back, ${responseData['user']['full_name']}'),
            backgroundColor: Colors.green,
          ),
        );
        
        // Replaced the TODO with the actual Dashboard routing
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(
            builder: (context) => DashboardScreen(userData: responseData['user']),
          ),
        );
        
      } else {
        // Failure: Show the specific error (e.g., "Account is Inactive")
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(responseData['error'] ?? 'Authentication failed'),
            backgroundColor: Colors.redAccent,
          ),
        );
      }
    } catch (e) {
      // Catch network errors if the Flask server isn't running
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('System offline. Cannot connect to Udra Auth Server.'),
          backgroundColor: Colors.red,
        ),
      );
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[100], // Light grey background for web
      body: Center(
        child: Container(
          constraints: const BoxConstraints(maxWidth: 400),
          padding: const EdgeInsets.all(32.0),
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(12),
            boxShadow: const [
              BoxShadow(color: Colors.black12, blurRadius: 15, spreadRadius: 2)
            ],
          ),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Icon(Icons.admin_panel_settings, size: 64, color: Color(0xFF1E3A8A)),
              const SizedBox(height: 16),
              const Text(
                'Udra Challan\nSecurity Portal',
                textAlign: TextAlign.center,
                style: TextStyle(fontSize: 26, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 32),
              TextField(
                controller: _usernameController,
                decoration: const InputDecoration(
                  labelText: 'Username / Employee ID',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.person),
                ),
              ),
              const SizedBox(height: 16),
              TextField(
                controller: _passwordController,
                obscureText: true,
                decoration: const InputDecoration(
                  labelText: 'Password',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.lock),
                ),
              ),
              const SizedBox(height: 32),
              SizedBox(
                width: double.infinity,
                height: 50,
                child: ElevatedButton(
                  onPressed: _isLoading ? null : _attemptLogin,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Theme.of(context).colorScheme.primary,
                    foregroundColor: Colors.white,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(8),
                    ),
                  ),
                  child: _isLoading
                      ? const SizedBox(
                          height: 24,
                          width: 24,
                          child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2),
                        )
                      : const Text('AUTHENTICATE', style: TextStyle(letterSpacing: 1.5, fontWeight: FontWeight.bold)),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
