import 'dart:io';
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;
import 'package:pro_me/unauthenticated.dart';

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
  bool isValid = false;
  final _tagList = [
    'terrorism',
    'theft',
    'robbery',
    'drugs',
    'aggression',
    'arrest',
    'accident',
    'vandalism',
    'investigation',
    'death',
  ];

  void _addReport() async {
    setState(() {
      _street = streetController.text;
      _summary = summaryController.text;
      isLoading = true;
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
            builder: (context) => const UnauthenticatedPage(
              selectedIndex: 0,
            ),
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
          await Future.delayed(const Duration(seconds: 1));

          response = await http.post(
              Uri.https('pro-me.herokuapp.com', '/api/report'),
              headers: {HttpHeaders.authorizationHeader: '$token'},
              body: params);

          setState(
            () {
              isLoading = false;
              isValid = true;
            },
          );
        } else {
          setState(
            () {
              isLoading = false;
            },
          );
        }
      }
    } catch (exception) {
      throw Exception('Error in sending the report');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: <Widget>[
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
            'Type of Activity: ',
            style: TextStyle(
              fontSize: 18,
              fontWeight: FontWeight.bold,
            ),
          ),
        ),
        Expanded(
          child: ListView.builder(
            itemCount: _tagList.length,
            itemBuilder: (context, index) {
              var item = _tagList[index];
              return ListTile(
                title: Text(item[0].toUpperCase() + item.substring(1)),
                leading: Radio(
                  value: item,
                  groupValue: _tag,
                  onChanged: (String? value) {
                    setState(() {
                      _tag = '$value';
                    });
                  },
                ),
              );
            },
          ),
        ),
        Padding(
          padding: const EdgeInsets.all(10.0),
          child: isLoading
              ? Column(
                  children: const <Widget>[
                    Text(
                        'Adding report to risk database... This may take some time...'),
                    CircularProgressIndicator(),
                  ],
                )
              : isValid
                  ? const Text(
                      'The incident report has been added to our risk database.')
                  : const Text(
                      'Please enter all the fields to report an incident.'),
        ),
        Flexible(
          child: ElevatedButton(
            onPressed: _addReport,
            child: const Text('Add Report'),
          ),
        ),
      ],
    );
  }
}
