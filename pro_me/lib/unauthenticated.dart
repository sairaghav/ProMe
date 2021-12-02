import 'package:flutter/material.dart';
import 'package:pro_me/login.dart';
import 'package:pro_me/register.dart';

class UnauthenticatedPage extends StatefulWidget {
  final int selectedIndex;
  const UnauthenticatedPage({Key? key, required this.selectedIndex})
      : super(key: key);

  @override
  _UnauthenticatedPageState createState() => _UnauthenticatedPageState();
}

class _UnauthenticatedPageState extends State<UnauthenticatedPage> {
  final List<Widget> _screens = [
    const LoginPage(),
    const RegisterPage(),
  ];

  void _onItemTapped(int index) {
    setState(() {
      Navigator.pop(context);
      Navigator.push(
          context,
          MaterialPageRoute(
              builder: (context) => UnauthenticatedPage(selectedIndex: index)));
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
            icon: Icon(Icons.person),
            label: 'Login',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.person_add),
            label: 'Register',
          ),
        ],
      ),
    );
  }
}
