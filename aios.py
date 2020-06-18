# udp_gb_server.py
'''服务端（UDP协议局域网广播）'''
import threading
import socket
import time
import json
from enum import Enum


class AxisState(Enum):
        AXIS_STATE_UNDEFINED = 0
        AXIS_STATE_IDLE = 1
        AXIS_STATE_STARTUP_SEQUENCE = 2
        AXIS_STATE_FULL_CALIBRATION_SEQUENCE = 3
        AXIS_STATE_MOTOR_CALIBRATION = 4
        AXIS_STATE_SENSORLESS_CONTROL = 5
        AXIS_STATE_ENCODER_INDEX_SEARCH = 6
        AXIS_STATE_ENCODER_OFFSET_CALIBRATION = 7
        AXIS_STATE_CLOSED_LOOP_CONTROL = 8

class ControlMode(Enum):
        CTRL_MODE_VOLTAGE_CONTROL = 0
        CTRL_MODE_CURRENT_CONTROL = 1
        CTRL_MODE_VELOCITY_CONTROL = 2
        CTRL_MODE_POSITION_CONTROL = 3
        CTRL_MODE_TRAJECTORY_CONTROL = 4

start_time = 0
stop_time = 0





s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(3.0)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

PORT_rt = 2333
PORT_srv = 2334

Server_IP_1 = '192.168.1.118'
Server_IP_2 = '192.168.1.149'

# s.bind(('', PORT_srv))

network = '<broadcast>'

print('Listening for broadcast at ', s.getsockname())

def AIOSEnable(server_ip):
    data = {
        'method' : 'SET',
        'reqTarget' : '/m1/requested_state',
        'property' : AxisState.AXIS_STATE_CLOSED_LOOP_CONTROL.value
    }
    json_str = json.dumps(data)
    print ("Send JSON Obj:", json_str)
    s.sendto(str.encode(json_str), (server_ip, PORT_srv))
    try:
        data, address = s.recvfrom(1024)
        print('Server received from {}:{}'.format(address, data.decode('utf-8')))
        json_obj = json.loads(data)
    except socket.timeout: # fail after 1 second of no activity
        print("Didn't receive anymore data! [Timeout]")

    if (json_obj.get('status') == 'OK' and json_obj.get('reqTarget') == '/m1/requested_state'):
        return json_obj.get('property')
    else:
        print("Recv Data Error !")

def AIOSDisable(server_ip):
    data = {
        'method' : 'SET',
        'reqTarget' : '/m1/requested_state',
        'property' : AxisState.AXIS_STATE_IDLE.value
    }
    json_str = json.dumps(data)
    print ("Send JSON Obj:", json_str)
    s.sendto(str.encode(json_str), (server_ip, PORT_srv))

    try:
        data, address = s.recvfrom(1024)
        print('Server received from {}:{}'.format(address, data.decode('utf-8')))
        json_obj = json.loads(data)
    except socket.timeout: # fail after 1 second of no activity
        print("Didn't receive anymore data! [Timeout]")

def AIOSGetRoot(server_ip):
    data = {
        'method' : 'GET',
        'reqTarget' : '/',
    }
    json_str = json.dumps(data)
    print ("Send JSON Obj:", json_str)
    s.sendto(str.encode(json_str), (server_ip, PORT_srv))
    try:
        data, address = s.recvfrom(1024)
        print('Server received from {}:{}'.format(address, data.decode('utf-8')))
        json_obj = json.loads(data)
    except socket.timeout: # fail after 1 second of no activity
        print("Didn't receive anymore data! [Timeout]")

def getCVP(server_ip):
    data = {
        'method' : 'GET',
        'reqTarget' : '/m1/CVP',
    }
    json_str = json.dumps(data)
    # print ("Send JSON Obj:", json_str)
    s.sendto(str.encode(json_str), (server_ip, PORT_rt))
    try:
        data, address = s.recvfrom(1024)
        # print('Server received from {}:{}'.format(address, data.decode('utf-8')))
        json_obj = json.loads(data)
        if (json_obj.get('status') == 'OK' and json_obj.get('reqTarget') == '/m1/CVP'):
            print("Position = %.2f, Velocity = %.0f, Current = %.4f" %(json_obj.get('position'), json_obj.get('velocity'), json_obj.get('current')))
    except socket.timeout: # fail after 1 second of no activity
        print("Didn't receive anymore data! [Timeout]")

