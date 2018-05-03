/* File: communication.c
 * Authors: Alexis Sy (mas264) and Isabelle Lynch (irl18)
 * Date: 11 Oct 2016
 * Descr:  
 */

#include "system.h"
#include "ir_uart.h"
#include <avr/io.h>
#include "communication.h"
#include "states.h"

uint8_t get_opponent(void)
{
    uint8_t opponent = DEFAULT_STATE;

    opponent = ir_uart_getc();
    opponent -= CONVERT_TO_ASCII;

    return opponent;
}

void send_state(uint8_t selected)
{
    PORTC = (1 << 2);
    ir_uart_putc(selected + CONVERT_TO_ASCII);
}
