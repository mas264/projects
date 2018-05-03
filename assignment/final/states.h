/* File: states.c
 * Authors: Alexis Sy (mas264) and Isabelle Lynch (irl18)
 * Date: 11 Oct 2016
 * Descr: The states of which the players can choose from in the game
 */

#ifndef STATES_H
#define STATES_H

#include "system.h"
#include "tinygl.h"
#include "../fonts/font5x7_1.h"
#include "navswitch.h"

/** Integer equivalent of the states */
#define PAPER 0
#define SCISSORS 1
#define ROCK 2
#define DEFAULT_STATE 3

/** Defines the states that the player can choose from */
extern const char *states[];

/** Scroll through the states.
	Goes through the states by PAPER -> SCISSOR -> ROCK via pushing 
	NAVSWITHCH_NORTH (wraps around ie. ROCK -> PAPER is next)
	Goes through the states by PAPER -> ROCK -> SCISSOR via pushing 
	NAVSWITHCH_SOUTH (wraps around ie. SCISSORs -> PAPER is next)
	@param current_state is the state that the player is currently on
	@return the new state after player has pushed north or south */
uint8_t scroll_state(uint8_t current_state);

#endif
