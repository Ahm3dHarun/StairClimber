#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, GyroSensor, TouchSensor, UltrasonicSensor
from pybricks.parameters import Port, Direction, Button
from pybricks.tools import wait
from pybricks.media.ev3dev import Font, SoundFile

# Initialize the EV3 brick.
ev3 = EV3Brick()

# Configure the front motor, which drives the front wheels.  Set the
# motor direction to counterclockwise, so that positive speed values
# make the robot move forward.
front_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE)

# Configure the rear motor, which drives the rear wheels.  Set the motor
# direction to counterclockwise, so that positive speed values make the
# robot move forward.

#rear_motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
rear_motor = Motor(Port.D, Direction.COUNTERCLOCKWISE)



# Configure the lift motor, which lifts the rear structure.  It has an
# 8-tooth, a 24-tooth, and a 40-tooth gear connected to it.  Set the
# motor direction to counterclockwise, so that positive speed values
# make the rear structure move upward.
#lift_motor = Motor(Port.D, Direction.COUNTERCLOCKWISE, [8, 24, 40])



lift_motor = Motor(Port.A, Direction.COUNTERCLOCKWISE, [8, 24, 40])
# Set up the Gyro Sensor.  It is used to measure the angle of the robot.
# Keep the Gyro Sensor and EV3 steady when connecting the cable and
# during start-up of the EV3.
gyro_sensor = GyroSensor(Port.S2)

sonar_sensor = UltrasonicSensor(Port.S4)

# Set up the Touch Sensor.  It is used to detect when the rear
# structure has moved to its maximum position.
touch_sensor = TouchSensor(Port.S3)

steps = 3

def reset_climber():
    rear_motor.dc(-20)
    lift_motor.dc(100)
    while not touch_sensor.pressed():
        wait(10)
    lift_motor.dc(-100)
    rear_motor.dc(40)
    wait(50)
    lift_motor.run_angle(-145, 510)
    rear_motor.hold()
    lift_motor.run_angle(-30, 15)
    lift_motor.reset_angle(0)
    wait(10)
    gyro_sensor.reset_angle(0)
    wait(100)


def climb_up_stairs(steps):
    while steps > 0:

        # Run the front and rear motors so the robot moves forward.
        front_motor.dc(100)
        rear_motor.dc(90)

        # Keep moving until the robot is at an angle of at least 10 degrees.
        while gyro_sensor.angle() < 10:
            wait(10)

        # Run the lift motor to move the rear structure up, while
        # simultaneously running the front and rear motors.
        lift_motor.dc(85)
        front_motor.dc(80)
        rear_motor.dc(50)

        # Keep moving the rear structure up until the Touch Sensor is
        # pressed, or the robot is at an angle of less than -3 degrees.
        while not touch_sensor.pressed():
            if gyro_sensor.angle() < -4:
                break
            #wait(10)
        lift_motor.hold()

        # Move the robot forward for some time using the front and rear
        # motors.
        front_motor.dc(100)
        rear_motor.dc(90)
        wait(150) # just edited 

        # Play a sound and pull the rear structure up so it gets back to
        # its starting position.  Keep moving forward slowly by
        # simultaneously running the front and rear motors.
        ev3.speaker.beep()        
        front_motor.dc(100)
        rear_motor.dc(80)
        lift_motor.run_target(200, 0)

        # Update the "steps" variable and display it on the screen.
        steps -= 1


def on_edge(distance):
  return distance >= 150 and distance <= 190

def climb_down_stairs(steps):
    front_motor.dc(-40)
    rear_motor.dc(-40)
    while not on_edge(sonar_sensor.distance()):
        wait(30)


    front_motor.hold()
    rear_motor.hold()
    lift_motor.hold()

    front_motor.dc(-30)
    rear_motor.dc(-30)

    wait(1300)

    front_motor.hold()
    rear_motor.hold()
    lift_motor.hold()


    lift_motor.run_angle(80, 360)
    front_motor.dc(-40)

    wait(1000)

    front_motor.hold()
    rear_motor.hold()
    lift_motor.hold()



    front_motor.dc(-27)
    rear_motor.dc(-40)
    lift_motor.dc(-50)
    # lift_motor.run_angle(-60, 360)
    wait(4500)


    front_motor.hold()
    rear_motor.hold()
    lift_motor.hold()


    front_motor.dc(-40)
    rear_motor.dc(-40)
    wait(1700)

    front_motor.hold()
    rear_motor.hold()
    lift_motor.hold()

    """
    front_motor.dc(-20)
    rear_motor.dc(-20)
    wait(2000)

    front_motor.hold()
    rear_motor.hold()
    lift_motor.hold()
    """
  # edge = 166 , platform = 63


def settle_robot():
    reset_climber()
    climb_up_stairs(3)
    wait(1000)

    
    front_motor.dc(30)
    rear_motor.dc(30)
    wait(1000)
    
    climb_down_stairs(1)
    wait(1000)
    reset_climber()
    wait(1000)


    climb_down_stairs(1)
    wait(1000)
    reset_climber()
    wait(1000)

    climb_down_stairs(1)
    wait(1000)


def main():
    #reset_climber()
    #climb_down_stairs(1)
    settle_robot()

if __name__ == '__main__':
    ev3.speaker.beep()
    main()
    ev3.speaker.beep()