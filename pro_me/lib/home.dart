import 'package:flutter/material.dart';
import 'package:pro_me/profile.dart';
import 'package:pro_me/reportincident.dart';
import 'package:pro_me/saferoute.dart';
import 'package:pro_me/streetrisk.dart';

class HomePage extends StatefulWidget {
  int selectedIndex = 0;
  HomePage({Key? key, required this.selectedIndex}) : super(key: key);

  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final List<Widget> _screens = [
    const SafeRoute(),
    const StreetRisk(),
    const ReportIncident(),
    const UserProfile(),
  ];

  void _onItemTapped(int index) {
    setState(() {
      widget.selectedIndex = index;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('ProMe'),
        backgroundColor: Colors.blue,
        centerTitle: true,
      ),
      body: _screens[widget.selectedIndex],
      bottomNavigationBar: BottomNavigationBar(
        type: BottomNavigationBarType.fixed,
        backgroundColor: Colors.blue,
        selectedItemColor: Colors.black,
        unselectedItemColor: Colors.white,
        currentIndex: widget.selectedIndex,
        onTap: _onItemTapped,
        items: const <BottomNavigationBarItem>[
          BottomNavigationBarItem(
            icon: Icon(Icons.alt_route),
            label: 'SafeRoute',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.manage_search),
            label: 'StreetRisk',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.report),
            label: 'ReportIncident',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.person),
            label: 'Profile',
          ),
        ],
      ),
    );
  }
}
