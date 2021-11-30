import 'package:flutter/material.dart';
import 'package:pro_me/home.dart';

class ProMeNavBar extends StatefulWidget {
  final int selectedIndex;
  final bool shouldPop = true;
  const ProMeNavBar({Key? key, required this.selectedIndex, shouldPop})
      : super(key: key);

  @override
  _ProMeNavBarState createState() => _ProMeNavBarState();
}

class _ProMeNavBarState extends State<ProMeNavBar> {
  void _onItemTapped(int index) {
    setState(() {
      if (widget.shouldPop) {
        print('Popping');
        Navigator.pop(context);
      }
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
