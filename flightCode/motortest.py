import time
import pigpio

pi = pigpio.pi()
dick = 180

print('***Connect Battery & Press ENTER to start')
res = raw_input()

print('***Enter GPIO Pin to Modify')
res = input()
modPin = res

pi.set_PWM_frequency(modPin,400)
pi.set_PWM_range(modPin, 2500)
pi.set_PWM_dutycycle(modPin,  dick)

print ('increase > a | decrease > z | set Wh > h|quit > 9')

cycling = True
try:
    while cycling:
        pi.set_PWM_dutycycle(modPin,  dick)
	print (dick)
        res = raw_input()
        if res == 'a':
            dick = dick + 5
        if res == 'z':
            dick = dick - 5
        if res == '9':
            cycling = False
finally:
    # shut down cleanly
    dick = 0
    pi.set_PWM_dutycycle(modPin,  dick)
    print ("dick var setting is: ")
    print (dick)

print('***Press ENTER to quit')
res = raw_input()
