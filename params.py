MAX_BRIGHTNESS = 10
MIN_BRIGHTNESS = 1

SEGMENT_INTERVAL = 30
PRE_COLOR = (0,MAX_BRIGHTNESS,0)
POST_COLOR = (0,0,MAX_BRIGHTNESS)
CURRENT_COLOR = (MAX_BRIGHTNESS,0,0)

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