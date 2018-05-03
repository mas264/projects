/* File: communication.h
 * Authors: Alexis Sy (mas264) and Isabelle Lynch (irl18)
 * Date: 11 Oct 2016
 * Descr:  
 */

#ifndef COMMUNICATION_H
#define COMMUNICATION_H

#include "system.h"
#include "ir_uart.h"
#include <avr/io.h>
#include "states.h"

#define CONVERT_TO_ASCII 48

uint8_t get_opponent(void);

void send_state(uint8_t selected);

#endif
