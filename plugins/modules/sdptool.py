#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)
"""Intel SDP Tool Plugin Doc Module"""

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = '''
module: sdptool
author:
  - Yeshaswi M R Gowda (@intel)
  - Mohammed Mujahid Ul Islam (@intel)
short_description: SDP Tool plugin for managing BMC
version_added: "2.1.0"
description: 'The module allows to executes SDPTool command which manages a BMC'
options:
  action:
    description:
      - SDPTool command argument
    type: 'str'
    required: True
  args:
    description:
      - Valid SDPTool command such as systeminfo, update, custom_deploy
    type: 'list'
    required: False
    elements: 'str'
requirements:
    - Python >=3.6.5
    - pexecpt
    - Intel(R) SDP Tool >= 2.0-0 (Intel(R) Server Debug and Provisioning Tool)
'''

EXAMPLES = '''
---
- name: CPU Information
  sdptool:
    action: "cpuinfo"
  register: output

- name: SDPTool output
  debug:
    msg: "{{ output.stdout_lines }}"

- name: System Information
  sdptool:
    action: "systeminfo"
  register: output

- name: System Info Output
  debug:
    msg: "{{ output.stdout_lines }}"
'''

RETURN = '''
rc:
    description: Return Code by SDPTool
    type: int
    returned: always
    sample: 0
stdout_lines:
    description: Output of SDPTool command
    type: list
    returned: always
'''

from ansible.module_utils.basic import AnsibleModule


def run_module():
    module_args = dict(
        action=dict(type='str', required=True),
        args=dict(type='list', required=False, elements='str'),
    )
    module = AnsibleModule(
        argument_spec=module_args
    )
    module.exit_json(**module.params)


def main():
    run_module()


if __name__ == '__main__':
    main()
