################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
C:/Users/Flavio/Pren/git_pren-et/stepper/driver/drv/l6480.c 

OBJS += \
./Sources/Stepper_driver/l6480.o 

C_DEPS += \
./Sources/Stepper_driver/l6480.d 


# Each subdirectory must supply rules for building sources it contributes
Sources/Stepper_driver/l6480.o: C:/Users/Flavio/Pren/git_pren-et/stepper/driver/drv/l6480.c
	@echo 'Building file: $<'
	@echo 'Invoking: Cross ARM C Compiler'
	arm-none-eabi-gcc -mcpu=cortex-m0plus -mthumb -O0 -fmessage-length=0 -fsigned-char -ffunction-sections -fdata-sections  -g3 -DPL_FRDM -I"C:\Freescale\KDS_2.0.0\eclipse\ProcessorExpert/lib/Kinetis/pdd/inc" -I"C:\Freescale\KDS_2.0.0\eclipse\ProcessorExpert/lib/Kinetis/iofiles" -I"C:/Users/Flavio/Pren/git_pren-et/Pren1GR33/FRDM-SW/Shell/Sources" -I"C:/Users/Flavio/Pren/git_pren-et/Pren1GR33/FRDM-SW/Shell/Generated_Code" -std=c99 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" -c -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


