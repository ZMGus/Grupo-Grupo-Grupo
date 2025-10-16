Primeramente correr en la terminal dentro de esta carpeta lo siguiente para utilizar ActiveMQ y MailHog:
docker compose up -d

luego debemos correr el programa en Python que será el encargado de escuchar las señales de Unity:
python email_consumer.py

Por último corremos el proyecto en Unity e intentamos salir de la casa o tocar las paredes y se enviará un "correo" MailHog el cual se puede ver en http://localhost:8025

(Para mover el círculo blanco se utiliza WASD)

Requisitos:
Tener docker instalado
Python y librería STOMP