import RPi.GPIO as GPIO
import time

# Configurar los pines GPIO
GPIO.setmode(GPIO.BCM)

TRIG = 23  # Pin 16 como TRIG
ECHO = 24  # Pin 18 como ECHO

print("Distance Measurement In Progress")

# Configurar los pines TRIG y ECHO
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Inicializar TRIG en bajo
GPIO.output(TRIG, False)
print("Waiting For Sensor To Settle")
time.sleep(2)

# Crear pulso de 10us en TRIG
GPIO.output(TRIG, True)
time.sleep(0.00001)
GPIO.output(TRIG, False)

# Inicializar variables de tiempo
start_time = time.time()
end_time = time.time()

# Registrar el tiempo inicial y final
while GPIO.input(ECHO) == 0:
    start_time = time.time()

while GPIO.input(ECHO) == 1:
    end_time = time.time()

# Calcular la duración del pulso
pulse_duration = end_time - start_time

# Calcular la distancia
distance = pulse_duration * 17150
distance = round(distance, 2)

print(f"Distance: {distance} cm")

# Limpiar los pines GPIO al finalizar
GPIO.cleanup()
