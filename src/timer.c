
#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/gpio.h"

#define MAX_BRIGHTNESS 255
#define MIN_BRIGHTNESS 1
#define SEGMENT_INTERVAL 30
#define STOP_DISPLAY_TIME 2
#define NP_PIN 16
#define NP_COUNT 8
#define BUTTON_1_PIN 13
#define BUTTON_2_PIN 14
#define BUTTON_3_PIN 15


// const tuple <int, int, int> PRE_COLOR = (0,MAX_BRIGHTNESS,0)
// const tuple <int, int, int> POST_COLOR = (0,0,MAX_BRIGHTNESS)
// const tuple <int, int, int> CURRENT_COLOR = (MAX_BRIGHTNESS,0,0)

void start_callback(uint gpio, uint32_t events)
{
    printf("GPIO %d\n", gpio);
}

void stop_callback(uint gpio, uint32_t events)
{}

void add_callback(uint gpio, uint32_t events)
{}

int main() {
    stdio_init_all();

    gpio_set_irq_enabled_with_callback(BUTTON_1_PIN, GPIO_IRQ_EDGE_FALL, true, &start_callback);

    while (true) {
        printf("hi\n");
        sleep_ms(1000);
    }
}
