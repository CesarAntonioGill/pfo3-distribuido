# 🧠 PFO3 – Rediseño como Sistema Distribuido (Cliente-Servidor)

## 🎯 Objetivo
El objetivo de este trabajo práctico es **transformar un sistema en una arquitectura distribuida** utilizando comunicación mediante **sockets** en Python, e integrando componentes reales de infraestructura como **RabbitMQ**, **PostgreSQL** y **MinIO (S3)**.

---

## 🧱 Arquitectura general

El sistema se basa en una arquitectura **cliente-servidor distribuida**, donde:

- Los **clientes** (móvil o web) envían tareas al servidor principal.
- El **balanceador de carga** (simulado con Nginx/HAProxy) distribuye las solicitudes entre varios **servidores workers**.
- Cada worker ejecuta las tareas usando **hilos (ThreadPoolExecutor)**.
- Los resultados o mensajes entre servidores se coordinan mediante **RabbitMQ**.
- Los datos persistentes se almacenan en **PostgreSQL**.
- Los archivos o resultados pesados se guardan en **MinIO (compatible con S3)**.

📄 Diagrama general (en PDF):  
➡️ [📘 Diagrama.pdf](Diagrama.pdf)

---

## 🧩 Diagrama del sistema (PlantUML)

```plantuml
@startuml
skinparam backgroundColor #FFFFFF
skinparam componentStyle rectangle
skinparam shadowing false

actor "Cliente Web" as Web
actor "Cliente Móvil" as Movil

node "Balanceador de Carga\n(Nginx / HAProxy)" as LB {
}

node "Servidores Workers" {
    [Worker 1\n(Pool de hilos)]
    [Worker 2\n(Pool de hilos)]
    [Worker 3\n(Pool de hilos)]
}

queue "Cola de Mensajes\n(RabbitMQ)" as MQ
database "PostgreSQL" as DB
cloud "MinIO / S3\nAlmacenamiento distribuido" as S3

Web --> LB
Movil --> LB
LB --> [Worker 1\n(Pool de hilos)]
LB --> [Worker 2\n(Pool de hilos)]
LB --> [Worker 3\n(Pool de hilos)]
[Worker 1\n(Pool de hilos)] --> MQ
[Worker 2\n(Pool de hilos)] --> MQ
[Worker 3\n(Pool de hilos)] --> MQ
MQ --> DB
MQ --> S3

@enduml

Estructura del proyecto

pfo3-distribuido/
├── server/
│   ├── server.py
│   ├── requirements.txt
│   └── venv/
├── client/
│   ├── client.py
│   ├── requirements.txt
├── docker-compose.yml
└── Diagrama.pdf

🐍 Ejecución del sistema
1️⃣ Configurar entorno del servidor
cd $env:USERPROFILE\Desktop\pfo3-distribuido\server
python -m venv venv
.\venv\Scripts\Activate
pip install -r requirements.txt
python server.py

Verás:
[SERVER] Escuchando en 0.0.0.0:5000

2️⃣ Ejecutar el cliente

Abrí otra ventana de PowerShell:
cd $env:USERPROFILE\Desktop\pfo3-distribuido\client
python client.py

Resultado esperado:
Resultado recibido: {'id': 1, 'status': 'ok', 'input': {'id': 1, 'action': 'saludo', 'data': 'Antonio'}, 'output': 'Resultado de saludo'}

Servicios distribuidos con Docker

Para levantar la infraestructura simulada:
cd $env:USERPROFILE\Desktop\pfo3-distribuido
docker compose up -d
docker compose ps

Servicios disponibles:

Servicio	Puerto	Usuario	Contraseña
RabbitMQ UI	http://localhost:15672
	user	pass
PostgreSQL	5432	pguser	pgpass
MinIO UI	http://localhost:9001
	minio	minio123
