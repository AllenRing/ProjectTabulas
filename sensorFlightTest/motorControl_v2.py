#---------------------------------------------------------------------------------------------------------------|
# Organization: AllenRing                                                                                       |
# -- Created by Ritch                                                                                           |
#                                                                                                               |
# This program is responsible for controlling the settings of RPi pins and the speed of the attached motors.    |
# It is also set up to execute other scripts (more to come).                                                    |
#                                                                                                               |
# Scripts:                                                                                                      |    
#   motorSpeedLimiter                                                                                           |
#     This program will countinuously check the frequency and dutycycle ranges of all pins assigned with motors.|
#---------------------------------------------------------------------------------------------------------------|

import logging
import sys
import time
import pigpio

from Adafruit_BNO055 import BNO055

#---------------------------------------------------------------------------------------------------------------|
# --- Initialize Orientation Sensor --- 
bno = BNO055.BNO055(serial_port='/dev/ttyAMA0', rst=18)

# Enable verbose debug logging if -v is passed as a parameter.
if len(sys.argv) == 2 and sys.argv[1].lower() == '-v':
    logging.basicConfig(level=logging.DEBUG)

# Initialize the BNO055 and stop if something went wrong.
if not bno.begin():
    raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

# Print system status and self test result.
status, self_test, error = bno.get_system_status()
print('System status: {0}'.format(status))
print('Self test result (0x0F is normal): 0x{0:02X}'.format(self_test))
# Print out an error if system status is in error mode.
if status == 0x01:
    print('System error: {0}'.format(error))
    print('See datasheet section 4.3.59 for the meaning.')

# Print BNO055 software revision and other diagnostic data.
sw, bl, accel, mag, gyro = bno.get_revision()
print('Software version:   {0}'.format(sw))
print('Bootloader version: {0}'.format(bl))
print('Accelerometer ID:   0x{0:02X}'.format(accel))
print('Magnetometer ID:    0x{0:02X}'.format(mag))
print('Gyroscope ID:       0x{0:02X}\n'.format(gyro))
#---------------------------------------------------------------------------------------------------------------|

pi = pigpio.pi()
systemOn = True
motorOneSpeed = 180
motorTwoSpeed = 180
motorThreeSpeed = 180
motorFourSpeed = 185

min = 180
strength = 218


#---------------------
#------Functions------
#---------------------

def initializeMotors(motorOne, motorTwo, motorThree, motorFour):
    pi.set_PWM_frequency(motorOne, 400)
    pi.set_PWM_range(motorOne, 2500)
    pi.set_PWM_frequency(motorTwo, 400)
    pi.set_PWM_range(motorTwo, 2500)
    pi.set_PWM_frequency(motorThree, 400)
    pi.set_PWM_range(motorThree, 2500)
    pi.set_PWM_frequency(motorFour, 400)
    pi.set_PWM_range(motorFour, 2500)

    pi.set_PWM_dutycycle(motorOne,  motorOneSpeed)
    pi.set_PWM_dutycycle(motorTwo,  motorTwoSpeed)
    pi.set_PWM_dutycycle(motorThree,  motorThreeSpeed)
    pi.set_PWM_dutycycle(motorFour,  motorFourSpeed)

def increaseSpeed(motorSpeed):
    motorSpeed = motorSpeed + 5
    return motorSpeed

def decreaseSpeed(motorSpeed):
    motorSpeed = motorSpeed - 5
    return motorSpeed

def shutdownMotor(motorSpeed):
    while motorSpeed > 0:
        motorSpeed = motorSpeed - 1
        return motorSpeed

#-----------------------------
#------Movement Fucntions-----
#-----------------------------

def strafeLeft():
    motorThreeSpeed = increaseSpeed(motorThreeSpeed)
    motorTwoSpeed = increaseSpeed(motorTwoSpeed)
    sleep(.5)
    motorThreeSpeed = decreaseSpeed(motorThreeSpeed)
    motorTwoSpeed = decreaseSpeed(motorTwoSpeed)

def strafeRight():
    motorOneSpeed = increaseSpeed(motorOneSpeed)
    motorFourSpeed = increaseSpeed(motorFourSpeed)
    sleep(.5)
    motorOneSpeed = decreaseSpeed(motorOneSpeed)
    motorFourSpeed = decreaseSpeed(motorFourSpeed)

def moveForward():
    motorFourSpeed = increaseSpeed(motorFourSpeed)
    motorTwoSpeed = increaseSpeed(motorTwoSpeed)
    sleep(.5)
    motorFourpeed = decreaseSpeed(motorFourSpeed)
    motorTwoSpeed = decreaseSpeed(motorTwoSpeed)

