Primeramente correr en la terminal dentro de esta carpeta lo siguiente para utilizar ActiveMQ y MailHog:
docker compose up -d

luego debemos correr los brokers que recibiran en cadena las señales de Unity:
python forwarder.py
python consumer_b.py
python email_consumer.py

Por último corremos el proyecto en Unity y nos movemos por la habitación y cada 10 segundos se enviará un "correo" MailHog el cual se puede ver en http://localhost:8025

(Para mover el círculo blanco se utiliza WASD)

Requisitos:
Tener docker instalado
Python y librería STOMP