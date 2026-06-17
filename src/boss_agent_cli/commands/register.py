"""Click command registration helpers (recruiter-only version)."""

import click

from boss_agent_cli.commands import (
	config_cmd,
	doctor,
	login,
	logout,
	platforms,
	schema,
	status,
)
from boss_agent_cli.commands.recruiter import applications as recruiter_applications
from boss_agent_cli.commands.recruiter import candidates as recruiter_candidates
from boss_agent_cli.commands.recruiter import chat as recruiter_chat
from boss_agent_cli.commands.recruiter import jobs as recruiter_jobs
from boss_agent_cli.commands.recruiter import reply as recruiter_reply
from boss_agent_cli.commands.recruiter import request_resume as recruiter_request_resume
from boss_agent_cli.commands.recruiter import resume as recruiter_resume
from boss_agent_cli.display import handle_error_output
from boss_agent_cli.platforms import list_recruiter_platforms


def register_candidate_commands(cli: click.Group) -> None:
	"""DEPRECATED: Candidate commands disabled in recruiter-only mode."""
	pass


@click.group("hr", help="招聘者模式命令")
@click.pass_context
def hr_group(ctx: click.Context) -> None:
	ctx.obj["role"] = "recruiter"
	platform_name = ctx.obj.get("platform") or "zhipin"
	recruiter_name = f"{platform_name}-recruiter"
	supported = list_recruiter_platforms()
	if recruiter_name not in supported:
		handle_error_output(
			ctx,
			"hr",
			code="PLATFORM_NOT_SUPPORTED",
			message=(
				f"招聘者模式暂不支持平台 {platform_name!r}；"
				f"当前仅支持: {', '.join(supported)}"
			),
			recoverable=True,
			recovery_action="boss --platform zhipin",
		)
		raise SystemExit(1)


def register_recruiter_commands(cli: click.Group) -> None:
	"""Register recruiter commands (default in recruiter-only mode)."""
	# 系统命令
	cli.add_command(schema.schema_cmd, "schema")
	cli.add_command(login.login_cmd, "login")
	cli.add_command(logout.logout_cmd, "logout")
	cli.add_command(status.status_cmd, "status")
	cli.add_command(platforms.platforms_cmd, "platforms")
	cli.add_command(doctor.doctor_cmd, "doctor")
	cli.add_command(config_cmd.config_group, "config")
	
	# 招聘者命令
	cli.add_command(hr_group, "hr")
	hr_group.add_command(recruiter_applications.applications_cmd, "applications")
	hr_group.add_command(recruiter_resume.resume_cmd, "resume")
	hr_group.add_command(recruiter_chat.recruiter_chat_cmd, "chat")
	hr_group.add_command(recruiter_chat.recruiter_chatmsg_cmd, "chatmsg")
	hr_group.add_command(recruiter_chat.recruiter_last_messages_cmd, "last-messages")
	hr_group.add_command(recruiter_jobs.jobs_group, "jobs")
	hr_group.add_command(recruiter_candidates.candidates_cmd, "candidates")
	hr_group.add_command(recruiter_reply.reply_cmd, "reply")
	hr_group.add_command(recruiter_request_resume.request_resume_cmd, "request-resume")
