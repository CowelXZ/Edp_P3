MI CODIGO:

const int sensorLuz = A0;        // Pin del sensor LDR
const int led1 = 5;              // LED 1
const int led2 = 6;              // LED 2
const int led3 = 7;              // LED 3

void setup() {
  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);
  pinMode(led3, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  int lecturaLuz = analogRead(sensorLuz);
  Serial.print("Nivel de luz: ");
  Serial.println(lecturaLuz);

  // Apagar todos por defecto
  digitalWrite(led1, LOW);
  digitalWrite(led2, LOW);
  digitalWrite(led3, LOW);

  if (lecturaLuz > 100) {
    digitalWrite(led1, HIGH);  // Un poco oscuro
  }
  if (lecturaLuz > 300) {
    digitalWrite(led2, HIGH);  // Más oscuro
  }
  if (lecturaLuz > 500) {
    digitalWrite(led3, HIGH);  // Muy oscuro
  }

  delay(500);
}