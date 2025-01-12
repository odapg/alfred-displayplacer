#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
import json
import os
import re

#------------------

def extract_modes_for_serial_id(result, target_serial_id):
    serial_id_pattern = re.compile(r"Serial screen id: (?P<serial_id>[\w-]+)")
    mode_pattern = re.compile(r"mode (?P<mode>\d+):")
    res_pattern = re.compile(r"res:(?P<res>[\dx]+)")
    hz_pattern = re.compile(r"hz:(?P<hz>\d+)")
    color_depth_pattern = re.compile(r"color_depth:(?P<color_depth>\d+)")
    scaling_pattern = re.compile(r"scaling:(?P<scaling>\w+)")
    current_mode_pattern = re.compile(r"current mode")

    lines = result.splitlines()
    modes = []
    current_serial_id = None
    target_section = False

    for line in lines:
        serial_id_match = serial_id_pattern.search(line)
        if serial_id_match:
            current_serial_id = serial_id_match.group("serial_id")
            if current_serial_id == target_serial_id:
                target_section = True
            elif target_section:
                # If we've reached a new persistent ID after finding the target, stop processing
                break

        if target_section and "mode" in line:
            mode_data = {
                "mode": None,
                "res": None,
                "hz": None,
                "color_depth": None,
                "scaling": None,
                "current": False
            }
            mode_match = mode_pattern.search(line)
            res_match = res_pattern.search(line)
            hz_match = hz_pattern.search(line)
            color_depth_match = color_depth_pattern.search(line)
            scaling_match = scaling_pattern.search(line)
            current_match = current_mode_pattern.search(line)

            if mode_match:
                mode_data["mode"] = mode_match.group("mode")
            if res_match:
                mode_data["res"] = res_match.group("res")
            if hz_match:
                mode_data["hz"] = hz_match.group("hz")
            if color_depth_match:
                mode_data["color_depth"] = color_depth_match.group("color_depth")
            if scaling_match:
                mode_data["scaling"] = scaling_match.group("scaling")
            if current_match:
                mode_data["current"] = True

            modes.append(mode_data)
    return modes

#------------------

def add_mode_item(resultJSON, mode, serial_id):

    title = ""
    if mode["current"]:
        title += "✔ " 
    title += "Mode " + mode["mode"]
    subtitle = ""
    if mode["res"]:
        subtitle += "Res.: " + mode["res"] + ", "
    if mode["hz"]:
        subtitle += "Fq.: " + mode["hz"] + "hz, "
    if mode["color_depth"]:
        subtitle += "Color depth: " + mode["color_depth"] + ", "
    if mode["scaling"]:
        subtitle += "Scaling: " + mode["scaling"]

    variables = { "serial_id": serial_id, "mode":  mode["mode"]}
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

    serial_id = os.getenv('serial_id')
    displayplacer_output = os.getenv('displayplacer_output')
    origin = os.getenv('origin')

    modes = extract_modes_for_serial_id(displayplacer_output, serial_id)

    resultJSON = {"items": []} 
    for mode in [mode for mode in modes if mode["current"]]:
    	add_mode_item(resultJSON, mode, serial_id)
    for mode in [mode for mode in modes if not mode["current"]]:
        add_mode_item(resultJSON, mode, serial_id)

    print(json.dumps(resultJSON))

#--------------------
    
if __name__ == "__main__":
    main()
