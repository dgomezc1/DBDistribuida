from time import sleep
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# Import routers

from app.core.config import settings
from app.api.router import router

from app.works.initialization import Initialization
from app.works.redistribution import Redistribution

app = FastAPI(
    title=settings.APP_NAME,
    redoc_url=f"{settings.PREFIX}/redoc",
    docs_url=f"{settings.PREFIX}/docs",
    swagger_ui_oauth2_redirect_url=f"{settings.PREFIX}/docs/oauth2-redirect",
    openapi_url=f"{settings.PREFIX}/openapi.json"
)

# Initialize nodes
sleep(5)
init_nodes = Initialization()
settings.NODES = init_nodes.run()

# Register Middlewares

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register routers
app.include_router(router, prefix=settings.PREFIX)

# Workers
redistribution = Redistribution()
redistribution.start()

# Default endpoint
@app.get(f"{settings.PREFIX}/info")
def root():
    return {
        "message": f"Welcome to {settings.APP_NAME} | Version: {settings.VERSION}"
    }
