import grpc
from const import *
from concurrent import futures
from iot_service_pb2_grpc import IoTServiceStub
from iot_service_pb2 import LedCommand, TemperatureRequest

def run():
    with grpc.secure_channel('localhost:50051', credentials=grpc.ssl_channel_credentials()) as channel:
        stub = IoTServiceStub(channel)
        # Adiciona as credenciais ao cabeçalho das requisições
        metadata = [('user', 'user1'), ('password', 'password1')]
        response = stub.SayTemperature(TemperatureRequest(), metadata=metadata)
        print("Temperature: {}".format(response.temperature))
        # Adiciona as credenciais ao cabeçalho das requisições
        metadata = [('user', 'user2'), ('password', 'password2')]
        response = stub.BlinkLed(LedCommand(ledname='red', state=True), metadata=metadata)
        print("LED state: {}".format(response.ledstate))

if __name__ == '__main__':
    run()
