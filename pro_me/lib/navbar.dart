import 'package:flutter/material.dart';
import 'package:pro_me/home.dart';

class AuthNavBar extends StatefulWidget {
  final int selectedIndex;
  const AuthNavBar({Key? key, required this.selectedIndex}) : super(key: key);

  @override
  _AuthNavBarState createState() => _AuthNavBarState();
}

class _AuthNavBarState extends State<AuthNavBar> {
  void _onItemTapped(int index) {
    setState(() {
      Navigator.pop(context);
      Navigator.push(
          context,
          MaterialPageRoute(
              builder: (context) => HomePage(selectedIndex: index)));
    });
  }

  @override
  Widget build(BuildContext context) {
    return BottomNavigationBar(
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
          label: 'SafetyMeter',
        ),
        BottomNavigationBarItem(
          icon: Icon(Icons.report),
          label: 'IncidentReport',
        ),
      ],
    );
  }
}
