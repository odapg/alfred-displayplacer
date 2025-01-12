# Alfred displayplacer

Change the screen(s) resolution within Alfred.
Save and load screens configurations.

### Installation

1. Install the [displayplacer](https://github.com/jakehilborn/displayplacer) command with `brew install displayplacer`.
Since this workflow requires displayplacer v. ≥ 1.4.0, if you already have it installed, you may need to update it with `brew upgrade displayplacer`.

2. (Optional) Change the keywords in the configuration window and add hotkeys.

### Usage

- Change the resolution of your screen(s) with `dplc`.
  <img width="764" alt="Capture2" src="https://github.com/user-attachments/assets/b04da8be-72e5-40b6-8c74-7e72ea273fa2" />

- Save your current screen configuration (which you can modify in System Preferences > Displays as well) with `dpls`.
  
  <img width="764" alt="Capture1" src="https://github.com/user-attachments/assets/173c8207-f0d3-41b2-93d4-e640aecc2f31" />

- Load a screen configuration with `dpll`. You can remove a configuration with ⌘↩, move it up the list with ⌥↩, and get a detailed view of it with ⇧↩.
<img width="764" alt="Capture3" src="https://github.com/user-attachments/assets/d3409d82-d678-43e9-9827-11e05b69bb51" />

### Remark

- Some proposed resolutions may not work (in particular for the last presented modes). This is also true in command-line.

### Acknowledgements

- [displayplacer](https://github.com/jakehilborn/displayplacer) is due to @jakehilborn
