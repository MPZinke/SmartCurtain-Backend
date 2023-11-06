#!/opt/homebrew/bin/python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2023.10.28                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from datetime import datetime, timedelta
import os
import re
import requests
import sys
from time import sleep
from typing import Optional, TypeVar


Version = TypeVar("Version")


class Version:
	def __init__(self, version_string: str):
		version_expression = r"v?(?P<MAJOR>[0-9]+)(?:\.(?P<MINOR>[0-9]+)(?:\.(?P<PATCH>[0-9]+))?)?(?:\-(?P<BUILD>.+))?"
		match: Optional[re.Match] = re.match(version_expression, version_string)

		if(match is None or match.span()[1] != len(version_string)):
			version_format = "v?[0-9]+(\\.[0-9]+(\\.[0-9]+)?)?(\\-.+)?"
			raise ValueError(f"Version '{version_string}' is not of proper format '{version_format}'")

		version_parts: dict = match.groupdict()
		self.v: bool = version_string[0] == 'v'
		self.major = int(version_parts["MAJOR"])
		self.minor = int(version_parts["MINOR"] or 0)
		self.patch = int(version_parts["PATCH"] or 0)
		self.build = version_parts["BUILD"] or ""


	def __add__(self: Version, right: list) -> Version:
		major = self.major + right[0]
		minor = self.minor + right[1]
		patch = self.patch + right[2]
		build = right[3]

		if(right[0] > 0):
			minor = patch = 0

		elif(right[1] > 0):
			patch = 0

		return Version(f"""{["", "v"][self.v]}{major}.{minor}.{patch}{["", "-"][bool(build)]}{build}""")


	def __iter__(self: Version) -> iter:
		yield from [self.major, self.minor, self.patch, self.build]


	def __str__(self: Version) -> str:
		return f"""{["", "v"][self.v]}{self.major}.{self.minor}.{self.patch}{["", "-"][bool(self.build)]}{self.build}"""


	def __sub__(self: Version, right: Version) -> Version:
		version_differences = [left - right for left, right in zip(list(self)[:3], list(right)[:3])] + [self.build]
		return version_differences


	def copy(self: Version) -> Version:
		return Version(str(self))


def get_runs(repo: str) -> list[dict]:
	url = f"""https://api.github.com/repos/{repo}/actions/runs"""
	headers = {"Authorization": f"""Bearer {os.getenv("SMARTCURTAIN_RW_TOKEN")}"""}
	response: requests.Response = requests.get(url, headers=headers, timeout=21)
	response.raise_for_status()

	return response.json()["workflow_runs"]


def wait_while_another_action_is_running(submodule_run_id: int, submodule_repo: str, parent_repo: str) -> None:
	end_time = datetime.now() + timedelta(hours=1)
	finished_statuses = ["completed", "failure", "cancelled", "skipped", "stale", "success", "timed_out"]
	submodule_run_url = f"https://api.github.com/repos/{submodule_repo}/actions/runs/{submodule_run_id}"

	while(datetime.now() < end_time):
		submodule_runs: list[dict] = get_runs(submodule_repo)
		parent_runs: list[dict] = get_runs(parent_repo)
		runs = submodule_runs + parent_runs
		if(all(run["status"] in finished_statuses or run["url"] == submodule_run_url for run in runs)):
			return

		sleep(2)

	raise TimeoutError("Another action has run for too long, blocking this one.")


def get_releases(repo: str, length: int=1) -> list[dict]:
	url = f"""https://api.github.com/repos/{repo}/releases"""
	headers = {"Authorization": f"""Bearer {os.getenv("SMARTCURTAIN_RW_TOKEN")}"""}
	response: requests.Response = requests.get(url, headers=headers, timeout=21)
	response.raise_for_status()

	releases: list[dict] = response.json()[:length]
	releases.sort(key=lambda release: release["published_at"], reverse=True)

	return [{key: release[key] for key in ["tag_name", "name", "body"]} for release in releases]


def get_parent_releases(repo: str) -> dict:
	parent_releases = get_releases(repo)
	if(len(parent_releases) == 1):
		return {"repo": repo, **parent_releases[0]}

	return {"repo": repo, "tag_name": "0.0.0", "name": "", "body": ""}


def get_submodule_releases(repo: str) -> Optional[list[dict]]:
	submodule_releases = get_releases(repo, 2)
	if(len(submodule_releases) == 0):
		return None

	if(len(submodule_releases) > 1):
		return {"repo": repo, **submodule_releases[0]}, {"repo": repo, **submodule_releases[1]}

	return {"repo": repo, **submodule_releases[0]}, {"repo": repo, "tag_name": "0.0.0", "name": "", "body": ""}


def parent_release_body(current_submodule_release: dict) -> str:
	tag_name = current_submodule_release["tag_name"]
	parent_body = f"Increments the release from the submodule's release `{tag_name}`."
	parent_body += "\nRelease notes below."
	parent_body += "\n> " + "\n> ".join(current_submodule_release["body"].split("\n"))

	return parent_body


def increment_parent_version(parent_release: dict, current_submodule_release: dict, previous_submodule_release: dict
) -> Version:
	parent_version = Version(parent_release["tag_name"])
	current_submodule_version = Version(current_submodule_release["tag_name"])
	previous_submodule_version = Version(previous_submodule_release["tag_name"])

	submodule_version_difference: list = current_submodule_version - previous_submodule_version
	build: str = submodule_version_difference[3]
	normalized_submodule_version_difference = [*[int(bool(value)) for value in submodule_version_difference[:3]], build]

	return parent_version + normalized_submodule_version_difference


def create_parent_release(repo: str, new_parent_release: dict) -> bool:
	url = f"https://api.github.com/repos/{repo}/releases"
	headers = {"Authorization": f"""Bearer {os.getenv("SMARTCURTAIN_RW_TOKEN")}"""}
	print(new_parent_release)
	response: requests.Response = requests.post(url, headers=headers, json=new_parent_release, timeout=21)
	print(response.text)
	response.raise_for_status()


def main(argv: list[str]):
	submodule_run_id = argv[1]
	submodule_repo = argv[2]
	parent_repo = argv[3]

	wait_while_another_action_is_running(submodule_run_id, submodule_repo, parent_repo)

	# Get submodule releases
	submodule_releases = get_submodule_releases(submodule_repo)
	if(submodule_releases is None):
		raise Exception(f"There are no releases for '{submodule_repo}'")

	current_submodule_release, previous_submodule_release = submodule_releases

	# Get parent releases
	parent_release = get_parent_releases(parent_repo)

	# Format data for new parent release
	new_parent_body = parent_release_body(current_submodule_release)
	new_parent_name = f"""[{current_submodule_release["repo"]}] {current_submodule_release["name"]}"""
	new_parent_version = increment_parent_version(parent_release, current_submodule_release, previous_submodule_release)
	new_parent_release = {"body": new_parent_body, "name": new_parent_name, "tag_name": str(new_parent_version)}

	create_parent_release(parent_repo, new_parent_release)


if(__name__ == "__main__"):
	main(sys.argv)
