/* ###################################################################
**     THIS COMPONENT MODULE IS GENERATED BY THE TOOL. DO NOT MODIFY IT.
**     Filename    : Stepperspi.c
**     Project     : Shell
**     Processor   : MKL25Z128VLK4
**     Component   : SynchroMaster
**     Version     : Component 02.347, Driver 01.01, CPU db: 3.00.000
**     Compiler    : GNU C Compiler
**     Date/Time   : 2015-05-06, 10:46, # CodeGen: 2
**     Abstract    :
**         This component "SynchroMaster" implements MASTER part of synchronous
**         serial master-slave communication.
**     Settings    :
**         Synchro type                : MASTER
**
**         Serial channel              : SPI1
**
**         Protocol
**             Clock edge              : rising
**             Width                   : 8 bits
**             Empty character         : 0
**             Empty char. on input    : RECEIVED
**
**         Registers
**             Input buffer            : SPI1_D    [0x40077005]
**             Output buffer           : SPI1_D    [0x40077005]
**             Control register        : SPI1_C1   [0x40077000]
**             Mode register           : SPI1_C2   [0x40077001]
**             Baud setting reg.       : SPI1_BR   [0x40077002]
**
**         Input interrupt
**             Vector name             : INT_SPI1
**             Priority                : 2
**
**         Output interrupt
**             Vector name             : INT_SPI1
**             Priority                : 2
**
**         Used pins                   :
**         ----------------------------------------------------------
**              Function    | On package |    Name
**         ----------------------------------------------------------
**               Input      |     2      |  PTE1/SPI1_MOSI/UART1_RX/SPI1_MISO/I2C1_SCL
**               Output     |     4      |  PTE3/SPI1_MISO/SPI1_MOSI
**               Clock      |     3      |  PTE2/SPI1_SCK
**           Select slave   |     5      |  PTE4/SPI1_PCS0
**         ----------------------------------------------------------
**
**     Contents    :
**         RecvChar        - byte Stepperspi_RecvChar(Stepperspi_TComData *Chr);
**         SendChar        - byte Stepperspi_SendChar(Stepperspi_TComData Chr);
**         GetCharsInRxBuf - word Stepperspi_GetCharsInRxBuf(void);
**
**     Copyright : 1997 - 2014 Freescale Semiconductor, Inc. 
**     All Rights Reserved.
**     
**     Redistribution and use in source and binary forms, with or without modification,
**     are permitted provided that the following conditions are met:
**     
**     o Redistributions of source code must retain the above copyright notice, this list
**       of conditions and the following disclaimer.
**     
**     o Redistributions in binary form must reproduce the above copyright notice, this
**       list of conditions and the following disclaimer in the documentation and/or
**       other materials provided with the distribution.
**     
**     o Neither the name of Freescale Semiconductor, Inc. nor the names of its
**       contributors may be used to endorse or promote products derived from this
**       software without specific prior written permission.
**     
**     THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
**     ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
**     WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
**     DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
**     ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
**     (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
**     LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
**     ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
**     (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
**     SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
**     
**     http: www.freescale.com
**     mail: support@freescale.com
** ###################################################################*/
/*!
** @file Stepperspi.c
** @version 01.01
** @brief
**         This component "SynchroMaster" implements MASTER part of synchronous
**         serial master-slave communication.
*/         
/*!
**  @addtogroup Stepperspi_module Stepperspi module documentation
**  @{
*/         

/* MODULE Stepperspi. */

#include "Events.h"
#include "Stepperspi.h"

