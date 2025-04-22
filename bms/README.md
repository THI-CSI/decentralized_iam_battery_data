# BMS (Battery Management System)

A firmware project for managing and monitoring battery systems.

---

## Installation

### Requirements

Make sure the following tools are installed:

- **J-Link** – for flashing/debugging firmware  
  [Download J-Link Software and Documentation Pack](https://www.segger.com/downloads/jlink/)
  
- **Visual Studio Code** – for editing and developing the project  
  [Download VS Code](https://code.visualstudio.com/)

- **Dependencies for Zephyr** – RTOS for embedded devices
[Install dependencies for Zephyr](https://docs.zephyrproject.org/latest/develop/getting_started/index.html#install-dependencies)

---

## Setup

1. Clone this repository:

   ```bash
   git clone https://github.com/THI-CSI/decentralized_iam_battery_data.git
   git checkout feat/bms-http-client
   cd bms
   ```

2. Open the project in **VS Code**:

   ```bash
   code .
   ```

3. Install the recommended Extensions

4. Set up **Zephyr IDE:**

   1. Open the **Zephyr IDE** tab in VS Code.
   2. In the **Zephyr Extension Setup** section, click **Workspace**.
   3. Click **Initialize Workspace** → choose **Select west.yml in Workspace**.
   4. Navigate to the `west-manifest/west.yml` file inside your project folder and select it.
   5. When prompted, choose the **`arm` Toolchain**.

5. In the **Zephyr IDE** tab:

   - Navigate to the **Project** section.
   - Click **Add Build** for the `bms` project.
   - When prompted:
     - Select **Zephyr Directory Only**.
     - Choose the board: **ek_ra6m5**.
     - Accept all default values for the remaining prompts.
   - After the build is added, click **Add Runner**.
   - Select **jlink** as the runner and use the default values for all prompts.


## Building and Flashing the Image

### To Build:

1. Open the **Zephyr IDE** tab.
2. Under the **BMS: Build / EK_RA6M5** section, click the **Build** button.

### To Flash:

1. Connect a **Micro USB cable** from your host device (e.g., laptop) to the **Micro USB port** on your target hardware (**USB DEBUG**).



2. In the **Zephyr IDE** tab, under the **BMS: Build / EK_RA6M5** section, click the **Flash** button.

