/* File: states.c
 * Authors: Alexis Sy (mas264) and Isabelle Lynch (irl18)
 * Date: 11 Oct 2016
 * Descr: The states of which the players can choose from in the game.
 */

#include "system.h"
#include "tinygl.h"
#include "../fonts/font5x7_1.h"
#include "navswitch.h"
#include "states.h"

/** Defines the states that the player can choose from */
const char *states[] = { "PAPER", "SCISSORS", "ROCK" };

/** Scroll through the states.
	Goes through the states by PAPER -> SCISSOR -> ROCK via pushing 
	NAVSWITHCH_NORTH (wraps around ie. ROCK -> PAPER is next)
	Goes through the states by PAPER -> ROCK -> SCISSOR via pushing 
	NAVSWITHCH_SOUTH (wraps around ie. SCISSORs -> PAPER is next)
	@param current_state is the state that the player is currently on
	@return the new state after player has pushed north or south */
uint8_t scroll_state(uint8_t current_state)
{
    if (navswitch_push_event_p(NAVSWITCH_NORTH)) {
        if (current_state == ROCK) {
            current_state = PAPER;
            tinygl_text(states[current_state]);
        } else {
            current_state++;
            tinygl_text(states[current_state]);
        }
    }

    if (navswitch_push_event_p(NAVSWITCH_SOUTH)) {
        if (current_state == PAPER) {
            current_state = ROCK;
            tinygl_text(states[current_state]);
        } else {
            current_state--;
            tinygl_text(states[current_state]);
        }
    }

    return current_state;
}
