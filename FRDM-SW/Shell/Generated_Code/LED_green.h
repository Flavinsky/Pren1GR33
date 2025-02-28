/* ###################################################################
**     THIS COMPONENT MODULE IS GENERATED BY THE TOOL. DO NOT MODIFY IT.
**     Filename    : LED_green.h
**     Project     : Shell
**     Processor   : MKL25Z128VLK4
**     Component   : LED
**     Version     : Component 01.063, Driver 01.00, CPU db: 3.00.000
**     Compiler    : GNU C Compiler
**     Date/Time   : 2015-05-06, 10:39, # CodeGen: 1
**     Abstract    :
**          This component implements a universal driver for a single LED.
**     Settings    :
**          Component name                                 : LED_green
**          Turned On with initialization                  : no
**          HW Interface                                   : 
**            On/Off                                       : Enabled
**              Pin                                        : LEDpin
**            PWM                                          : Disabled
**            High Value means ON                          : no
**          Shell                                          : Enabled
**            Shell                                        : CLS1
**            Utility                                      : UTIL1
**     Contents    :
**         Init         - void LED_green_Init(void);
**         Deinit       - void LED_green_Deinit(void);
**         On           - void LED_green_On(void);
**         Off          - void LED_green_Off(void);
**         Neg          - void LED_green_Neg(void);
**         Get          - byte LED_green_Get(void);
**         Put          - void LED_green_Put(byte val);
**         SetRatio16   - void LED_green_SetRatio16(word ratio);
**         ParseCommand - byte LED_green_ParseCommand(const unsigned char *cmd, bool *handled, const...
**
**     License   : Open Source (LGPL)
**     Copyright : Erich Styger, 2013, all rights reserved.
**     Web       : www.mcuoneclipse.com
**     This an open source software implementing a driver using Processor Expert.
**     This is a free software and is opened for education, research and commercial developments under license policy of following terms:
**     * This is a free software and there is NO WARRANTY.
**     * No restriction on use. You can use, modify and redistribute it for personal, non-profit or commercial product UNDER YOUR RESPONSIBILITY.
**     * Redistributions of source code must retain the above copyright notice.
** ###################################################################*/
/*!
** @file LED_green.h
** @version 01.00
** @brief
**          This component implements a universal driver for a single LED.
*/         
/*!
**  @addtogroup LED_green_module LED_green module documentation
**  @{
*/         

#ifndef __LED_green_H
#define __LED_green_H

/* MODULE LED_green. */

/* Include shared modules, which are used for whole project */
#include "PE_Types.h"
#include "PE_Error.h"
#include "PE_Const.h"
#include "IO_Map.h"
/* Include inherited beans */
#include "LEDpin1.h"
#include "CLS1.h"
#include "UTIL1.h"

#include "Cpu.h"

#define LED_green_ClrVal()    LEDpin1_ClrVal() /* put the pin on low level */
#define LED_green_SetVal()    LEDpin1_SetVal() /* put the pin on high level */
#define LED_green_SetInput()  LEDpin1_SetInput() /* use the pin as input pin */
#define LED_green_SetOutput() LEDpin1_SetOutput() /* use the pin as output pin */

#define LED_green_PARSE_COMMAND_ENABLED  1 /* set to 1 if method ParseCommand() is present, 0 otherwise */


#define LED_green_On() LEDpin1_ClrVal()
/*
** ===================================================================
**     Method      :  LED_green_On (component LED)
**     Description :
**         This turns the LED on.
**     Parameters  : None
**     Returns     : Nothing
** ===================================================================
*/

#define LED_green_Off() LEDpin1_SetVal()
/*
** ===================================================================
**     Method      :  LED_green_Off (component LED)
**     Description :
**         This turns the LED off.
**     Parameters  : None
**     Returns     : Nothing
** ===================================================================
*/

#define LED_green_Neg() LEDpin1_NegVal()
/*
** ===================================================================
**     Method      :  LED_green_Neg (component LED)
**     Description :
**         This negates/toggles the LED
**     Parameters  : None
**     Returns     : Nothing
** ===================================================================
*/

#define LED_green_Get() (!(LEDpin1_GetVal()))
/*
** ===================================================================
**     Method      :  LED_green_Get (component LED)
**     Description :
**         This returns logical 1 in case the LED is on, 0 otherwise.
**     Parameters  : None
**     Returns     :
**         ---             - Status of the LED (on or off)
** ===================================================================
*/

#define LED_green_Init() LED_green_Off()
/*
** ===================================================================
**     Method      :  LED_green_Init (component LED)
**     Description :
**         Performs the LED driver initialization.
**     Parameters  : None
**     Returns     : Nothing
** ===================================================================
*/

#define LED_green_Put(val)  ((val) ? LED_green_On() : LED_green_Off())
/*
** ===================================================================
**     Method      :  LED_green_Put (component LED)
**     Description :
**         Turns the LED on or off.
**     Parameters  :
**         NAME            - DESCRIPTION
**         val             - value to define if the LED has to be on or
**                           off.
**     Returns     : Nothing
** ===================================================================
*/

void LED_green_Deinit(void);
/*
** ===================================================================
**     Method      :  LED_green_Deinit (component LED)
**     Description :
**         Deinitializes the driver
**     Parameters  : None
**     Returns     : Nothing
** ===================================================================
*/

byte LED_green_ParseCommand(const unsigned char *cmd, bool *handled, const CLS1_StdIOType *io);
/*
** ===================================================================
**     Method      :  LED_green_ParseCommand (component LED)
**     Description :
**         Shell Command Line parser. This method is enabled/disabled
**         depending on if you have the Shell enabled/disabled in the
**         properties.
**     Parameters  :
**         NAME            - DESCRIPTION
**       * cmd             - Pointer to command string
**       * handled         - Pointer to variable which tells if
**                           the command has been handled or not
**       * io              - Pointer to I/O structure
**     Returns     :
**         ---             - Error code
** ===================================================================
*/

void LED_green_SetRatio16(word ratio);
/*
** ===================================================================
**     Method      :  LED_green_SetRatio16 (component LED)
**     Description :
**         Method to specify the duty cycle. If using a PWM pin, this
**         means the duty cycle is set. For On/off pins, values smaller
**         0x7FFF means off, while values greater means on.
**     Parameters  :
**         NAME            - DESCRIPTION
**         ratio           - Ratio value, where 0 means 'off' and
**                           0xffff means 'on'
**     Returns     : Nothing
** ===================================================================
*/

/* END LED_green. */

#endif
/* ifndef __LED_green_H */
/*!
** @}
*/
/*
** ###################################################################
**
**     This file was created by Processor Expert 10.4 [05.11]
**     for the Freescale Kinetis series of microcontrollers.
**
** ###################################################################
*/
