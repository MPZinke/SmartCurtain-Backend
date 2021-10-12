#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2021.10.07                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from re import search as re_search;
from subprocess import call as subprocess_call, check_output as subprocess_check_output;

from Class.ZWidget import ZWidget;
from Other.Global import substr;


class Updater(ZWidget):
	def __init__(self):
		ZWidget.__init__(self, "Updater", None);

		self.local_version = self.get_local_version();
		self.origin_Production_version = self.get_remote_version();

	# Get current version from repo
	def get_local_version(self):
		git_describe = subprocess_check_output(["git", "describe"]);
		if(not git_describe): raise Exception("git describe was unable to get version number");

		search = re_search(r"v[0-9]+\.[0-9]+\.[0-9]+", git_describe);
		if(not search):  raise Exception("Unable to search version number from git describe");

		return search.group(0);


	# Get remote version from remote repo
	def get_remote_version(self):
		git_ls_remote = subprocess_check_output(["git", "ls-remote", "--tag", "origin"]);
		if(not git_ls_remote): raise Exception("git describe was unable to get version number");

		search = re_search(r"v[0-9]+\.[0-9]+\.[0-9]+", git_ls_remote);
		if(not search):  raise Exception("Unable to search version number from git describe");

		return search.group(0);


	def call_shell_command(self, params: list):
		with open(devnull, 'w') as FNULL:
			return subprocess_call(params, stdout=FNULL);


	# Increment versions, checking for DB updates. If found, update DB
	def _loop_process(self):
		self.origin_Production_version = self.get_remote_version();

		if(self.origin_Production_version != self.local_version):
			if(self.call_shell_command(["git", "-C", "/usr/local/SmartCurtain", "stash"])):
				raise Exception("Could not stash local repository");
			if(self.call_shell_command(["git", "-C", "/usr/local/SmartCurtain", "checkout", "Production"])):
				raise Exception("Could not checkout Production branch");
			if(self.call_shell_command(["git", "-C", "/usr/local/SmartCurtain", "pull"])):
				raise Exception("Could not pull repository");
			if(self.call_shell_command(["sudo", "systemctl", "restart", "SmartCurtain.service"])):
				raise Exception("Could not restart systemctl service");



# CLI update function
