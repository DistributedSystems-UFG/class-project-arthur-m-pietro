#from __future__ import print_function

import logging
import time

import grpc
import iot_service_pb2
import iot_service_pb2_grpc

from const import *

def run():
    print("username: ")
    username = input()
    print("password: ")
    password = input()

    metadata = {'username': username}, password


    with grpc.insecure_channel(GRPC_SERVER+':'+GRPC_PORT) as channel:
        stub = iot_service_pb2_grpc.IoTServiceStub(channel)
        response = stub.SayTemperature(iot_service_pb2.TemperatureRequest(sensorName='my_sensor'), metadata=metadata)

    print("Temperatura atual: " + str(round(float(response.temperature), 2)) + "ºC.")

if __name__ == '__main__':
    logging.basicConfig()
    while True:
        run()
        time.sleep(1)