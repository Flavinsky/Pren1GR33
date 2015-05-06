################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Sources/BLDC.c \
../Sources/DC.c \
../Sources/Error.c \
../Sources/Events.c \
../Sources/Shell.c \
../Sources/main.c 

OBJS += \
./Sources/BLDC.o \
./Sources/DC.o \
./Sources/Error.o \
./Sources/Events.o \
./Sources/Shell.o \
./Sources/main.o 

C_DEPS += \
./Sources/BLDC.d \
./Sources/DC.d \
./Sources/Error.d \
./Sources/Events.d \
./Sources/Shell.d \
./Sources/main.d 


# Each subdirectory must supply rules for building sources it contributes
Sources/%.o: ../Sources/%.c
	@echo 'Building file: $<'
	@echo 'Invoking: Cross ARM C Compiler'
	arm-none-eabi-gcc -mcpu=cortex-m0plus -mthumb -O0 -fmessage-length=0 -fsigned-char -ffunction-sections -fdata-sections  -g3 -I"C:\Freescale\KDS_2.0.0\eclipse\ProcessorExpert/lib/Kinetis/pdd/inc" -I"C:\Freescale\KDS_2.0.0\eclipse\ProcessorExpert/lib/Kinetis/iofiles" -I"C:/Users/Flavio/Pren/git_pren-et/Pren1GR33/FRDM-SW/Shell/Sources" -I"C:/Users/Flavio/Pren/git_pren-et/Pren1GR33/FRDM-SW/Shell/Generated_Code" -std=c99 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" -c -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


