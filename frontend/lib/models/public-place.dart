import 'dart:convert';

import '../services/web-service.dart';
import './report.dart';

class PublicPlace {
  final int id;

  final String name;
  final String owner;

  final List<Report> reports;

  PublicPlace({
    required this.id,
    required this.name,
    required this.owner,
    required this.reports,
  });

  factory PublicPlace.fromJson(Map<String, dynamic> json) {
    return PublicPlace(
      id: json['id'],
      name: json['name'],
      owner: json['owner'],
      reports: (jsonDecode(json['reports']) as List)
          .map((report) => Report.fromJson(report))
          .toList(),
    );
  }

  static Resource<List<PublicPlace>> get all {
    return Resource(
        url: 'http://127.0.0.1:8000/public-places/',
        parse: (response) {
          final result = json.decode(response.body);

          return result
              .map((publicPlace) => PublicPlace.fromJson(publicPlace))
              .toList();
        });
  }
}