/*
 * File: game.c
 * Author: Simon
 * Date: 14/10/14
 * Brief: The main module
 */

#include "select.h"
#include "win_lose.h"
#include "symbols.h"

#include "system.h"
#include "tinygl.h"
#include "pacer.h"
#include "../fonts/font5x7_1.h"
#include "navswitch.h"
#include "ir_uart.h"


#define LOOP_RATE 1000

#define MESSAGE_RATE 30 /* Text scroll speed */


int main(void)
{
    char sent = 0;          /* non-zero when ir symbol has been sent */
    char received = 0;      /* non-zero when ir symbol is received */
    char ready = 0;         /* non-zero when the player has chosen a symbol */
    char text_set = 0;      /* non-zero when win/lose/draw text has been set */

    symbol_t symbol;                /* Used for the received symbol */
    symbol_t my_symbol = PAPER;     /* This player's symbol */
    symbol_t their_symbol;          /* The other player's symbol */

    /* Initialize everything */
    system_init();
    tinygl_init(LOOP_RATE);

    tinygl_font_set(&font5x7_1);
    tinygl_text_speed_set(MESSAGE_RATE);
    tinygl_text_mode_set(TINYGL_TEXT_MODE_SCROLL);

    navswitch_init();

    ir_uart_init();

    pacer_init(LOOP_RATE);

    /* Main game loop */
    while (1)
    {
        navswitch_update();

        /* The player hasn't chosen a symbol yet */
        if (!ready) {
            /* Allow them to select a symbol */
            my_symbol = get_symbol(my_symbol);

            display_symbol(my_symbol);
            
            /* Chooses the selected symbol */
            if (navswitch_push_event_p (NAVSWITCH_PUSH)) {
                tinygl_clear();
                ready = 1;
            }
        } 
        /* The player has chosen a symbol */
        else {
            ir_uart_putc(my_symbol); /* Transmit the symbol */
            sent = 1;
        }

        /* The other player's symbol hasn't been received yet */
        if (!received) {
            if (ir_uart_read_ready_p()) {
                symbol = ir_uart_getc();
                /* Check that the received symbol is valid */
                if (symbol == PAPER || symbol == SCISSORS || symbol == ROCK) {
                    their_symbol = symbol;
                    received = 1;
                }
            }
        }

        /* Waiting for the other player to send their symbol */
        if (sent && !received) {
            tinygl_draw_line(tinygl_point(0,0), tinygl_point(4,6), 1);
        }

        /* Ready to calculate win/lose/draw */
        if (sent && received) {
            if (win_lose(my_symbol, their_symbol) == WIN) {
                if (!text_set) {
                    tinygl_text("WINNER");
                    text_set = 1;
                }
            } else if (win_lose(my_symbol, their_symbol) == LOSE) {
                if (!text_set) {
                    tinygl_text("LOSER");
                    text_set = 1;
                }
            } else if (win_lose(my_symbol, their_symbol) == DRAW) {
                if (!text_set) {
                    tinygl_text("DRAW");
                    text_set = 1;
                }
            }

            /* Start a new game */
            if (navswitch_push_event_p(NAVSWITCH_PUSH)) {
                sent = 0;
                received = 0;
                ready = 0;
                text_set = 0;
                my_symbol = PAPER;
            }
        }
        
        tinygl_update();
    }

    return 0;
}