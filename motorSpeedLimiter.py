import time
import pigpio
import motortest

pi = pigpio.pi()
motortest.declareGlobalMotors
monitoring = motortest.monitoring
monitoring = True

motorOne = motortest.motorOne
motorTwo = motortest.motorTwo
motorThree = motortest.motorThree
motorFour = motortest.motorFour

print("Ritch Senpai's Motor Speed Limiter")
print("Preventing Drone Explosions Since 2016!")

#-----------------------------
#------Begin the program------
#-----------------------------

# Loop until done monitoring. 
# Monitoring is updated by closing motortest program.
while monitoring:
	dcOneLimit = pi.get_PWM_dutycycle(motorOne)
	dcTwoLimit = pi.get_PWM_dutycycle(motorTwo)
	dcThreeLimit = pi.get_PWM_dutycycle(motorThree)
	dcFourLimit = pi.get_PWM_dutycycle(motorFour)

	fOneLimit = pi.get_PWM_frequency(motorOne)
	fTwoLimit = pi.get_PWM_frequency(motorTwo)
	fThreeLimit = pi.get_PWM_frequency(motorThree)
	fFourLimit = pi.get_PWM_frequency(motorFour)

	if dcOneLimit > 210 or dcTwoLimit > 210 or dcThreeLimit > 210 or dcFourLimit > 210:
		pi.set_PWM_dutycycle(motorOne,  0)
    	pi.set_PWM_dutycycle(motorTwo,  0)
    	pi.set_PWM_dutycycle(motorThree,  0)
    	pi.set_PWM_dutycycle(motorFour,  0)
    	print ('Motor Dutycycle exceeded on motor branch 1-4')

	monitoring = motortest.monitoring

print("GOODBYE!")
print("I sure hope stuff didn't explode!")
