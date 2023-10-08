from machine import Pin
from neopixel import NeoPixel
import time

MAX_BRIGHTNESS = 10
MIN_BRIGHTNESS = 1

SEGMENT_INTERVAL = 30
PRE_COLOR = (0,MAX_BRIGHTNESS,0)
POST_COLOR = (0,0,MAX_BRIGHTNESS)
CURRENT_COLOR = (MAX_BRIGHTNESS,0,0)

t = None
last_push = 0
last_push_min =0
debounce = 1

current_command = None
running = False

class Command:
    IDLE = 0
    STARTED = 1
    STOPPING = 2
    ADD_MINUTE = 3

def add_minute_anim():
    global t

def tick_anim():
    global t

def stop_anim():
    global t

def irq_start_stop(pin):
    global t,  last_push, current_command
    if time.time() < debounce + last_push:
        print('stopped debounce')
        return
    print('button pushed')
    last_push = time.time()
    if running:
        running = False
        current_command = Command.STOPPING
    else:
        running = True
        current_command = Command.STARTED


def irq_add(pin):
    global t, last_push, current_command 
    if time.time() < debounce + last_push_min:
        print('stopped debounce')
        return
    print('button pushed')
    last_push_min = time.time()
    current_command = Command.ADD_MINUTE
    t.time_remaining.add_minute()


def irq_callback(pin):
    global t, last_push
    if time.time() < debounce + last_push:
        print('stopped debounce')
        return
    print('button pushed')
    last_push = time.time()
    if t.running != True:
        t.time_remaining = 0
        t.add_minute()
        t.add_minute()
        t.add_minute()
        t.add_minute()
        t.start()
    else:
        t.stop()
    

class Timer():
    def __init__(self,np_pin=16,np_count=8):
        self.np_pin = Pin(np_pin,Pin.OUT)
        self.time_remaining = 0
        self.np = NeoPixel(self.np_pin,np_count)
        self.running = False
        
    def add_minute(self):
        self.time_remaining += 60
        print(f'Adding minute, current time remaining = {self.time_remaining}')
        
    def start(self):
        print('start')
        self.running = True
        #self.tick()
        
    def stop(self):
        self.running = False
        self.time_remaining = 0
        for i in range(len(self.np)):
            self.np[i] = (MIN_BRIGHTNESS,0,0)
        self.np.write()
        time.sleep(0.1)
        for i in range(len(self.np)):
            self.np[i] = (MAX_BRIGHTNESS,MAX_BRIGHTNESS,MAX_BRIGHTNESS)
        self.np.write()
        time.sleep(0.5)
        for i in range(len(self.np)):
            self.np[i] = (MIN_BRIGHTNESS,0,0)
        self.np.write()
        print('stop')
    
    def tick(self):
        while self.time_remaining > 0:
            print(f'Time remaining: {self.time_remaining}')
            self.draw_time()
            self.time_remaining -= 1
        self.stop()
            
    def draw_time(self):
        active_pixel = -1
        for i in range(len(self.np)):
            min_time = i*SEGMENT_INTERVAL
            max_time = (i+1)*SEGMENT_INTERVAL
              
            if self.time_remaining > max_time:
                self.np[i] = PRE_COLOR
            
            elif self.time_remaining < max_time and self.time_remaining > min_time:
                self.np[i] = CURRENT_COLOR
                active_pixel = i
            
            elif self.time_remaining < min_time:
                self.np[i] = POST_COLOR
            
        self.np.write()
        time.sleep(0.5)
        if active_pixel != -1:
            self.np[active_pixel] = (0,0,0)
            self.np.write()
        time.sleep(0.5)
        
#https://docs.micropython.org/en/latest/esp8266/quickref.html#deep-sleep-mode
    
    
if __name__ == "__main__":
    button = Pin(14, Pin.IN, Pin.PULL_DOWN)
    t = Timer()
    button.irq(trigger=Pin.IRQ_FALLING,handler=irq_callback)
    t.stop()
    while True:
        if t.running:
            t.tick()
