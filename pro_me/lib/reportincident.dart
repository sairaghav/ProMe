import 'dart:io';
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;
import 'package:pro_me/login.dart';

class ReportIncident extends StatefulWidget {
  const ReportIncident({Key? key}) : super(key: key);

  @override
  _ReportIncidentState createState() => _ReportIncidentState();
}

class _ReportIncidentState extends State<ReportIncident> {
  TextEditingController streetController = TextEditingController();
  TextEditingController summaryController = TextEditingController();
  TextEditingController tagController = TextEditingController();
  String _street = '', _summary = '', _tag = '';
  final storage = const FlutterSecureStorage();
  bool isLoading = false;

  void _addReport() async {
    setState(() {
      _street = streetController.text;
      _summary = summaryController.text;
    });

    String? token = await storage.read(key: 'token');
    var response = await http.get(
        Uri.https('pro-me.herokuapp.com', '/api/auth/users/me'),
        headers: {HttpHeaders.authorizationHeader: '$token'});

    try {
      var reponseData = jsonDecode(response.body);
      if (response.statusCode == HttpStatus.unauthorized ||
          response.statusCode == HttpStatus.forbidden) {
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (context) => const Login(),
          ),
        );
      } else {
        if (_street.isNotEmpty && _summary.isNotEmpty && _tag.isNotEmpty) {
          var params = {
            'street': _street,
            'summary': _summary,
            'tags': _tag,
            'user': reponseData['username'],
          };

          response = await http.post(
              Uri.https('pro-me.herokuapp.com', '/api/report'),
              headers: {HttpHeaders.authorizationHeader: '$token'},
              body: params);

          setState(() {
            isLoading = true;
          });
        } else {
          setState(() {
            isLoading = false;
          });
        }
      }
    } catch (exception) {
      throw Exception('Error in sending the report');
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
                'Report an Incident',
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
              textAlign: TextAlign.center,
              controller: summaryController,
              decoration: const InputDecoration(
                contentPadding: EdgeInsets.all(20.0),
                hintText: 'Enter summary of your report',
                labelText: 'Summary',
                labelStyle: TextStyle(
                  fontSize: 18,
                  color: Colors.black,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
            const Padding(
              padding: EdgeInsets.all(10.0),
              child: Text(
                'Tags: ',
                style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
            ListTile(
              title: const Text('Terrorismo'),
              leading: Radio(
                value: 'terrorismo',
                groupValue: _tag,
                onChanged: (String? value) {
                  setState(
                    () {
                      _tag = '$value';
                    },
                  );
                },
              ),
            ),
            ListTile(
              title: const Text('Furti'),
              leading: Radio(
                value: 'furti',
                groupValue: _tag,
                onChanged: (String? value) {
                  setState(
                    () {
                      _tag = '$value';
                    },
                  );
                },
              ),
            ),
            ListTile(
              title: const Text('Rapine'),
              leading: Radio(
                value: 'rapine',
                groupValue: _tag,
                onChanged: (String? value) {
                  setState(
                    () {
                      _tag = '$value';
                    },
                  );
                },
              ),
            ),
            ListTile(
              title: const Text('Droga'),
              leading: Radio(
                value: 'droga',
                groupValue: _tag,
                onChanged: (String? value) {
                  setState(
                    () {
                      _tag = '$value';
                    },
                  );
                },
              ),
            ),
            ListTile(
              title: const Text('Aggressioni'),
              leading: Radio(
                value: 'aggressioni',
                groupValue: _tag,
                onChanged: (String? value) {
                  setState(
                    () {
                      _tag = '$value';
                    },
                  );
                },
              ),
            ),
            ListTile(
              title: const Text('Arresti'),
              leading: Radio(
                value: 'arresti',
                groupValue: _tag,
                onChanged: (String? value) {
                  setState(
                    () {
                      _tag = '$value';
                    },
                  );
                },
              ),
            ),
            ListTile(
              title: const Text('Incidenti'),
              leading: Radio(
                value: 'incidenti',
                groupValue: _tag,
                onChanged: (String? value) {
                  setState(
                    () {
                      _tag = '$value';
                    },
                  );
                },
              ),
            ),
            ListTile(
              title: const Text('Vandali'),
              leading: Radio(
                value: 'vandali',
                groupValue: _tag,
                onChanged: (String? value) {
                  setState(
                    () {
                      _tag = '$value';
                    },
                  );
                },
              ),
            ),
            ListTile(
              title: const Text('Incidenti-stradali'),
              leading: Radio(
                value: 'incidenti-stradali',
                groupValue: _tag,
                onChanged: (String? value) {
                  setState(
                    () {
                      _tag = '$value';
                    },
                  );
                },
              ),
            ),
            ListTile(
              title: const Text('Indagini'),
              leading: Radio(
                value: 'indagini',
                groupValue: _tag,
                onChanged: (String? value) {
                  setState(
                    () {
                      _tag = '$value';
                    },
                  );
                },
              ),
            ),
            ListTile(
              title: const Text('Morti'),
              leading: Radio(
                value: 'morti',
                groupValue: _tag,
                onChanged: (String? value) {
                  setState(
                    () {
                      _tag = '$value';
                    },
                  );
                },
              ),
            ),
            Center(
              child: isLoading
                  ? const Text(
                      'The incident report has been added to our risk database.')
                  : const Text(
                      'Please enter all the fields to report an incident.'),
            ),
            ElevatedButton(
              onPressed: _addReport,
              child: const Text('Add Report'),
            ),
          ],
        ),
      ),
    );
  }
}
