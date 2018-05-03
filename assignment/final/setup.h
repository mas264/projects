/* File: setup.h
 * Authors: Alexis Sy (mas264) and Isabelle Lynch (irl18)
 * Date: 11 Oct 2016
 * Descr:  
 */

#ifndef SETUP_H
#define SETUP_H

#include "system.h"
#include "pacer.h"
#include "navswitch.h"
#include "ir_uart.h"
#include "tinygl.h"
#include "../fonts/font5x7_1.h"
#include <avr/io.h>

#define PACER_RATE 500
#define MESSAGE_RATE 20

int button_pressed_p(void);

void initialise(void);

void update(void);

#endif
