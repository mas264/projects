/*
 * File: select.h
 * Author: Victor
 * Date: 14/10/14
 * Brief: Allows the player to choose a symbol
 */

#ifndef SELECT_H
#define SELECT_H

#include "symbols.h"

symbol_t get_symbol(symbol_t current_symbol);
void display_symbol(symbol_t symbol);

#endif /* SELECT_H */