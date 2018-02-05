#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import logging
import threading
import zmq


class ToroboArm(object):
    COMError = zmq.ZMQError
    NOBLOCK = zmq.NOBLOCK
    REQ = zmq.REQ
    SUB = zmq.SUB

    def __init__(self, port, socktype, debug):
        log_format = '%(asctime)s:%(levelname)s:ToroboArm: %(message)s'
        if debug:
            log_level = logging.DEBUG
        else:
            log_level = logging.INFO
        logging.basicConfig(format=log_format, level=log_level)

        logging.info("port: " + str(port))
        logging.info("type: " + str(socktype))
        logging.info("debug: " + str(debug))
        self._stub = False
        self._ctx = None
        self._sock = None
        self._port = port
        self._socktype = socktype
        self._start_event = threading.Event()
        self._stop_event = threading.Event()
        self._exit_event = threading.Event()
        self._lock = threading.Lock()
        self._thread = threading.Thread(target=self.run)
        self._thread.setDaemon(True)
        self._thread.start()

    def _init_communication(self):
        if not self._stub:
            # initialize ZMQ communication
            logging.debug("init communication")
            self._ctx = zmq.Context()

    def _exit_communication(self):
        if not self._stub:
            if self._ctx:
                # finalize ZMQ communication
                logging.debug("exit communication")
                self._ctx.term()

    def _open_socket(self):
        if not self._stub:
            if self._ctx:
                # open ZMQ socket
                logging.debug("open zmq socket")
                self._sock = self._ctx.socket(self._socktype)
                if self._socktype == self.SUB:
                    self._sock.setsockopt(zmq.SUBSCRIBE, b"ToroboArmManager")
                self._sock.setsockopt(zmq.LINGER, 0)
                self._sock.connect(self._port)
                self._poll = zmq.Poller()
                self._poll.register(self._sock, zmq.POLLIN)

    def _close_socket(self):
        if not self._stub:
            if self._ctx:
                # close ZMQ socket
                logging.debug("close zmq socket")
                self._poll.unregister(self._sock)
                self._sock.close()

    def _process(self):
        pass

    def _process_stub(self):
        pass

    def run(self):
        while not self._exit_event.is_set():
            # stop processing
            if self._stop_event.is_set():
                logging.debug("run-thread detects stop event")
                self._exit_communication()
                self._stop_event.clear()

            # start processing
            elif self._start_event.is_set():
                logging.debug("run-thread detects start event")
                self._init_communication()
                self._start_event.clear()

            # processing
            elif self._ctx and not self._ctx.closed:
                if self._stub:
                    sleep = self._process_stub()
                else:
                    sleep = self._process()
                time.sleep(sleep)
            else:
                # wait until start communication
                self._start_event.wait(1)

        logging.debug("run-thread exit")

    def start(self):
        logging.debug("set start event")
        self._start_event.set()
        return True

    def stop(self):
        logging.debug("set stop event")
        self._stop_event.set()
        return True

    def exit(self):
        logging.debug("set exit event")
        self._exit_event.set()
        self._thread.join()
        return True

    @property
    def stub(self):
        logging.debug("stub mode = " + str(self._stub))
        return self._stub

    @stub.setter
    def stub(self, value):
        logging.debug("set stub mode = " + str(value))
        self._stub = value
        return True


if __name__ == '__main__':
    t = ToroboArm('tcp://localhost:5555', True)
    t.start()
    time.sleep(0.1)
    t.start()
    time.sleep(0.1)
    t.stub = True
    time.sleep(0.1)
    t.stub = False
    time.sleep(0.1)
    t.start()
    time.sleep(0.1)
    t.stop()
    time.sleep(0.1)
    t.stop()
    time.sleep(0.1)
    t.exit()
    time.sleep(0.1)
    t.exit()
    t.stub
