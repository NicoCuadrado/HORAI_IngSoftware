from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from .core.db import get_db
from .operaciones import (
    crear_conversacion_con_ia,
    obtener_conversaciones_por_sesion,
    obtener_todas_las_conversaciones,
    obtener_sesiones_agrupadas,
    eliminar_sesion_completa,
    eliminar_todas_las_conversaciones
)
import uuid
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

app = FastAPI(title="HORAI Asistente")

# Configurar Jinja2 de forma explícita
template_dir = Path(__file__).parent.parent / "templates"
env = Environment(loader=FileSystemLoader(str(template_dir)))

def render_template(template_name: str, context: dict):
    """Helper para renderizar templates"""
    template = env.get_template(template_name)
    return template.render(context)

@app.get("/", response_class=HTMLResponse)
def inicio(request: Request):
    return HTMLResponse(render_template("inicio.html", {"request": request}))

@app.get("/organizacion", response_class=HTMLResponse)
def organizacion(request: Request):
    return HTMLResponse(render_template("organizacion.html", {"request": request}))

@app.get("/bienestar", response_class=HTMLResponse)
def bienestar(request: Request):
    return HTMLResponse(render_template("bienestar.html", {"request": request}))

@app.get("/progreso", response_class=HTMLResponse)
def progreso(request: Request):
    return HTMLResponse(render_template("inicio.html", {"request": request}))  # Por ahora usa el mismo

@app.get("/chat", response_class=HTMLResponse)
def mostrar_chat(request: Request, sesion_id: str = None, db: Session = Depends(get_db)):
    if not sesion_id:
        sesion_id = str(uuid.uuid4())
    conversaciones = obtener_conversaciones_por_sesion(db, sesion_id)
    return HTMLResponse(render_template("chat.html", {
        "request": request, 
        "conversaciones": conversaciones,
        "sesion_id": sesion_id
    }))

@app.post("/enviar", response_class=HTMLResponse)
async def enviar_mensaje(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    mensaje_usuario = str(form.get("mensaje_usuario", "")).strip()
    sesion_id = str(form.get("sesion_id", "")).strip()
    
    if not mensaje_usuario:
        return RedirectResponse("/chat", status_code=303)
    
    if not sesion_id:
        sesion_id = str(uuid.uuid4())
    
    crear_conversacion_con_ia(db, mensaje_usuario, sesion_id)
    return RedirectResponse(f"/chat?sesion_id={sesion_id}", status_code=303)

@app.get("/historial", response_class=HTMLResponse)
def historial(request: Request, db: Session = Depends(get_db)):
    todas_conversaciones = obtener_todas_las_conversaciones(db)
    sesiones_agrupadas = obtener_sesiones_agrupadas(db)
    return HTMLResponse(render_template("historial.html", {
        "request": request,
        "todas_conversaciones": todas_conversaciones,
        "sesiones_agrupadas": sesiones_agrupadas  # Ya es una lista, no necesitamos .values()
    }))

@app.get("/nuevo-chat", response_class=HTMLResponse)
def nuevo_chat():
    nuevo_sesion_id = str(uuid.uuid4())
    return RedirectResponse(f"/chat?sesion_id={nuevo_sesion_id}", status_code=303)

@app.post("/eliminar-sesion/{sesion_id}")
def eliminar_sesion(sesion_id: str, db: Session = Depends(get_db)):
    eliminar_sesion_completa(db, sesion_id)
    return RedirectResponse("/historial", status_code=303)

@app.post("/eliminar-todo")
def eliminar_todo(db: Session = Depends(get_db)):
    eliminar_todas_las_conversaciones(db)
    return RedirectResponse("/historial", status_code=303)