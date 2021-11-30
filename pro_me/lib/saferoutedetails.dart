import 'package:flutter/material.dart';
import 'package:pro_me/navbar.dart';
import 'package:pro_me/topbar.dart';

class SafeRouteDetails extends StatefulWidget {
  final List<dynamic> details;
  const SafeRouteDetails({Key? key, required this.details}) : super(key: key);

  @override
  _SafeRouteDetailsState createState() => _SafeRouteDetailsState();
}

class _SafeRouteDetailsState extends State<SafeRouteDetails> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: const ProMeAppBar(),
      body: Column(
        children: <Widget>[
          Flexible(child: Text('${widget.details}')),
        ],
      ),
      bottomNavigationBar: const ProMeNavBar(
        selectedIndex: 0,
      ),
    );
  }
}
