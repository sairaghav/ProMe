import 'package:flutter/material.dart';
import 'package:pro_me/profile.dart';
import 'package:pro_me/reportincident.dart';
import 'package:pro_me/saferoute.dart';
import 'package:pro_me/streetrisk.dart';

class ProMeNavBar extends StatefulWidget {
  const ProMeNavBar({Key? key}) : super(key: key);

  @override
  _ProMeNavBarState createState() => _ProMeNavBarState();
}

class _ProMeNavBarState extends State<ProMeNavBar> {
  int _selectedIndex = 0;
  List<Widget> _screens = [
    SafeRoute(),
    StreetRisk(),
    ReportIncident(),
    UserProfile(),
  ];

  void _onItemTapped(int index) {
    setState(() {
      _selectedIndex = index;
    });
  }

  @override
  Widget build(BuildContext context) {
    return BottomNavigationBar(
      type: BottomNavigationBarType.fixed,
      backgroundColor: Colors.blue,
      selectedItemColor: Colors.black,
      unselectedItemColor: Colors.white,
      currentIndex: _selectedIndex,
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
    );
  }
}
