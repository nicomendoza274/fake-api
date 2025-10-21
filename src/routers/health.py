from fastapi import APIRouter

from core.database.database import SessionDep
from core.database.health import DatabaseHealthChecker
from core.models.response import ResponseData

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get(
    path="/",
    response_model=ResponseData[dict],
    summary="Health check endpoint",
    description="Check the overall health of the application",
)
def health_check(session: SessionDep):
    """Endpoint básico de health check"""
    health_data = DatabaseHealthChecker.comprehensive_health_check(session)

    # If there is a problem, return status 503
    if health_data["overall_status"] == "unhealthy":
        from fastapi import HTTPException, status

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=health_data
        )

    return {"data": health_data}


@router.get(
    path="/database",
    response_model=ResponseData[dict],
    summary="Database health check",
    description="Check the health of the database connection and pool",
)
def database_health_check(session: SessionDep):
    """Endpoint específico para verificar la salud de la base de datos"""
    health_data = DatabaseHealthChecker.comprehensive_health_check(session)

    return {"data": health_data["checks"]}


@router.get(
    path="/pool",
    response_model=ResponseData[dict],
    summary="Connection pool status",
    description="Check the status of the database connection pool",
)
def pool_status_check():
    """Endpoint para verificar el estado del pool de conexiones"""
    pool_data = DatabaseHealthChecker.check_pool_status()

    return {"data": pool_data}
