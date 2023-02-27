#from __future__ import print_function

import logging

import grpc
import iot_service_pb2
import iot_service_pb2_grpc

from const import *


def run():
    credentials = grpc.ssl_channel_credentials()
    auth_credentials = grpc.metadata_call_credentials(metadata_plugin)
    composite_credentials = grpc.composite_channel_credentials(credentials, auth_credentials)
    with grpc.insecure_channel(GRPC_SERVER+':'+GRPC_PORT, composite_credentials) as channel:
        
        metadata = (('username1', 'user1'), ('username2','user2'), ('password1', 'password1'), ('password2', 'password2'))
        context = grpc.metadata_call_context(metadata=metadata)

        stub = iot_service_pb2_grpc.IoTServiceStub(channel)
        response = stub.SayTemperature(iot_service_pb2.TemperatureRequest(sensorName='my_sensor'))

    print("Temperature received: " + response.temperature)

if __name__ == '__main__':
    logging.basicConfig()
    run()
