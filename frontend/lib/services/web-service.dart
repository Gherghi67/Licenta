import 'package:http/http.dart' as http;
import 'package:http/http.dart';

class Resource<T> {
  final String url;
  T Function(Response response) parse;

  Resource({required this.url, required this.parse});
}

class WebService {
  Future<T> load<T>(Resource<T> resource) async {
    final response = await http.get(Uri.parse(resource.url), headers: {
      "Access-Control-Allow-Origin": "*", // Required for CORS support to work
      // Required for cookies, authorization headers with HTTPS
      "Access-Control-Allow-Headers":
          "Origin,Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,locale",
      "Access-Control-Allow-Methods": "GET, POST, OPTIONS"
    });

    if (response.statusCode == 200 || response.statusCode == 201) {
      return resource.parse(response);
    } else {
      throw Exception('Failed to get the request');
    }
  }
}
