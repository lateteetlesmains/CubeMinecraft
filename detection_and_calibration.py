from machine import Pin, TouchPad
import time

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

# Boucle pour lire les valeurs des capteurs tactiles
while True:
    touch_values = [touch_pad.read() for touch_pad in touch_pads]
    print("Valeurs actuelles : ", touch_values)
    
    for i, touch_value in enumerate(touch_values):
        if touch_value < thresholds[i]:
            print(f"Touch detected on pin {touch_pins[i]}!")
        else:
            print(f"No touch detected on pin {touch_pins[i]}.")
    
    time.sleep(0.1)  # Attendre un court instant entre les lectures
