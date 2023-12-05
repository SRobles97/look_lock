from picamera2 import Picamera2
import time

# Única instancia de Picamera2
picam2 = Picamera2()


def take_picture(camera):
    try:
        camera_config = camera.create_still_configuration(main={"size": (1920, 1080)})
        camera.configure(camera_config)
        camera.start()
        time.sleep(2)
        camera.capture_file("app/static/images/last_photo.jpg")
    finally:
        camera.stop()


def initialize_photo_process():
    while True:
        take_picture(picam2)
        time.sleep(300)  # Tiempo de espera entre cada foto
