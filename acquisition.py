import time
import Adafruit_ADS1x15
import smbus
import Adafruit_DHT

# Définir le type de capteur (DHT11 ici) et le numéro de broche du Raspberry Pi sur lequel il est connecté
sensor = Adafruit_DHT.DHT11
pin = 4

# Définir l'adresse du capteur de lumière BH1750
DEVICE     = 0x23 # Default device I2C address
bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

# Définir les modes de mesure de la lumière
CONTINUOUS_HIGH_RES_MODE_1 = 0x10
ONE_TIME_HIGH_RES_MODE_1 = 0x20

# Fonction pour convertir les données du capteur de lumière en lux
def convertToNumber(data):
    result=(data[1] + (256 * data[0])) / 1.2
    return (result)

# Fonction pour lire les données du capteur de lumière
def readLight(addr=DEVICE):
    data = bus.read_i2c_block_data(addr,ONE_TIME_HIGH_RES_MODE_1)
    return convertToNumber(data)

# Créer un objet ADS1115
adc = Adafruit_ADS1x15.ADS1115()

# Paramètres du gain et du nombre de bits
GAIN = 1
BITS = 16

# Plage d'entrée (lecture brute de l'ADS1115)
entree_min = 32767
entree_max = 0

# Plage de sortie (humidité du sol)
sortie_min = 0
sortie_max = 100

while True:
    # Mesure de la température et de l'humidité
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    
    # Mesure de l'intensité lumineuse
    lightLevel = readLight()
    
    # Lecture de la valeur brute de l'ADS1115 pour le canal 0
    val = adc.read_adc(0, gain=GAIN, data_rate=BITS)

    # Calcul de la proportion de la valeur d'entrée dans la plage d'entrée
    proportion_entree = (val - entree_min) / (entree_max - entree_min)

    # Calcul de la valeur de sortie en appliquant la proportion à la plage de sortie
    humidite = round(sortie_min + proportion_entree * (sortie_max - sortie_min), 2)

    # Affichage des résultats
    print("Température: {:.1f}°C, Humidité: {:.1f}%, Niveau de lumière: {:.1f} lx, Humidité du sol : {} %".format(temperature, humidity, lightLevel, humidite))
    
    # Pause de 1 seconde entre chaque mesure
    time.sleep(1)

