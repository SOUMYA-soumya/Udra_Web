import 'package:flutter/material.dart';

class DashboardScreen extends StatefulWidget {
  final Map<String, dynamic> userData;

  const DashboardScreen({super.key, required this.userData});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  int _selectedIndex = 0;

  @override
  Widget build(BuildContext context) {
    // Extracting user info passed from the Flask API
    final String fullName = widget.userData['full_name'] ?? 'Authorized User';
    final String role = widget.userData['role'] ?? 'Standard Access';

    return Scaffold(
      backgroundColor: Colors.grey[100],
      body: Row(
        children: [
          // 1. The Web Side Navigation Rail
          NavigationRail(
            selectedIndex: _selectedIndex,
            onDestinationSelected: (int index) {
              setState(() {
                _selectedIndex = index;
              });
            },
            labelType: NavigationRailLabelType.all,
            backgroundColor: const Color(0xFF1E3A8A), // Corporate Blue
            unselectedIconTheme: const IconThemeData(color: Colors.white70),
            unselectedLabelTextStyle: const TextStyle(color: Colors.white70),
            selectedIconTheme: const IconThemeData(color: Colors.white),
            selectedLabelTextStyle: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
            leading: const Padding(
              padding: EdgeInsets.symmetric(vertical: 20.0),
              child: Icon(Icons.local_shipping, color: Colors.white, size: 40),
            ),
            destinations: const [
              NavigationRailDestination(
                icon: Icon(Icons.dashboard),
                label: Text('Overview'),
              ),
              NavigationRailDestination(
                icon: Icon(Icons.receipt_long),
                label: Text('Challans'),
              ),
              NavigationRailDestination(
                icon: Icon(Icons.account_balance_wallet),
                label: Text('Finance'),
              ),
              NavigationRailDestination(
                icon: Icon(Icons.security),
                label: Text('Security Admin'),
              ),
            ],
            trailing: Expanded(
              child: Align(
                alignment: Alignment.bottomCenter,
                child: Padding(
                  padding: const EdgeInsets.only(bottom: 20.0),
                  child: IconButton(
                    icon: const Icon(Icons.logout, color: Colors.redAccent),
                    onPressed: () {
                      // Logout and return to Login Screen
                      Navigator.pop(context);
                    },
                  ),
                ),
              ),
            ),
          ),
          
          // 2. The Main Content Area
          Expanded(
            child: Padding(
              padding: const EdgeInsets.all(32.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Welcome, $fullName',
                    style: const TextStyle(fontSize: 32, fontWeight: FontWeight.bold, color: Color(0xFF1E3A8A)),
                  ),
                  Text(
                    'Current Entitlement Level: $role',
                    style: const TextStyle(fontSize: 16, color: Colors.grey),
                  ),
                  const SizedBox(height: 32),
                  
                  // Content based on selected module
                  Expanded(
                    child: Card(
                      elevation: 4,
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                      child: Center(
                        child: Text(
                          'Module View: ${_getModuleName(_selectedIndex)}\n\n(Granular RBAC checks will be applied here)',
                          textAlign: TextAlign.center,
                          style: const TextStyle(fontSize: 18, color: Colors.black54),
                        ),
                      ),
                    ),
                  )
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  String _getModuleName(int index) {
    switch (index) {
      case 0: return 'System Overview';
      case 1: return 'Challan Entry & Management';
      case 2: return 'Financial Redemption';
      case 3: return 'User Provisioning & Roles';
      default: return 'Unknown Module';
    }
  }
}
