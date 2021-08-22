import 'dart:convert';

import '../services/web-service.dart';
import './report.dart';

class PublicPlace {
  final int id;
  final int maxCapacity;

  final String name;
  final String owner;
  final String address;

  final List<Report> reports;

  PublicPlace({
    required this.id,
    required this.name,
    required this.owner,
    required this.reports,
    required this.address,
    required this.maxCapacity,
  });

  factory PublicPlace.fromJson(Map<String, dynamic> json) {
    return PublicPlace(
      id: json['id'],
      name: json['name'],
      owner: json['owner'],
      address: json['address'],
      maxCapacity: json['max_capacity'],
      reports: List<Report>.from(
        json['reports'].map((report) => Report.fromJson(report)),
      ),
    );
  }
}
