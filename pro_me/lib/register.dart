import 'dart:io';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:pro_me/login.dart';
import 'package:pro_me/navbar.dart';
import 'package:pro_me/topbar.dart';

class RegisterPage extends StatefulWidget {
  const RegisterPage({Key? key}) : super(key: key);

  @override
  _RegisterPageState createState() => _RegisterPageState();
}

class _RegisterPageState extends State<RegisterPage> {
  TextEditingController userController = TextEditingController();
  TextEditingController emailController = TextEditingController();
  TextEditingController phoneController = TextEditingController();
  TextEditingController passwordController = TextEditingController();
  TextEditingController firstNameController = TextEditingController();
  TextEditingController lastNameController = TextEditingController();

  String _user = '',
      _email = '',
      _phone = '',
      _password = '',
      _fName = '',
      _lName = '';

  bool isValid = true;

  void _registerUser() async {
    setState(() {
      _user = userController.text;
      _email = emailController.text;
      _phone = phoneController.text;
      _password = passwordController.text;
      _fName = firstNameController.text;
      _lName = lastNameController.text;
    });

    var params = {
      'username': _user,
      'email': _email,
      'password': _password,
      'first_name': _fName,
      'last_name': _lName,
      'phone': _phone
    };
    var response = await http.post(
        Uri.https('pro-me.herokuapp.com', '/api/auth/users/'),
        body: params);

    if (response.statusCode != HttpStatus.created) {
      setState(() {
        isValid = false;
      });
    } else {
      Navigator.pop(context);
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => const Login(),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: const ProMeAppBar(),
      body: SingleChildScrollView(
        child: Column(
          children: [
            const Text(
              'User Registration',
              style: TextStyle(
                fontWeight: FontWeight.bold,
                fontSize: 24,
              ),
            ),
            TextField(
              textAlign: TextAlign.center,
              controller: userController,
              decoration: const InputDecoration(
                contentPadding: EdgeInsets.all(20.0),
                hintText: 'Enter Username',
                labelText: 'Username',
                labelStyle: TextStyle(
                  fontSize: 18,
                  color: Colors.black,
                  fontWeight: FontWeight.bold,
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
                ),
              ),
            ),
            TextField(
              textAlign: TextAlign.center,
              controller: phoneController,
              decoration: const InputDecoration(
                contentPadding: EdgeInsets.all(20.0),
                hintText: 'Enter Phone Number',
                labelText: 'Phone',
                labelStyle: TextStyle(
                  fontSize: 18,
                  color: Colors.black,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
            TextField(
              obscureText: true,
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
                ),
              ),
            ),
            TextField(
              textAlign: TextAlign.center,
              controller: firstNameController,
              decoration: const InputDecoration(
                contentPadding: EdgeInsets.all(20.0),
                hintText: 'Enter First Name',
                labelText: 'First Name',
                labelStyle: TextStyle(
                  fontSize: 18,
                  color: Colors.black,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
            TextField(
              textAlign: TextAlign.center,
              controller: lastNameController,
              decoration: const InputDecoration(
                contentPadding: EdgeInsets.all(20.0),
                hintText: 'Enter Last Name',
                labelText: 'Last Name',
                labelStyle: TextStyle(
                  fontSize: 18,
                  color: Colors.black,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
            ElevatedButton(
              onPressed: _registerUser,
              child: const Text('Register'),
            ),
            Center(
              child: isValid
                  ? const Text(
                      'Please enter all the fields to create a user account.')
                  : const Text(
                      'There is some error with the information entered.'),
            )
          ],
        ),
      ),
      bottomNavigationBar: const ProMeNavBar(selectedIndex: 0),
    );
  }
}
