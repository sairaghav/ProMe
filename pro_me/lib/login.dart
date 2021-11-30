import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:pro_me/home.dart';
import 'package:pro_me/navbar.dart';
import 'package:pro_me/topbar.dart';

class Login extends StatefulWidget {
  const Login({Key? key}) : super(key: key);

  @override
  _LoginState createState() => _LoginState();
}

class _LoginState extends State<Login> {
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
      appBar: const ProMeAppBar(),
      body: Column(children: [
        TextField(
            controller: emailController,
            decoration: const InputDecoration(
                hintText: 'Enter Email',
                labelText: 'Email',
                labelStyle: TextStyle(
                  fontSize: 24,
                  color: Colors.black,
                ))),
        TextField(
          controller: passwordController,
          decoration: const InputDecoration(
              hintText: 'Enter Password',
              labelText: 'Password',
              labelStyle: TextStyle(
                fontSize: 24,
                color: Colors.black,
              )),
          obscureText: true,
          autocorrect: false,
        ),
        ElevatedButton(
          onPressed: _getUserCreds,
          child: const Text('Login'),
        ),
      ]),
      bottomNavigationBar: const ProMeNavBar(
        selectedIndex: 3,
      ),
    );
  }
}
