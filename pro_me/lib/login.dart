import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:pro_me/home.dart';
import 'package:pro_me/unauthenticated.dart';

class LoginPage extends StatefulWidget {
  const LoginPage({Key? key}) : super(key: key);

  @override
  _LoginPageState createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  TextEditingController emailController = TextEditingController();
  TextEditingController passwordController = TextEditingController();
  String _email = '', _password = '';
  final storage = const FlutterSecureStorage();
  bool isValid = true;
  bool isLoading = false;
  bool isSuccess = false;

  void _doUserRegistration() async {
    Navigator.pop(context);
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => const UnauthenticatedPage(
          selectedIndex: 1,
        ),
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
    setState(() {
      isLoading = true;
    });
    if (jsonDecode(response.body)['auth_token'] == null) {
      await Future.delayed(const Duration(seconds: 1));
      setState(() {
        isValid = false;
        isLoading = false;
      });
    } else {
      await Future.delayed(const Duration(seconds: 1));
      setState(() {
        isLoading = false;
        isSuccess = true;
      });
      await Future.delayed(const Duration(seconds: 1));
      var token = "Token " + jsonDecode(response.body)['auth_token'];
      await storage.write(key: 'token', value: token);
      Navigator.pop(context);
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => const HomePage(
            selectedIndex: 0,
          ),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
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
            child: isSuccess
                ? const Text('Login successful!')
                : isLoading
                    ? Column(
                        children: const <Widget>[
                          CircularProgressIndicator(),
                          Text('Logging you in... Please wait...'),
                        ],
                      )
                    : isValid
                        ? const Text('Please login to continue.')
                        : const Text('Username or password is incorrect.'),
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
                  child: const Text('New User'),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
