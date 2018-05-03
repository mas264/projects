/*
 * File: select.c
 * Author: Victor
 * Date: 14/10/14
 * Brief: Allows the player to choose a symbol
 */

#include "select.h"
#include "symbols.h"

#include "system.h"
#include "tinygl.h"
#include "pacer.h"
#include "../fonts/font5x7_1.h"
#include "navswitch.h"

/* Displays a single character (symbol) on the screen */
void display_symbol(symbol_t symbol)
{
    char buffer[2];
    buffer[0] = symbol;
    buffer[1] = '\0';
    tinygl_text(buffer);
}

/* Changes the current symbol and returns it if the navswitch was pressed
 * north or south */
symbol_t get_symbol(symbol_t current_symbol)
{
	symbol_t my_symbol = current_symbol;

	if (navswitch_push_event_p (NAVSWITCH_NORTH)) {
        if (my_symbol == PAPER) {
            my_symbol = ROCK;
        } 
        else if (my_symbol == ROCK) {
            my_symbol = SCISSORS;
        }
        else {
            my_symbol = PAPER;
        }
    }
    
    /* Scrolls through the symbols to play,
     * P->S, R->P, S->R when navswitch_south is pressed */
    if (navswitch_push_event_p (NAVSWITCH_SOUTH)) {
        if (my_symbol == PAPER) {
            my_symbol = SCISSORS;
        } 
        else if (my_symbol == ROCK) {
            my_symbol = PAPER;
        }
        else {
            my_symbol = ROCK;
        }
    }

    return my_symbol;
}