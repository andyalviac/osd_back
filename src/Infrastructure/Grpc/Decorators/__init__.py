import logging
import json
from functools import wraps
from pydantic import ValidationError
from src.Infrastructure.Grpc.Generated import Common_pb2
from src.Shared.Enums.Code import Code

logger = logging.getLogger(__name__)

def rpc_handler(func):
    """
    Decorator that:
    - Safely extracts and parses request.data to a dict (payload).
    - Handles cases where request has no data or invalid JSON.
    - Wraps the result in Common_pb2.Response.
    """

    @wraps(func)
    async def wrapper(self, request, context, *args, **kwargs):
        try:
            # --- Extract payload safely ---
            payload = {}

            if hasattr(request, "data"):
                data = request.data
                if data:
                    # Try parse JSON or accept dict directly
                    if isinstance(data, (str, bytes)):
                        try:
                            payload = json.loads(data)
                        except json.JSONDecodeError:
                            logger.debug("Invalid JSON in request.data, using empty payload")
                            payload = {}
                    elif isinstance(data, dict):
                        payload = data
                    else:
                        logger.debug(f"Unsupported data type in request: {type(data)}")
            
            # --- Execute original RPC function ---
            result = await func(self, payload, context, *args, **kwargs)

            # --- Build gRPC response ---
            return Common_pb2.Response(
                status=result.get("status", Code.PROCESS_SUCCESS_CODE),
                message=result.get("message", "ok"),
                data=result.get("data", None)
            )

        except ValidationError as exc:
            errors = exc.errors()
            msg_error = errors[0]["msg"]

            logger.exception(f"Request validation error: {errors}")
            return Common_pb2.Response(
                status="RPC_REQUEST_VALIDATION_ERROR",
                message=msg_error,
                data=None
            )
        except Exception as e:
            logger.exception("Unhandled exception in gRPC method")
            return Common_pb2.Response(
                status="RPC_UNEXPECTED_ERROR",
                message=str(e),
                data=None
            )

    return wrapper
