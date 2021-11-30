import 'package:flutter/material.dart';
import 'package:pro_me/home.dart';

void main() => runApp(const ProMe());

class ProMe extends StatelessWidget {
  const ProMe({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
        title: 'ProMe',
        home: HomePage(
          selectedIndex: 0,
        ));
  }
}
