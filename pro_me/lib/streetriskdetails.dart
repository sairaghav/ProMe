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
      body: Center(
        child: Column(
          children: <Widget>[
            Text(
              'Safety Information for ' + widget.details["street"],
              style: const TextStyle(
                fontWeight: FontWeight.bold,
                fontSize: 24,
              ),
            ),
            Expanded(
              child: SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: DataTable(
                  columns: const <DataColumn>[
                    DataColumn(
                      label: Text(
                        'Date',
                        style: TextStyle(fontStyle: FontStyle.italic),
                      ),
                    ),
                    DataColumn(
                      label: Text(
                        'Source',
                        style: TextStyle(fontStyle: FontStyle.italic),
                      ),
                    ),
                    DataColumn(
                      label: Text(
                        'Tags',
                        style: TextStyle(fontStyle: FontStyle.italic),
                      ),
                    ),
                    DataColumn(
                      label: Text(
                        'Summary',
                        style: TextStyle(fontStyle: FontStyle.italic),
                      ),
                    ),
                    DataColumn(
                      label: Text(
                        'Link',
                        style: TextStyle(fontStyle: FontStyle.italic),
                      ),
                    ),
                  ],
                  rows: widget.details['risk_metadata']
                      .map<DataRow>(
                        ((element) => DataRow(
                              cells: <DataCell>[
                                DataCell(Text(element['date'])),
                                DataCell(Text(element['source'])),
                                DataCell(Text(element['tags'])),
                                DataCell(Text(element['news'])),
                                DataCell(Text(element['link'])),
                              ],
                            )),
                      )
                      .toList(),
                ),
              ),
            ),
            Expanded(child: Text('${widget.details}')),
          ],
        ),
      ),
      bottomNavigationBar: const ProMeNavBar(
        selectedIndex: 1,
      ),
    );
  }
}
