-------------------------------- IoT Sink Repository -------------------------------------

Este repositório hospeda todo código utilizado para a solução de persistencia de medidas IoT.
O dispositivos IoT conectados a uma instancia do  Amazon IoT Core  são processados por uma função Lambda.
As medições são armazenadas em um banco DynamoDB e com replicação em um Bucket S3.


O repositório é composto pelos seguintes arquivos :

-> AWS-IOTDevicesCreation.ps1 : Script da AWS CLI para criar 50 Things com certificados no IoT Core. 
-> IoT-message-charts.html : Página Web para visualizar medidas e metadados de alguns dispositivos salvos no DynamoDB
-> IoT-Simulator.py : Script em Python para simular o envio de mensagens de sensores para o IoT Core.
-> IoT-Sink-Lambda.js : Lambda em Javascript para monitorar novas mensagens no IoT Core e armazena-las no Bucket S3 e no DynamoDB.
