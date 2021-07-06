from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import sys
path = os.path.dirname(os.path.realpath(__file__))
path = '/'.join(path.replace('\\', '/').split('/')[:-4] + ['plugins', 'action'])
sys.path.append(path)

from sdptool import ActionModule
from ansible.errors import AnsibleError


def test_sel_path():
    task_vars = {
        'inventory_hostname': 'testhost'
    }
    expected_path = '/tmp/[testhost]_sel.log'
    received_path = ActionModule.change_path('/tmp/sel.log', task_vars)
    assert expected_path == received_path


def test_unsupported_command():
    task_vars = {
        'inventory_hostname': 'testhost'
    }
    unsupported_action = ['getini', 'getbiosoptions', 'setoptions', 'deployoptions']
    task_args = {}
    for action in unsupported_action:
        task_args['action'] = action
        try:
            ActionModule.supported_sdptool_args(task_args, task_vars)
            assert False
        except AnsibleError:
            assert True


def test_update_args():
    sup_path = '/tmp/temp_sup'
    task_vars = {
        'inventory_hostname': 'testhost',
        'sup_path': sup_path
    }
    task_args = {
        'action': 'update'
    }
    os.mkdir(sup_path)
    expected_return = [sup_path]
    try:
        args = ActionModule.supported_sdptool_args(task_args, task_vars)
        os.rmdir(sup_path)
        assert expected_return == args
    except AnsibleError:
        os.rmdir(sup_path)
        assert False


def test_set_biosconfig_all_args():
    ini_path = '/tmp/temp_syscfg.INI'
    task_vars = {
        'inventory_hostname': 'testhost',
        'ini_path': ini_path
    }
    task_args = {
        'action': 'set_biosconfig_all'
    }
    with open(ini_path, 'w') as f:
        f.write('Test Content')
    expected_return = [ini_path]
    try:
        args = ActionModule.supported_sdptool_args(task_args, task_vars)
        os.remove(ini_path)
        assert expected_return == args
    except AnsibleError:
        os.remove(ini_path)
        assert False


def test_sel_cmd():
    task_vars = {
        'inventory_hostname': 'testhost'
    }
    task_args = {
        'action': 'sel',
        'args': '-c'
    }
    expected_return = ['-c']
    try:
        args = ActionModule.process_additional_args(task_args, task_vars)
        assert expected_return == args
    except AnsibleError:
        assert False


def test_sel_cmd_with_file():
    task_vars = {
        'inventory_hostname': 'testhost'
    }
    task_args = {
        'action': 'sel',
        'args': ['-f', 'test.log']
    }
    expected_return = ['-f', '"[testhost]_test.log"']
    try:
        args = ActionModule.process_additional_args(task_args, task_vars)
        assert expected_return == args
    except AnsibleError:
        assert False


def test_unsupported_task_args():
    task_args = {
        'play': 'value',                    # not valid task arg
        'action': 'cpuinfo',
        'args': '-no_reboot'
    }
    try:
        ActionModule.check_task_args(task_args)
        assert False
    except AnsibleError:
        assert True


def test_non_existent_ini_file():
    ini_path = '/tmp/invalid-syscfg-file.INI'
    task_vars = {
        'inventory_hostname': 'testhost',
        'ini_path': ini_path
    }
    task_args = {
        'action': 'set_biosconfig_all'
    }
    expected_return = [ini_path]
    try:
        args = ActionModule.supported_sdptool_args(task_args, task_vars)
        assert expected_return != args
    except AnsibleError:
        assert True
