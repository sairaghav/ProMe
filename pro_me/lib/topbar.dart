import 'package:flutter/material.dart';

class ProMeAppBar extends StatefulWidget with PreferredSizeWidget {
  const ProMeAppBar({Key? key}) : super(key: key);

  @override
  Size get preferredSize => const Size.fromHeight(kToolbarHeight);

  @override
  _ProMeAppBarState createState() => _ProMeAppBarState();
}

class _ProMeAppBarState extends State<ProMeAppBar> {
  @override
  Widget build(BuildContext context) {
    return AppBar(
      title: const Text('ProMe'),
      backgroundColor: Colors.blue,
      centerTitle: true,
    );
  }
}
