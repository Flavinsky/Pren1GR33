################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Generated_Code/AS1.c \
../Generated_Code/ASerialLdd1.c \
../Generated_Code/BitIoLdd1.c \
../Generated_Code/BitIoLdd2.c \
../Generated_Code/BitIoLdd3.c \
../Generated_Code/BitIoLdd4.c \
../Generated_Code/BitIoLdd6.c \
../Generated_Code/CLS1.c \
../Generated_Code/CS1.c \
../Generated_Code/Cpu.c \
../Generated_Code/DC_DIR.c \
../Generated_Code/DC_EN.c \
../Generated_Code/ExtIntLdd3.c \
../Generated_Code/FRTOS1.c \
../Generated_Code/LED_blue.c \
../Generated_Code/LED_green.c \
../Generated_Code/LED_red.c \
../Generated_Code/LEDpin1.c \
../Generated_Code/LEDpin2.c \
../Generated_Code/LEDpin3.c \
../Generated_Code/PE_LDD.c \
../Generated_Code/PWM1.c \
../Generated_Code/PwmLdd2.c \
../Generated_Code/SMasterLdd1.c \
../Generated_Code/STP_REF.c \
../Generated_Code/Stepperspi.c \
../Generated_Code/TU1.c \
../Generated_Code/UTIL1.c \
../Generated_Code/Vectors.c \
../Generated_Code/WAIT1.c \
../Generated_Code/croutine.c \
../Generated_Code/event_groups.c \
../Generated_Code/heap_1.c \
../Generated_Code/heap_2.c \
../Generated_Code/heap_3.c \
../Generated_Code/heap_4.c \
../Generated_Code/heap_5.c \
../Generated_Code/list.c \
../Generated_Code/port.c \
../Generated_Code/queue.c \
../Generated_Code/tasks.c \
../Generated_Code/timers.c 

OBJS += \
./Generated_Code/AS1.o \
./Generated_Code/ASerialLdd1.o \
./Generated_Code/BitIoLdd1.o \
./Generated_Code/BitIoLdd2.o \
./Generated_Code/BitIoLdd3.o \
./Generated_Code/BitIoLdd4.o \
./Generated_Code/BitIoLdd6.o \
./Generated_Code/CLS1.o \
./Generated_Code/CS1.o \
./Generated_Code/Cpu.o \
./Generated_Code/DC_DIR.o \
./Generated_Code/DC_EN.o \
./Generated_Code/ExtIntLdd3.o \
./Generated_Code/FRTOS1.o \
./Generated_Code/LED_blue.o \
./Generated_Code/LED_green.o \
./Generated_Code/LED_red.o \
./Generated_Code/LEDpin1.o \
./Generated_Code/LEDpin2.o \
./Generated_Code/LEDpin3.o \
./Generated_Code/PE_LDD.o \
./Generated_Code/PWM1.o \
./Generated_Code/PwmLdd2.o \
./Generated_Code/SMasterLdd1.o \
./Generated_Code/STP_REF.o \
./Generated_Code/Stepperspi.o \
./Generated_Code/TU1.o \
./Generated_Code/UTIL1.o \
./Generated_Code/Vectors.o \
./Generated_Code/WAIT1.o \
./Generated_Code/croutine.o \
./Generated_Code/event_groups.o \
./Generated_Code/heap_1.o \
./Generated_Code/heap_2.o \
./Generated_Code/heap_3.o \
./Generated_Code/heap_4.o \
./Generated_Code/heap_5.o \
./Generated_Code/list.o \
./Generated_Code/port.o \
./Generated_Code/queue.o \
./Generated_Code/tasks.o \
./Generated_Code/timers.o 

C_DEPS += \
./Generated_Code/AS1.d \
./Generated_Code/ASerialLdd1.d \
./Generated_Code/BitIoLdd1.d \
./Generated_Code/BitIoLdd2.d \
./Generated_Code/BitIoLdd3.d \
./Generated_Code/BitIoLdd4.d \
./Generated_Code/BitIoLdd6.d \
./Generated_Code/CLS1.d \
./Generated_Code/CS1.d \
./Generated_Code/Cpu.d \
./Generated_Code/DC_DIR.d \
./Generated_Code/DC_EN.d \
./Generated_Code/ExtIntLdd3.d \
./Generated_Code/FRTOS1.d \
./Generated_Code/LED_blue.d \
./Generated_Code/LED_green.d \
./Generated_Code/LED_red.d \
./Generated_Code/LEDpin1.d \
./Generated_Code/LEDpin2.d \
./Generated_Code/LEDpin3.d \
./Generated_Code/PE_LDD.d \
./Generated_Code/PWM1.d \
./Generated_Code/PwmLdd2.d \
./Generated_Code/SMasterLdd1.d \
./Generated_Code/STP_REF.d \
./Generated_Code/Stepperspi.d \
./Generated_Code/TU1.d \
./Generated_Code/UTIL1.d \
./Generated_Code/Vectors.d \
./Generated_Code/WAIT1.d \
./Generated_Code/croutine.d \
./Generated_Code/event_groups.d \
./Generated_Code/heap_1.d \
./Generated_Code/heap_2.d \
./Generated_Code/heap_3.d \
./Generated_Code/heap_4.d \
./Generated_Code/heap_5.d \
./Generated_Code/list.d \
./Generated_Code/port.d \
./Generated_Code/queue.d \
./Generated_Code/tasks.d \
./Generated_Code/timers.d 


# Each subdirectory must supply rules for building sources it contributes
Generated_Code/%.o: ../Generated_Code/%.c
	@echo 'Building file: $<'
	@echo 'Invoking: Cross ARM C Compiler'
	arm-none-eabi-gcc -mcpu=cortex-m0plus -mthumb -O0 -fmessage-length=0 -fsigned-char -ffunction-sections -fdata-sections  -g3 -I"C:\Freescale\KDS_2.0.0\eclipse\ProcessorExpert/lib/Kinetis/pdd/inc" -I"C:\Freescale\KDS_2.0.0\eclipse\ProcessorExpert/lib/Kinetis/iofiles" -I"C:/Users/Flavio/Pren/git_pren-et/Pren1GR33/FRDM-SW/Shell/Sources" -I"C:/Users/Flavio/Pren/git_pren-et/Pren1GR33/FRDM-SW/Shell/Generated_Code" -std=c99 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" -c -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


