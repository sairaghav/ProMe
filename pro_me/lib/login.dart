import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:pro_me/home.dart';
import 'package:pro_me/profile.dart';
import 'package:pro_me/reportincident.dart';
import 'package:pro_me/saferoute.dart';
import 'package:pro_me/streetrisk.dart';

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

  int _selectedIndex = 0;

  void _onItemTapped(int index) {
    setState(() {
      _selectedIndex = index;
      Navigator.push(
          context,
          MaterialPageRoute(
              builder: (context) => HomePage(selectedIndex: index)));
    });
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
    token = "Token " + jsonDecode(response.body)['auth_token'];
    await storage.write(key: 'token', value: token);
    print(token);
    Navigator.pop(context);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('ProMe'),
      ),
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
      bottomNavigationBar: BottomNavigationBar(
        type: BottomNavigationBarType.fixed,
        backgroundColor: Colors.blue,
        selectedItemColor: Colors.black,
        unselectedItemColor: Colors.white,
        currentIndex: _selectedIndex,
        onTap: _onItemTapped,
        items: const <BottomNavigationBarItem>[
          BottomNavigationBarItem(
            icon: Icon(Icons.alt_route),
            label: 'SafeRoute',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.manage_search),
            label: 'StreetRisk',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.report),
            label: 'ReportIncident',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.person),
            label: 'Profile',
          ),
        ],
      ),
    );
  }
}
