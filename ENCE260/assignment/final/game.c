/* File: game.c
 * Authors: Alexis Sy (mas264) and Isabelle Lynch (irl18)
 * Date: 11 Oct 2016
 * Descr: Main module for paper-scissors-rock game  
 */

#include "navswitch.h"
#include "ir_uart.h"
#include "tinygl.h"
#include "../fonts/font5x7_1.h"
#include <avr/io.h>
#include "states.h"
#include "result.h"
#include "setup.h"
#include "communication.h"


int main(void)
{
    initialise();
    uint8_t current_state = PAPER;
    uint8_t selected = DEFAULT_STATE;
    uint8_t start_push = 0;
    uint8_t opp_selected = DEFAULT_STATE;
    uint8_t won = 0;
    uint8_t played = 0;
    uint8_t set = 0;

    while (1) {
        update();

        if ((ir_uart_read_ready_p())) {
            opp_selected = get_opponent();
        }

        if (!set && selected != DEFAULT_STATE && opp_selected != DEFAULT_STATE) {
            won += get_result(selected, opp_selected);
            played++;
            set = 1;
        }

        if (navswitch_push_event_p(NAVSWITCH_PUSH) && start_push == 0) {
            tinygl_text(states[current_state]);
            start_push = 1;
            continue;
        }

        if (selected == DEFAULT_STATE) {
            current_state = scroll_state(current_state);
        }

        if (navswitch_push_event_p(NAVSWITCH_PUSH) && start_push == 1) {
            selected = current_state;
            send_state(selected);
        }

        if (button_pressed_p() && start_push == 1) {
            current_state = PAPER;
            selected = DEFAULT_STATE;
            opp_selected = DEFAULT_STATE;
            tinygl_text(states[current_state]);
            PORTC &= ~(1 << 2);
            set = 0;
        }

        if (played == 10) {
            tinygl_text("PRESS PUSH BUTTON FOR NEW ROUND");
            played = 0;
            won = 0;
        }

        display_stat(played, won);
    }
}
