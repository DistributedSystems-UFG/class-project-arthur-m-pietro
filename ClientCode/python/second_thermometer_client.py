import logging

import grpc
import iot_service_pb2
import iot_service_pb2_grpc

from const import *




def run():
    with grpc.insecure_channel(GRPC_SERVER+':'+GRPC_PORT) as channel:
        stub = iot_service_pb2_grpc.IoTServiceStub(channel)
        temperatures = []

        avarage = NULL;

        for _ in range(5): # recebe as últimas 5 temperaturas
            response = stub.SayTemperature(iot_service_pb2.TemperatureRequest(sensorName='my_sensor'))
            temperature = float(response.temperature)
            temperatures.append(temperature)
            avarage = sum(temperatures) / len(temperatures);

        print("avarage temperature: {:.2f}°C".format(avarage))

if __name__ == '__main__':
    logging.basicConfig()
    run()
