from datetime import datetime
from typing import Any, Dict

from sqlalchemy import text
from sqlmodel import Session

from src.core.database.database import engine


class DatabaseHealthChecker:
    """Database health checker"""

    @staticmethod
    def check_connection(session: Session) -> Dict[str, Any]:
        """Check the connection to the database"""
        try:
            # Execute a simple query using session.execute (correct method)
            result = session.execute(text("SELECT 1 as health_check"))
            result.fetchone()

            return {
                "status": "healthy",
                "message": "Database connection is working",
                "timestamp": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "message": f"Database connection failed: {str(e)}",
                "timestamp": datetime.utcnow().isoformat(),
            }

    @staticmethod
    def check_pool_status() -> Dict[str, Any]:
        """Check the status of the connection pool"""
        try:
            pool = engine.pool

            return {
                "status": "healthy",
                "pool_size": getattr(pool, "size", lambda: "unknown")(),
                "checked_in": getattr(pool, "checkedin", lambda: "unknown")(),
                "checked_out": getattr(pool, "checkedout", lambda: "unknown")(),
                "overflow": getattr(pool, "overflow", lambda: "unknown")(),
                "invalid": getattr(pool, "invalid", lambda: "unknown")(),
                "timestamp": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "message": f"Pool status check failed: {str(e)}",
                "timestamp": datetime.utcnow().isoformat(),
            }

    @staticmethod
    def get_database_info(session: Session) -> Dict[str, Any]:
        """Get information about the database"""
        try:
            # PostgreSQL version
            version_result = session.execute(text("SELECT version()"))
            version_row = version_result.fetchone()
            version = version_row[0] if version_row else "Unknown"

            # Active connections information
            connections_result = session.execute(
                text(
                    """
                SELECT 
                    count(*) as active_connections,
                    state,
                    application_name
                FROM pg_stat_activity 
                WHERE datname = current_database()
                GROUP BY state, application_name
            """
                )
            )
            connections_info = [dict(row._mapping) for row in connections_result]

            # Database size
            size_result = session.execute(
                text(
                    """
                SELECT pg_size_pretty(pg_database_size(current_database())) as database_size
            """
                )
            )
            size_row = size_result.fetchone()
            db_size = size_row[0] if size_row else "Unknown"

            return {
                "status": "healthy",
                "version": version,
                "database_size": db_size,
                "connections": connections_info,
                "timestamp": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "message": f"Database info check failed: {str(e)}",
                "timestamp": datetime.utcnow().isoformat(),
            }

    @staticmethod
    def comprehensive_health_check(session: Session) -> Dict[str, Any]:
        """Complete database health check"""
        connection_check = DatabaseHealthChecker.check_connection(session)
        pool_check = DatabaseHealthChecker.check_pool_status()
        db_info = DatabaseHealthChecker.get_database_info(session)

        overall_status = "healthy"
        if any(
            check["status"] == "unhealthy"
            for check in [connection_check, pool_check, db_info]
        ):
            overall_status = "unhealthy"

        return {
            "overall_status": overall_status,
            "checks": {
                "connection": connection_check,
                "pool": pool_check,
                "database_info": db_info,
            },
            "timestamp": datetime.utcnow().isoformat(),
        }
