from picamera2 import Picamera2
import RPi.GPIO as GPIO
import time

from app.util.files_utils import upload_image

# Configurar los pines GPIO
GPIO.setmode(GPIO.BCM)

TRIG = 23  # Pin 16 como TRIG
ECHO = 24  # Pin 18 como ECHO

# Única instancia de Picamera2
picam2 = Picamera2()


def take_picture(camera):
    try:
        camera_config = camera.create_still_configuration(main={"size": (1920, 1080)})
        camera.configure(camera_config)
        camera.start()
        time.sleep(2)
        camera.capture_file("app/static/images/last_photo.jpg")
        upload_image("last_photo.jpg")
    finally:
        camera.stop()


def measure_distance():
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

    GPIO.output(TRIG, False)
    time.sleep(2)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    start_time = time.time()

    while GPIO.input(ECHO) == 0:
        start_time = time.time()

    while GPIO.input(ECHO) == 1:
        end_time = time.time()

    pulse_duration = end_time - start_time
    distance = pulse_duration * 17150
    distance = round(distance, 2)

    return distance


def initialize_photo_process():
    try:
        while True:
            distance = measure_distance()
            print(f"Distance: {distance} cm")

            # Define la distancia prudente para tomar la foto
            if distance < 100:  # por ejemplo, menos de 100 cm
                take_picture(picam2)
                # Tiempo de espera después de tomar una foto
                time.sleep(300)
            else:
                # Tiempo de espera para la próxima medición de distancia
                time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping distance measurement...")
    finally:
        GPIO.cleanup()
