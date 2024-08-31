from fastapi import FastAPI
from app.routes.start_stop_detection import router as start_stop_detection
from app.routes.health_check import router as health_check
from app.routes.login import router as login
from app.middleware.jwt_auth import JWTAuthMiddleware
# load_dotenv(".env")


app = FastAPI(title="FastAPI Boiler Plate")
app.add_middleware(JWTAuthMiddleware)

app.include_router(start_stop_detection)
app.include_router(health_check)
app.include_router(login)

# init_logging()

if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
