"""Print the safe OutcomeIQ database-readiness result."""

from app.db.health import check_database_connection


def main() -> int:
    result = check_database_connection()
    status = result["status"]

    if status == "connected":
        print("DATABASE CONNECTED")
        return 0

    if status == "not_configured":
        print("DATABASE NOT CONFIGURED")
        return 0

    print("DATABASE ERROR")
    if result.get("message"):
        print(result["message"])
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
