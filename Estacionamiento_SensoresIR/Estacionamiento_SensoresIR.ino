const int numSensores = 20; // se va a ajustar en base a lo que nos digan los de implemetnacion y documentacion
const int sensores[numSensores] = {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20};
int estadoSensores[numSensores];
int estadoAnteriorSensores[numSensores];
int lugaresLibres = numSensores; //valor inicial equivalente al numero de cajones (se piensa que todos esta libres inicialmente)
int lugaresOcupados = 0; // valor inicial

void setup() {
  Serial.begin(9600);

  //ciclo for para establecer los pines de los sensores como input
  for (int i = 0; i < numSensores; i++){ 
    pinMode(sensores[i], INPUT);
    estadoSensores[i] = HIGH; //Se asume que high es libre
    estadoAnteriorSensores[i] = HIGH;
  }

}

void loop() {
  

  // Ciclo for parta leer los valores de cada sensor 
  for (int i = 0; i < numSensores; i++){
    estadoSensores[i] = digitalRead(sensores[i]);
    //checar si el resultado del sensor cambio
    if (estadoSensores[i] != estadoAnteriorSensores[i]){

      //si se libero un lugar
      if (estadoAnteriorSensores[i] == LOW && estadoSensores[i] == HIGH){ 
        lugaresOcupados--;
        lugaresLibres++; 
      }
      //si se ocupo un lugar
      else if(estadoAnteriorSensores[i] == HIGH && estadoSensores[i] == LOW){ 
        lugaresOcupados++;
        lugaresLibres--;
      }
    }
    }
  
  Serial.print("Lugares Libres: ");
  Serial.println(lugaresLibres);
  Serial.print("Lugares Ocupados: ");
  Serial.println(lugaresOcupados);
  

  delay(5000);//verificar si el delay es correcto con pruebas 
}