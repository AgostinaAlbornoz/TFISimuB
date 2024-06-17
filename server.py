from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
import uvicorn
import main as mn



app = FastAPI(
    title='API Simulacion',
    description='API para enviar datos de la simulación',
    version='1.0.0'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*']
)



@app.get("/generate_json")
def generate_json(ce:int = 60, oa:int = 420000 ):
    '''
    Test
    '''
    informe_camiones = mn.main(ce,oa)
    return informe_camiones





if __name__ == "__main__":
    # ----------------------------------------
     config = uvicorn.Config("server:app", port=1234, host='127.0.0.1')
     server = uvicorn.Server(config)
     server.run()

    # PARA ACTIVARLO PONER EN LA TERMINAL:
    # python -m uvicorn server:app --reload --port 8080 --host '127.0.0.1'
