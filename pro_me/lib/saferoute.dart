import 'dart:convert';
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:pro_me/login.dart';
import 'package:pro_me/saferoutedetails.dart';

class SafeRoute extends StatefulWidget {
  const SafeRoute({Key? key}) : super(key: key);

  @override
  _SafeRouteState createState() => _SafeRouteState();
}

class _SafeRouteState extends State<SafeRoute> {
  TextEditingController sourceController = TextEditingController();
  TextEditingController destinationController = TextEditingController();
  String _source = '', _destination = '';
  final storage = const FlutterSecureStorage();

  void _getRoute() async {
    setState(() {
      _source = sourceController.text;
      _destination = destinationController.text;
    });
    String? token = await storage.read(key: 'token');
    var params = {'start': _source, 'end': _destination};
    var response = await http.get(
      Uri.https('pro-me.herokuapp.com', '/api/directions', params),
      headers: {HttpHeaders.authorizationHeader: '$token'},
    );

    try {
      var routeData = jsonDecode(response.body);
      if (routeData['detail'] ==
              "Authentication credentials were not provided." ||
          routeData['detail'] == "Invalid token.") {
        Navigator.push(
          context,
          MaterialPageRoute(builder: (context) => const Login()),
        );
      } else {
        for (var result in routeData['results']) {
          params = {'street': result['name']};
          response = await http.get(
            Uri.https('pro-me.herokuapp.com', '/api/getriskdata', params),
            headers: {HttpHeaders.authorizationHeader: '$token'},
          );
          var riskData = jsonDecode(response.body);
          result['risk_metadata'] = riskData;
          print(riskData);
        }
        Navigator.push(
          context,
          MaterialPageRoute(
              builder: (context) => SafeRouteDetails(
                    details: routeData['results'],
                  )),
        );
      }
    } catch (exception) {}
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        body: Column(children: [
      TextField(
          controller: sourceController,
          decoration: const InputDecoration(
              hintText: 'Enter Source',
              labelText: 'Source',
              labelStyle: TextStyle(
                fontSize: 24,
                color: Colors.black,
              ))),
      TextField(
        controller: destinationController,
        decoration: const InputDecoration(
            hintText: 'Enter Destination',
            labelText: 'Destination',
            labelStyle: TextStyle(
              fontSize: 24,
              color: Colors.black,
            )),
      ),
      ElevatedButton(
        onPressed: _getRoute,
        child: const Text('Get route'),
      ),
    ]));
  }
}
