# Alfred displayplacer

Change the screen(s) resolution within Alfred.
Save and load screens configurations.

### Installation

1. Install displayplacer command with `brew install displayplacer`.
Since this workflow requires displayplacer v. ≥ 1.4.0, if you already have it installed, you may need to update it with `brew upgrade displayplacer`.

2. (Optional) Change the keywords in the configuration window and add hotkeys.

### Usage

- Change the resolution of your screen(s) with `dplc`.
- Save your current screen configuration (which you can modify in System Preferences > Displays as well) with `dpls`.
- Load a screen configuration with `dpll`. You can remove a configuration with ⌘↩, move it up the list with ⌥↩, and get a detailed view of it with ⇧↩.

### Remark

- Some proposed resolutions may not work (in particular for the last presented modes). This is also true in command-line.

### Acknowledgements

- [displayplacer](https://github.com/jakehilborn/displayplacer) is due to [jakehilborn](https://github.com/jakehilborn)