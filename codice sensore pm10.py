import serial
import time
import simple_colors
print("Lettura dati dalla porta: COM 4")

ser = serial.Serial(
    port='COM3' , #porta a cui si riferisce
    baudrate=9600, #numero porta
    timeout=2 #timeout per la lettura
)

#while True: #se verificato
    
while True:
    #print(data)
    rawdata = ser.readline()
    data = rawdata.decode().strip() #comando per far legger i dati dalla porta
    #print("RAW: " + data)
    value = 0

    try:
        #for part in rawdata:
            #print(int(part))
            value = int(rawdata[6])
            print("PM Value: " + str(value))
            break

    except:
        time.sleep(1200)

ser.close()

if value <= 25:
    print(simple_colors.green("Approvato dalla legge D.Lgs n°155"))
else:
    print(simple_colors.red("NON approvato dalla legge D.Lgs n°155"))


if value <= 20:
    print(simple_colors.green("Approvato dalla legge D.Lgs n°155"))
else:
    print(simple_colors.red("NON approvato dalla legge D.Lgs n°155"))


if value <= 15:
    print(simple_colors.green("Approvato dal OMS"))
else:
    print(simple_colors.red("NON approvato dal OMS"))


if value <= 5:
    print(simple_colors.green("Approvato dal OMS"))
else:
    print(simple_colors.red("NON approvato dal OMS"))