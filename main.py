from machine import Pin, Timer
from neopixel import NeoPixel
import time

MAX_BRIGHTNESS = 255
MIN_BRIGHTNESS = 1

SEGMENT_INTERVAL = 30
PRE_COLOR = (0,MAX_BRIGHTNESS,0)
POST_COLOR = (0,0,MAX_BRIGHTNESS)
CURRENT_COLOR = (MAX_BRIGHTNESS,0,0)

STOP_DISPLAY_TIME = 2

NP_PIN = 16
NP_COUNT = 8


BUTTON_1_PIN = 13
BUTTON_2_PIN = 14
BUTTON_3_PIN = 15

class Command:
    IDLE = 0
    STARTED = 1
    STOPPING = 2
    ADD_MINUTE = 3

t = None

def start_irq(pin):
    global t
    t.current_state = Command.STARTED
    t.last_command_time = time.time()
    print('pressed start')

def stop_irq(pin):
    global t
    if t.current_state == Command.STARTED:
        t.current_state = Command.STOPPING
        t.last_command_time = time.time()
    print('pressed stop')


def add_irq(pin):
    global t
    if t.current_state not in [Command.STOPPING,Command.STARTED]:
        t.current_state = Command.ADD_MINUTE
        t.last_command_time = time.time()
    print('pressed add')

class KiddoTimer:
    def __init__(self):
        self.current_state = Command.IDLE
        self.last_command_time = time.time()
        self.remaining_time = 0
        self.np_pin = Pin(NP_PIN,Pin.OUT)
        self.np = NeoPixel(self.np_pin,NP_COUNT)

    def add_minute(self):
        self.remaining_time += 60
        print(f'Current time: {self.remaining_time}')
        self.current_state = Command.IDLE
        for i in range(NP_COUNT):
            min_time = i*SEGMENT_INTERVAL
            max_time = (i+1)*SEGMENT_INTERVAL
            print(f'{i}: min {min_time} max {max_time}')
            if self.remaining_time == max_time:
                print(f'active {i}')
                self.np[i] = (0,0,MAX_BRIGHTNESS)
            else:
                self.np[i] = (MIN_BRIGHTNESS,0,0)
            
        self.np.write()

    def display_idle(self):
        for i in range(NP_COUNT):
            self.np[i] = (MIN_BRIGHTNESS,0,0)
        self.np.write()
        
    def display_time(self):
        if self.remaining_time < 1:
            self.current_state = Command.STOPPING
            return
        self.remaining_time -= 1
        print(f'Remaining time: {self.remaining_time}')
        active_pixel = -1
        for i in range(NP_COUNT):
            min_time = i*SEGMENT_INTERVAL
            max_time = (i+1)*SEGMENT_INTERVAL
              
            if self.remaining_time > max_time:
                self.np[i] = PRE_COLOR
            
            elif self.remaining_time < max_time and self.remaining_time > min_time:
                self.np[i] = CURRENT_COLOR
                active_pixel = i
            
            elif self.remaining_time < min_time:
                self.np[i] = POST_COLOR
        self.np.write()
        time.sleep(0.5)
        if active_pixel != -1:
            self.np[active_pixel] = (0,0,0)
            self.np.write()
            
    def display_finish(self):
        # if time.time() > self.last_command_time + STOP_DISPLAY_TIME:
            # self.current_state = Command.IDLE
        for i in range(NP_COUNT):
            self.np[i] = (MAX_BRIGHTNESS,MAX_BRIGHTNESS,MAX_BRIGHTNESS)
        self.np.write()
        self.current_state = Command.IDLE       

    def tick(self,t):
        if self.current_state == Command.IDLE:
            self.display_idle()
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