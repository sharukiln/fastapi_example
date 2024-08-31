from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.jwt_utility import decode_access_token

class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in ["/docs", "/create_user", "/login"]:
            response = await call_next(request)
            return response
        auth_header = request.headers.get("Authorization")
        if auth_header:
            try:
                scheme, token = auth_header.split()
                if scheme.lower() != "bearer":
                    raise HTTPException(status_code=401, detail="Invalid authentication scheme.")
                token_data = decode_access_token(token)
                request.state.user = token_data
            except ValueError:
                raise HTTPException(status_code=401, detail="Invalid authorization format.")
        else:
            raise HTTPException(status_code=401, detail="Authorization header missing.")

        response = await call_next(request)
        return response

