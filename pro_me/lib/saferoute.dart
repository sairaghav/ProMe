import 'package:flutter/material.dart';

class SafeRoute extends StatefulWidget {
  const SafeRoute({Key? key}) : super(key: key);

  @override
  _SafeRouteState createState() => _SafeRouteState();
}

class _SafeRouteState extends State<SafeRoute> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(body: const Center(child: Text('SafeSearch page')));
  }
}
