class Report {
  final int id;
  final int publicPlaceId;
  final DateTime timestamp;
  final bool hasMask;

  Report({
    required this.id,
    required this.publicPlaceId,
    required this.timestamp,
    required this.hasMask,
  });

  factory Report.fromJson(Map<String, dynamic> json) {
    return Report(
      id: json['id'],
      publicPlaceId: json['public_place_id'],
      timestamp: DateTime.parse(json['timestamp']),
      hasMask: json['has_mask'],
    );
  }
}
