from __future__ import annotations

import os

from openenv.core.env_server.http_server import create_app

try:
    from email_triage_env.models import EmailTriageAction, EmailTriageObservation
    from email_triage_env.server.email_triage_environment import EmailTriageEnvironment
except ImportError:
    from models import EmailTriageAction, EmailTriageObservation
    from .email_triage_environment import EmailTriageEnvironment


def create_email_triage_environment() -> EmailTriageEnvironment:
    default_task_id = os.getenv("EMAIL_TRIAGE_DEFAULT_TASK_ID")
    return EmailTriageEnvironment(default_task_id=default_task_id)


MAX_CONCURRENT_ENVS = int(os.getenv("MAX_CONCURRENT_ENVS", "64"))

app = create_app(
    create_email_triage_environment,
    EmailTriageAction,
    EmailTriageObservation,
    env_name="email_triage_env",
    max_concurrent_envs=MAX_CONCURRENT_ENVS,
)


def main(host: str = "0.0.0.0", port: int = 8000) -> None:
    import uvicorn

    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()
