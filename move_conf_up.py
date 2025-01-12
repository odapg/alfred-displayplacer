#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
import json
import subprocess
import os

#------------------

def move_up_conf(nb):

    data_folder = os.getenv('alfred_workflow_data')
    confs_file = os.path.join(data_folder, 'configurations.json')

    try:
        with open(confs_file, "r") as file:
            data = json.load(file)
    except Exception as e:
        print(f"Error reading the file: {e}")
        sys.exit()

    sorted_conf = sorted(data["confs"], key=lambda x: x["nb"])
    sorted_conf[nb-1]["nb"] -= 1
    sorted_conf[nb-2]["nb"] += 1
    data["confs"] = sorted(sorted_conf, key=lambda x: x["nb"])

    try:
        with open(confs_file, "w") as file:
            json.dump(data, file, indent=4) 
    except Exception as e:
        print(f"Error saving configurations file: {e}")
    return

#------------------

def main():

    nb = int(os.getenv('nb'))
    move_up_conf(nb)

#--------------------
    
if __name__ == "__main__":
    main()
