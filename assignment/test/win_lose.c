/*
 * File: win_lose.h
 * Author: Simon
 * Date: 15/10/14
 * Brief: Determines whether the player won, lost or drew the game
 */

#include "win_lose.h"
#include "symbols.h"

#include "pacer.h"
#include "tinygl.h"

/* Returns the result of the game, WIN, DRAW, OR LOSE */
result_t win_lose(symbol_t my_symbol, symbol_t their_symbol)
{
    if (my_symbol == their_symbol) {
        return DRAW;
    } else if ((my_symbol == PAPER && their_symbol == ROCK)
            || (my_symbol == ROCK && their_symbol == SCISSORS)
            || (my_symbol == SCISSORS && their_symbol == PAPER)) {
        return WIN;
    } else {
        return LOSE;
    }
}