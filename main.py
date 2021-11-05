from fastapi import FastAPI
import logging
from route.route_transaction import router_transaction

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


app = FastAPI()

app.include_router(router_transaction,tags=['Transaction End Point'],prefix="/transaction")