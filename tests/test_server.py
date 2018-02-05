import time
import threading
import json
import zmq

import sensor_data


def receiver():
    ctx = zmq.Context()
    sock = ctx.socket(zmq.REP)
    sock.bind("tcp://127.0.0.1:5555")

    while True:
        msg = sock.recv()
        print(msg)
        sock.send("")
        time.sleep(0.1)


def sender():
    ctx = zmq.Context()
    sock = ctx.socket(zmq.PUB)
    sock.bind("tcp://127.0.0.1:5554")

    while True:
        msg = [b"ToroboArmManager", json.dumps(sensor_data.data)]
        sock.send_multipart(msg)
        time.sleep(0.1)


def main():
    send_thread = threading.Thread(target=sender)
    recv_thread = threading.Thread(target=receiver)
    send_thread.setDaemon(True)
    recv_thread.setDaemon(True)
    send_thread.start()
    recv_thread.start()

    while True:
        pass


if __name__ == '__main__':
    main()
