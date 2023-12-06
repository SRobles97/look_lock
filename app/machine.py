import face_recognition
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
        picture_path = "app/static/images/last_photo.jpg"
        camera.capture_file(picture_path)
        check_for_face_and_upload(picture_path)
    finally:
        camera.stop()


def check_for_face_and_upload(picture_path):
    sent_image = face_recognition.load_image_file(picture_path)
    sent_encoding = face_recognition.face_encodings(sent_image)
    if not sent_encoding:
        print("No se encontró una cara en la imagen")
        return

    # Cargar la imagen de la persona autorizada
    print("Cargando imagen de la persona autorizada...")
    upload_image(picture_path)


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
                time.sleep(10)
            else:
                # Tiempo de espera para la próxima medición de distancia
                time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping distance measurement...")
    finally:
        GPIO.cleanup()
