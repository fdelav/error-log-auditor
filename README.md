# Auditoría de Logs para XAMPP

Sistema de monitoreo que genera logs de error/warning/info en Apache y los envía a n8n vía webhook.

## Requisitos

- XAMPP instalado (con Apache)
- Docker Desktop
- Python 3.x

## Instalación

### 1. Copiar al htdocs de XAMPP

Copiar la carpeta `error-log-test` en la ruta htdocs de XAMPP:

```bash
C:\xampp\htdocs\error-log-test\
```

### 2. Iniciar n8n con Docker

Ejecutar el contenedor latest de n8n:

```bash
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -v n8n_data:/home/node/.n8n \
  docker.n8n.io/n8nio/n8n:latest
```

Esperar a que n8n esté disponible en http://localhost:5678

### 3. Importar proyecto en n8n

1. Acceder a http://localhost:5678
2. Crear una cuenta o iniciar sesión
3. Ir a **Settings > Credentials** o importar el workflow manualmente
4. Crear un webhook con la URL: `http://localhost:5678/webhook-test/8dd2d54a-3de8-4904-a053-42e0bbb89cf7`
5. Activar el webhook para recibir POST requests

### 4. Ejecutar el script watchdog

Desde la carpeta del proyecto:

```bash
python main.py
```

El script monitoreará `C:\xampp\apache\logs\error.log` y enviará cada línea nueva a n8n.

## Uso

1. Abrir http://localhost/error-log-test/ en el navegador
2. Hacer clic en los botones para generar logs:
   - **ERROR** (rojo) - Genera log de error
   - **WARNING** (amarillo) - Genera log de warning
   - **INFO** (blanco) - Genera log de info
   - **NMAP SIMULADO** (verde) - Genera scan simulado

Los logs aparecerán en el archivo `C:\xampp\apache\logs\error.log` y el script watchdog los enviará automáticamente al webhook de n8n.

## Rutas importantes

| Componente | Ruta |
|------------|------|
| Error log XAMPP | `C:\xampp\apache\logs\error.log` |
| Web n8n | http://localhost:5678 |
| Webhook n8n | http://localhost:5678/webhook-test/8dd2d54a-3de8-4904-a053-42e0bbb89cf7 |