from fastapi import FastAPI, Request
from app.api.hotels import router as hotels_router
from app.api.rooms import router as rooms_router
from app.api.bookings import router as bookings_router
from app.api.auth import router as authx_router
from app.core.security import security
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from app.exceptions import BaseBookingException


app = FastAPI(title="Бронирование отелей")


@app.exception_handler(BaseBookingException)
async def booking_exception_handler(request: Request, exc: BaseBookingException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Booking API",
        version="1.0.0",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    openapi_schema["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema

    return app.openapi_schema


app.openapi = custom_openapi

security.handle_errors(app)

app.include_router(hotels_router)
app.include_router(rooms_router)
app.include_router(bookings_router)
app.include_router(authx_router)
