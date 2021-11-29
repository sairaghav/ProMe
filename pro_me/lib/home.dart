import 'package:flutter/material.dart';
import 'package:pro_me/login.dart';
import 'package:pro_me/reportincident.dart';
import 'package:pro_me/saferoute.dart';
import 'package:pro_me/streetrisk.dart';

class HomePage extends StatefulWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  int _selectedIndex = 0;

  List<Widget> _screens = [
    Login(),
    SafeRoute(),
    StreetRisk(),
    ReportIncident(),
  ];

  void _onItemTapped(int index) {
    setState(() {
      _selectedIndex = index;
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
      body: _screens[_selectedIndex],
      bottomNavigationBar: BottomNavigationBar(
        type: BottomNavigationBarType.fixed,
        backgroundColor: Colors.blue,
        selectedItemColor: Colors.black,
        unselectedItemColor: Colors.white,
        currentIndex: _selectedIndex,
        onTap: _onItemTapped,
        items: const <BottomNavigationBarItem>[
          BottomNavigationBarItem(
            icon: Icon(Icons.person),
            label: 'Login',
          ),
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
        ],
      ),
    );
  }
}
