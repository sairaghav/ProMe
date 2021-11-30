import 'dart:io';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:pro_me/login.dart';

class ProMeAppBar extends StatefulWidget with PreferredSizeWidget {
  final bool isLoggedIn = true;
  const ProMeAppBar({Key? key, isLoggedIn}) : super(key: key);

  @override
  Size get preferredSize => const Size.fromHeight(kToolbarHeight);

  @override
  _ProMeAppBarState createState() => _ProMeAppBarState();
}

class _ProMeAppBarState extends State<ProMeAppBar> {
  final storage = const FlutterSecureStorage();
  void _onTapLogout() async {
    String? token = await storage.read(key: 'token');
    await http.post(
      Uri.https('pro-me.herokuapp.com', '/api/auth/token/logout'),
      headers: {HttpHeaders.authorizationHeader: '$token'},
    );
    Navigator.pop(context);
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => const Login(),
      ),
    );
  }

  void _onTapLogin() async {
    Navigator.pop(context);
    Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => const Login(),
        ));
  }

  @override
  Widget build(BuildContext context) {
    if (widget.isLoggedIn) {
      return AppBar(
        title: const Text('ProMe'),
        backgroundColor: Colors.blue,
        centerTitle: true,
        actions: <Widget>[
          Padding(
            padding: const EdgeInsets.only(right: 20.0),
            child: GestureDetector(
              onTap: _onTapLogout,
              child: const Icon(Icons.power_settings_new_rounded),
            ),
          ),
        ],
      );
    } else {
      return AppBar(
        title: const Text('ProMe'),
        backgroundColor: Colors.blue,
        centerTitle: true,
        actions: <Widget>[
          Padding(
            padding: const EdgeInsets.only(right: 20.0),
            child: GestureDetector(
              onTap: _onTapLogin,
              child: const Icon(Icons.power_settings_new_rounded),
            ),
          ),
        ],
      );
    }
  }
}
