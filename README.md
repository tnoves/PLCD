This is an ongoing personal project to display Plex data on a 16x2 LCD display connected to an Arduino.

The repo contains 2 .ino files for use with an Arduino:
 - RadioDisplay.ino : Displays characters with no scrolling text. Anything more than 16 characters is not displayed.
 - RadioDisplayScrollInstantUpdate.ino : Checks if displayed characters on each line surpass 16 characters and implements scrolling text to show all characters if so.
