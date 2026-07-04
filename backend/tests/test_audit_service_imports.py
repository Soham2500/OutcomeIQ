"""Import and redaction tests for the audit service."""

from app.services import audit_service


def test_audit_service_import_and_sensitive_metadata_filter(monkeypatch) -> None:
    captured: dict[str, object] = {}

    def fake_create_audit_event(_db, **fields):
        captured.update(fields)
        return fields

    monkeypatch.setattr(audit_service, "create_audit_event", fake_create_audit_event)

    result = audit_service.record_audit_event(
        None,
        action="update",
        metadata_json={
            "updated_fields": ["name"],
            "password": "must-not-be-recorded",
            "access_token": "must-not-be-recorded",
        },
    )

    assert result is not None
    assert captured["metadata_json"] == {"updated_fields": ["name"]}
