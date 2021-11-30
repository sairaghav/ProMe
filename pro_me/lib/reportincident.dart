import 'package:flutter/material.dart';

class ReportIncident extends StatefulWidget {
  const ReportIncident({Key? key}) : super(key: key);

  @override
  _ReportIncidentState createState() => _ReportIncidentState();
}

class _ReportIncidentState extends State<ReportIncident> {
  @override
  Widget build(BuildContext context) {
    return const Scaffold(body: Center(child: Text('ReportIncident page')));
  }
}
