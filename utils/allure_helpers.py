import json

import allure


def attach_json(name: str, data) -> None:
    """Attach JSON-serializable data to the Allure report."""
    allure.attach(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2,
            default=str,
        ),
        name=name,
        attachment_type=allure.attachment_type.JSON,
    )


def attach_text(name: str, content: str) -> None:
    """Attach text data to the Allure report."""
    allure.attach(
        content,
        name=name,
        attachment_type=allure.attachment_type.TEXT,
    )