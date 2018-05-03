#include "pio.h"
#include "button.h"

#define BUTTON_PIO PIO_DEFINE(PORT_D, 7)
/** Return non-zero if button pressed.  */
int button_pressed_p (void)
{
    if(pio_input_get(BUTTON_PIO)) {
		return 1;
	} else {
		return 0;
	}
}


/** Initialise button1.  */
void button_init (void)
{
    pio_config_set(BUTTON_PIO, PIO_INPUT);
}

