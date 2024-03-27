import 'package:flutter/material.dart';
import 'package:get/get.dart';

class MainPage extends GetView<JoystickController> {
  const MainPage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Obx(() {
          return Column(
            children: [
              Expanded(
                child: Stack(
                  alignment: Alignment.center,
                  children: [
                    Align(
                      alignment: Alignment.center,
                      child: Transform.translate(
                          offset: controller.circle.value,
                          child: CircleAvatar(backgroundColor: Colors.green)
                      ),
                    ),
                    Positioned(
                      left: 40,
                      bottom: 50,
                      child: GestureDetector(
                        onPanStart: (details) {
                          controller.center.value = details.localPosition;
                          controller.movement.value = Offset(0, 0);
                        },
                        onPanUpdate: (details) {
                          controller.updatePosition(details);
                        },
                        onPanEnd: (details) {
                          controller.movement.value = Offset(0, 0);
                        },
                        child: CircleAvatar(
                          radius: controller.radius,
                          backgroundColor: Colors.grey[300],
                          child: Transform.translate(
                            offset: controller.movement.value,
                            child: CircleAvatar(
                              backgroundColor: Colors.grey[700],
                            ),
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          );
        }),
      ),
    );
  }
}


class JoystickController extends GetxController {
  // 조이스틱 중심점 위치
  var center = Offset(0, 0).obs;

  // 조이스틱 움직임 위치
  var movement = Offset(0, 0).obs;

  // 조이스틱으로 움직이는 원 위치
  var circle = Offset(0, 0).obs;

  // 배경 원 반지름
  double radius = 50;

  updatePosition(DragUpdateDetails position) {
    // 현재 드래그 위치와 초기 드래그 위치의 차이 계산해서 movement 변수에 저장
    movement.value = position.localPosition - center.value;

    // 현재 드래그 위치와 원점(조이스틱 중심) 간의 거리 계산
    double distance = movement.value.distance;

    // 만약 드래그 위치가 조이스틱의 원의 반지름을 초과하면
    if (distance > radius) {
      // 드래그 위치를 조이스틱의 원 둘레에 맞게 조정
      movement.value = movement.value * (radius / distance);
    }
    print(movement.value);

    circle.value += movement.value * 0.1;
  }
}


