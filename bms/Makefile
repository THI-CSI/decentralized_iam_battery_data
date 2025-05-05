CC=arm-none-eabi-gcc
OBJCOPY=arm-none-eabi-objcopy
CFLAGS=-g -mfloat-abi=hard -mcpu=cortex-m33 -mfpu=fpv5-sp-d16 -Wunused -Wuninitialized -Wall -Wextra -Wmissing-declarations -Wconversion -Wpointer-arith -Wshadow -Wlogical-op -Waggregate-return -Wfloat-equal -fmessage-length=0 -fsigned-char -Xlinker --gc-sections -ffunction-sections -fdata-sections -mthumb -std=c99 -MMD -MP
LDFLAGS=-T./ra-lib/ld/fsp.ld -T./ra-lib/ld/memory_regions.ld
PROJECT_NAME=bms
SRC_DIRS = ra-lib ra_gen src
SRC = $(shell find $(SRC_DIRS) -name '*.c')
OBJ=$(SRC:.c=.o)
# If you want to add modules you need to install the Renesas Smart Configurator, which is included in e2studio
RASC_EXE_PATH=/home/m4tse/renesas/ra/sc_v2025-01_fsp_v5.8.0/eclipse/rasc

D_FILES=$(SRC:.c=.d)
INCLUDES = -I./ra-lib/ra/arm/CMSIS_6/CMSIS/Core/Include 	\
    -I./ra-lib/ra/aws/FreeRTOS/FreeRTOS-Plus/Source/FreeRTOS-Plus-TCP/source/include \
    -I./ra-lib/ra/aws/FreeRTOS/FreeRTOS-Plus/Source/FreeRTOS-Plus-TCP/source/portable/Compiler/GCC \
    -I./ra-lib/ra/aws/FreeRTOS/FreeRTOS/Source/include	\
    -I./ra-lib/ra/fsp/inc	\
    -I./ra-lib/ra/fsp/inc/api	\
    -I./ra-lib/ra/fsp/inc/instances	\
    -I./ra-lib/ra/fsp/src/rm_freertos_port	\
    -I./ra-lib/ra_cfg/aws	\
    -I./ra-lib/ra_cfg/fsp_cfg	\
    -I./ra-lib/ra_cfg/fsp_cfg/bsp	\
    -I./ra-lib/ra_gen	\
    -I./src	\
    -I./ra-lib/ra/aws/FreeRTOS/FreeRTOS-Plus/Source/FreeRTOS-Plus-TCP/source/include


all: move $(PROJECT_NAME).elf obj_copy


# ---- YOU NEED TO HAVE E2STUDIO/RASC INSTALLED IN ORDER TO EXECUTE THE TARGETS -----
# Move generated files to subfolder
move:
	@if [ -d ld ]; then mv ld ra-lib; fi 
	@if [ -d ra_gen ]; then mv ra_gen ra-lib; fi
	@if [ -d ra_cfg ]; then mv ra_cfg ra-lib; fi
	@if [ -d ra ]; then mv ra ra-lib; fi
	sed -i -e 's/INCLUDE ld/INCLUDE ra-lib\/ld/' ra-lib/ld/fsp.ld

config:
	$(RASC_EXE_PATH) configuration.xml

# ----------------------------------------------------------------------------------

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


.PHONY: all clean obj_copy move