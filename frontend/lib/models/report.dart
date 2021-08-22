class Report {
  final int id;
  final int publicPlaceId;
  final DateTime timestamp;

  Report({
    required this.id,
    required this.publicPlaceId,
    required this.timestamp,
  });

  factory Report.fromJson(Map<String, dynamic> json) {
    return Report(
      id: json['id'],
      publicPlaceId: json['public_place_id'],
      timestamp: DateTime.parse(json['timestamp']),
    );
  }
}
