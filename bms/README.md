# BMS (Battery Management System)

## Mock BMS
### Usage

Run the Mock BMS:
```shell
python3 main.py
```

You can specify the interval of generating new data in minutes with the `INTERVAL_MIN` environment variable flag:
```shell
# This will generate every 6 seconds new data (default: 1 minute)
INTERVAL_MIN=0.1 python3 main.py
```


Run the Mock BMS in a docker container:
```shell
docker build -f build/dockerfiles/bms.Dockerfile -t bms .
docker run --rm -it --network host bms
```


## On Device

### Installation

#### 1. Install Flexible Software Package 

Download and execute FSP Platform Installer from the official website:

[https://www.renesas.com/en/software-tool/flexible-software-package-fsp](https://www.renesas.com/en/software-tool/flexible-software-package-fsp)

> [!Note] 
> When downloading the FSP Platform Installer, make sure to select FreeRTOS as the RTOS.

#### 2. Install SEGGER J-Link

Download and install the SEGGER J-Link software and drivers: 

https://www.segger.com/downloads/jlink

#### 3. Clone the GitHub Repository

Open a terminal or command prompt and run:
```bash
git clone https://github.com/THI-CSI/decentralized_iam_battery_data.git
```

#### 4. Open and Prepare the Eclipse Project in e²studio (if you use e² studio)

- Launch e²studio, then follow these steps:

- Go to File > Open Projects from File System.

- Navigate to the bms folder inside the cloned repository and select it.

- Open the configuration.xml file.

- Click Generate Project Content to generate the necessary files.

#### 5. Build the project

To build the project, first select it, then click the Build button in the IDE, when using e² studios or by executing `make`


### Flashing the Image 

1. Install the [Renesas Flash Programmer](https://www.renesas.com/en/software-tool/renesas-flash-programmer-programming-gui#overview) tool if you haven't already. 
2. Flash the compiled image using: 
```bash 
rfp-cli -device ra -tool jlink -file <path-to-srec-file> -a -s 1M -vo 3.3 -if swd 
```

---

### Usage

To communicate with the device over Ethernet, you must first configure your network interface. Since only IPv4 is supported and DHCP is not available, you need to manually assign IP addresses. Additionally hostnames can be assigned in the `dns-server.conf` file.

#### Linux

To set your Gateway IP address:
```bash
sudo ip addr add 192.168.0.3/24 dev <your_interface_name>
```
To assign your DNS server
```bash
sudo ip addr add 192.168.0.2/24 dev <your_interface_name>
```
To assign the server IP address:
```bash
sudo ip addr add 192.168.1.100/24 dev <your_interface_name>
```

To forward packets to the internet or the Docker network, you need to configure your firewall. In this example, I’ll use `iptables`, though you can use any firewall of your choice. Just make sure to watch for any rules that might block the packets.

```bash
# Enable forwarding of packets
sudo sysctl -w net.ipv4.ip_forward=1
# internal is the interface to the BMS
# external is the interface to the outside, e.g. internet or docker network
sudo iptables -A FORWARD -i <internal> -o <external> -j ACCEPT
sudo iptables -A FORWARD -i <external> -o <internal> -m state --state RELATED,ESTABLISHED -j ACCEPT 

# If you want to access the internet you need to masquerade the IP from the BMS for routing purposes
sudo iptables -t nat -A POSTROUTING -o <external> -j MASQUERADE
```

> [!CAUTION]
> If you want to access the container you need to start the docker-compose files from the cloud and blockchain with podman-compose as root. The external interface is going to be podman0.

#### Windows

> [!Note] 
> These steps should be performed outside of WSL.

To set your IP address:
```powershell
netsh interface ip add address <your_interface_name> static 192.168.0.3 255.255.255.0
```

To assign the dns server IP address:
```powershell 
netsh interface ip add address <your_interface_name> static 192.168.0.2 255.255.255.0
```
