CC=arm-none-eabi-gcc
OBJCOPY=arm-none-eabi-objcopy
CFLAGS=-g -mfloat-abi=hard -mcpu=cortex-m33 -mfpu=fpv5-sp-d16 -fmessage-length=0 -fsigned-char -Xlinker --gc-sections -ffunction-sections -fdata-sections -mthumb -std=c99 -MMD -MP
LDFLAGS=-T./memory_regions.ld  -T./script/fsp.ld 
PROJECT_NAME=bms
SRC_DIRS = ra ra_cfg ra_gen src
SRC = $(shell find $(SRC_DIRS) -name '*.c')
OBJ=$(SRC:.c=.o)
# If you want to add modules you need to install the Renesas Smart Configurator, which is included in e2studio
RASC_EXE_PATH=/home/m4tse/renesas/ra/sc_v2025-04_fsp_v5.9.0/eclipse/rasc

D_FILES=$(SRC:.c=.d)
INCLUDES = \
	-I./bms-config-override \
    -I./src \
	-I./src/c_json \
	-I./ra/fsp/inc \
	-I./ra_cfg/arm \
	-I./ra/arm/littlefs \
    -I./ra/arm/CMSIS_6/CMSIS/Core/Include 	\
	-I./ra/arm/mbedtls/library \
	-I./ra/arm/mbedtls/include \
	-I./ra/aws/FreeRTOS/FreeRTOS-Plus/Source/coreJSON/source/include \
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
    -I./ra/aws/FreeRTOS/FreeRTOS-Plus/Source/FreeRTOS-Plus-TCP/source/include \
	-I./ra/fsp/src/rm_psa_crypto/inc/ \
	-I./ra/fsp/src/r_sce/ \
	-I./ra/fsp/src/r_sce/common/ \
	-I./ra/fsp/src/r_sce/crypto_procedures/src/sce9/plainkey/public/inc \
	-I./ra/fsp/src/r_sce/crypto_procedures/src/sce9/plainkey/private/inc \
	-I./ra_cfg/arm/littlefs/
	



all: $(PROJECT_NAME).elf obj_copy


# ---- YOU NEED TO HAVE E2STUDIO/RASC INSTALLED IN ORDER TO EXECUTE THE TARGETS -----
rasc_check:
ifndef RASC_EXE_PATH
	$(error RASC_EXE_PATH is not set)
endif

config: rasc_check
	$(RASC_EXE_PATH) configuration.xml

generate: rasc_check
	$(RASC_EXE_PATH) --generate configuration.xml

# ----------------------------------------------------------------------------------

# Build docs
docs:
	doxygen

dns:
	dnsmasq -C dns-server.conf

# Build final Firmware ELF
$(PROJECT_NAME).elf: $(OBJ)
	$(CC) $(CFLAGS) $(LDFLAGS) -specs=nosys.specs $(INCLUDES) -o build/$@ $^

%.o: %.c
	$(CC) $(CFLAGS) $(LDFLAGS) -specs=nosys.specs $(INCLUDES) -c $< -o $@

# Make it flashable
obj_copy: $(PROJECT_NAME).elf
	$(OBJCOPY) -O srec build/$< build/$(PROJECT_NAME).srec

clean:
	rm -rf $(OBJ) build/$(PROJECT_NAME).elf build/$(PROJECT_NAME).srec $(D_FILES) docs
	kill -9 $(pgrep dnsmasq)

.PHONY: all clean obj_copy generate rasc_check
