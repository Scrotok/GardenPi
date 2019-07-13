
# External module imp
import RPi.GPIO as GPIO
import datetime
import time

init = False

GPIO.setmode(GPIO.BOARD) # Broadcom pin-numbering scheme

# Configures one sensor and one control pin.
# Output LOW on the control pin so the pump native state is OFF

def setup_one(sensor_pin, control_pin):
    GPIO.setup(sensor_pin, GPIO.IN)
    GPIO.setup(control_pin, GPIO.OUT)
    GPIO.output(control_pin, GPIO.LOW)

# Pump pins are 7, 18, 36 and 37 - 5v shared from pin 3
# Sensor pins are 8, 29, 31 and 33 - 5v shared from pin 1

def setup_all():
    setup_one(8, 7)
    setup_one(29, 18)
    setup_one(31, 36)
    setup_one(33, 37)

def get_last_watered():
    try:
        f = open("last_watered.txt", "r")
        return f.readline()
    except:
        return "NEVER!"


# Sensors
      
def get_status1(pin = 8):
    return GPIO.input(pin)

def get_status2(pin = 29):
    return GPIO.input(pin)

def get_status3(pin = 31):
    return GPIO.input(pin)

def get_status4(pin = 33):
    return GPIO.input(pin)

# Pump 1
    
def auto_water(delay = 1, pump_pin1 = 7, water_sensor_pin1 = 8):
    consecutive_water_count1 = 0
    setup_all()
    print("Engage! Press CTRL+C to exit")
    try:
        while 1 and consecutive_water_count1 < 10:
            time.sleep(delay)
            wet1 = get_status1(pin = water_sensor_pin1) == 1
            if not wet1:
                if consecutive_water_count1 < 5:
                    pump_on1(pump_pin1, 1)
                consecutive_water_count1 += 1
            if wet1:
                if consecutive_water_count1 > 5:
                    pump_off1(pump_pin1, 0)
                consecutive_water_count1 -= 1
            else:
                consecutive_water_count1 = 0
    except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
        GPIO.cleanup() # cleanup all GPI

def pump_on1(pump_pin1 = 7, delay = 1):
    init_output(pump_pin1)
    f = open("last_watered.txt", "w")
    f.write("Last watered1 {}".format(datetime.datetime.now()))
    f.close()
    GPIO.output(pump_pin1, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(pump_pin1, GPIO.LOW)

def pump_off1(pump_pin1 = 7, delay = 1):
    init_output(pump_pin1)
    f = open("last_watered.txt", "w")
    f.write("Last watered1 {}".format(datetime.datetime.now()))
    f.close()
    GPIO.output(pump_pin1, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(pump_pin1, GPIO.LOW)
