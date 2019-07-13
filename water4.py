
# External module imports
import RPi.GPIO as GPIO
import datetime
import time

# There will be one instance of PumpSystem for each pair of
# sensor and control pins, and each instance contains the
# current state (e.g. how long it's been turned on).

class PumpSystem(object):
    def __init__(self, pump_id, sensor_pin, control_pin):
        self.pump_id = pump_id
        self.sensor_pin = sensor_pin
        self.control_pin = control_pin
        self.consecutive_water_count = 0
        self.is_pumping = False

        # Setup I/Os
        GPIO.setup(sensor_pin, GPIO.IN)
        GPIO.setup(control_pin, GPIO.OUT)
        # Turn the pump off
        GPIO.output(control_pin, GPIO.LOW)

    def get_status(self):
        wet = GPIO.input(self.sensor_pin)
        print('Read status:', wet)
        return wet

    def pump_on(self):
        if self.is_pumping:
            # Pump is already on; nothing to do
            return

        f = open("last_watered.txt", "a")
        f.write("Pump {} ON at {}".format(self.pump_id, datetime.datetime.now()))
        f.close()
        GPIO.output(self.control_pin, GPIO.HIGH)
        self.consecutive_water_count += 1
        self.is_pumping = True

    def pump_off(self):
        if not self.is_pumping:
            # Pump is already off; nothing to do
            return

        f = open("last_watered.txt", "a")
        f.write("Pump {} OFF at {}".format(self.pump_id, datetime.datetime.now()))
        f.close()
        GPIO.output(self.control_pin, GPIO.LOW)
        self.consecutive_water_count = 0
        self.is_pumping = False

# ------------------------- End of class PumpSystem -------------------------

def get_last_watered():
    try:
        f = open("last_watered.txt", "r")
        return f.readline()
    except:
        return "NEVER!"


# Pump 1
    
def auto_water(system_x):
    print("Engage! Press CTRL+C to exit")
    delay = 2
    try:
        while True:
            time.sleep(delay)
            wet = system_x.get_status() == 1
            if not wet:
                if system_x.consecutive_water_count < 5:
                    system_x.pump_on()
            else:
                if system_x.consecutive_water_count > 5:
                    system_x.pump_off()
    except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
        GPIO.cleanup() # cleanup all GPI

def main():
    # Must be run before any other GPIO calls
    GPIO.setmode(GPIO.BOARD) # Broadcom pin-numbering scheme

    # Pump pins are 7, 18, 36 and 37 - 5v shared from pin 3
    # Sensor pins are 8, 29, 31 and 33 - 5v shared from pin 1

    # Only set up first pump system at this point
    system_1 = PumpSystem(1, 8, 7)

    # Later, can do:
    # pumps = [
    #     PumpSystem(1, 8, 7)
    #     PumpSystem(2, 29, 18)
    #     PumpSystem(3, 31, 36)
    #     PumpSystem(4, 33, 37)
    # ]

    auto_water(system_1)


main()
