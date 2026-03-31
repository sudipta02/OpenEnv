from envs.email_triage_env.models import EmailTriageAction
from envs.email_triage_env.server.email_triage_environment import EmailTriageEnvironment


def test_reset_returns_task_observation():
    env = EmailTriageEnvironment(default_task_id="easy_security_triage")
    obs = env.reset(seed=1)

    assert obs.task_id == "easy_security_triage"
    assert obs.current_step == 0
    assert len(obs.checklist) >= 3
    assert not obs.done


def test_easy_task_can_be_completed_deterministically():
    env = EmailTriageEnvironment(default_task_id="easy_security_triage")
    env.reset(seed=2)

    env.step(
        EmailTriageAction(
            action_type="classify",
            email_id="E-100",
            category="security_incident",
            priority="urgent",
            assignee="security_team",
        )
    )
    env.step(
        EmailTriageAction(
            action_type="draft_reply",
            email_id="E-100",
            reply_template="security_escalation",
        )
    )
    env.step(
        EmailTriageAction(
            action_type="set_follow_up",
            email_id="E-100",
            follow_up_days=1,
        )
    )
    result = env.step(
        EmailTriageAction(
            action_type="close_case",
            email_id="E-100",
            resolution_note="Escalated and credentials rotation requested.",
        )
    )

    assert result.done
    assert result.score >= 0.99


def test_wrong_action_is_penalized():
    env = EmailTriageEnvironment(default_task_id="easy_security_triage")
    env.reset(seed=3)

    result = env.step(
        EmailTriageAction(
            action_type="classify",
            email_id="E-100",
            category="billing_issue",
            priority="low",
            assignee="billing_ops",
        )
    )

    assert (result.reward or 0.0) < 0.0
    assert result.invalid_actions == 0
