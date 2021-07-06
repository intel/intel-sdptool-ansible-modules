#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)
"""Intel(R) SDP Tool Action Plugin Module"""

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
from ansible.utils.display import Display
from ansible.errors import AnsibleError
from ansible.plugins.action import ActionBase


display = Display()


class ActionModule(ActionBase):
    """Intel(R) SDP Tool Action Plugin Class"""

    @staticmethod
    def change_path(log_path, task_vars):
        """Get updated path for sel log path"""
        path = log_path.split('/')
        if len(path) > 1:
            ActionModule.verify_path(os.path.dirname(log_path), directory=True)
        path[-1] = "[" + task_vars["inventory_hostname"] + "]_" + path[-1]
        path = "/".join(path)
        return path

    def check_sdptool_installed(self, tmp, task_vars):
        """Verify SDP Tool is installed"""
        module_return = self._execute_module(
            module_name='command',
            module_args={"argv": ["which", "SDPTool"]}, task_vars=task_vars, tmp=tmp)
        if module_return['rc'] != 0:
            raise AnsibleError("SDPTool not installed")
        return True

    @staticmethod
    def check_task_args(task_args):
        """Validate task arguments"""
        supported_args = ['action', 'args']
        for arg in task_args.keys():
            if arg not in supported_args:
                raise AnsibleError("'{0}' is not valid argument. ".format(arg)
                                   + "Supported arguments are {0}".format(supported_args))
        if 'action' not in task_args.keys():
            raise AnsibleError("'action' argument is mandatory")

    @staticmethod
    def verify_path(path, directory=False):
        """Check if file or directory exists"""
        if directory:
            if not os.path.isdir(path):
                raise AnsibleError("{0} directory does not exist".format(path))
            return True
        if not os.path.isfile(path):
            raise AnsibleError("{0} file does not exist".format(path))
        return True

    @staticmethod
    def supported_sdptool_args(task_args, task_vars):
        """Check supported SDP Tool argument and required parameters"""
        args = []
        if task_args['action'] in ['getini', 'getbiosoptions', 'setoptions', 'deployoptions']:
            raise AnsibleError("Operation not Supported")
        if task_args["action"] == "set_biosconfig_all":
            if 'ini_path' not in task_vars:
                raise AnsibleError("INI Path not provided")
            ActionModule.verify_path(task_vars["ini_path"])
            args.append(task_vars["ini_path"])
        elif task_args["action"] in ["vmedia", "unmount"]:
            if task_args["action"] + '_iso_path' not in task_vars:
                raise AnsibleError("{0} not provided".format(
                    task_args["action"] + '_iso_path') + '"')
            args.append('"' + task_vars[task_args["action"] + '_iso_path'])
        elif task_args["action"] == "update":
            if 'sup_path' not in task_vars:
                raise AnsibleError("SUP not provided")
            ActionModule.verify_path(task_vars["sup_path"], directory=True)
            args.append(task_vars["sup_path"])
        elif task_args["action"] == "custom_deploy":
            if 'custom_sup_path' not in task_vars:
                raise AnsibleError("Custom SUP not provided")
            ActionModule.verify_path(
                task_vars["custom_sup_path"], directory=True)
            args.append(task_vars["custom_sup_path"])
        return args

    @staticmethod
    def process_additional_args(task_args, task_vars):
        """Process action arguments and flags of SDP Tool command"""
        args = []
        if 'args' in task_args.keys():
            if isinstance(task_args['args'], list):
                args += task_args['args']
            elif isinstance(task_args['args'], str):
                args += [task_args['args']]
        if task_args['action'] == 'sel' and '-f' in args:
            i = args.index('-f')
            if i + 1 < len(args):
                args[i + 1] = '"' + \
                    ActionModule.change_path(args[i + 1], task_vars) + '"'
        return args

    @staticmethod
    def check_pexpect_module():
        """Check Required Module Installed"""
        try:
            import pexpect
        except ImportError:
            raise AnsibleError(
                "pexpect module missing. Please install the module.")

    def run(self, tmp=None, task_vars=None):
        """Plugin execution method"""
        super(ActionModule, self).run(tmp, task_vars)
        self.check_sdptool_installed(tmp, task_vars)
        self.check_pexpect_module()
        task_args = self._task.args.copy()
        self.check_task_args(task_args)
        params = ["SDPTool", task_vars["inventory_hostname"],
                  task_vars["bmc_username"], task_vars["bmc_password"], task_args["action"]]
        params += self.supported_sdptool_args(task_args, task_vars)
        params += self.process_additional_args(task_args, task_vars)
        if task_args['action'] in ['set_biosconfig', 'set_biosconfig_all']\
                and '-no_reboot' not in params:
            params.append('-no_reboot')
        params = list(map(str, params))
        command = " ".join(params)
        params[3] = '*' * 5
        module_args = dict(
            command=command,
            responses={
                "..*": "y"
            },
            timeout=200
        )
        try:
            display.banner(msg=' '.join(params), color='green')
            module_return = self._execute_module(
                module_name='expect',
                module_args=module_args, task_vars=task_vars, tmp=tmp)
        except Exception as exp:
            module_return = {
                "name": "Error",
                "params": module_args,
                "error": exp,
                "failed": True
            }
        if 'failed' not in module_return \
            and task_args['action'] in ['update', 'custom_deploy',
                                        'set_biosconfig', 'set_biosconfig_all']:
            if '-no_reboot' in params:
                display.warning(
                    "Please reboot the system for changes to take effect")
        output_dict = {}
        if 'rc' in module_return:
            output_dict['rc'] = module_return['rc']
        if 'msg' in module_return:
            output_dict['msg'] = module_return['msg']
        if 'failed' in module_return:
            output_dict['failed'] = module_return['failed']
        if 'stdout_lines' in module_return:
            output_dict['stdout_lines'] = module_return['stdout_lines']

        return output_dict
