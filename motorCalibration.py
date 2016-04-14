#---------------------------------------------------------------------------------------------------------------|
# Organization: AllenRing                                                                                       |
# -- Created by Ritch                                                                                           |
#                                                                                                               |
# This program is responsible for controlling the settings of RPi pins and the speed of the attached motors.    |
# It is also set up to execute other scripts (more to come).                                                    |
#---------------------------------------------------------------------------------------------------------------|

#------------------------------
#-----Variables & Imports------
#------------------------------

import time
import pigpio

pi = pigpio.pi()
systemOn = True
motorOneSpeed, motorTwoSpeed motorThreeSpeed, motorFourSpeed = 0

#---------------------
#------Functions------
#---------------------

def initializeMotors(motorOne, motorTwo, motorThree, motorFour):
    pi.set_PWM_dutycycle(motorOne,  motorOneSpeed)
    pi.set_PWM_dutycycle(motorTwo,  motorTwoSpeed)
    pi.set_PWM_dutycycle(motorThree,  motorThreeSpeed)
    pi.set_PWM_dutycycle(motorFour,  motorFourSpeed)

    pi.set_PWM_frequency(motorOne, 500)
    pi.set_PWM_range(motorOne, 100)
    pi.set_PWM_frequency(motorTwo, 500)
    pi.set_PWM_range(motorTwo, 100)
    pi.set_PWM_frequency(motorThree, 500)
    pi.set_PWM_range(motorThree, 100)
    pi.set_PWM_frequency(motorFour, 500)
    pi.set_PWM_range(motorFour, 100)

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
#------Begin the program------
#-----------------------------

print('***Connect Battery & Press ENTER to start***')
res = raw_input()

print('***Beginning***')
initializeMotors(motorOne, motorTwo, motorThree, motorFour)

print('Press enter to throttle the motors at 10%')
motorOneSpeed, motorTwoSpeed, motorThreeSpeed, motorFourSpeed = 10
print ('System initialized and running.')

#----------------------------------------
# All motors will now be initialized
# The loop-to-follow will receive inputs and then change motorspeeds accordingly
#----------------------------------------

print ('Follow your reference key or press 9 to shutdown')

cycling = True
try:
    while cycling:
        pi.set_PWM_dutycycle(motorOne,  motorOneSpeed)
        pi.set_PWM_dutycycle(motorTwo,  motorTwoSpeed)
        pi.set_PWM_dutycycle(motorThree,  motorThreeSpeed)
        pi.set_PWM_dutycycle(motorFour,  motorFourSpeed)

        print ("Motor One: %s" % (motorOneSpeed))
        print ("Motor Two: %s" % (motorTwoSpeed))
        print ("Motor Three: %s" % (motorThreeSpeed))
        print ("Motor Four: %s" % (motorFourSpeed))

        res = raw_input()

        if res == 'q':
            motorOneSpeed = increaseSpeed(motorOneSpeed)
        if res == 'a':
            motorOneSpeed = decreaseSpeed(motorOneSpeed)
        if res == 'z':
            motorOneSpeed = 0     

        if res == 'w':
            motorTwoSpeed = increaseSpeed(motorTwoSpeed)
        if res == 's':
            motorTwoSpeed = decreaseSpeed(motorTwoSpeed)
        if res == 'x':
            motorTwoSpeed = 0

        if res == 'e':
            motorThreeSpeed = increaseSpeed(motorThreeSpeed)
        if res == 'd':
            motorThreeSpeed = decreaseSpeed(motorThreeSpeed)
        if res == 'c':
            motorThreeSpeed = 0

        if res == 'r':
            motorFourSpeed = increaseSpeed(motorFourSpeed)
        if res == 'f':
            motorFourSpeed = decreaseSpeed(motorFourSpeed)
        if res == 'v':
            motorFourSpeed = 0

        if res == '9':
            cycling = False
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