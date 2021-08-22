import 'dart:async';
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

import '../models/public-place.dart';
import '../services/web-service.dart';

Future<List<PublicPlace>> getPublicPlaces() async {
  final response =
      await http.get(Uri.parse('http://127.0.0.1:8000/public-places/'));

  final result = json.decode(response.body);

  if (response.statusCode == 200) {
    final List<PublicPlace> publicPlaces =
        List<PublicPlace>.from(result.map((publicPlace) {
      return PublicPlace.fromJson(publicPlace);
    }).toList());

    return publicPlaces;
  } else {
    throw Exception('Failed to load data');
  }
}

class Item {
  Item({
    required this.owner,
    required this.name,
    required this.address,
    required this.maxCapacity,
    required this.numberOfReports,
    this.isExpanded = false,
  });

  String owner;
  String name;
  String address;
  int maxCapacity;
  int numberOfReports;
  bool isExpanded;
}

class PublicPlacesList extends StatefulWidget {
  const PublicPlacesList({Key? key}) : super(key: key);

  @override
  State<PublicPlacesList> createState() => _PublicPlacesListState();
}

class _PublicPlacesListState extends State<PublicPlacesList> {
  List<Item> _data = [];

  List<PublicPlace> _publicPlaces = [];

  late Future<List<Item>> myFuture;

  Future<List<Item>> _generateItems(int numberOfItems) async {
    return List<Item>.generate(numberOfItems, (int index) {
      return Item(
        owner: _publicPlaces[index].owner,
        address: _publicPlaces[index].address,
        maxCapacity: _publicPlaces[index].maxCapacity,
        name: _publicPlaces[index].name,
        numberOfReports: _publicPlaces[index].reports.length,
      );
    });
  }

  bool _isDanger(Item item) {
    if (item.numberOfReports > 0.05 * item.maxCapacity) {
      return true;
    }

    return false;
  }

  @override
  void initState() {
    super.initState();

    myFuture = _generateData();
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
  }

  Future<List<Item>> _generateData() async {
    _publicPlaces = await getPublicPlaces();

    final items = await _generateItems(_publicPlaces.length);

    return items;
  }

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      child: Container(
        child: _buildPanel(),
      ),
    );
  }

  Widget _buildPanel() {
    return FutureBuilder<List<Item>>(
        future: myFuture,
        builder: (BuildContext context, AsyncSnapshot<List<Item>> snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return CircularProgressIndicator();
          } else {
            if (snapshot.hasData) {
              return ExpansionPanelList(
                expansionCallback: (int index, bool isExpanded) {
                  setState(() {
                    snapshot.data![index].isExpanded = !isExpanded;
                  });
                },
                children: snapshot.data!.map<ExpansionPanel>((Item item) {
                  return ExpansionPanel(
                    headerBuilder: (BuildContext context, bool isExpanded) {
                      return Card(
                        elevation: 5,
                        child: ListTile(
                          title: Center(
                            child: Text(
                              item.name,
                              style: TextStyle(
                                color: Theme.of(context).primaryColorDark,
                                fontSize: 20,
                              ),
                            ),
                          ),
                          trailing: _isDanger(item)
                              ? Tooltip(
                                  message:
                                      'In acest loc public nu se respecta regulile',
                                  child: Icon(
                                    Icons.warning,
                                    color: Colors.red,
                                  ),
                                )
                              : null,
                        ),
                      );
                    },
                    body: Container(
                      height: 50,
                      child: Card(
                        elevation: 5,
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                          children: [
                            Text('Proprietar: ${item.owner}'),
                            Text('Adresa: ${item.address}'),
                            Text(
                                'Capacitate maxima: ${item.maxCapacity.toString()}'),
                            Text(
                                'Numar de persoane intrate fara masca: ${item.numberOfReports.toString()}'),
                          ],
                        ),
                      ),
                    ),
                    isExpanded: item.isExpanded,
                  );
                }).toList(),
              );
            } else {
              throw Exception('eroare');
            }
          }
        });
  }
}
