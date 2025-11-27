int RED_PIN = D5;
int YELLOW_PIN = D6;
int GREEN_PIN = D7;

char incoming[20];
int indexPos = 0;
int state = 0;

void setup() {
  Serial.begin(115200);

  pinMode(RED_PIN, OUTPUT);
  pinMode(YELLOW_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);

  digitalWrite(RED_PIN, LOW);
  digitalWrite(YELLOW_PIN, LOW);
  digitalWrite(GREEN_PIN, LOW);

  Serial.println("ESP_READY");
}

void loop() {
  while (Serial.available()) {
    char c = Serial.read();

    if (c == '\n') {
      incoming[indexPos] = '\0';   // end string

      if (strcmp(incoming, "NEXT") == 0) {
        state = (state + 1) % 3;
        setLED(state);
      }

      indexPos = 0; // clear buffer
    }
    else {
      if (indexPos < sizeof(incoming) - 1)
        incoming[indexPos++] = c;
    }
  }
}

void setLED(int s) {
  if (s == 0) {
    digitalWrite(RED_PIN, HIGH);
    digitalWrite(YELLOW_PIN, LOW);
    digitalWrite(GREEN_PIN, LOW);
    Serial.println("READY RED");
  }
  else if (s == 1) {
    digitalWrite(RED_PIN, LOW);
    digitalWrite(YELLOW_PIN, HIGH);
    digitalWrite(GREEN_PIN, LOW);
    Serial.println("READY YELLOW");
  }
  else {
    digitalWrite(RED_PIN, LOW);
    digitalWrite(YELLOW_PIN, LOW);
    digitalWrite(GREEN_PIN, HIGH);
    Serial.println("READY GREEN");
  }
}
