from fastapi import *

from spotify_clone.auth import sign_in
from spotify_clone.auth  import sign_up
from spotify_clone.services.db import init_db

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    init_db()
    
app.include_router(sign_in.router, prefix="/api/v1/auth")
app.include_router(sign_up.router, prefix="/api/v1/auth")
