import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:pro_me/navbar.dart';
import 'package:pro_me/register.dart';
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
  final storage = const FlutterSecureStorage();
  bool isLoginCorrect = true;

  void _doUserRegistration() async {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => const RegisterPage(),
      ),
    );
  }

  void _getUserCreds() async {
    setState(() {
      _email = emailController.text;
      _password = passwordController.text;
    });
    var response = await http.post(
      Uri.https('pro-me.herokuapp.com', '/api/auth/token/login'),
      body: {'email': _email, 'password': _password},
    );
    if (jsonDecode(response.body)['auth_token'] == null) {
      setState(() {
        isLoginCorrect = false;
      });
    } else {
      var token = "Token " + jsonDecode(response.body)['auth_token'];
      await storage.write(key: 'token', value: token);
      Navigator.pop(context);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: const ProMeAppBar(),
      body: Column(
        children: [
          const Padding(
            padding: EdgeInsets.all(10.0),
            child: Text(
              'Login',
              style: TextStyle(
                fontWeight: FontWeight.bold,
                fontSize: 24,
              ),
            ),
          ),
          TextField(
              textAlign: TextAlign.center,
              controller: emailController,
              decoration: const InputDecoration(
                  contentPadding: EdgeInsets.all(20.0),
                  hintText: 'Enter Email',
                  labelText: 'Email',
                  labelStyle: TextStyle(
                    fontSize: 18,
                    color: Colors.black,
                    fontWeight: FontWeight.bold,
                  ))),
          TextField(
            textAlign: TextAlign.center,
            controller: passwordController,
            decoration: const InputDecoration(
                contentPadding: EdgeInsets.all(20.0),
                hintText: 'Enter Password',
                labelText: 'Password',
                labelStyle: TextStyle(
                  fontSize: 18,
                  color: Colors.black,
                  fontWeight: FontWeight.bold,
                )),
            obscureText: true,
            autocorrect: false,
          ),
          Padding(
            padding: const EdgeInsets.all(10.0),
            child: isLoginCorrect
                ? const Text('Please login to continue.')
                : const Text('Email or password is incorrect.'),
          ),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              Padding(
                padding: const EdgeInsets.all(10.0),
                child: ElevatedButton(
                  onPressed: _getUserCreds,
                  child: const Text('Login'),
                ),
              ),
              Padding(
                padding: const EdgeInsets.all(10.0),
                child: ElevatedButton(
                  onPressed: _doUserRegistration,
                  child: const Text('Register'),
                ),
              ),
            ],
          ),
        ],
      ),
      bottomNavigationBar: const ProMeNavBar(selectedIndex: 0),
    );
  }
}
