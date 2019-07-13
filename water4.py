
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
	
 def pump_id():
    pump_pin1(pin = 7)
    pump_pin2(pin = 18)
    pump_pin3(pin = 36)
    pump_pin4(pin = 37)
    return GPIO.output(pin)

def get_last_watered():
    try:
        f = open("last_watered.txt", "r")
        return f.readline()
    except:
        return "NEVER!"


# Sensors
      
def get_status_all():
    get_status(pin =8)
    get_status(pin = 29)
    get_status(pin = 31)
    get_status(pin = 33)
    return GPIO.input(pin)

# Pump 1
    
def auto_water(delay = 1, pump_id, get_status_all):
    consecutive_water_count1 = 0
    setup_all()
    print("Engage! Press CTRL+C to exit")
    try:
        while 1 and consecutive_water_count < 10:
            time.sleep(delay)
            wet = get_status_all == 1
            if not wet:
                if consecutive_water_count < 5:
                    pump_on(1, pump_id)
                consecutive_water_count += 1
            if wet:
                if consecutive_water_count > 5:
                    pump_off(1, pump_id)
                consecutive_water_count -= 1
            else:
                consecutive_water_count = 0
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
#	auto_water(delay = 1, pump_pin1 = 7, water_sensor_pin1 = 8)
        auto_water(delay = 1, pump_id, get_status_all)
main()
