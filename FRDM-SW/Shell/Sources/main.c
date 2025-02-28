/* ###################################################################
**     Filename    : main.c
**     Project     : Shell
**     Processor   : MKL25Z128VLK4
**     Version     : Driver 01.01
**     Compiler    : GNU C Compiler
**     Date/Time   : 2015-03-06, 09:12, # CodeGen: 0
**     Abstract    :
**         Main module.
**         This module contains user's application code.
**     Settings    :
**     Contents    :
**         No public methods
**
** ###################################################################*/
/*!
** @file main.c
** @version 01.01
** @brief
**         Main module.
**         This module contains user's application code.
*/         
/*!
**  @addtogroup main_module main module documentation
**  @{
*/         
/* MODULE main */



/* Including needed modules to compile this module/procedure */
#include "Cpu.h"
#include "Events.h"
#include "FRTOS1.h"
#include "UTIL1.h"
#include "LED_green.h"
#include "LEDpin1.h"
#include "BitIoLdd1.h"
#include "LED_blue.h"
#include "LEDpin3.h"
#include "BitIoLdd3.h"
#include "LED_red.h"
#include "LEDpin2.h"
#include "BitIoLdd2.h"
#include "TU1.h"
#include "CLS1.h"
#include "WAIT1.h"
#include "CS1.h"
#include "AS1.h"
#include "ASerialLdd1.h"
#include "PWM1.h"
#include "PwmLdd2.h"
#include "Stepperspi.h"
#include "SMasterLdd1.h"
#include "DC_DIR.h"
#include "BitIoLdd4.h"
#include "DC_EN.h"
#include "BitIoLdd6.h"
#include "STP_REF.h"
#include "ExtIntLdd3.h"
#include "STP_BSY.h"
#include "ExtIntLdd1.h"
/* Including shared modules, which are used for whole project */
#include "PE_Types.h"
#include "PE_Error.h"
#include "PE_Const.h"
#include "IO_Map.h"
/* User includes (#include below this line is not maintained by Processor Expert) */

#include "Shell.h"
#include "Error.h"
#include "BLDC.h"
#include "../../../../stepper/driver/drv/l6480.h"



static void Task1(void *pvParameters)
{
	(void)pvParameters;
	while (1) {
		LED_green_Neg();
		FRTOS1_vTaskDelay(1000/portTICK_RATE_MS);
	}

}

static void Task2(void *pvParameters)
{
	(void)pvParameters;
	while (1) {
		LED_red_Neg();
		FRTOS1_vTaskDelay(500/portTICK_RATE_MS);
	}
}

/*lint -save  -e970 Disable MISRA rule (6.3) checking. */
int main(void)
/*lint -restore Enable MISRA rule (6.3) checking. */
{
  /* Write your local variable definition here */
	xTaskHandle A;
	xTaskHandle B;

  /*** Processor Expert internal initialization. DON'T REMOVE THIS CODE!!! ***/
  PE_low_level_init();
  /*** End of Processor Expert internal initialization.                    ***/

  /* Write your code here */
  /* For example: for(;;) { } */

  /*
  if (FRTOS1_xTaskCreate(
		  Task1,
		  (signed portCHAR *)"Task1",
		  configMINIMAL_STACK_SIZE,
		  (void*)NULL,
		  tskIDLE_PRIORITY,
		  (xTaskHandle*)NULL
  	  ) != pdPASS) {
	  while (1) {
		  // out of heap?
	  }
  }
  */

  set_status(STATUS_RESET);
  SHELL_Init();

  if (FRTOS1_xTaskCreate(
  		  BLDC_update_task,
  		  (signed portCHAR *)"BLDC",
  		  configMINIMAL_STACK_SIZE,
  		  (void*)NULL,
  		  tskIDLE_PRIORITY,
  		  (xTaskHandle*)NULL
    	  ) != pdPASS) {
  	  while (1) {
  		  // out of heap?
  	  }
  }

  /*** Don't write any code pass this line, or it will be deleted during code generation. ***/
  /*** RTOS startup code. Macro PEX_RTOS_START is defined by the RTOS component. DON'T MODIFY THIS CODE!!! ***/
  #ifdef PEX_RTOS_START
    PEX_RTOS_START();                  /* Startup of the selected RTOS. Macro is defined by the RTOS component. */
  #endif
  /*** End of RTOS startup code.  ***/
  /*** Processor Expert end of main routine. DON'T MODIFY THIS CODE!!! ***/
  for(;;){}
  /*** Processor Expert end of main routine. DON'T WRITE CODE BELOW!!! ***/
} /*** End of main routine. DO NOT MODIFY THIS TEXT!!! ***/

/* END main */
/*!
** @}
*/
/*
** ###################################################################
**
**     This file was created by Processor Expert 10.4 [05.10]
**     for the Freescale Kinetis series of microcontrollers.
**
** ###################################################################
*/
