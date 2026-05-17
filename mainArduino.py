import serial,time
import main1
ser = serial.Serial(port='COM4', baudrate=9600) # відкрити порт COM
print(ser.portstr) # перевірити чи порт використовується

angles=[]
for x in range(360):
    ser.write(b"1"+b"\n") # послати дані на COM
    time.sleep(0.1) # чекати
    angles.append(main1.detect())
    print(x)

ser.close() # закрити порт
main1.cap.release()