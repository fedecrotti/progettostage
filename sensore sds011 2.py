import serial

# Configura la porta seriale
ser = serial.Serial('/dev/ttyUSB0', 9600)

# Invia il comando di attivazione del sensore
ser.write(bytes([0xAA, 0xB4, 0x06, 0x01, 0x01, 0x00, 0x1F, 0xA5]))

while True:
    # Leggi i dati dal sensore
    data = ser.read(10)
    
    # Verifica se la risposta è valida
    if data[0] == 0xAA and data[1] == 0xC0:
        # Calcola i valori PM2.5 e PM10
        pm25 = (data[3] * 256 + data[2]) / 10.0
        pm10 = (data[5] * 256 + data[4]) / 10.0
        
        # Stampa i valori
        print(f"PM2.5: {pm25} μg/m³")
        print(f"PM10: {pm10} μg/m³")