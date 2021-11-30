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
            ListTile(
              title: const Text(
                'Risk Score',
                style: TextStyle(
                  fontWeight: FontWeight.bold,
                ),
              ),
              trailing: Text(
                widget.details['risk_score'],
                style: TextStyle(
                  color: Colors.white,
                  fontWeight: FontWeight.bold,
                  backgroundColor: widget.details['risk_score'] == 'Safe'
                      ? Colors.green
                      : widget.details['risk_score'] == 'Unsafe'
                          ? Colors.red
                          : Colors.orange,
                ),
              ),
            ),
            ListTile(
              title: const Text(
                'Most Reported Periods',
                style: TextStyle(
                  fontWeight: FontWeight.bold,
                ),
              ),
              trailing: Text(
                widget.details['all_top_timeline'].keys.toList().length > 0
                    ? widget.details['all_top_timeline'].keys
                        .toList()
                        .join(', ')
                    : 'None',
                style: const TextStyle(
                  color: Colors.black,
                ),
              ),
            ),
            ListTile(
              title: const Text(
                'Most Reported Activities',
                style: TextStyle(
                  fontWeight: FontWeight.bold,
                ),
              ),
              trailing: Text(
                widget.details['all_top_tag'].keys.toList().length > 0
                    ? widget.details['all_top_tag'].keys.toList().join(', ')
                    : 'None',
                style: const TextStyle(
                  color: Colors.black,
                ),
              ),
            ),
            Expanded(
              child: SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: SingleChildScrollView(
                  scrollDirection: Axis.vertical,
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
            ),
          ],
        ),
      ),
      bottomNavigationBar: const ProMeNavBar(
        selectedIndex: 1,
      ),
    );
  }
}
