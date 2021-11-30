import 'package:flutter/material.dart';
import 'package:pro_me/home.dart';
import 'package:pro_me/topbar.dart';

class SafeRouteDetails extends StatefulWidget {
  final List<dynamic> details;
  const SafeRouteDetails({Key? key, required this.details}) : super(key: key);

  @override
  _SafeRouteDetailsState createState() => _SafeRouteDetailsState();
}

class _SafeRouteDetailsState extends State<SafeRouteDetails> {
  int _selectedIndex = 0;

  void _onItemTapped(int index) {
    setState(() {
      _selectedIndex = index;
      Navigator.push(
          context,
          MaterialPageRoute(
              builder: (context) => HomePage(selectedIndex: index)));
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: const ProMeAppBar(),
      body: Column(
        children: <Widget>[
          Flexible(child: Text('${widget.details}')),
          Flexible(
              child: ElevatedButton(
                  onPressed: () {
                    setState(() {
                      Navigator.pop(context);
                    });
                  },
                  child: const Text('Go Back'))),
        ],
      ),
      bottomNavigationBar: BottomNavigationBar(
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
      ),
    );
  }
}
