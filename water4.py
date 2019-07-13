
# External module imp
import RPi.GPIO as GPIO
import datetime
import time

# Constants

pump1=8
pump2=29
pump3=31
pump4=33
sensor1=8
sensor2=29
sensor3=31
sensor4=33

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
# When sensor reports 0 it's dry, 1 is wet

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
      
def get_status(pin):
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
                    pump_on(1, pump_pin1)
                consecutive_water_count1 += 1
            if wet1:
                if consecutive_water_count1 > 5:
                    pump_off(1, pump_pin1)
                consecutive_water_count1 -= 1
            else:
                consecutive_water_count1 = 0
    except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
        GPIO.cleanup() # cleanup all GPI

def pump_on(pump_id, control_pin):
    f = open("last_watered.txt", "a")
    f.write("Pump {} ON at {}".format(pump_id, datetime.datetime.now()))
    f.close()
    GPIO.output(control_pin, GPIO.HIGH)
    time.sleep(1)

def pump_off(pump_id, control_pin):
    f = open("last_watered.txt", "a")
    f.write("Pump {} OFF at {}".format(pump_id, datetime.datetime.now()))
    f.close()
    GPIO.output(pump_id, control_pin, GPIO.LOW)
    time.sleep(1)

def main():
	auto_water(delay = 1, pump_pin1 = 7, water_sensor_pin1 = 8)

main()
