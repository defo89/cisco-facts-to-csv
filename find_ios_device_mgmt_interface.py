#!/usr/bin/env python

'''
This script takes a list of Cisco IOS devices as input,
finds subnet mask and interface of the management IP address
and writes results to a csv file.
'''

from __future__ import print_function

import csv
import socket
import getpass
from collections import OrderedDict
import textfsm
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import NetMikoAuthenticationException

def write_csv_row(csvfile, dict_write):
    ''' Write dictionary values to rows in csv file'''
    with open(csvfile, 'a') as outcsv1:
        writer = csv.DictWriter(outcsv1, dict_write.keys())
        writer.writerow(dict_write)

# Switch login
USERNAME = raw_input('Username: ')
PASSWORD = getpass.getpass('Password: ')
SECRET = getpass.getpass('Secret (press enter if not in use): ')

# Input file for device list
FILE_SWITCH_LIST = raw_input('Switch list file: ')

# Output CSV file
FILE_CSV_OUTPUT = raw_input('Output file name: ')

# NTC templates
TEMPLATE_IOS_SHOW_VERSION = 'ntc_textfsm_templates/cisco_ios_show_version.template'
TEMPLATE_IOS_SHOW_INTERFACES = 'ntc_textfsm_templates/cisco_ios_show_interfaces.template'

# Define connection settings for IOS devices
IOS_DEVICE = {
    'device_type': 'cisco_ios',
    'username': USERNAME,
    'password': PASSWORD,
    'secret': SECRET,
}

# Write headers to a CSV file
with open(FILE_CSV_OUTPUT, 'wb') as outcsv:
    CSVWRITER = csv.writer(outcsv)
    CSVWRITER.writerow(['IP Address', 'Hostname', 'Management IP Address',
                        'Management Interface'])

# Create an empty list to be filled with switch IP addresses
IOS_IP_LIST = []

# Fill the list with IPs from file
with open(FILE_SWITCH_LIST) as readfile:
    for line in readfile:
        IOS_IP_LIST.append(line.strip())

# loop through devices in the switch list
for ios_ip in IOS_IP_LIST:
    try:
        ios_conn = ConnectHandler(host=ios_ip, **IOS_DEVICE)

        # enter enable mode
        ios_conn.enable()

        # Create a new ordered dictionary
        dict_result = OrderedDict()

        # Open FSM template file
        template_show_interfaces = open(TEMPLATE_IOS_SHOW_INTERFACES)
        re_table_show_interfaces = textfsm.TextFSM(template_show_interfaces)

        # Execute a show command and run TextFSM template against the output
        fsm_input_show_interfaces = ios_conn.send_command('show interfaces')
        fsm_results_show_interfaces = re_table_show_interfaces.ParseText(fsm_input_show_interfaces)

        # Open FSM template file
        template_version = open(TEMPLATE_IOS_SHOW_VERSION)
        re_table_version = textfsm.TextFSM(template_version)

        # Execute a show command and run TextFSM template against the output
        fsm_input_version = ios_conn.send_command('show version')
        fsm_results_version = re_table_version.ParseText(fsm_input_version)

        # Find interface for management IP address
        for key in fsm_results_show_interfaces:
            if ios_ip in key[7]:
            # When IP is found, write results to CSV
                # Fill the dictionary with required keys-values
                dict_result['ip'] = ios_ip
                dict_result['hostname'] = fsm_results_version[0][2]
                dict_result['mgmt_ip'] = key[7]
                dict_result['mgmt_if'] = key[0]
                # Append a dictionary to csv file
                write_csv_row(FILE_CSV_OUTPUT, dict_result)

                print ('Wrote results for %s' % ios_ip)

        # close the SSH connection
        ios_conn.disconnect()

    except socket.gaierror:
        print ('Could not connect to %s' % ios_ip)
        continue

    except socket.error:
        print ('Could not connect to %s' % ios_ip)
        continue

    except NetMikoTimeoutException:
        print ('Timeout connecting to %s' % ios_ip)
        continue

    except NetMikoAuthenticationException:
        print ('Authentication failed with %s' % ios_ip)
        continue
