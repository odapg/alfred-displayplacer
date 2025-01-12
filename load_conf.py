#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
import json
import os

#------------------

def add_conf_item(resultJSON, name, comment, command, nb, description):

    variables = {"command": command, "nb": nb, description: "description"}
    mods = {"ctrl": {"valid": False, "subtitle": comment},  
            "shift": {
                "arg": description,
                "valid": True, 
                "subtitle": "Get details about this configuration"},
            "cmd": {
                "valid": True,
                "subtitle": "Delete this configuration",
                },
            }
    
    if nb > 1:
        mods.update({"alt": {
                        "valid": True,
                        "subtitle": "Move this configuration up in the list",
                    },
                })
    else: mods.update({"alt": {"valid": False, "subtitle": comment}})

    new_item = {                 
        "title": name,
        "subtitle": comment,
        "variables": variables,
        "valid": True,
        "mods": mods,
    }
    resultJSON["items"].append(new_item)
    return

#------------------

def no_conf_yet(resultJSON):

    title = "No configuration has been found"
    new_item = {                 
        "title": title,
        "valid": True
    }
    resultJSON["items"].append(new_item)
    return

#------------------

def read_conf_file():

    data_folder = os.getenv('alfred_workflow_data')
    confs_file = os.path.join(data_folder, 'configurations.json')

    try:
        with open(confs_file, "r") as file:
            data = json.load(file)
    except Exception:
        data = {}

    resultJSON = {"items": []} 

    if "confs" in data and len(confs:=data["confs"])>0:
        for conf in sorted(confs, key=lambda x: x["nb"]):
            add_conf_item(resultJSON, conf["name"], conf["comment"], conf["command"], conf["nb"], conf["description"])
    else:
        no_conf_yet(resultJSON)

    print(json.dumps(resultJSON))

    return

#--------------------
    
if __name__ == "__main__":
    read_conf_file()
