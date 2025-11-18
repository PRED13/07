# Despliegue en Render

Este repositorio contiene una aplicación Django. Para desplegarla en Render se recomienda lo siguiente:

- Asegúrate de que `requirements.txt` esté actualizado.
- Usa el `Procfile` incluido para que Render (y otros PaaS) inicien Gunicorn con la aplicación WSGI correcta.

Start command recomendado (usado en `Procfile`):

```
web: gunicorn configuracion_web.wsgi:application --bind 0.0.0.0:$PORT
```

Opcional: el archivo `render.yaml` incluido define un servicio web que instala dependencias y ejecuta `collectstatic`.

Variables de entorno recomendadas en Render:
- `DJANGO_SETTINGS_MODULE=configuracion_web.settings`
- `SECRET_KEY` (no ponerlo en el repo)
- `DEBUG=False`
- Configurar `ALLOWED_HOSTS` o usar `ALLOWED_HOSTS=['*']` temporalmente

Comandos locales para probar Gunicorn antes de desplegar:

```bash
source venv/bin/activate
gunicorn configuracion_web.wsgi:application --bind 0.0.0.0:8000
```

Si quieres, puedo intentar hacer commit y push de estos cambios al remote `origin` por ti. Si el push falla por permisos, te indicaré los comandos para empujarlo desde tu máquina.
