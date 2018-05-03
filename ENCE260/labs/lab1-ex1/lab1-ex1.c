#include <avr/io.h>
#include "system.h"

int main (void)
{
    system_init ();

    /* Initialise port to drive LED 1.  */
    DDRC |= (1 << 2);
    /* TODO.  */
    DDRD &= ~(1 << 7);
    uint8_t isOn = 0;

    while (1)
    {
		if ((PIND & BIT(7)) && !isOn) {
			while(PIND & BIT(7)) { continue; }
        /* Turn LED 1 on.  */
			PORTC |= (1 << 2);
			isOn = 1;

		} else if ((PIND & BIT(7)) && isOn) {
			while(PIND & BIT(7)) { continue; }
			PORTC &= ~(1 << 2);	
			isOn = 0;
		}
        /* TODO.  */

    }
}
