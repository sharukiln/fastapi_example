from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.db.database_config import database

router = APIRouter()


@router.get("/healthcheck", status_code=200)
async def healthcheck():
    """
    Simple health check endpoint to verify the application is running and can connect to the database.

    Returns a 200 status code and a JSON response with a "status" key set to "Healthy yayy!" if the application is
    running and can connect to the database. If there's an issue with the database connection, it will return a
    500 status code and a JSON response with a "status" key set to "Unhealthy" and an "error" key set to a string
    describing the error.
    """
    try:
        # Perform a test query to check the MongoDB connection
        await database.command("ping")
        return JSONResponse(content=jsonable_encoder({"status": "Healthy yayy!"}))
    except Exception as e:
        # If there's an issue with the database connection, return an error
        return JSONResponse(content=jsonable_encoder({"status": "Unhealthy", "error": str(e)}), status_code=500)
