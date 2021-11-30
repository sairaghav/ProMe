import 'dart:convert';
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;
import 'package:pro_me/login.dart';
import 'package:pro_me/streetriskdetails.dart';
import 'package:intl/intl.dart';

class StreetRisk extends StatefulWidget {
  const StreetRisk({Key? key}) : super(key: key);

  @override
  _StreetRiskState createState() => _StreetRiskState();
}

class _StreetRiskState extends State<StreetRisk> {
  TextEditingController streetController = TextEditingController();
  TextEditingController startDateController = TextEditingController();
  TextEditingController endDateController = TextEditingController();
  String _street = '', _startDate = '', _endDate = '';
  final storage = const FlutterSecureStorage();

  void _getRisk() async {
    setState(() {
      _street = streetController.text;
      _startDate = startDateController.text;
      _endDate = endDateController.text;
    });
    String? token = await storage.read(key: 'token');
    var params = {'street': _street, 'from': _startDate, 'to': _endDate};
    var response = await http.get(
      Uri.https('pro-me.herokuapp.com', '/api/getriskdata', params),
      headers: {HttpHeaders.authorizationHeader: '$token'},
    );
    try {
      var riskData = jsonDecode(response.body);

      if (riskData['detail'] ==
              "Authentication credentials were not provided." ||
          riskData['detail'] == "Invalid token.") {
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (context) => const Login(),
          ),
        );
      } else {
        Navigator.push(
          context,
          MaterialPageRoute(
              builder: (context) => StreetRiskDetails(
                    details: riskData['results'],
                  )),
        );
      }
    } catch (exception) {}
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        body: Column(children: [
      const Text(
        'StreetRisk',
        style: TextStyle(
          fontWeight: FontWeight.bold,
          fontSize: 24,
        ),
      ),
      TextField(
        controller: streetController,
        decoration: const InputDecoration(
          hintText: 'Enter Street',
          labelText: 'Street',
          labelStyle: TextStyle(
            fontSize: 18,
            color: Colors.black,
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
      TextField(
        controller: startDateController,
        decoration: const InputDecoration(
          hintText: 'yyyy-mm-dd',
          labelText: 'Evaluate From',
          labelStyle: TextStyle(
            fontSize: 18,
            color: Colors.black,
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
      TextField(
        controller: endDateController,
        decoration: const InputDecoration(
          hintText: 'yyyy-mm-dd',
          labelText: 'Evaluate Till',
          labelStyle: TextStyle(
            fontSize: 18,
            color: Colors.black,
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
      ElevatedButton(
        onPressed: _getRisk,
        child: const Text('Get Risk'),
      ),
    ]));
  }
}
