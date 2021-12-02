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
  bool isLoading = false;
  bool isSuccess = false;

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
    setState(() {
      isLoading = true;
    });

    if (response.statusCode != HttpStatus.created) {
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
            const Padding(
              padding: EdgeInsets.all(10.0),
              child: Text(
                'User Registration',
                style: TextStyle(
                  fontWeight: FontWeight.bold,
                  fontSize: 24,
                ),
              ),
            ),
            TextField(
              textAlign: TextAlign.center,
              controller: firstNameController,
              decoration: const InputDecoration(
                contentPadding: EdgeInsets.all(20.0),
                hintText: 'Your First Name',
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
                hintText: 'Your Last Name',
                labelText: 'Last Name',
                labelStyle: TextStyle(
                  fontSize: 18,
                  color: Colors.black,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
            TextField(
              textAlign: TextAlign.center,
              controller: userController,
              decoration: const InputDecoration(
                contentPadding: EdgeInsets.all(20.0),
                hintText: 'This will be used to recognize you',
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
                hintText: 'This email will be used for login',
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
                hintText: 'Your Phone Number',
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
                hintText: 'Minimum of 8 characters',
                labelText: 'Password',
                labelStyle: TextStyle(
                  fontSize: 18,
                  color: Colors.black,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(10.0),
              child: isSuccess
                  ? const Text(
                      'User account has been created. You will now be redirected to the login screen.')
                  : isLoading
                      ? Column(
                          children: const <Widget>[
                            CircularProgressIndicator(),
                            Text(
                                'Creating a new user account... Please wait...'),
                          ],
                        )
                      : isValid
                          ? const Text(
                              'Please enter all the fields to create a user account.')
                          : const Text(
                              'There is some error with the information provided. Please check the data entered.'),
            ),
            ElevatedButton(
              onPressed: _registerUser,
              child: const Text('Register'),
            ),
          ],
        ),
      ),
      bottomNavigationBar: const ProMeNavBar(selectedIndex: 0),
    );
  }
}
