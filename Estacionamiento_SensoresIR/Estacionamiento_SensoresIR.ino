// int infrarrojo = 8;
// int valor = 1;

// void setup() {
//   Serial.begin(9600);
//   pinMode(infrarrojo, INPUT);
// }

// void loop() {
//   valor = random(0, 2);  // Genera un número aleatorio entre 0 y 1
//   if (valor == 1) {
//     Serial.println("Obstaculo Detectado");  // Usar comillas dobles para cadenas de texto
//   } else {
//     Serial.println("No hay obstaculo");  // Añadido para ver el otro caso
//   }
//   delay(500);
// }
int infrarrojo = 0;
int valor = 1;

void setup() {
  Serial.begin(9600);
  pinMode(infrarrojo, INPUT);
}

void loop() {
  valor =  digitalRead(infrarrojo); 
  if (valor == LOW) {
    Serial.println("Obstaculo Detectado");  
  } else {
    Serial.println("No hay obstaculo"); 
  }
  delay(500);
}