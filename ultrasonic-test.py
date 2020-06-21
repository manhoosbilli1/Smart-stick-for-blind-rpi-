import RPi.GPIO as GPIO
import time
import os
import serial



    
try:
    GPIO.setmode(GPIO.BCM)  #settings gpios as per BCM convention
    ser = serial.Serial('/dev/ttyUSB0', 9600)   #setup serial
    trig = 23
    echo = 24
    moisture = 22
    flame = 27
    shutdown_btn = 6

    GPIO.setup(trig, GPIO.OUT)
    GPIO.output(trig, 0)
    GPIO.setup(echo, GPIO.IN)
    GPIO.setup(moisture, GPIO.IN)
    GPIO.setup(flame, GPIO.IN)
    
    def ultrasonic():
        GPIO.output(trig, True)
        time.sleep(0.00001)
        GPIO.output(trig, False)
        while GPIO.input(echo) == 0:
                pass
        pulse_start = time.time()
        while GPIO.input(echo) == 1:   #code will only proceed if this condition is true
            pass
        pulse_end = time.time()     
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17000
        distance = round(distance, 2)   
        return distance
    
    
        
    
#-----------------------------MAIN LOOP-------------------  
    
    
    
    
    
    
    
    
    while True:
        time.sleep(0.05)  #settling delay. 
        
        distance = ultrasonic()
        
        #when shutting down
        #if(GPIO.input(shutdown_btn) == 0):  #when the shutdown button is grounded
        #   os.system('mpg321 shutting-down.mp3')
        #    time.sleep(1)
        #    os.system('sudo shutdown now -h')
            
        #flame detection
        if(GPIO.input(flame) == 0):
            os.system('mpg321 Fire-detected.mp3')
          
        #moisture detection
        elif(GPIO.input(moisture) == 0):                   #moisture detection 
            os.system('mpg321 moisture-detected.mp3')    #plays sound
        
        #obstacle detection
        elif(distance > 8 and distance <12):
            os.system('mpg321 sound.mp3')
        
        #pulse detection
        if(ser.in_waiting>0):             #pulse detection
            pulse = ser.readline()
            pulse = int(pulse.strip())
            if(pulse >50 and pulse < 160):
                #os.system('mpg321 BPM-high.mp3')
                print("pulse detected, {}".format(pulse))
            
            
            
except KeyboardInterrupt:
    print("Exiting program")

finally:
    print("Cleaning GPIO's")
    GPIO.cleanup()


