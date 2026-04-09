from fastapi.responses import JSONResponse

async def error_response(code: str, message: str, status_code: int):
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": code,
                "message": message
            }
        }
    )