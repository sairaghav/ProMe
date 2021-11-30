import 'package:flutter/material.dart';
import 'package:pro_me/navbar.dart';
import 'package:pro_me/topbar.dart';

class StreetRiskDetails extends StatefulWidget {
  final Map<dynamic, dynamic> details;
  const StreetRiskDetails({Key? key, required this.details}) : super(key: key);

  @override
  _StreetRiskDetailsState createState() => _StreetRiskDetailsState();
}

class _StreetRiskDetailsState extends State<StreetRiskDetails> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: const ProMeAppBar(),
      body: Column(
        children: <Widget>[
          Flexible(child: Text('${widget.details['risk_score']}')),
        ],
      ),
      bottomNavigationBar: const ProMeNavBar(
        selectedIndex: 1,
      ),
    );
  }
}
