#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
import json
import subprocess
import re
import os

#------------------

def extract_screen_data(result):

    try:
        command = "system_profiler SPDisplaysDataType -json"
        result_sp = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, text=True)
        result_json = json.loads(result_sp.stdout)
        displays = result_json["SPDisplaysDataType"][0]["spdisplays_ndrvs"]
    except Exception:
        displays = None

    keys = ["persistent_id", "serial_id", "type", "resolution", "hertz", "color_depth", "scaling", "origin"]
    patterns = {
    "persistent_id": re.compile(r"Persistent screen id: (?P<persistent_id>[\w-]+)"),
    "serial_id": re.compile(r"Serial screen id: (?P<serial_id>\w+)"),
    "type": re.compile(r"Type: (?P<type>.+)"),
    "resolution": re.compile(r"Resolution: (?P<resolution>[\dx]+)"),
    "hertz": re.compile(r"Hertz: (?P<hertz>.+)"),
    "color_depth": re.compile(r"Color Depth: (?P<color_depth>.+)"),
    "scaling": re.compile(r"Scaling: (?P<scaling>.+)"),
    "origin": re.compile(r"Origin: (?P<origin>[\d(),-]+)"),
    }
    screens = []
    current = {key: None for key in keys}

    lines = result.splitlines()

    for line in lines:
        for key in keys:
            if not current[key]:
                key_match = patterns[key].search(line)
                if key_match:
                    current[key] = key_match.group(key)
                continue

        if all(current.values()):
            # displayplacer says Macbook even on iMacs
            if current["type"] == "MacBook built in screen":
                current["type"] = "Built in screen"
            # Completes the screen's name with system_profiler
            display_apple_name = ""
            if displays:
                serial_id_dec = int(current["serial_id"][1:])
                serial_id_hex = format(serial_id_dec, 'x')
                for display in displays:
                    if display["_spdisplays_display-serial-number"] == serial_id_hex:
                        current["type"] += "/" + display["_name"]

            screen_data = {key: current[key] for key in keys}
            screens.append(screen_data)
            current = {key: None for key in keys}
            # for key in keys: current[key] = None

    return screens

#------------------

def add_screen_item(resultJSON, screens, i):

	title = "Screen " + str(i+1) + ": " + screens[i]["type"]
	subtitle = "Resolution: " + screens[i]["resolution"] 
	variables = { "serial_id": screens[i]["serial_id"], "origin": screens[i]["origin"] }
	new_item = {                 
        "title": title,
        "subtitle": subtitle,
        "variables": variables,
        "valid": True
    }
	resultJSON["items"].append(new_item)
	return

#------------------

def main():

    result = os.getenv('displayplacer_output')
    screens = extract_screen_data(result)

    resultJSON = {"items": []} 
    i=0
    for screen in screens:
    	add_screen_item(resultJSON, screens, i)
    	i=+1

    print(json.dumps(resultJSON))

#--------------------
    
if __name__ == "__main__":
    main()
