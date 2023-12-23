#include <LiquidCrystal.h>

LiquidCrystal lcd(7, 8, 9, 10, 11, 12);

// Variables to store track and artist names
String currentTrack = "";
String currentArtist = "";

// Scrolling variables
int scrollDelay = 500;  // Adjust the scrolling speed (milliseconds)
int initialDelay = 1000;
unsigned long lastUpdateTime = 0;
unsigned long lastScrollTime = 0;

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
      lastUpdateTime = millis();
    }
  }

  // Check if scrolling is needed
  if (millis() - lastScrollTime > scrollDelay) {
    scrollText();
    lastScrollTime = millis();
  }

  // Your other code can go here if needed
}

void updateDisplay() {
  // Clear the LCD screen
  lcd.clear();

  // Set the cursor to the beginning of the first line
  lcd.setCursor(0, 0);
  lcd.print(currentTrack.substring(0, 16));

  // Set the cursor to the beginning of the second line
  lcd.setCursor(0, 1);
  lcd.print(currentArtist.substring(0, 16));
}

void scrollText() {
  // Scroll the track and artist names
  scrollTextLine(currentTrack, 0);
  scrollTextLine(currentArtist, 1);
}


void scrollTextLine(String text, int line) {
  // Scroll the text on the specified line
  int textLength = text.length();
  if (textLength > 16) {
    // If text is longer than the LCD width, scroll it
    for (int i = 0; i <= textLength - 16; i++) {
      if (Serial.available() > 0) {
        return;
      }
      lcd.setCursor(0, line);
      lcd.print(text.substring(i, i + 16));
      delay(150);  // Adjust the delay for smoother scrolling
    }
    delay((initialDelay/2 + 150)/2);
    if (Serial.available() > 0) {
      return;
    }
    delay((initialDelay/2 + 150)/2);
    if (Serial.available() > 0) {
      return;
    }
    lcd.setCursor(0, line);
    lcd.print(text.substring(0, 16));
    delay((initialDelay + 150)/2);
    if (Serial.available() > 0) {
      return;
    }
    delay((initialDelay + 150)/2);

  } else {
    // If text is shorter than the LCD width, display it without scrolling
    lcd.setCursor(0, line);
    lcd.print(text);
    //delay(150);
  }
}