"""Print the safe OutcomeIQ database-readiness result."""

from app.db.health import check_database_connection


def main() -> int:
    try:
        result = check_database_connection()
        status = result["status"]
    except Exception:
        # Unexpected script errors fail without exposing environment details.
        print("DATABASE ERROR")
        print("Database readiness check could not complete.")
        return 1

    if status == "connected":
        print("DATABASE CONNECTED")
        return 0

    if status == "not_configured":
        print("DATABASE NOT CONFIGURED")
        return 0

    if status == "error":
        print("DATABASE ERROR")
        print(result.get("message", "Database connection check failed."))
        # A connection/configuration failure is a valid diagnostic result.
        return 0

    print("DATABASE ERROR")
    print("Database readiness check returned an unknown status.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
