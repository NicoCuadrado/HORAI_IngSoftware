import os
from dotenv import load_dotenv

# Carga las variables del archivo .env cuando estás en tu computadora
load_dotenv()

class Settings:
    # os.getenv busca la llave de forma invisible en el sistema
    GROQ_API_KEY = os.getenv("GROQ_API_KEY") 
    
    # El modelo no es información sensible, puede quedar escrito directamente
    GROQ_MODEL = "llama-3.1-8b-instant"

settings = Settings()