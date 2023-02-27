from kafka import KafkaConsumer, KafkaProducer
from const import *
import threading
from concurrent import futures
from grpc import (
    ServerInterceptor,
    ServerCallContext,
    ServerCredentials,
    secure_channel_credentials,
)
import logging

import grpc
import iot_service_pb2
import iot_service_pb2_grpc

class AuthInterceptor(ServerInterceptor):
    def __init__(self, users):
        self.users = users

    def intercept_service(self, continuation, handler_call_details):
        meta = dict(handler_call_details.invocation_metadata)
        user = meta.get('user', None)
        password = meta.get('password', None)

        if user and password and self.users.get(user) == password:
            return continuation(handler_call_details)
        else:
            context = handler_call_details.context
            context.abort(
                grpc.StatusCode.UNAUTHENTICATED,
                'Invalid credentials'
            )

# Dicionário de usuários e senhas
USERS = {
    'user1': 'password1',
    'user2': 'password2',
}

# Twin state
current_temperature = 'void'
led_state = {'red':0, 'green':0}

# Kafka consumer to run on a separate thread
def consume_temperature():
    global current_temperature
    consumer = KafkaConsumer(bootstrap_servers=KAFKA_SERVER+':'+KAFKA_PORT)
    consumer.subscribe(topics=('temperature'))
    for msg in consumer:
        print (msg.value.decode())
        current_temperature = msg.value.decode()

def produce_led_command(state, ledname):
    producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER+':'+KAFKA_PORT)
    producer.send('ledcommand', key=ledname.encode(), value=str(state).encode())
    return state
        
class IoTServer(iot_service_pb2_grpc.IoTServiceServicer):

    def SayTemperature(self, request, context):
        return iot_service_pb2.TemperatureReply(temperature=current_temperature)
    
    def BlinkLed(self, request, context):
        print ("Blink led ", request.ledname)
        print ("...with state ", request.state)
        produce_led_command(request.state, request.ledname)
        # Update led state of twin
        led_state[request.ledname] = request.state
        return iot_service_pb2.LedReply(ledstate=led_state)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    iot_service_pb2_grpc.add_IoTServiceServicer_to_server(IoTServer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    trd = threading.Thread(target=consume_temperature)
    trd.start()
    # Initialize the state of the leds on the actual device
    for color in led_state.keys():
        produce_led_command (led_state[color], color)
    serve()
