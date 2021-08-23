import 'dart:async';
import 'dart:typed_data';
import 'dart:convert';

import 'package:universal_io/io.dart';
import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Check mask',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: MyHomePage(title: 'Flutter Demo Home Page'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  MyHomePage({Key? key, required this.title}) : super(key: key);

  final String title;

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  bool _isUploaded = false;

  late File _imageFile;

  bool _hasMask = false;

  void _uploadImage() async {
    FilePickerResult? result = await FilePicker.platform.pickFiles(
        type: FileType.custom, allowedExtensions: ['png', 'jpg', 'jpeg']);

    if (result != null) {
      PlatformFile platformFile = result.files.first;

      Uri uri = Uri.parse('http://10.0.2.2:8000/public-places/1/reports');

      http.MultipartRequest request = new http.MultipartRequest('POST', uri);

      http.MultipartFile multipartFile = await http.MultipartFile.fromPath(
          'file', platformFile.path.toString());

      request.files.add(multipartFile);

      var streamedResponse = await request.send();

      var response = await streamedResponse.stream.bytesToString();

      if (streamedResponse.statusCode == 200) {
        setState(() {
          _imageFile = File(platformFile.path.toString());

          _isUploaded = true;

          if (json.decode(response)['has_mask'] == true) {
            print('masca');
            _hasMask = true;
          } else {
            print('fara masca');
            _hasMask = false;
          }
        });
      } else {
        throw Exception('Eroare');
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          children: [
            Container(
              decoration: BoxDecoration(border: Border.all(color: Colors.grey)),
              padding: const EdgeInsets.all(15.0),
              height: 400,
              width: 400,
              child: FittedBox(
                fit: BoxFit.fill,
                child: !_isUploaded
                    ? Image.asset(
                        'assets/placeholder.png',
                      )
                    : Image.file(_imageFile),
              ),
            ),
            Container(
              padding: const EdgeInsets.all(8.0),
              height: 50,
              width: 200,
              child: ElevatedButton(
                onPressed: _uploadImage,
                child: const Text('Upload image'),
              ),
            ),
            _isUploaded
                ? Text(_hasMask ? 'Cu masca' : 'Fara masca')
                : Container(),
          ],
        ),
      ),
    );
  }
}
