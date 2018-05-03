/* File: result.c
 * Authors: Alexis Sy (mas264) and Isabelle Lynch (irl18)
 * Date: 11 Oct 2016
 * Descr: responsible for displaying the stats of the game and the 
		  result of each game.
 */

#include "system.h"
#include "tinygl.h"
#include "../fonts/font5x7_1.h"
#include "states.h"
#include "navswitch.h"
#include "result.h"

/** Get result and displays the result on the matrix by calculating
	what each player picked.
	@param player is what the player picked on their own funkit
	@param opponent is what their opponent picked on their own board
	@return returns a 0 or 1 depending if the player won the round */
uint8_t get_result(uint8_t player, uint8_t opponent)
{
    uint8_t won = 0;
    if (player == PAPER) {
        if (opponent == ROCK) {
            tinygl_text("W");
            won++;
        } else if (opponent == SCISSORS) {
            tinygl_text("L");
        } else if (opponent == PAPER) {
            tinygl_text("T");
        }
    }

    if (player == ROCK) {
        if (opponent == SCISSORS) {
            tinygl_text("W");
            won++;
        } else if (opponent == PAPER) {
            tinygl_text("L");
        } else if (opponent == ROCK) {
            tinygl_text("T");
        }
    }

    if (player == SCISSORS) {
        if (opponent == PAPER) {
            tinygl_text("W");
            won++;
        } else if (opponent == ROCK) {
            tinygl_text("L");
        } else if (opponent == SCISSORS) {
            tinygl_text("T");
        }

    }

    return won;
}

/** Responsible for displaying the number of times the player won and 
	the number of times the player and the opponent played each other.
	@param played is the number of times that they played together
	@param won is the number of times that the player has won against
	his/her opponent */
void display_stat(uint8_t played, uint8_t won)
{
    char buffer[2];

    if (navswitch_push_event_p(NAVSWITCH_EAST)) {
        buffer[0] = played + CONVERT_TO_ASCII;
        buffer[1] = '\0';
        tinygl_text(buffer);
    }


    if (navswitch_push_event_p(NAVSWITCH_WEST)) {
        buffer[0] = won + CONVERT_TO_ASCII;
        buffer[1] = '\0';
        tinygl_text(buffer);
    }
}
