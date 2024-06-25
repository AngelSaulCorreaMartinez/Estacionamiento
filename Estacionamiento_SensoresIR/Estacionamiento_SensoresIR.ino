// Código funcional para sensores
// Sensor Relex 12m Salida A Relé Cable 2m Led Rojo Spdt Optex
// Sensor Fotoeléctrico De Barrera Autonics Bms5m-tdt-p
#include <TimeLib.h>

const int numSensores = 1; // Se ajustará según la implementación y documentación
const int sensores[numSensores] = {2};
int estadoSensores[numSensores];
int estadoAnteriorSensores[numSensores];
int lugaresLibres = numSensores; // Valor inicial equivalente al número de cajones (se asume que todos están libres inicialmente)
int lugaresOcupados = 0; // Valor inicial

void setup() {
  Serial.begin(9600);
  // Configurar la hora inicial: Año, Mes, Día, Hora, Minuto, Segundo
  setTime(16, 45, 00, 15, 06, 2024); // 16:45:00 del 15 de junio de 2024

  // Ciclo for para establecer los pines de los sensores como input
  for (int i = 0; i < numSensores; i++) { 
    pinMode(sensores[i], INPUT);
    estadoSensores[i] = digitalRead(sensores[i]); // Se asume que HIGH es libre
    estadoAnteriorSensores[i] = estadoSensores[i];
  }
}

void loop() {
  // Ciclo for para leer los valores de cada sensor 
  for (int i = 0; i < numSensores; i++) {
    estadoSensores[i] = digitalRead(sensores[i]); // Leer el estado del sensor (HIGH o LOW)

    // Checar si el resultado del sensor cambió
    if (estadoSensores[i] != estadoAnteriorSensores[i]) {

      
      // Leer la hora actual usando TimeLib.h
      time_t t = now();
      // Formatear la fecha y hora en el formato ISO 8601: "YYYY-MM-DD HH:MM:SS"
      char datetime[20]; // YYYY-MM-DD HH:MM:SS
      snprintf(datetime, sizeof(datetime), "%04d-%02d-%02d %02d:%02d:%02d",
               year(t), 
               month(t), 
               day(t),
               hour(t),
               minute(t),
               second(t));


      // Si se liberó un lugar
      if (estadoAnteriorSensores[i] == LOW && estadoSensores[i] == HIGH) { 
        lugaresOcupados--;
        lugaresLibres++;


        Serial.println("-----------------------------------------------------------");
        Serial.print("Fecha y hora : ");
        Serial.println(datetime);
        Serial.print(" Se libero el cajon numero: ");
        Serial.println(i);
        Serial.println("-----------------------------------------------------------");

        
      }
      // Si se ocupó un lugar
      else if (estadoAnteriorSensores[i] == HIGH && estadoSensores[i] == LOW) { 
        lugaresOcupados++;
        lugaresLibres--;
        
        
        Serial.println("-----------------------------------------------------------");
        Serial.print("Fecha y hora : ");
        Serial.println(datetime);
        Serial.print(" Se ocupo el cajon numero: ");
        Serial.println(i);
        Serial.println("-----------------------------------------------------------");


      }
      // Actualizar el estado anterior del sensor
      estadoAnteriorSensores[i] = estadoSensores[i];
    }
  }
  
  Serial.print("Lugares Libres: ");
  Serial.println(lugaresLibres);
  Serial.print("Lugares Ocupados: ");
  Serial.println(lugaresOcupados);
  Serial.print("Lugares totales: ");
  Serial.println(lugaresOcupados + lugaresLibres);
  Serial.println("--------------------------------------------------");
  
  delay(2000); // Verificar si el delay es correcto con pruebas 
}