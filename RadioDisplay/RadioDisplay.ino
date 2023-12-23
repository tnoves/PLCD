#include <LiquidCrystal.h>

LiquidCrystal lcd(7, 8, 9, 10, 11, 12);

// Variables to store track and artist names
String currentTrack = "";
String currentArtist = "";

void setup() {
  // Initialize the LCD
  lcd.begin(16, 2);

  // Serial communication setup
  Serial.begin(9600);
}

void loop() {
  // Check if there is serial data available
  if (Serial.available() > 0) {
    // Read the serial input until a newline character is received
    String serialData = Serial.readStringUntil('\n');

    // Parse the serial data (format: "track^artist")
    int separatorIndex = serialData.indexOf('^');
    if (separatorIndex != -1) {
      currentTrack = serialData.substring(0, separatorIndex);
      currentArtist = serialData.substring(separatorIndex + 1);

      // Update the LCD display only if there's new information
      updateDisplay();
    }
  }

  // Your other code can go here if needed
}

void updateDisplay() {
  // Clear the LCD screen
  lcd.clear();

  // Set the cursor to the beginning of the first line
  lcd.setCursor(0, 0);
  lcd.print(currentTrack);

  // Set the cursor to the beginning of the second line
  lcd.setCursor(0, 1);
  lcd.print(currentArtist);
}
