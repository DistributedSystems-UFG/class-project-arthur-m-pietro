import logging
import time

import grpc
import iot_service_pb2
import iot_service_pb2_grpc

from const import *

def run():
    with grpc.insecure_channel(GRPC_SERVER+':'+GRPC_PORT) as channel:
        stub = iot_service_pb2_grpc.IoTServiceStub(channel)
        response = stub.SayTemperature(iot_service_pb2.TemperatureRequest(sensorName='my_sensor'))
        return response.temperature
  

if __name__ == '__main__':
    logging.basicConfig()

    temperatures_array = []
    while True:
        for i in range(5):
            temperature = run()
            temperatures_array.append(temperature)
            print(type(temperature))
            print("Temperatura média: {:.2f}ºC." )            
            time.sleep(1)