def moveBackwards():
    motorOneSpeed = increaseSpeed(motorOneSpeed)
    motorThreeSpeed = increaseSpeed(motorThreeSpeed)
    sleep(.5)
    motorThreeSpeed = decreaseSpeed(motorThreeSpeed)
    motorOneSpeed = decreaseSpeed(motorTwoSpeed)

#-----------------------------
#------Begin the program------
#-----------------------------

#----------------------------------------
# This will prompt for the pins to modify
# Each entered pin will be initialized and have global values set to default
#----------------------------------------

print('***Connect Battery & Press ENTER to start***')
res = raw_input()

print('***Enter Pins for Each Prompted Motor***')

print('Motor 1')
res = input()
motorOne = res

print('Motor 2')
res = input()
motorTwo = res

print('Motor 3')
res = input()
motorThree = res

print('Motor 4')
res = input()
motorFour = res

#----------------------------------------
# All motors will now be initialized
# The loop-to-follow will receive inputs and then change motorspeeds accordingly
#----------------------------------------

initializeMotors(motorOne, motorTwo, motorThree, motorFour)

res = raw_input()
motorOneSpeed = 195
motorTwoSpeed = 185
motorThreeSpeed = 190
motorFourSpeed = 190

res = raw_input()

print ('System initialized and running.')
print ('Follow your reference key or press 9 to shutdown')
cycling = True
try:
    while cycling:
        pi.set_PWM_dutycycle(motorOne,  motorOneSpeed)
        pi.set_PWM_dutycycle(motorTwo,  motorTwoSpeed)
        pi.set_PWM_dutycycle(motorThree,  motorThreeSpeed)
        pi.set_PWM_dutycycle(motorFour,  motorFourSpeed)

        print ("motorOne: %s" % (motorOneSpeed))
        print ("motorTwo: %s" % (motorTwoSpeed))
        print ("motorThree: %s" % (motorThreeSpeed))
        print ("motorFour: %s" % (motorFourSpeed))     

        # Read the Euler angles for heading, roll, pitch (all in degrees).
        heading, roll, pitch = bno.read_euler()
        # Read the calibration status, 0=uncalibrated and 3=fully calibrated.
        sys, gyro, accel, mag = bno.get_calibration_status()
        # Print everything out.
        print('Heading={0:0.2F} Roll={1:0.2F} Pitch={2:0.2F}\tSys_cal={3} Gyro_cal={4} Accel_cal={5} Mag_cal={6}'.format(heading, roll, pitch, sys, gyro, accel, mag))
        
        range = (strength - min)
        

        Right = ((roll / float(30)) * range)
        Left = -1 * ((roll / float(30)) * range)

        Front = -1 * ((pitch / float(30)) * range)
        Back = ((pitch / float(30)) * range)

        #sets the motors actual values
        motorTwoSpeed = Back + Right + strength
        motorFourSpeed = Back + Left + strength
        motorThreeSpeed = Front + Right + strength
        motorOneSpeed = Front + Left + strength
        """
        if (motorOneSpeed > 220):
            motorOneSpeed = 220
            print("Excess prevented on Motor 1")           
        if (motorTwoSpeed > 210):
            motorTwoSpeed = 210
            print("Excess prevented on Motor 2")           
        if (motorThreeSpeed > 215):
            motorThreeSpeed = 215
            print("Excess prevented on Motor 3")            
        if (motorFourSpeed > 215):
            motorFourSpeed = 215
            print("Excess prevented on Motor 4")
            
        """
    # End of while
# End of Try

#----------------------------------------
# When the while loop has ended, the code will proceed here
# This will shutdown all motors in increments of one, until the speed value has reached '0'
#----------------------------------------

finally:
    # shut down cleanly
    while (systemOn):
        if motorOneSpeed > 0:
            motorOneSpeed = motorOneSpeed - 1
        if motorTwoSpeed > 0:
            motorTwoSpeed = motorTwoSpeed - 1
        if motorThreeSpeed > 0:
            motorThreeSpeed = motorThreeSpeed - 1
        if motorFourSpeed > 0:
            motorFourSpeed = motorFourSpeed - 1
        
        pi.set_PWM_dutycycle(motorOne,  motorOneSpeed)
        pi.set_PWM_dutycycle(motorTwo,  motorTwoSpeed)
        pi.set_PWM_dutycycle(motorThree,  motorThreeSpeed)
        pi.set_PWM_dutycycle(motorFour,  motorFourSpeed)

        if (motorOneSpeed == 0) and (motorTwoSpeed == 0) and (motorThreeSpeed == 0) and (motorFourSpeed == 0):
            systemOn = False
            
monitoring = False

print ("System Shutdown")

# Done