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

# Tableau de couleurs
colors = [
    (255, 0, 0),    # Rouge
    (0, 255, 0),    # Vert
    (0, 0, 255),    # Bleu
    (255, 255, 0),  # Jaune
    (0, 255, 255),  # Cyan
    (255, 0, 255),  # Magenta
    (255, 255, 255),# Blanc
    (128, 0, 128)   # Violet
]

# Index de la couleur actuelle
current_color_index = 0
current_pulse_color_index = 0

# Fonction pour définir la couleur de tous les pixels avec la couleur actuelle
def set_all_pixels(color):
    for i in range(28):
        pixels[i] = color
    pixels.write()

# Nouvelle fonction pour définir la couleur de tous les pixels en utilisant tour à tour les couleurs du tableau
def set_all_pixels_next_color():
    global current_color_index
    color = colors[current_color_index]
    set_all_pixels(color)
    current_color_index = (current_color_index + 1) % len(colors)

# Nouvelle fonction pour définir la couleur de pulsation en utilisant tour à tour les couleurs du tableau
def set_pulse_color_next():
    global current_pulse_color_index
    color = colors[current_pulse_color_index]
    set_all_pixels(color)
    current_pulse_color_index = (current_pulse_color_index + 1) % len(colors)

# Fonction pour générer un effet arc-en-ciel
def wheel(pos):
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)

def rainbow_cycle(wait):
    for j in range(256):
        for i in range(28):
            rc_index = (i * 256 // 28) + j
            pixels[i] = wheel(rc_index & 255)
        pixels.write()
        time.sleep(wait)

# Fonction pour générer un effet de pulsation
def pulse(color, wait):
    print(f"Début de la pulsation avec la couleur {color}")
    start_time = time.time()
    while True:
        if time.time() - start_time > 2:  # Arrêter après 2 secondes
            print("Fin de la pulsation")
            break
        
        for brightness in range(0, 256, 5):  # Augmenter la luminosité
            scaled_color = tuple(int(brightness / 255 * c) for c in color)
            set_all_pixels(scaled_color)
            print(f"Pulsation - Augmenter la luminosité: {brightness}, Couleur: {scaled_color}")
            time.sleep(wait)
            if any(touch_pad.read() < thresholds[i] for i, touch_pad in enumerate(touch_pads)):
                print("Interruption de la pulsation - Capteur tactile activé")
                return
        for brightness in range(255, -1, -5):  # Diminuer la luminosité
            scaled_color = tuple(int(brightness / 255 * c) for c in color)
            set_all_pixels(scaled_color)
            print(f"Pulsation - Diminuer la luminosité: {brightness}, Couleur: {scaled_color}")
            time.sleep(wait)
            if any(touch_pad.read() < thresholds[i] for i, touch_pad in enumerate(touch_pads)):
                print("Interruption de la pulsation - Capteur tactile activé")
                return

def Start():
    pulse((0, 0, 255), 0.05)  # Pulsation en Rouge
    time.sleep(0.1)
    pulse((255, 255, 255), 0.05)  # Pulsation en Blanc
    time.sleep(0.1)
    pulse((255, 0, 0), 0.05)  # Pulsation en Bleu
    time.sleep(0.1)
    
    set_all_pixels((0, 0, 0))  # Éteint
    time.sleep(0.1)

Start()

# Boucle principale
while True:
    # Lire les valeurs des capteurs tactiles
    touch_values = [touch_pad.read() for touch_pad in touch_pads]
    
    # Vérifier chaque capteur tactile
    for i, touch_value in enumerate(touch_values):
        if touch_value < thresholds[i]:
            if i == 0:
                # Si le capteur 1 est touché, changer la couleur et la définir
                set_all_pixels_next_color()
            elif i == 1:
                # Si le capteur 2 est touché, éteindre tous les pixels
                set_all_pixels((0, 0, 0))
            elif i == 2:
                # Si le capteur 3 est touché, activer l'effet arc-en-ciel
                rainbow_cycle(0.01)
            elif i == 3:
                # Si le capteur 4 est touché, changer la couleur de pulsation et l'activer
                set_pulse_color_next()
                pulse(colors[current_pulse_color_index], 0.05)  # Pulsation en couleur courante
                time.sleep(0.5)
    
    # Attendre un court instant avant de lire à nouveau les capteurs
    time.sleep(0.1)
