import RPi.GPIO as GPIO
from time import sleep
import time
from w1thermsensor import W1ThermSensor
from mqtt.publisher import Publisher
from const.const import TOPIC

class Temperature:
    def __init__(self, serverPin):
        self.serverPin = serverPin
        self.topic = TOPIC

        # declare pin
        self.servoPin = 25
        # set to use Broadcom GPIO numbers
        GPIO.setmode(GPIO.BCM)
        # disable warnings
        GPIO.setwarnings(False)
        # set servo pin as output
        GPIO.setup(self.servoPin, GPIO.OUT)
        # initialize PWM on pin at 50Hz
        self.pwm = GPIO.PWM(self.servoPin, 50)
        # start pwm with 0 duty cycle so it doesn't set any angles on start
        self.pwm.start(2.5)
        # DS18B20 Temperature Sensor reading
        self.sensor = W1ThermSensor()
    
    # create function so we can call this later
    def Set_Angle(self, angle):

        # calculate duty cycle from angle
        duty = angle / 18 + 2
        # turn on servo pin
        GPIO.output(self.servoPin, True)
        # set duty cycle to pin
        self.pwm.ChangeDutyCycle(duty)
        # wait 1s for servo to move into position
        sleep(0.9)
        print('angle =', angle)
        # turn off servo pin
        GPIO.output(self.servoPin, False)
        # set duty cycle to 0 to stop signal
        self.pwm.ChangeDutyCycle(0)
    
    def Publish_temp(self,temperature_c):
        publisher = Publisher(self.topic)   
        publisher.publish_msg(temperature_c)
    
    def getTempReadings(self):
        # main loop
        while True:
            try:
                # Print the values to the serial port
                temperature_c = self.sensor.get_temperature()               
                print("Temp:{:.1f} C ".format(temperature_c))
                
                #Publish_temp(temperature_c)
                    
                #simplyfy the below function ----------------
                if temperature_c <= 15:
                    self.Set_Angle(0)
                        
                elif 15 <= temperature_c <= 25:
                    self.Set_Angle(45)
                        
                elif 25 <= temperature_c <= 35:
                    self.Set_Angle(90)
                        
                elif 35 <= temperature_c <= 38:
                    self.Set_Angle(135)
                        
                #elif temperature_c <= 33:
                    # self.Set_Angle(45)
                elif temperature_c >= 38:
                    self.Set_Angle(180)
                    
                #----------------------------------------------#
                
            except RuntimeError as error:
                print(error.args[0])
                continue
            except Exception as error:
                raise error
            sleep(0.1)
            
            # stop pwm on exit
        pwm.stop()

            # release GPIOs on exit
        GPIO.cleanup()