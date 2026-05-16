# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Proyecto

Sistema de auditoría de logs para XAMPP. Una página web estilo "please, don't touch anything" con 3 botones que generan logs de error, warning e info en el error.log de Apache. Un script watchdog (main.py) monitorea el archivo y envía las nuevas líneas a n8n vía webhook.

## Estructura de archivos

- `index.php` - Página principal con los 3 botones
- `style.css` - Estilos con efectos de hover/active y animación glitch
- `script.js` - Cliente que envía tipo de log a log.php via fetch
- `log.php` - Backend que escribe en el error.log de XAMPP
- `main.py` - Script watchdog que monitorea `C:\xampp\apache\logs\error.log` y envía a n8n

## Uso

1. **Página web**: Acceder a `http://localhost/error-log-test/`
2. **Botón ERROR** (rojo) - Genera log error en formato syslog
3. **Botón WARNING** (amarillo) - Genera log warning en formato syslog
4. **Botón INFO** (blanco) - Genera log info en formato syslog
5. **Botón NMAP SIMULADO** (verde黑客风) - Genera scan simulado con IP y puertos abiertos

## Script watchdog

```bash
python main.py
```

Monitorea `C:\xampp\apache\logs\error.log` y envía cada línea nueva a n8n en:
`http://localhost:5678/webhook-test/8dd2d54a-3de8-4904-a053-42e0bbb89cf7`

El payload incluye:
- `fecha_deteccion` - Timestamp del envío
- `log_raw` - Línea cruda del log
- `proyecto` - "Auditoria_Logs_XAMPP"

## Formato de logs

**Syslog estándar:**
```
May 16 12:30:45 xampp-server php[1234]: [error] IP: 127.0.0.1 Port: 54321 - Client error generated
```

**NMAP simulado:**
```
May 16 12:30:45 nmap-simulator nmap[9999]: [scan] IP: 192.168.1.42 Ports: 22,80,443,8080 Status: open - NMAP SIMULATED SCAN
```

El parser en `main.py` detecta automáticamente el tipo y extrae los campos correspondientes.

## Rutas importantes

- Error log XAMPP: `C:\xampp\apache\logs\error.log`
- Webhook n8n: `http://localhost:5678/webhook-test/8dd2d54a-3de8-4904-a053-42e0bbb89cf7`