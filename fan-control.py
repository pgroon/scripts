########################################
#
#  Short script to control the cooling
#  fan on a Bigtreetech Pi 1.2
#
########################################


import time
import gpiod
import subprocess

from gpiod.line import Direction, Value

LINE = 211 # Pin for onboard cooling fan socket
threshold = 46.0

def run():
    with gpiod.request_lines(
        "/dev/gpiochip0",
        consumer="fan-control",
        config={
            LINE: gpiod.LineSettings(
                direction=Direction.OUTPUT, output_value=Value.ACTIVE
            )
        },
    ) as request:
        while True:
            tmp=gettemp()
            print("tmp:", tmp)
            if tmp >= threshold:
                # turn cooling fan on
                request.set_value(LINE, Value.ACTIVE)
                print("zu warm!")
            else:
                # turn cooling fan off
                request.set_value(LINE, Value.INACTIVE)
                print("cool enough")
            print(request._check_released())
            # wait before next loop
            time.sleep(15)

def gettemp():
    # shell command to get the CPU temperature
    cmd="sensors | egrep -o -m 1 '(\+)([0-9]{1,2})(\.[0-9]{1,2})?' | head -1"
    # run the above command as a subprocess and return the result
    temperature=subprocess.run(cmd, 
            shell=True, 
            text=True,
            capture_output=True,
            executable='/bin/bash')
    string = temperature.stdout
    return float(string[1:])

if __name__ == "__main__":
    run()
