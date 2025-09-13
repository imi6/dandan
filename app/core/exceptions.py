"""Exception handlers and custom exceptions"""
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException


class DanDanPlayException(Exception):
    """Base exception for DanDanPlay"""
    pass


class VideoNotFoundException(DanDanPlayException):
    """Video not found exception"""
    pass


class InvalidFormatException(DanDanPlayException):
    """Invalid format exception"""
    pass


class APIException(DanDanPlayException):
    """External API exception"""
    pass


def setup_exception_handlers(app: FastAPI):
    """Setup custom exception handlers"""
    
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        """Handle HTTP exceptions"""
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": exc.detail,
                "status_code": exc.status_code
            }
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Handle validation errors"""
        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "error": "Validation error",
                "details": exc.errors()
            }
        )
    
    @app.exception_handler(DanDanPlayException)
    async def dandanplay_exception_handler(request: Request, exc: DanDanPlayException):
        """Handle custom DanDanPlay exceptions"""
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "error": str(exc),
                "type": exc.__class__.__name__
            }
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle general exceptions"""
        # In production, you should log this error
        import traceback
        traceback.print_exc()
        
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "Internal server error",
                "detail": str(exc) if app.debug else "An unexpected error occurred"
            }
        )