#include "system.h"
#include "button.h"
#include "pacer.h"
#include "tinygl.h"
#include "../fonts/font3x5_1.h"

/* Define polling rates in Hz.  */
#define BUTTON_TASK_RATE 100

#define DISPLAY_TASK_RATE 250

#define TIMER_TASK_RATE 100

#define TASK_RATE (F_CPU / 256)


static bool run;


static void button_task_init (void)
{
    button_init ();
}


static void button_task (__unused__ void *data)
{
    button_update ();

    if (button_push_event_p (BUTTON1))
    {
        run = !run;
    }
}


static void display_task_init (void)
{
    tinygl_init (DISPLAY_TASK_RATE);
    tinygl_font_set (&font3x5_1);
    tinygl_text_mode_set (TINYGL_TEXT_MODE_STEP);
    tinygl_text_dir_set (TINYGL_TEXT_DIR_ROTATE);
}


static void display_task (__unused__ void *data)
{
    tinygl_update ();
}


static void timer_task_init (void)
{
    tinygl_text ("00");
}


static void timer_task (__unused__ void *data)
{
    static uint16_t time;
    char str[3];

    if (!run)
    {
        time = 0;
        return;
    }

    str[0] = ((time / 10) % 10) + '0';
    str[1] = (time % 10) + '0';
    str[2] = 0;

    tinygl_text (str);

    time++;
}



int main (void)
{
    system_init();
    
    /* TODO: Initialise the button driver, tinygl, and the pacer.  */

    
    system_init ();

    display_task_init ();
    button_task_init ();
    timer_task_init ();
    
    while(1)
    {
        pacer_wait();

	/* TODO: Implement the functionality of the tasks in the
           stopwatch1 program.  */
      

      display_task(TASK_RATE / DISPLAY_TASK_RATE);
      button_task(TASK_RATE / BUTTON_TASK_RATE);
      timer_task(TASK_RATE / TIMER_TASK_RATE);

     
    }
    
    return 0;
}
