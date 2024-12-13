int buzzerPin = 5;  // Pin connected to the buzzer
char data;           // Data received

void setup() {
    pinMode(buzzerPin, OUTPUT);
    Serial.begin(9600);  // Initialize serial communication
}

void loop() {
    if (Serial.available() > 0) {
        data = Serial.read();  // Read serial data
        if (data == '1') {     // Slow buzzer signal
            for (int i = 0; i < 3; i++) {
                digitalWrite(5, HIGH);
                delay(500);  // Slow interval of 500 milliseconds
                digitalWrite(5, LOW);
                delay(500);
            }
        } else if (data == '2') {  // Fast buzzer signal
            for (int i = 0; i < 5; i++) {
                digitalWrite(5, HIGH);
                delay(200);  // Fast interval of 200 milliseconds
                digitalWrite(5, LOW);
                delay(200);
            }
        } else if (data == '0') {  // No buzzer
            digitalWrite(5, LOW);
        }
    }
}
