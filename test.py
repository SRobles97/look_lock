from picamera2 import Picamera2
import time

# Crea una instancia de Picamera2
picam2 = Picamera2()

# Crea una configuración para una captura de imagen fija
camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)})

# Configura la cámara con la configuración creada
picam2.configure(camera_config)

# Inicia la cámara
picam2.start()

# Espera un breve período para permitir que la cámara se ajuste
time.sleep(2)

# Captura la imagen y la guarda en un archivo
picam2.capture_file("test.jpg")

# Detiene la cámara después de la captura
picam2.stop()
