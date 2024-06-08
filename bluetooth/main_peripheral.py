import bluetooth

from peripheral import BLEPeripheral
from ble_services_definitions import ROBOT_UUID, MOTOR_RX_UUID, MOTOR_TX_UUID
from parser import decode_motor, encode_motor
from pin_map import MOTOR_LEFT_FORWARD, MOTOR_LEFT_BACKWARD, MOTOR_RIGHT_FORWARD, MOTOR_RIGHT_BACKWARD
from motor import Motor
from time import sleep


def main():
    controller = BLEPeripheral(add_robot_stuff=True)
    motor_left = Motor(MOTOR_LEFT_FORWARD, MOTOR_LEFT_BACKWARD)
    motor_right = Motor(MOTOR_RIGHT_FORWARD, MOTOR_RIGHT_BACKWARD)

    def read(buffer: memoryview):
        left_direction, right_direction, left_speed, right_speed = decode_motor(bytes(buffer))
        print(f"set left motor forwards: {left_direction} with speed {left_speed}")
        print(f"set right motor forwards: {right_direction} with speed {right_speed}")
        motor_left.set_direction(left_direction)
        motor_left.set_speed(left_speed)
        motor_right.set_direction(right_direction)
        motor_right.set_speed(right_speed)
        to_send = encode_motor(motor_left.moving_forwards(), motor_right.moving_forwards(),
                               motor_left.get_speed(), motor_right.get_speed())
        controller.send(ROBOT_UUID, MOTOR_TX_UUID, to_send)

    controller.register_read_callback(MOTOR_RX_UUID, read)
    controller.advertise()
    while True:
        sleep(65535)  # sleep forever


if __name__ == "__main__":
    main()
