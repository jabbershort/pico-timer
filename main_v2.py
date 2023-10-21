from machine import Pin, Timer
from neopixel import NeoPixel
import time
from params import *

t = None

def start_irq(pin):
    global t
    t.current_state = Command.STARTED
    t.last_command_time = time.time()

def stop_irq(pin):
    global t
    if t.current_state == Command.STARTED:
        t.current_state = Command.STOPPING
        t.last_command_time = time.time()


def add_irq(pin):
    global t
    if t.current_state not in [Command.STOPPING,Command.STARTED]:
        t.current_state = Command.ADD_MINUTE
        t.last_command_time = time.time()

class KiddoTimer:
    def __init__(self):
        self.current_state = Command.IDLE
        self.last_command_time = time.time()
        self.remaining_time = 0
        self.np_pin = Pin(NP_PIN,Pin.OUT)
        self.np = NeoPixel(self.np_pin,NP_COUNT)

    def add_minute(self):
        self.remaining_time += 60
        self.current_state = Command.IDLE

    def display_idle(self):
        
        
    def display_time(self):
        self.remaining_time -= 1
    
    def display_finish(self):
        if time.time() > self.last_command_time + STOP_DISPLAY_TIME:
            self.current_state = Command.IDLE
        

    def tick(self,t):
        print('tick')
        if self.current_state == Command.IDLE:
            self.display_idle()
            return
        elif self.current_state == Command.STARTED:
            self.display_time()
        elif self.current_state == Command.ADD_MINUTE:
            self.add_minute()
        elif self.current_state == Command.STOPPING:
            self.display_finish()

if __name__ == "__main__":
    print('init')
    start_button = Pin(BUTTON_1_PIN, Pin.IN, Pin.PULL_DOWN)
    stop_button = Pin(BUTTON_2_PIN, Pin.IN, Pin.PULL_DOWN)
    add_button = Pin(BUTTON_3_PIN, Pin.IN, Pin.PULL_DOWN)
    t = KiddoTimer()
    start_button.irq(trigger=Pin.IRQ_FALLING,handler=start_irq)
    stop_button.irq(trigger=Pin.IRQ_FALLING,handler=stop_irq)
    add_button.irq(trigger=Pin.IRQ_FALLING,handler=add_irq)
    tim = Timer()
    tim.init(mode=Timer.PERIODIC,freq=1,callback=t.tick)