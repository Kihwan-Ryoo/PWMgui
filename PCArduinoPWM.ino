const int mtr = 6;

void setup() {
  pinMode(mtr, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  int a = 0;
  while (Serial.available()){
    a = Serial.read();
    Serial.write(a);
    analogWrite(mtr, a);
    delay(10);
  }
}
