#!/usr/bin/env python3

# Flic button client application to control Philips hue lights.
#
# This program attempts to connect to all previously verified Flic buttons by this server.
# Once connected, it uses the Qhue libtrary to query the Hue bridge API when (any) button is clicked.
# It also monitors when new buttons are verified and connects to them as well. For example, run this program and at the same time the scan_wizard.py program.

# import libraries
import json
import fliclib
from hue import init_hue_lights, HueLight, HueBridge
from os import path

CRED_FILE_PATH = 'hue_username'
BRIDGE_IP = '192.168.1.1'

# read username from credential file
if not path.exists(CRED_FILE_PATH):
	print ('No credential file found!')
	
else:
	print ('Getting username from file...')
	with open(CRED_FILE_PATH, "r") as cred_file:
		username = cred_file.read()
		print ('username: ' + username)

# initialise lights
bridge = HueBridge(username, BRIDGE_IP)

# load button groups from file
with open('groups') as f:
	json_data = f.read()
groups = json.loads(json_data)

# create flic client
client = fliclib.FlicClient("localhost")

def click_handler(channel, click_type, was_queued, time_diff):
	print(channel.bd_addr + " " + str(click_type))
	if str(click_type) == 'ClickType.ButtonSingleClick':
		try:
			print ("> Switching on associated lights... " + str(groups[channel.bd_addr]['group']))
			for light in groups[channel.bd_addr]['group']:
				bridge.get(light).on()
		except KeyError:
			print ("> Error finding lights associated with button " + str(channel.bd_addr))
	elif str(click_type) == 'ClickType.ButtonHold':
		# turn off all lights
		print ("> Turning off all lights...")
		for light in bridge:
			light.off()
	return

def got_button(bd_addr):
	cc = fliclib.ButtonConnectionChannel(bd_addr)
	# Assign function to call when a button is clicked
	cc.on_button_single_or_double_click_or_hold = click_handler
	cc.on_connection_status_changed = \
		lambda channel, connection_status, disconnect_reason: \
			print(channel.bd_addr + " " + str(connection_status) + (" " + str(disconnect_reason) if connection_status == fliclib.ConnectionStatus.Disconnected else ""))
	client.add_connection_channel(cc)

def got_info(items):
	print(items)
	for bd_addr in items["bd_addr_of_verified_buttons"]:
		got_button(bd_addr)

client.get_info(got_info)

client.on_new_verified_button = got_button

client.handle_events()
