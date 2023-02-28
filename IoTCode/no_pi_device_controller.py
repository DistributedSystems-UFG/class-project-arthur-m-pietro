import random
import time
from kafka import KafkaProducer
from const import *

producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER+':'+KAFKA_PORT)

while True:
    # Gerar temperatura aleatória entre 0 e 100 graus Celsius
    temp_c = random.uniform(0, 100)
    print('Temperature generated: {:.2f}°C'.format(temp_c))

    # Enviar temperatura para o servidor Kafka
    producer.send('temperature', str(temp_c).encode())

    # Aguardar um tempo aleatório entre 1 e 5 segundos antes de gerar a próxima temperatura
    time.sleep(1)
