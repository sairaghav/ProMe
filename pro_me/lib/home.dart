import 'package:flutter/material.dart';
import 'package:pro_me/navbar.dart';
import 'package:pro_me/reportincident.dart';
import 'package:pro_me/saferoute.dart';
import 'package:pro_me/streetrisk.dart';
import 'package:pro_me/appbar.dart';

class HomePage extends StatefulWidget {
  final int selectedIndex;
  const HomePage({Key? key, required this.selectedIndex}) : super(key: key);

  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final List<Widget> _screens = [
    const SafeRoute(),
    const StreetRisk(),
    const ReportIncident(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: const AuthAppBar(),
      body: _screens[widget.selectedIndex],
      bottomNavigationBar: AuthNavBar(
        selectedIndex: widget.selectedIndex,
      ),
    );
  }
}
