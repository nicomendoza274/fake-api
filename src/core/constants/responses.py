from typing import Any, Dict

from fastapi import status

NOT_422: Dict[int | str, Dict[str, Any]] = {
    status.HTTP_422_UNPROCESSABLE_ENTITY: {
        "description": "Unprocessable Entity",
        "content": None,
    }
}

NOT_200: Dict[int | str, Dict[str, Any]] = {
    status.HTTP_200_OK: {
        "description": "Successful Response",
        "content": None,
    }
}

NOT_201: Dict[int | str, Dict[str, Any]] = {
    status.HTTP_201_CREATED: {
        "description": "Created",
        "content": None,
    },
}
