import time
import gpiod
import subprocess

from gpiod.line import Direction, Value

LINE = 211 
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
        for i in range(1):
            tmp=gettemp()
            print("tmp:", tmp)
            if tmp >= threshold:
                print("zu warm!")
            else:
                print("cool enough")
            print(request._check_released())
            #request.set_value(LINE, Value.ACTIVE)
            #time.sleep(1)
            request.set_value(LINE, Value.INACTIVE)
            #time.sleep(5)
        request.release()

def gettemp():
    cmd="sensors | egrep -o -m 1 '(\+)([0-9]{1,2})(\.[0-9]{1,2})?' | head -1"
    temperature=subprocess.run(cmd, 
            shell=True, 
            text=True,
            capture_output=True,
            executable='/bin/bash')
    string = temperature.stdout
    return float(string[1:])

if __name__ == "__main__":
    run()
