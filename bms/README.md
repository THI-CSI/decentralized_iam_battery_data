# BMS (Battery Management System)

A firmware project for managing and monitoring battery systems.

## Project Setup Instructions

Follow these steps to set up your development environment for this project:

---

### 1. Install Visual Studio Code

Download and install Visual Studio Code from the official website:

[https://code.visualstudio.com/](https://code.visualstudio.com/)

---

### 2. Install ARM Cross Compiler Toolchain

Install the ARM GCC cross compiler toolchain. You can do this by installing the appropriate package for your platform:

- **Windows (recommended):** [Arm GNU Toolchain Downloads](https://developer.arm.com/downloads/-/arm-gnu-toolchain-downloads)
- **Linux (Ubuntu):**  
```bash
sudo apt install gcc-arm-none-eabi
```
### 3. Install SEGGER J-Link

Download and install the SEGGER J-Link software and drivers:

https://www.segger.com/downloads/jlink
### 4. Clone the GitHub Repository

Open a terminal or command prompt and run:
   ```bash
   git clone https://github.com/THI-CSI/decentralized_iam_battery_data.git
   cd bms
   ```

Additionally, update the `CC` and `OBJCOPY` variables in the `Makefile` to point to your installed ARM toolchain executable.

### 5. Open the Repository in VS Code

Launch Visual Studio Code, then:

Select `File` > `Open Folder`

Browse to the cloned repository and open it

### 6. Install RA Device Support Files

In your system's command prompt or start menu search bar:
Search for `Renesas Support Files Manager`

Launch it

Under **Device Family**, select **RA**

Install all support files for the RA family

### 7. Additional Extensions

When you open the project in VS Code for the first time, you'll be prompted to install recommended extensions — go ahead and install all of them.

If you missed the prompt, you can still install them manually by opening the Extensions view and searching: `@recommended`

## Building and Flashing the Image 
### Build
To compile the project, run the following command in the project root:
```bash
make clean 
make 
``` 
### Flash
1. Install the [Renesas Flash Programmer](https://www.renesas.com/en/software-tool/renesas-flash-programmer-programming-gui#overview) tool if you haven't already. 
2. Flash the compiled image using: 
```bash 
rfp-cli -device ra -tool jlink -file build/bms.srec -a -s 1M -vo 3.3 -if swd 
```

