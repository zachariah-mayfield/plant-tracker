from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.sessions import SessionMiddleware
import secrets
import time
from typing import Callable
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_security_middleware(app: FastAPI) -> None:
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],  # Add your frontend URL
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add trusted hosts middleware
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*"]  # Configure this based on your environment
    )

    # Add session middleware
    app.add_middleware(
        SessionMiddleware,
        secret_key=secrets.token_urlsafe(32),
        max_age=3600  # 1 hour
    )

    # Add rate limiting middleware
    @app.middleware("http")
    async def rate_limit_middleware(request: Request, call_next: Callable):
        # Simple rate limiting - 100 requests per minute
        client_ip = request.client.host
        current_time = time.time()
        
        # You should implement proper rate limiting with Redis or similar
        # This is just a basic example
        if not hasattr(app.state, 'request_counts'):
            app.state.request_counts = {}
        
        if client_ip not in app.state.request_counts:
            app.state.request_counts[client_ip] = []
        
        # Remove requests older than 1 minute
        app.state.request_counts[client_ip] = [
            t for t in app.state.request_counts[client_ip]
            if current_time - t < 60
        ]
        
        if len(app.state.request_counts[client_ip]) >= 100:
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            return {"error": "Rate limit exceeded"}, 429
        
        app.state.request_counts[client_ip].append(current_time)
        return await call_next(request)

    # Add security headers middleware
    @app.middleware("http")
    async def add_security_headers(request: Request, call_next: Callable):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        return response 