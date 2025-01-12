#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
import json
import re
import os
import subprocess

def main():

    try:
        result = subprocess.check_output(["displayplacer", "list"], text=True)
    except FileNotFoundError:
        print("Error : the 'displayplacer' command was not found.")
        exit(1)

    persistent_screen_pattern = re.compile(r"Persistent screen id:")
    nb_screens = len(re.findall(persistent_screen_pattern, result))
    my_vars = {
        "displayplacer_output": result,
        "nb_screens": nb_screens,
    }
    if (nb_screens == 1):
        serial_id_pattern = re.compile(r"Serial screen id: (?P<serial_id>\w+)\n")
        origin_pattern = re.compile(r"Origin: (?P<origin>[\d(),-]+)")
        id_match = serial_id_pattern.search(result)
        origin_match = origin_pattern.search(result)
        my_vars["serial_id"] = id_match.group("serial_id")
        my_vars["origin"] = origin_match.group("origin")

    ResultJSON= { "alfredworkflow": { "arg" : "", "variables": my_vars, } }
    print(json.dumps(ResultJSON))


#--------------------
    
if __name__ == "__main__":
    main()
