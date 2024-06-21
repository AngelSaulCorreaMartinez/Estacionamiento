const int numSensores = 20; // se va a ajustar en base a lo que nos digan los de implemetnacion y documentacion
const int sensores[numSensores] = {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20};
int estadoSensores[numSensores];

void setup() {
  Serial.begin(9600);

  //ciclo for para establecer los pines de los sensores como input
  for (i = 0; i < numSensores; i++){ 
    pinMode(sensores[i], INPUT)
  }

}

void loop() {
  int lugaresLibres = 0; //valor inicial
  int lugaresOcupados = 0; // valor inicial

  // Ciclo for parta leer los valores de cada sensor 
  for (int i = 0; i < numSensores; i++){
    estadoSensores[i] = digitalRead(sensores[i]);
    //Si estan ocupados, se incrementa uno en la variable lugares ocupados , si no , se aumenta uno en los libres
    if (estadoSensores[i] == LOW){ //checar que si sea LOW cuando esta ocupado
      lugaresOcupados++;
    }else{
      lugaresLibres++;
    }
  }
  Serial.print("Lugares Libres: ");
  Serial.println(lugaresLibres);
  Serial.print("Lugares Ocupados: ");
  Serial.println(lugaresOcupados);

  delay(10000)//verificar si el delay es correcto con pruebas 
}