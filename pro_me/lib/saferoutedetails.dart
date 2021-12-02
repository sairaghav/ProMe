import 'package:flutter/material.dart';
import 'package:pro_me/navbar.dart';
import 'package:pro_me/streetriskdetails.dart';
import 'package:pro_me/topbar.dart';

class SafeRouteDetails extends StatefulWidget {
  final List<dynamic> details;
  const SafeRouteDetails({Key? key, required this.details}) : super(key: key);

  @override
  _SafeRouteDetailsState createState() => _SafeRouteDetailsState();
}

class _SafeRouteDetailsState extends State<SafeRouteDetails> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: const ProMeAppBar(),
      body: Column(
        children: <Widget>[
          const Padding(
            padding: EdgeInsets.all(10.0),
            child: Text(
              'Route Safety Information',
              style: TextStyle(
                fontWeight: FontWeight.bold,
                fontSize: 24,
              ),
            ),
          ),
          Expanded(
            child: ListView.builder(
              itemCount: widget.details.length,
              itemBuilder: (context, index) {
                final item = widget.details[index];
                item['directions'] = item['narrative'] +
                    " for " +
                    "${item['distance']} kilometers" +
                    " by " +
                    item['mode'];
                final tags =
                    item['risk_metadata']['all_tags'].keys.toList().join(', ');
                return ListTile(
                  title: Text(item['directions']),
                  subtitle: tags.length == 0
                      ? const Text('No reports found.')
                      : Text('Reports available for ' + tags),
                  leading: ConstrainedBox(
                    constraints: const BoxConstraints(
                      minWidth: 100,
                      minHeight: 150,
                      maxWidth: 150,
                      maxHeight: 200,
                    ),
                    child: Image.network(item['mapUrl'], fit: BoxFit.cover),
                  ),
                  trailing: ElevatedButton(
                    child: Text(item['risk_metadata']['risk_score']),
                    onPressed: () => {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                            builder: (context) => StreetRiskDetails(
                                  details: item['risk_metadata'],
                                )),
                      )
                    },
                    style: ButtonStyle(
                      backgroundColor:
                          item['risk_metadata']['risk_score'] == 'Safe'
                              ? MaterialStateProperty.all(Colors.green)
                              : item['risk_metadata']['risk_score'] ==
                                      'Moderately Unsafe'
                                  ? MaterialStateProperty.all(Colors.orange)
                                  : MaterialStateProperty.all(Colors.red),
                    ),
                  ),
                );
              },
            ),
          ),
        ],
      ),
      bottomNavigationBar: const ProMeNavBar(
        selectedIndex: 0,
      ),
    );
  }
}
