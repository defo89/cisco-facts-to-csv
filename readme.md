## Cisco Facts to CSV

Small scripts to collect information from Cisco devices running IOS or IOS-XE software and write it into a CSV file.

IP and hostname are present in every row for easier filtering.

Leverages [TextFSM](https://github.com/google/textfsm "google/textfsm") and [templates created by NTC](https://github.com/networktocode/ntc-templates "networktocode/ntc-templates").

## Installation

Requires Python 2

```
git clone https://github.com/dmitrijsf/cisco-facts-to-csv.git
cd cisco-facts-to-csv
pip install -r requirements.txt
chmod u+x ./collect_cdp_neighbors.py
```

## Usage

Create a list of IP addreses in project folder.
Run the desired script, enter credentials, choose your list and enter the filename of an output CSV file.


Create a list with Cisco devices
```
> cat ios_device_list 
10.1.1.2
10.2.1.2
10.5.1.2
```

Run the script

```
> python collect_cdp_neighbors.py 
Username: adminuser
Password: (your secret data)
Secret (press enter if not in use): (your secret data)
Switch list file: ios_device_list 		// reference the file created before
Output file name: cdp_list.csv			// CSV file will be created

Wrote results for 10.1.1.2
Wrote results for 10.2.1.2
Wrote results for 10.5.1.2
```

Observe results

```
> cat cdp_list.csv
IP Address,Hostname,Local Interface,Remote Hostname,Remote Platform,Remote Interface
10.1.1.2,switch1,GigabitEthernet0/1,remote_switch10.lab.net,cisco WS-C2960S-48FPS-L,GigabitEthernet1/0/1
10.2.1.2,switch3,GigabitEthernet1/0/1,remote_switch20.lab.net,Cisco CISCO1921/K9,GigabitEthernet0/1
10.5.1.2,switch5,GigabitEthernet1/0/11,remote_switch21.lab.net,cisco WS-C2960S-24PS-L,GigabitEthernet1/0/28
10.5.1.2,switch5,GigabitEthernet2/0/24,remote_switch22.lab.net,cisco WS-C3850-48T,GigabitEthernet1/0/46
```

## Credits

https://github.com/google/textfsm - Python module for parsing semi-structured text into python tables.
https://github.com/networktocode/ntc-templates - TextFSM templates for parsing show commands of network devices.
https://gist.github.com/zenorocha/4526327 - readme template.