def EncoderOffsetCalibration(server_ip):
    data = {
        'method' : 'SET',
        'reqTarget' : '/m1/requested_state',
        'property' : AxisState.AXIS_STATE_ENCODER_OFFSET_CALIBRATION.value
    }
    json_str = json.dumps(data)
    print ("Send JSON Obj:", json_str)
    s.sendto(str.encode(json_str), (server_ip, PORT_srv))
    try:
        data, address = s.recvfrom(1024)
        print('Server received from {}:{}'.format(address, data.decode('utf-8')))
        json_obj = json.loads(data)
    except socket.timeout: # fail after 1 second of no activity
        print("Didn't receive anymore data! [Timeout]")

def EncoderIsReady(server_ip):
    data = {
        'method' : 'GET',
        'reqTarget' : '/m1/encoder/is_ready',
    }
    json_str = json.dumps(data)
    print ("Send JSON Obj:", json_str)
    s.sendto(str.encode(json_str), (server_ip, PORT_srv))
    try:
        data, address = s.recvfrom(1024)
        print('Server received from {}:{}'.format(address, data.decode('utf-8')))
        json_obj = json.loads(data)
    except socket.timeout: # fail after 1 second of no activity
        print("Didn't receive data! [Timeout]")

    if (json_obj.get('status') == 'OK' and json_obj.get('reqTarget') == '/m1/encoder/is_ready'):
        return json_obj.get('property')
    else:
        print("Recv Data Error !")

def ControlMode(server_ip, ctrlMode):
    data = {
        'method' : 'SET',
        'reqTarget' : '/m1/controller/config/control_mode',
        'property' : 2
    }
    data['property'] = ctrlMode
    json_str = json.dumps(data)
    print ("Send JSON Obj:", json_str)
    s.sendto(str.encode(json_str), (server_ip, PORT_srv))
    try:
        data, address = s.recvfrom(1024)
        print('Server received from {}:{}'.format(address, data.decode('utf-8')))
        json_obj = json.loads(data)
    except socket.timeout: # fail after 1 second of no activity
        print("Didn't receive anymore data! [Timeout]")

def vel_ramp_enable(server_ip, enable):
    data = {
        'method' : 'SET',
        'reqTarget' : '/m1/controller/config/vel_ramp_enable',
        'property' : False
    }
    data['property'] = enable
    json_str = json.dumps(data)
    print ("Send JSON Obj:", json_str)
    s.sendto(str.encode(json_str), (server_ip, PORT_srv))
    try:
        data, address = s.recvfrom(1024)
        print('Server received from {}:{}'.format(address, data.decode('utf-8')))
        json_obj = json.loads(data)
    except socket.timeout: # fail after 1 second of no activity
        print("Didn't receive anymore data! [Timeout]")

def vel_ramp_target(server_ip, target):
    data = {
        'method' : 'SET',
        'reqTarget' : '/m1/controller/vel_ramp_target',
        'property' : 0
    }
    data['property'] = target
    json_str = json.dumps(data)
    print ("Send JSON Obj:", json_str)
    s.sendto(str.encode(json_str), (server_ip, PORT_rt))
    try:
        data, address = s.recvfrom(1024)
        print('Server received from {}:{}'.format(address, data.decode('utf-8')))
        json_obj = json.loads(data)
    except socket.timeout: # fail after 1 second of no activity
        print("Didn't receive anymore data! [Timeout]")


