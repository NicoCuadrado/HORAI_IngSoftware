Proyecto HORAI - instrucciones para crear un entorno virtual (Windows / PowerShell)

Estos pasos te guiarán para crear un entorno virtual, activarlo, instalar dependencias desde `requirements.txt` e iniciar la aplicación FastAPI con `uvicorn`.

1) Abrir PowerShell en la carpeta del proyecto

   cd C:\Users\cuadr\Desktop\horai\horai

2) Crear el entorno virtual (usar `.venv` o `venv`)

   python -m venv .venv

3) Activar el entorno virtual (PowerShell)

   .\.venv\Scripts\Activate.ps1

   Si recibes un error de ejecución de scripts, ejecuta en PowerShell (como administrador) si confías en el proyecto:

   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

4) Actualizar pip y pip-tools (opcional)

   python -m pip install --upgrade pip

5) Instalar dependencias

   pip install -r requirements.txt

   Nota: si agregamos nuevas dependencias, repite este comando.

6) Variables de entorno necesarias

   Revisa `core/config.py` para ver qué variables busca el proyecto (por ejemplo `GROQ_API_KEY`, `GROQ_MODEL`). Puedes exportarlas en PowerShell:

   $env:GROQ_API_KEY = "tu_api_key_aqui"
   $env:GROQ_MODEL = "gpt-4o-mini"  # ejemplo

7) Iniciar la aplicación

   uvicorn api.principal:app --reload --host 127.0.0.1 --port 8000

8) Abrir en el navegador

   Visita http://127.0.0.1:8000 en tu navegador.

9) Solución del error 'ModuleNotFoundError: No module named "groq"'

   - Asegúrate de activar el entorno virtual antes de ejecutar `uvicorn`.
   - Si ya está activado y `groq` no se instala con `pip install -r requirements.txt`, intenta:

     pip install groq

10) Alternativas de gestión de ambiente

   - Poetry: reproducible, gestión de versiones y lockfile.
   - Pipenv: similar a venv + Pipfile.
   - Conda: si usas paquetes binarios complejos.

Si quieres, puedo crear el entorno `.venv` aquí y ejecutar la instalación para comprobar que todo arranca. Dime si quieres que lo haga.
