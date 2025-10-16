Instrucciones de ejecución
1. Iniciar servicios con Docker

Dentro de esta carpeta, abre una terminal y ejecuta el siguiente comando para levantar los servicios de ActiveMQ y MailHog:

docker compose up -d

2. Ejecutar el consumidor de correos en Python

Luego, corre el programa que se encargará de escuchar las señales enviadas desde Unity:

python email_consumer.py

3. Ejecutar el proyecto en Unity

Finalmente, abre y ejecuta el proyecto en Unity.
Al intentar salir de la casa o tocar las paredes, se enviará un “correo” a MailHog, el cual puedes visualizar ingresando a:

http://localhost:8025

Para mover el círculo blanco dentro del juego utiliza las teclas W, A, S y D.