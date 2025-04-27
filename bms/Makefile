CC=arm-none-eabi-gcc
OBJCOPY=arm-none-eabi-objcopy
CFLAGS=-mcpu=cortex-m4 -mthumb -Wall 
CFLAGS=-g -mfloat-abi=hard -mcpu=cortex-m33 -mfpu=fpv5-sp-d16 -Wunused -Wuninitialized -Wall -Wextra -Wmissing-declarations -Wconversion -Wpointer-arith -Wshadow -Wlogical-op -Waggregate-return -Wfloat-equal -fmessage-length=0 -fsigned-char -ffunction-sections -fdata-sections -mthumb -std=c99 -MMD -MP
LDFLAGS=-T./ld/fsp.ld -T./ld/memory_regions.ld
SRC=$(wildcard src/*.c)
PROJECT_NAME=bms
SRC_DIRS = ra ra_gen src
SRC = $(shell find $(SRC_DIRS) -name '*.c')
OBJ=$(SRC:.c=.o)
D_FILES=$(SRC:.c=.d)
INCLUDES = -I./ra/arm/CMSIS_6/CMSIS/Core/Include 	\
    -I./ra/aws/FreeRTOS/FreeRTOS-Plus/Source/FreeRTOS-Plus-TCP/source/include \
    -I./ra/aws/FreeRTOS/FreeRTOS-Plus/Source/FreeRTOS-Plus-TCP/source/portable/Compiler/GCC \
    -I./ra/aws/FreeRTOS/FreeRTOS/Source/include	\
    -I./ra/fsp/inc	\
    -I./ra/fsp/inc/api	\
    -I./ra/fsp/inc/instances	\
    -I./ra/fsp/src/rm_freertos_port	\
    -I./ra_cfg/aws	\
    -I./ra_cfg/fsp_cfg	\
    -I./ra_cfg/fsp_cfg/bsp	\
    -I./ra_gen	\
    -I./src	\
    -I.	\
    -I./ra/aws/FreeRTOS/FreeRTOS-Plus/Source/FreeRTOS-Plus-TCP/source/include

all: $(PROJECT_NAME).elf obj_copy

# Build final Firmware ELF
$(PROJECT_NAME).elf: $(OBJ)
	$(CC) $(CFLAGS) $(LDFLAGS) -specs=nosys.specs $(INCLUDES) -o build/$@ $^

%.o: %.c
	$(CC) $(CFLAGS) $(LDFLAGS) -specs=nosys.specs $(INCLUDES) -c $< -o $@

# Make it flashable
obj_copy: $(PROJECT_NAME).elf
	$(OBJCOPY) -O srec build/$< build/$(PROJECT_NAME).srec

clean:
	rm -f $(OBJ) build/$(PROJECT_NAME).elf build/$(PROJECT_NAME).srec $(D_FILES)


.PHONY: all clean obj_copy