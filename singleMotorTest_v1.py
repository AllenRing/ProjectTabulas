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

import time
import pigpio

pi = pigpio.pi()
systemOn = True
motorOneSpeed = 185

#-----------------------------
#------Begin the program------
#-----------------------------

print('***Connect Battery & Press ENTER to start***')
res = raw_input()

print('***Enter Pins for Each Prompted Motor***')

print('Motor 1')
res = input()
motorOne = res

pi.set_PWM_frequency(motorOne, 400)
pi.set_PWM_range(motorOne, 500)

pi.set_PWM_dutycycle(motorOne,  motorOneSpeed)

print (" ")
print ("motorOne: %s" % (pi.get_PWM_range(motorOne)))
print ("motorOne: %s" % (pi.get_PWM_frequency(motorOne)))
print (" ")

#----------------------------------------
# All motors will now be initialized
# The loop-to-follow will receive inputs and then change motorspeeds accordingly
#----------------------------------------

print ('System initialized and running.')
print ('Follow your reference key or press 9 to shutdown')
cycling = True
try:
    while cycling:
        pi.set_PWM_dutycycle(motorOne,  motorOneSpeed)

        print ("motorOne: %s" % (motorOneSpeed))     

        res = raw_input()

        if res == 'q':
            motorOneSpeed = motorOneSpeed + 5
        if res == 'a':
            motorOneSpeed = motorOneSpeed - 5
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
        
        if (motorOneSpeed == 0)
            pi.set_PWM_dutycycle(motorOne,  motorOneSpeed)
            systemOn = False
            
monitoring = False

print ("System Shutdown")

# Done
