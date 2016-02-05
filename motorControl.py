import time
import pigpio

pi = pigpio.pi()
defaultSpeed = 180
systemOn = True

#---------------------
#------Functions------
#---------------------

def increaseSpeed(motorSpeed):
    motorSpeed = motorSpeed + 5
    return motorSpeed

def decreaseSpeed(motorSpeed):
    motorSpeed = motorSpeed - 5
    return motorSpeed

def initializePin(modPin):
    pi.set_PWM_frequency(modPin, 400)
    pi.set_PWM_range(modPin, 500)

def shutdownMotor(motorSpeed):
    motorSpeed = 0
    return motorSpeed

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
initializePin(motorOne)
motorOneSpeed = defaultSpeed

print('Motor 2')
res = input()
motorTwo = res
initializePin(motorTwo)
motorTwoSpeed = defaultSpeed

print('Motor 3')
res = input()
motorThree = res
initializePin(motorThree)
motorThreeSpeed = defaultSpeed

print('Motor 4')
res = input()
motorFour = res
initializePin(motorFour)
motorFourSpeed = defaultSpeed

pi.set_PWM_dutycycle(motorOne,  motorOneSpeed)
pi.set_PWM_dutycycle(motorTwo,  motorTwoSpeed)
pi.set_PWM_dutycycle(motorThree,  motorThreeSpeed)
pi.set_PWM_dutycycle(motorFour,  motorFourSpeed)

print (" ")
print ("motorOne: %s" % (pi.get_PWM_range(motorOne)))
print ("motorOne: %s" % (pi.get_PWM_frequency(motorOne)))
print (" ")
print ("motorTwo: %s" % (pi.get_PWM_range(motorTwo)))
print ("motorTwo: %s" % (pi.get_PWM_frequency(motorTwo)))
print (" ")
print ("motorThree: %s" % (pi.get_PWM_range(motorThree)))
print ("motorThree: %s" % (pi.get_PWM_frequency(motorThree)))
print (" ")
print ("motorFour: %s" % (pi.get_PWM_range(motorFour)))
print ("motorFour: %s" % (pi.get_PWM_frequency(motorFour)))
print (" ")

#----------------------------------------
# All motors will now be initialized
# The loop-to-follow will receive inputs and then change motorspeeds accordingly
#----------------------------------------

print ('System initialized and running.')
print ('Follow your reference key or press 9 to shutdown')
print(" ")
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

        res = raw_input()

        if res == 'q':
            motorOneSpeed = increaseSpeed(motorOneSpeed)
        if res == 'a':
            motorOneSpeed = decreaseSpeed(motorOneSpeed)
        if res == 'z':
            motorOneSpeed = shutdownMotor(motorOneSpeed)        

        if res == 'w':
            motorTwoSpeed = increaseSpeed(motorTwoSpeed)
        if res == 's':
            motorTwoSpeed = decreaseSpeed(motorTwoSpeed)
        if res == 'x':
            motorTwoSpeed = shutdownMotor(motorTwoSpeed)

        if res == 'e':
            motorThreeSpeed = increaseSpeed(motorThreeSpeed)
        if res == 'd':
            motorThreeSpeed = decreaseSpeed(motorThreeSpeed)
        if res == 'c':
            motorThreeSpeed = shutdownMotor(motorThreeSpeed)

        if res == 'r':
            motorFourSpeed = increaseSpeed(motorFourSpeed)
        if res == 'f':
            motorFourSpeed = decreaseSpeed(motorFourSpeed)
        if res == 'v':
            motorFourSpeed = shutdownMotor(motorFourSpeed)

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
        
        if ((motorOneSpeed == 0) and (motorTwoSpeed == 0) and (motorThreeSpeed == 0) and (motorFourSpeed == 0)):
            pi.set_PWM_dutycycle(motorOne,  motorOneSpeed)
            pi.set_PWM_dutycycle(motorTwo,  motorTwoSpeed)
            pi.set_PWM_dutycycle(motorThree,  motorThreeSpeed)
            pi.set_PWM_dutycycle(motorFour,  motorFourSpeed)
            systemOn = False

print ("System Shutdown")

# Done


#print('***Press ENTER to quit***')
#res = raw_input()
