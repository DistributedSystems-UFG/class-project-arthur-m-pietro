import logging
import time

import grpc
import iot_service_pb2
import iot_service_pb2_grpc

from const import *

def run():
    with grpc.insecure_channel(GRPC_SERVER+':'+GRPC_PORT) as channel:
        stub = iot_service_pb2_grpc.IoTServiceStub(channel)
        response = stub.SayTemperature(iot_service_pb2.TemperatureRequest(sensorName='my_sensor', username=username, password=password))
        return response.temperature
  

if __name__ == '__main__':
    logging.basicConfig()

    print("username: ")
    username = input()
    print("password: ")
    password = input()

    temperatures_array = []
    while True:
        # Média dos últimos 5 valores
        for i in range(5):
            temperatureStr = run()
            temperature = float(temperatureStr)
            temperatures_array.append(temperature)
            media = sum(temperatures_array) / len(temperatures_array)
            print("Temperatura média: " + str(round(media, 2)) + "ºC.")            
            time.sleep(1)