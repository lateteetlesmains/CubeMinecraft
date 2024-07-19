import machine
import neopixel
import time
from machine import TouchPad, Pin

# Initialiser les NeoPixels sur la broche 5 avec 28 LEDs
pixels = neopixel.NeoPixel(machine.Pin(5), 28)

# Initialiser les capteurs tactiles sur les broches 13, 15, 2 et 0
touch_pins = [13, 15, 2, 0]
touch_pads = [TouchPad(Pin(pin)) for pin in touch_pins]

# Fonction pour obtenir la valeur moyenne de base pour chaque capteur
def calibrate_touch_pad(touch_pad, samples=100):
    total = 0
    for _ in range(samples):
        total += touch_pad.read()
        time.sleep(0.01)  # Attendre un court instant entre les lectures
    return total // samples

# Calibrer les capteurs tactiles
base_values = [calibrate_touch_pad(touch_pad) for touch_pad in touch_pads]
thresholds = [base_value * 0.8 for base_value in base_values]

print("Valeurs de base : ", base_values)
print("Seuils : ", thresholds)

# Fonction pour définir la couleur de tous les pixels
def set_all_pixels(color):
    for i in range(28):
        pixels[i] = color
    pixels.write()

def Start():
    set_all_pixels((0, 0, 255))  # Bleu
    time.sleep(0.5)
    
    set_all_pixels((255, 255, 255))  # Blanc
    time.sleep(0.5)
    
    set_all_pixels((255, 0, 0))  # Rouge
    time.sleep(0.5)
    
    set_all_pixels((0, 0, 0))  # Éteint
    time.sleep(0.5)

Start()
# Boucle principale
while True:
    # Lire les valeurs des capteurs tactiles
    touch_values = [touch_pad.read() for touch_pad in touch_pads]
    
    # Vérifier chaque capteur tactile
    for i, touch_value in enumerate(touch_values):
        if touch_value < thresholds[i]:
            if i == 0:
                # Si le capteur 1 est touché, mettre tous les pixels en bleu
                set_all_pixels((0, 0, 255))
            elif i == 1:
                # Si le capteur 2 est touché, mettre tous les pixels en blanc
                set_all_pixels((255, 255, 255))
            elif i == 2:
                # Si le capteur 3 est touché, mettre tous les pixels en rouge
                set_all_pixels((255, 0, 0))
            elif i == 3:
                # Si le capteur 4 est touché, éteindre tous les pixels
                set_all_pixels((0, 0, 0))
    
    # Attendre un court instant avant de lire à nouveau les capteurs
    time.sleep(0.1)
