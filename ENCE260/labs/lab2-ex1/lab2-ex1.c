#include <avr/io.h>
#include "system.h"
#include "led.h"


int main (void)
{
    system_init ();
    led_init ();
    
    /* TODO: Initialise timer/counter1.  */
    TCCR1A = 0x00;
    TCCR1B = 0x05;
    TCCR1C = 0x00;

    
    while (1)
    {
        TCNT1 = 0;
        /* Turn LED on.  */
        led_set (LED1, 1);
        
        /* TODO: wait for 500 milliseconds.  */
        while(TCNT1 < 3906/4) {
			continue;
		}

        /* Turn LED off.  */
		led_set (LED1, 0);
		TCNT1 = 0;

        /* TODO: wait for 500 milliseconds.  */
        while(TCNT1 < 3906/4) {
			continue;
		}
        
    }
    
}