def trapezoidalMove(position, server_ip):
    start = time.time()
    data = {
        'method' : 'SET',
        'reqTarget' : '/m1/trapezoidalMove',
        'property' : 0
    }
    data['property'] = position
    json_str = json.dumps(data)
    print ("Send JSON Obj:", json_str)
    s.sendto(str.encode(json_str), (server_ip, PORT_rt))
    try:
        data, address = s.recvfrom(1024)

        print('Server received from {}:{}'.format(address, data.decode('utf-8')))
        json_obj = json.loads(data)
    except socket.timeout: # fail after 1 second of no activity
        print("Didn't receive anymore data! [Timeout]")
    print(time.time() - start)

def trapezoidalMove_multiple(position):
    trapezoidalMove(position, Server_IP_1)
    # trapezoidalMove(position, Server_IP_2)


def broadcast_func():
    timeout = 2

    s.sendto('Client broadcast message!'.encode('utf-8'), (network, PORT_srv))
    print('\n')

    start = time.time();
    while True:
        try:
            data, address = s.recvfrom(1024)
            print('Server received from {}:{}'.format(address, data.decode('utf-8')))
            json_obj = json.loads(data)
        except socket.timeout: # fail after 1 second of no activity
            print("Didn't receive anymore data! [Timeout]")
            break

    print('\n')
    print('lookuping Finished! \n')

# # 为线程定义一个函数
# def recv_func():





def send_func():
    global lookup_finished
    global motion_finished
    global start_time
    global stop_time

    broadcast_func()

    if (not EncoderIsReady(Server_IP_1)):
        EncoderOffsetCalibration(Server_IP_1)
        time.sleep(10)
    else:
        AIOSGetRoot(Server_IP_1)
        # AIOSGetRoot(Server_IP_2)
        time.sleep( 1 )

        for i in range(1000):
            getCVP(Server_IP_1)
            time.sleep(0.01)

        AIOSEnable(Server_IP_1)
        # AIOSEnable(Server_IP_2)
        time.sleep( 1 )

        # ControlMode(Server_IP_1, 2)
        # time.sleep( 1 )
        # vel_ramp_enable(Server_IP_1, True)
        # time.sleep( 1 )
        # vel_ramp_target(Server_IP_1, 10000)
        # time.sleep( 2 )
        # vel_ramp_target(Server_IP_1, 20000)
        # time.sleep( 2 )
        # vel_ramp_target(Server_IP_1, 40000)
        # time.sleep( 2 )
        # vel_ramp_target(Server_IP_1, 60000)
        # time.sleep( 2 )
        # vel_ramp_target(Server_IP_1, 80000)
        # time.sleep( 2 )
        # vel_ramp_target(Server_IP_1, 120000)
        # time.sleep( 10 )
        # vel_ramp_target(Server_IP_1, 0)
        # time.sleep( 1 )
        trapezoidalMove_multiple(0)
        time.sleep( 2 )

        trapezoidalMove_multiple(1000)
        time.sleep( 0.3 )
        trapezoidalMove_multiple(2000)
        time.sleep( 0.3 )
        # print (stop_time - start_time)
        trapezoidalMove_multiple(3000)
        time.sleep( 0.3 )
        trapezoidalMove_multiple(5000)
        time.sleep( 0.6 )
        trapezoidalMove_multiple(2000)
        time.sleep( 0.6 )
        trapezoidalMove_multiple(6000)
        time.sleep( 0.6 )

        trapezoidalMove_multiple(10000)
        time.sleep( 1 )
        trapezoidalMove_multiple(0)
        time.sleep( 1 )
        trapezoidalMove_multiple(5000)
        time.sleep( 1 )
        trapezoidalMove_multiple(-10000)
        time.sleep( 2 )
        trapezoidalMove_multiple(15000)
        time.sleep( 2 )
        trapezoidalMove_multiple(20000)
        time.sleep( 2 )

        AIOSDisable(Server_IP_1)
        # AIOSDisable(Server_IP_2)



def main():
    # t1 = threading.Thread(target=broadcast_func)   # 定义线程
    # t2 = threading.Thread(target=recv_func)
    t3 = threading.Thread(target=send_func)
    # t1.start()  # 让线程开始工作
    # t2.start()
    t3.start()
    # t1.join()
    # t2.join()
    t3.join()





if __name__ == '__main__':
    main()
