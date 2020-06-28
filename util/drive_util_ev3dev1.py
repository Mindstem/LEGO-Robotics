from ev3dev.ev3 import (
    Motor, LargeMotor, OUTPUT_B, OUTPUT_C,
    InfraredSensor, RemoteControl, INPUT_4
)


class IRBeaconRemoteControlledTank:
    def __init__(
            self,
            left_motor_port: str = OUTPUT_B,
            right_motor_port: str = OUTPUT_C,
            ir_sensor_port: str = INPUT_4,
            ir_beacon_channel: int = 1):
        self.left_motor = LargeMotor(address=left_motor_port)
        self.right_motor = LargeMotor(address=right_motor_port)

        self.ir_sensor = InfraredSensor(address=ir_sensor_port)
        self.remote_control = RemoteControl(sensor=self.ir_sensor,
                                            channel=ir_beacon_channel)


    def drive_by_ir_beacon(
            self,
            speed: float = 1000   # degrees per second
        ):
        # forward
        if self.remote_control.red_up and self.remote_control.blue_up:
            self.left_motor.run_forever(speed_sp=speed)
            self.right_motor.run_forever(speed_sp=speed)

        # backward
        elif self.remote_control.red_down and self.remote_control.blue_down:
            self.left_motor.run_forever(speed_sp=-speed)
            self.right_motor.run_forever(speed_sp=-speed)

        # turn left on the spot
        elif self.remote_control.red_up and self.remote_control.blue_down:
            self.left_motor.run_forever(speed_sp=-speed)
            self.right_motor.run_forever(speed_sp=speed)

        # turn right on the spot
        elif self.remote_control.red_down and self.remote_control.blue_up:
            self.left_motor.run_forever(speed_sp=speed)
            self.right_motor.run_forever(speed_sp=-speed)

        # turn left forward
        elif self.remote_control.red_up:
            self.right_motor.run_forever(speed_sp=speed)

        # turn right forward
        elif self.remote_control.blue_up:
            self.left_motor.run_forever(speed_sp=speed)

        # turn left backward
        elif self.remote_control.red_down:
            self.right_motor.run_forever(speed_sp=-speed)

        # turn right backward
        elif self.remote_control.blue_down:
            self.left_motor.run_forever(speed_sp=-speed)

        # otherwise stop
        else:
            self.left_motor.stop(stop_action=Motor.STOP_ACTION_COAST)
            self.right_motor.stop(stop_action=Motor.STOP_ACTION_COAST)
