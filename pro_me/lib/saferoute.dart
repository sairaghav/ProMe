import 'dart:convert';
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:pro_me/saferoutedetails.dart';
import 'package:pro_me/unauthenticated.dart';

class SafeRoute extends StatefulWidget {
  const SafeRoute({Key? key}) : super(key: key);

  @override
  _SafeRouteState createState() => _SafeRouteState();
}

class _SafeRouteState extends State<SafeRoute> {
  TextEditingController sourceController = TextEditingController();
  TextEditingController destinationController = TextEditingController();
  String _source = '', _destination = '', _mode = 'pedestrian';
  final storage = const FlutterSecureStorage();
  bool isLoading = false;

  List<String> modes = ['pedestrian', 'fastest', 'bicycle'];

  void _getRiskData(Map<dynamic, dynamic> routeData, String token) async {
    for (var result in routeData['results']) {
      var params = {'street': result['name']};
      var response = await http.get(
        Uri.https('pro-me.herokuapp.com', '/api/getriskdata', params),
        headers: {HttpHeaders.authorizationHeader: token},
      );
      var riskData = jsonDecode(response.body);
      result['risk_metadata'] = riskData['results'];
    }
    setState(() {
      isLoading = false;
    });
    Navigator.push(
      context,
      MaterialPageRoute(
          builder: (context) => SafeRouteDetails(
                details: routeData['results'],
              )),
    );
  }

  void _getRoute() async {
    setState(() {
      _source = sourceController.text;
      _destination = destinationController.text;
    });
    String? token = await storage.read(key: 'token');
    if (_source.isNotEmpty && _destination.isNotEmpty) {
      setState(() {
        isLoading = true;
      });
      var params = {'start': _source, 'end': _destination, 'mode': _mode};
      var response = await http.get(
        Uri.https('pro-me.herokuapp.com', '/api/directions', params),
        headers: {HttpHeaders.authorizationHeader: '$token'},
      );
      try {
        var routeData = jsonDecode(response.body);
        if (response.statusCode == HttpStatus.unauthorized ||
            response.statusCode == HttpStatus.forbidden) {
          setState(() {
            isLoading = false;
          });
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (context) => const UnauthenticatedPage(
                selectedIndex: 0,
              ),
            ),
          );
        } else {
          _getRiskData(routeData, '$token');
        }
      } catch (exception) {
        throw Exception('Error in getting route data.');
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: <Widget>[
        const Padding(
          padding: EdgeInsets.all(10.0),
          child: Text(
            'SafeRoute',
            style: TextStyle(
              fontWeight: FontWeight.bold,
              fontSize: 24,
            ),
          ),
        ),
        TextField(
          textAlign: TextAlign.center,
          controller: sourceController,
          decoration: const InputDecoration(
            contentPadding: EdgeInsets.all(20.0),
            labelText: 'Source',
            hintText: 'Enter Source for Route',
            labelStyle: TextStyle(
              fontSize: 18,
              fontWeight: FontWeight.bold,
              color: Colors.black,
            ),
          ),
        ),
        TextField(
          textAlign: TextAlign.center,
          controller: destinationController,
          decoration: const InputDecoration(
            contentPadding: EdgeInsets.all(20.0),
            labelText: 'Destination',
            hintText: 'Enter Destination for Route',
            labelStyle: TextStyle(
              fontSize: 18,
              fontWeight: FontWeight.bold,
              color: Colors.black,
            ),
          ),
        ),
        const Padding(
          padding: EdgeInsets.all(10.0),
          child: Text(
            'Mode of Transport: ',
            style: TextStyle(
              fontSize: 18,
              fontWeight: FontWeight.bold,
            ),
          ),
        ),
        Expanded(
          child: ListView.builder(
            itemCount: modes.length,
            itemBuilder: (context, index) {
              var item = modes[index];
              return ListTile(
                title: Text(item[0].toUpperCase() + item.substring(1)),
                leading: Radio(
                  groupValue: _mode,
                  value: item,
                  onChanged: (String? value) {
                    setState(
                      () {
                        _mode = '$value';
                      },
                    );
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
                    Text('Getting the details... This may take some time...'),
                    CircularProgressIndicator(),
                  ],
                )
              : const Text(
                  'Please provide the source, destination and mode of travel to get safety metrics for all streets along the route.'),
        ),
        Flexible(
          child: ElevatedButton(
            onPressed: _getRoute,
            child: const Text('Get route'),
          ),
        ),
      ],
    );
  }
}
