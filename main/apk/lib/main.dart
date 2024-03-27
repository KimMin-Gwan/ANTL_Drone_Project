import 'package:flutter/material.dart';
import 'package:apk/src/home_widget.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return GetMaterialApp(
      initialBinding: BindingsBuilder(() {
        Get.lazyPut(() => JoystickController(), fenix: true);
      }),
      home: MainPage(),
    );
  }
}