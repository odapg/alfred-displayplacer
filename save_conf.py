#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
import json
import subprocess
import os
import re
from list_screens import extract_screen_data

#------------------

def extract_displayplacer_command(result):
    serial_id_pattern = re.compile(r"displayplacer (?P<arguments>.+)")
    lines = result.splitlines()
    match = serial_id_pattern.search(lines[-1])
    arguments = match.group("arguments")
    return arguments

#------------------

def add_conf_item(resultJSON, name, comment, command):

    title = ""
    subtitle = ""
    variables = { "command": command}
    new_item = {                 
        "title": name,
        "subtitle": comment,
        "variables": variables,
        "valid": True
    }
    resultJSON["items"].append(new_item)
    return

#------------------

def append_to_conf_file(command, comment, description):

    data_folder = os.getenv('alfred_workflow_data')
    config_name = os.getenv('config_name')

    if not os.path.isdir(data_folder):
        try:
            os.mkdir(data_folder)
        except Exception as e:
            comment = f"Error creating data folder" 
            sys.exit()
    
    confs_file = os.path.join(data_folder, 'configurations.json')

    if os.path.isfile(confs_file):
        try:
            with open(confs_file, "r") as file:
                data = json.load(file)
        except Exception as e:
            print(f"Error reading the file: {e}")
    else:
        data = { "confs": []}

    new_entry = {
        "nb": len(data["confs"]) +1,
        "name": config_name,
        "command": command,
        "comment": comment,
        "description": description        
    }
    data["confs"].append(new_entry)

    try:
        with open(confs_file, "w") as file:
            json.dump(data, file, indent=4) 
    except Exception as e:
        print(f"Error saving configurations file: {e}")
    return

#------------------

def md_for_description(screens):

    config_name = os.getenv('config_name')
    md_doc = "# Configuration: " + config_name + "\n"
    for screen in screens:
        md_doc += "#### " + screen["type"] + "\n"
        md_doc += "* Resolution: " + screen["resolution"] + "\n"
        md_doc += "* Frequency: " + screen["hertz"] + "hz \n"
        md_doc += "* Color depth: " + screen["color_depth"] + "\n"
        md_doc += "* Scaling: " + screen["scaling"] + "\n\n"
    return md_doc

#------------------

def main():

    try:
        result = subprocess.check_output(["displayplacer", "list"], text=True)
    except FileNotFoundError:
        print("Error : the 'displayplacer' command was not found.")
        exit(1)

    command = extract_displayplacer_command(result)
    screens = extract_screen_data(result)

    comment =""
    i = 0
    for screen in screens:
            # Replaces persistent_id with serial_id
            # Cf. https://github.com/jakehilborn/displayplacer/issues/89
        command = command.replace(screen["persistent_id"], screen["serial_id"])
        if comment: comment += " ❉ "
        i +=1
        match = re.search(r"(?P<first_name>.*)/(?P<second_name>.*)", screen["type"])
        if match:
            name = "Built in" if match.group("first_name") == "Built in screen" else match.group("second_name")
        else:
            name = "Screen " + str(i)
        comment += name + ": " + screen["resolution"] + "@" + screen["hertz"] + "hz"
    description = md_for_description(screens)
    append_to_conf_file(command, comment, description)

#--------------------
    
if __name__ == "__main__":
    main()
