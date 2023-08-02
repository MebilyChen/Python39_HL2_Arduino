import socket
import os
from datetime import datetime
import serial
import serial.tools.list_ports
from threading import Thread, current_thread

text = ''

# SPP - Arduino
# get serialport list


# 关闭连接
# client_socket.close()
# server_socket.close()

if __name__ == "__main__":
    save_folder = './received_data'
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
        print("创建文件夹")
    current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = os.path.join(save_folder, f'received_data_{current_time}.csv')
    with open(filename, 'w', encoding='gbk') as f:
        f.write('time,connetion,conection_data,Is_heart_beat,heart_rate,Is_beat_span,beat_span,Is_Valid\n')

    port_list = list(serial.tools.list_ports.comports())
    print(port_list)
    if len(port_list) == 0:
        print('none')
    else:
        for i in range(0, len(port_list)):
            print(port_list[i])
    # set serialport parameters
    portName = "COM5"
    baudRate = 115200
    timeOut = 3
    ser = serial.Serial(portName, baudRate, timeout=timeOut)
    print('Arduino已连接！')

    while 1:
        if ser.isOpen():
            time_stamp = datetime.now().strftime('%H:%M:%S:%f')
            readIn_Arduino = time_stamp + ',' + str(ser.readline())
            readIn_Arduino = readIn_Arduino.replace("'", '')
            readIn_Arduino = readIn_Arduino.replace('b', '')
            readIn_Arduino = readIn_Arduino.replace('\\n', '')
            readIn_Arduino = readIn_Arduino.replace('\\t', ',')
            readIn_Arduino = readIn_Arduino.replace('\\r', '')
            readIn_Arduino = readIn_Arduino.replace('S', 'True')
            readIn_Arduino = readIn_Arduino.replace('Q', 'True')
            readIn_Arduino = readIn_Arduino.replace('Null', 'False')
            readIn_Arduino += '\n'
            print(readIn_Arduino)
            # ser.close()
            # print("开始保存文件")
            # 将接收到的图片保存到指定文件夹中
            with open(filename, 'a', encoding='gbk') as f:
                f.write(readIn_Arduino)
            print(f'Saved received data to {filename}')