#ifdef __cplusplus
extern "C" {
#endif 

#define OVERRUN_ERR      0x01U         /* Overrun error flag bit   */
#define TX_BUF_EMPTY     0x02U         /* Tx buffer state flag bit   */
#define CHAR_IN_RX       0x08U         /* Char is in RX buffer     */
#define FULL_TX          0x10U         /* Full transmit buffer     */
#define RUNINT_FROM_TX   0x20U         /* Interrupt is in progress */
#define FULL_RX          0x40U         /* Full receive buffer      */

LDD_TDeviceData *SMasterLdd1_DeviceDataPtr; /* Device data pointer */
static byte SerFlag;                   /* Flags for serial communication */
                                       /* Bits: 0 - OverRun error */
                                       /*       1 - Tx buffer state after init */
                                       /*       2 - Unused */
                                       /*       3 - Char in RX buffer */
                                       /*       4 - Full TX buffer */
                                       /*       5 - Running int from TX */
                                       /*       6 - Full RX buffer */
                                       /*       7 - Unused */
static Stepperspi_TComData BufferRead; /* Input char SPI communication */
static Stepperspi_TComData OutBuffer;  /* Output buffer for SPI communication */

/*
** ===================================================================
**     Method      :  Stepperspi_RecvChar (component SynchroMaster)
**     Description :
**         If any data is received, this method returns one character,
**         otherwise it returns an error code (it does not wait for
**         data). 
**         For information about SW overrun behavior please see
**         <General info page>.
**     Parameters  :
**         NAME            - DESCRIPTION
**       * Chr             - A pointer to the received character
**     Returns     :
**         ---             - Error code, possible codes:
**                           ERR_OK - OK - The valid data is received.
**                           ERR_SPEED - This device does not work in
**                           the active speed mode.
**                           ERR_RXEMPTY - No data in receiver.
**                           ERR_OVERRUN - Overrun error was detected
**                           from the last char or block received. In
**                           polling mode, this error code is returned
**                           only when the hardware supports detection
**                           of the overrun error. If interrupt service
**                           is enabled, and input buffer allocated by
**                           the component is full, the component
**                           behaviour depends on <Input buffer size>
**                           property : if property is 0, last received
**                           data-word is preserved (and previous is
**                           overwritten), if property is greater than 0,
**                           new received data-word are ignored.
**                           ERR_FAULT - Fault error was detected from
**                           the last char or block received. In the
**                           polling mode the ERR_FAULT is return until
**                           the user clear the fault flag bit, but in
**                           the interrupt mode ERR_FAULT is returned
**                           only once after the fault error occured.
**                           This error is supported only on the CPUs
**                           supports the faul mode function - where
**                           <Fault mode> property is available.
** ===================================================================
*/
byte Stepperspi_RecvChar(Stepperspi_TComData *Chr)
{
  register byte FlagTmp;

  if ((SerFlag & CHAR_IN_RX) == 0U) {  /* Is any char in RX buffer? */
    return ERR_RXEMPTY;                /* If no then error */
  }
  EnterCritical();                     /* Disable global interrupts */
  *Chr = BufferRead;                   /* Read the char */
  FlagTmp = SerFlag;                   /* Safe the flags */
  SerFlag &= (byte)~(OVERRUN_ERR | CHAR_IN_RX | FULL_RX); /* Clear flag "char in RX buffer" */
  ExitCritical();                      /* Enable global interrupts */
  if ((FlagTmp & OVERRUN_ERR) != 0U) { /* Is the overrun occurred? */
    return ERR_OVERRUN;                /* If yes then return error */
  } else {
    return ERR_OK;
  }
}

/*
** ===================================================================
**     Method      :  Stepperspi_SendChar (component SynchroMaster)
**     Description :
**         Sends one character to the channel.
**     Parameters  :
**         NAME            - DESCRIPTION
**         Chr             - Character to send
**     Returns     :
**         ---             - Error code, possible codes:
**                           ERR_OK - OK
**                           ERR_SPEED - This device does not work in
**                           the active speed mode
**                           ERR_DISABLED - Device is disabled (only if
**                           output DMA is supported and enabled)
**                           ERR_TXFULL - Transmitter is full
** ===================================================================
*/
byte Stepperspi_SendChar(Stepperspi_TComData Chr)
{
  if ((SerFlag & FULL_TX) != 0U) {     /* Is any char in the TX buffer? */
    return ERR_TXFULL;                 /* If yes then error */
  }
  EnterCritical();                     /* Disable global interrupts */
  SerFlag |= FULL_TX;                  /* Set the flag "full TX buffer" */
  OutBuffer = Chr;
  (void)SMasterLdd1_SendBlock(SMasterLdd1_DeviceDataPtr, (LDD_TData *)&OutBuffer, 1U); /* Send one data byte */
  ExitCritical();                      /* Enable global interrupts */
  return ERR_OK;
}

/*
** ===================================================================
**     Method      :  Stepperspi_GetCharsInRxBuf (component SynchroMaster)
**     Description :
**         Returns the number of characters in the input buffer.
**         Note: If the Interrupt service is disabled, and the Ignore
**         empty character is set to yes, and a character has been
**         received, then this method returns 1 although it was an
**         empty character.
**     Parameters  : None
**     Returns     :
**         ---             - Number of characters in the input buffer.
** ===================================================================
*/
word Stepperspi_GetCharsInRxBuf(void)
{
  return ((word)(((SerFlag & CHAR_IN_RX) != 0U)? 1U:0U)); /* Return number of chars in receive buffer */
}

/*
** ===================================================================
**     Method      :  Stepperspi_Init (component SynchroMaster)
**
**     Description :
**         Initializes the associated peripheral(s) and the component 
**         internal variables. The method is called automatically as a 
**         part of the application initialization code.
**         This method is internal. It is used by Processor Expert only.
** ===================================================================
*/
void Stepperspi_Init(void)
{
  SerFlag = 0U;                        /* Reset all flags */
  SMasterLdd1_DeviceDataPtr = SMasterLdd1_Init(NULL); /* Calling init method of the inherited component */
  (void)SMasterLdd1_ReceiveBlock(SMasterLdd1_DeviceDataPtr, &BufferRead, 1U); /* Receive one data byte */
}

#define ON_ERROR        0x01U
#define ON_FULL_RX      0x02U
#define ON_RX_CHAR      0x04U
#define ON_RX_CHAR_EXT  0x08U
/*
** ===================================================================
**     Method      :  Stepperspi_SMasterLdd1_OnBlockReceived (component SynchroMaster)
**
**     Description :
**         This event is called when the requested number of data is 
**         moved to the input buffer. This method is available only if 
**         the ReceiveBlock method is enabled. The event services the 
**         event of the inherited component and eventually invokes other 
**         events.
**         This method is internal. It is used by Processor Expert only.
** ===================================================================
*/
void SMasterLdd1_OnBlockReceived(LDD_TUserData *UserDataPtr)
{

  (void)UserDataPtr;                   /* Parameter is not used, suppress unused argument warning */
  if ((SerFlag & CHAR_IN_RX) != 0U) {  /* Is the overrun error flag set? */
    SerFlag |= OVERRUN_ERR;            /* If yes then set the Error flag for RecvChar/Block method */
  }
  SerFlag |= CHAR_IN_RX;               /* Set flag "char in RX buffer" */
  Stepperspi_OnRxChar();               /* Invoke user event */
  (void)SMasterLdd1_ReceiveBlock(SMasterLdd1_DeviceDataPtr, &BufferRead, 1U); /* Receive one data byte */
}

#define ON_FREE_TX  0x01U
#define ON_TX_CHAR  0x02U
/*
** ===================================================================
**     Method      :  Stepperspi_SMasterLdd1_OnBlockSent (component SynchroMaster)
**
**     Description :
**         This event is called after the last character from the output 
**         buffer is moved to the transmitter. This event is available 
**         only if the SendBlock method is enabled. The event services 
**         the event of the inherited component and eventually invokes 
**         other events.
**         This method is internal. It is used by Processor Expert only.
** ===================================================================
*/
void SMasterLdd1_OnBlockSent(LDD_TUserData *UserDataPtr)
{
  (void)UserDataPtr;                   /* Parameter is not used, suppress unused argument warning */
  SerFlag &= (byte)~(FULL_TX);         /* Reset flag "full TX buffer" */
  Stepperspi_OnTxChar();               /* Invoke user event */
}

/* END Stepperspi. */

#ifdef __cplusplus
}  /* extern "C" */
#endif 

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
