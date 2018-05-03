/*
 * File: win_lose.h
 * Author: Simon
 * Date: 15/10/14
 * Brief: Determines whether the player won, lost or drew the game and provides
 * an enumerated type for the result of the game
 */

#ifndef WIN_LOSE_H
#define WIN_LOSE_H

#include "symbols.h"

/* Types used for the result of the game */
typedef enum {
	WIN,
	LOSE,
	DRAW
} result_t;

result_t win_lose(symbol_t my_symbol, symbol_t their_symbol);

#endif /* WIN_LOSE_H */