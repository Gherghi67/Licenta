import 'dart:async';
import 'dart:convert';

import 'package:http/http.dart' as http;

import '../models/public-place.dart';

class PublicPlaceService {
  List<PublicPlace> _publicPlaces = [];

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
}
