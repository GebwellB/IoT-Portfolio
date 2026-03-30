// Week 6/7 Task 1 — RFID Card Reader (SPI)
#include <Arduino.h>
#include <Wire.h>
#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN  17    // SDA pin connected to GPIO 17 (SPI SS)
#define RST_PIN 9    // RST pin connected to GPIO 9

#define RGB_R 10
#define RGB_G 11
#define RGB_B 12

MFRC522 mfrc522(SS_PIN, RST_PIN);

  // blue token: bcef454a
  // white card: 23ca7516

const String allowedCards[2] = {"bcef454b", "23ca7516"}; //bcef454b is wrong, should be: bcef454a
const int totalCards = 2;

void setRGB(int red, int green, int blue) {
  analogWrite(RGB_R, red);
  analogWrite(RGB_G, green);
  analogWrite(RGB_B, blue);
}

void setup() {
  Serial.begin(115200);
  SPI.begin();
  mfrc522.PCD_Init();
  Serial.println("RockCore Access Control: Ready");
  Serial.println("Scan RFID card...");
  analogWriteRange(255);
  pinMode(RGB_R, OUTPUT);
  pinMode(RGB_G, OUTPUT);
  pinMode(RGB_B, OUTPUT);
  setRGB(255,0,0);
}

void loop() {
  if (!mfrc522.PICC_IsNewCardPresent() || !mfrc522.PICC_ReadCardSerial()) {
    return;
  }

  String cardID = "";
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    cardID += String(mfrc522.uid.uidByte[i], HEX);
  }

  Serial.print("Card UID: ");
  Serial.println(cardID);

  mfrc522.PICC_HaltA();

  bool cardValid = false;

  for (int i = 0; i < totalCards; i++) {
	
    if (allowedCards[i] == cardID) {
		cardValid = true;
        break;
    }
  }

  if (cardValid){
	Serial.println("Welcome in!");
		setRGB(0,255,0);
		delay(1200);
		setRGB(255,0,0);
  }
  else{
		Serial.println("Go away!");
		for (int j = 0; j < 7; j++){
			setRGB(255,0,0);
			delay(100);
			setRGB(0,0,0);
			delay(100);
		}
		setRGB(255,0,0);
  };

  delay(1000);
}