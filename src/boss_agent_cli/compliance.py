"""Compliance guardrails disabled for recruiter-only mode."""

from __future__ import annotations

from typing import Any

import click


def low_risk_blocked_commands() -> set[str]:
	"""Return empty set (no commands blocked in recruiter mode)."""
	return set()


def is_low_risk_mode(ctx: click.Context) -> bool:
	"""Always return False - low risk mode is disabled."""
	return False


def require_compliance_allowed(ctx: click.Context, command: str) -> bool:
	"""Always allow - compliance checks disabled for recruiter-only CLI."""
	return True


def compliance_mode_data(ctx: click.Context) -> dict[str, Any]:
	"""Return disabled compliance mode data."""
	return {
		"default_boundary": "recruiter_full_access",
		"sensitive_commands_blocked": False,
		"description": "招聘专用版本 - 所有功能完全开放，无合规限制",
		"blocked_commands": [],
	}
