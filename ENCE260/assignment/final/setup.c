/* File: setup.c
 * Authors: Alexis Sy (mas264) and Isabelle Lynch (irl18)
 * Date: 11 Oct 2016
 * Descr:  
 */

#include "system.h"
#include "pacer.h"
#include "navswitch.h"
#include "ir_uart.h"
#include "tinygl.h"
#include "../fonts/font5x7_1.h"
#include <avr/io.h>
#include "setup.h"

int button_pressed_p(void)
{
    /* Return non-zero if button pressed_p.  */

    if ((PIND & BIT(7))) {
        return 1;
    } else {
        return 0;
    }

}

void initialise(void)
{
    system_init();
    DDRC |= (1 << 2);
    DDRD &= ~(1 << 7);

    tinygl_init(PACER_RATE);
    tinygl_font_set(&font5x7_1);
    tinygl_text_speed_set(MESSAGE_RATE);

    tinygl_text_mode_set(TINYGL_TEXT_MODE_SCROLL);


    pacer_init(PACER_RATE);

    ir_uart_init();
    tinygl_text("PRESS NAV BUTTON TO START");
}

void update(void)
{
    pacer_wait();
    tinygl_update();
    navswitch_update();
}
