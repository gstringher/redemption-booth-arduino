# https://forum.arduino.cc/t/two-ways-communication-between-python3-and-arduino/1219738

import serial
import serial.tools.list_ports
ports = serial.tools.list_ports.comports()

print("Elenco completo")
for index, value in enumerate(sorted(ports)):
    print(index, '\t', value.name, '\t', value.manufacturer)

print("\n\nCandidati migliori")
for port in ports:
    if "usb" in port.name.lower():
        print(index, '\t', port.name, '\t', port.manufacturer)