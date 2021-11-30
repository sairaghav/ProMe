import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class UserProfile extends StatefulWidget {
  const UserProfile({Key? key}) : super(key: key);

  @override
  _UserProfileState createState() => _UserProfileState();
}

class _UserProfileState extends State<UserProfile> {
  TextEditingController emailController = TextEditingController();
  TextEditingController passwordController = TextEditingController();
  String _email = '', _password = '';
  String token = '';
  final storage = const FlutterSecureStorage();

  void _getUserCreds() async {
    setState(() {
      _email = emailController.text;
      _password = passwordController.text;
    });
    var response = await http.post(
      Uri.https('pro-me.herokuapp.com', '/api/auth/token/login'),
      body: {'email': _email, 'password': _password},
    );
    token = "Token " + jsonDecode(response.body)['auth_token'];
    await storage.write(key: 'token', value: token);
    print(token);
    Navigator.pop(context);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        body: Column(
      children: const <Widget>[
        Text('Profile page'),
      ],
    ));
  }
}
