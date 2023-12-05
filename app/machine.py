from picamera2 import Picamera2
import time


def take_picture():
    picam2 = Picamera2()
    camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)})
    picam2.configure(camera_config)
    picam2.start()
    time.sleep(2)
    picam2.capture_file("test.jpg")
    picam2.stop()


def initialize_photo_process():
    while True:
        take_picture()
        time.sleep(300)  # Espera 5 minutos antes de tomar la siguiente foto
