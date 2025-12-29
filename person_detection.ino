const int TRIG_PIN = 8;
const int ECHO_PIN = 9;
const int BUZZER_PIN = 13;

const int BUTTON_PIN = 7;
const int FALL_THRESHOLD_CM = 90;

bool systemOn = false;
bool lastButton = HIGH;

long readDistanceCM() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  unsigned long duration = pulseIn(ECHO_PIN, HIGH, 30000UL);
  if (duration == 0) return 999;
  return duration / 58;
}

void setup() {
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);

  Serial.begin(9600);
}

void loop() {
  bool buttonNow = digitalRead(BUTTON_PIN);

  if (lastButton == HIGH && buttonNow == LOW) {
    systemOn = !systemOn;
    delay(200);
  }
  lastButton = buttonNow;

  // SYSTEM OFF
  if (!systemOn) {
    digitalWrite(BUZZER_PIN, LOW);
    Serial.println("0,0");   // distance=0, buzzer=0
    delay(100);
    return;
  }

  // SYSTEM ON
  long distance = readDistanceCM();
  bool fallDetected = (distance >= FALL_THRESHOLD_CM);

  digitalWrite(BUZZER_PIN, fallDetected ? HIGH : LOW);

  // SEND distance + buzzer state
  Serial.print(distance);
  Serial.print(",");
  Serial.println(fallDetected ? 1 : 0);

  delay(100);
}
