import logging

import grpc
import iot_service_pb2
import iot_service_pb2_grpc

from const import *

def get_temperatures(stub):
    temperatures = []
    for _ in range(5): # recebe as últimas 5 temperaturas
        response = stub.SayTemperature(iot_service_pb2.TemperatureRequest(sensorName='my_sensor'))
        temperature = float(response.temperature)
        temperatures.append(temperature)
    return temperatures

def calculate_avarage(temperatures):
    return sum(temperatures) / len(temperatures)

def run():
    with grpc.insecure_channel(GRPC_SERVER+':'+GRPC_PORT) as channel:
        stub = iot_service_pb2_grpc.IoTServiceStub(channel)
        temperatures = get_temperatures(stub)
        avarage_temperature = calculate_avarage(temperatures)
        print("avarage temperature: {:.2f}°C".format(avarage_temperature))

if __name__ == '__main__':
    logging.basicConfig()
    run()
