from fastapi import FastAPI
import logging
from route.route_transaction import router_transaction
from route.route_auth import router_auth

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


app = FastAPI()
@app.get("/ping")
async def ping():
    return{'pong'}
    
app.include_router(router_transaction,tags=['Transaction End Point'],prefix="/transaction")
app.include_router(router_auth,tags=["Authorize"],prefix="/auth")