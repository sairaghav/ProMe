import 'dart:convert';
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;
import 'package:pro_me/streetriskdetails.dart';
import 'package:pro_me/unauthenticated.dart';

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
  bool isLoading = false;

  void _getRisk() async {
    setState(() {
      _street = streetController.text;
      _startDate = startDateController.text;
      _endDate = endDateController.text;
    });
    isLoading = true;
    String? token = await storage.read(key: 'token');
    var params = {'street': _street, 'from': _startDate, 'to': _endDate};

    var response = await http.get(
      Uri.https('pro-me.herokuapp.com', '/api/getriskdata', params),
      headers: {HttpHeaders.authorizationHeader: '$token'},
    );
    try {
      var riskData = jsonDecode(response.body);

      if (response.statusCode == HttpStatus.unauthorized ||
          response.statusCode == HttpStatus.forbidden) {
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (context) => const UnauthenticatedPage(
              selectedIndex: 0,
            ),
          ),
        );
        setState(() {
          isLoading = false;
        });
      } else {
        Navigator.push(
          context,
          MaterialPageRoute(
              builder: (context) => StreetRiskDetails(
                    details: riskData['results'],
                  )),
        );
        setState(() {
          isLoading = false;
        });
      }
    } catch (exception) {
      throw Exception('Error in getting risk data');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SingleChildScrollView(
        child: Column(
          children: [
            const Padding(
              padding: EdgeInsets.all(10.0),
              child: Text(
                'SafetyMeter',
                style: TextStyle(
                  fontWeight: FontWeight.bold,
                  fontSize: 24,
                ),
              ),
            ),
            TextField(
              textAlign: TextAlign.center,
              controller: streetController,
              decoration: const InputDecoration(
                contentPadding: EdgeInsets.all(20.0),
                hintText: 'Enter Street Name',
                labelText: 'Street',
                labelStyle: TextStyle(
                  fontSize: 18,
                  color: Colors.black,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
            TextField(
              textAlign: TextAlign.center,
              controller: startDateController,
              decoration: const InputDecoration(
                contentPadding: EdgeInsets.all(20.0),
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
              textAlign: TextAlign.center,
              controller: endDateController,
              decoration: const InputDecoration(
                contentPadding: EdgeInsets.all(20.0),
                hintText: 'yyyy-mm-dd',
                labelText: 'Evaluate Till',
                labelStyle: TextStyle(
                  fontSize: 18,
                  color: Colors.black,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(10.0),
              child: isLoading
                  ? Column(
                      children: const <Widget>[
                        Text(
                            'Getting the details... This may take some time...'),
                        CircularProgressIndicator(),
                      ],
                    )
                  : const Text(
                      'If "Evaluate Till" is not provided, default value will be the current date and the "Evaluate From" date is 30 days from "Evaluate Till" date unless explicitly specified.'),
            ),
            ElevatedButton(
              onPressed: _getRisk,
              child: const Text('Get Safety Score'),
            ),
          ],
        ),
      ),
    );
  }
}
