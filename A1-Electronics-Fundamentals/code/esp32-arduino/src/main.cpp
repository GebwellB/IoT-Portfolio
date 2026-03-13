#include <Arduino.h>
#include <Wire.h>
#include <SPI.h>
#include <math.h>

#define RGB_R 19
#define RGB_G 20
#define RGB_B 21
#define THERM_PIN A2

const float BETA       = 3950.0;
const float R_FIXED    = 10000.0;
const float NOMINAL_R  = 10000.0;
const float NOMINAL_T  = 298.15;

float readThermistorTemp() {
  int adcVal = analogRead(THERM_PIN);

  // Guard against open/short circuit
  if (adcVal == 0 || adcVal == 4095) {
    Serial.println("ERROR: Thermistor read out of range");
    return -999;
  }

  float resistance = R_FIXED * adcVal / (4095.0 - adcVal);
  float tempK = 1.0 / (1.0 / NOMINAL_T + (1.0 / BETA) * log(resistance / NOMINAL_R));
  return tempK - 273.15;
}

void setRGB(int red, int green, int blue) {
  analogWrite(RGB_R, red);
  analogWrite(RGB_G, green);
  analogWrite(RGB_B, blue);
}

void setup() {
  Serial.begin(115200);
  Serial.println("Engine Monitor: Starting...");
  analogReadResolution(12);
  analogWriteRange(255);
  pinMode(THERM_PIN, INPUT);
  pinMode(RGB_R, OUTPUT);
  pinMode(RGB_G, OUTPUT);
  pinMode(RGB_B, OUTPUT);
}

void loop() {
  int temperature = analogRead(THERM_PIN);

  // Ensure temperature is valid
  float temp = readThermistorTemp();
  if (temp != -999) {
    Serial.print("Temp: ");
    Serial.print(temp);
    Serial.print("°C");

    // set tempreature to BLUE if between 0 and 22 degrees C
    if (temp >= 0 && temp <= 21.99){
        setRGB(0, 0, 255);
        Serial.print(" - ");
        Serial.println("Blue");
      }
      // set tempreature to GREEN if between 22 and 24 degrees C
      else if (temp >= 22 && temp <= 23.99){
        setRGB(0, 255, 0);
        Serial.print(" - ");
        Serial.println("Green");
      }
      // set tempreature to GREEN if between 24 and 28 degrees C
      else if (temp >= 24 && temp <= 27.99){
        setRGB(255, 255, 0);
        Serial.print(" - ");
        Serial.println("Yellow");
      }
      // set tempreature to RED if over 28 degrees C
      else if (temp >= 28){
        setRGB(255, 0, 0);
        Serial.print(" - ");
        Serial.println("Red");
      }
  }

  delay(1000);
}
