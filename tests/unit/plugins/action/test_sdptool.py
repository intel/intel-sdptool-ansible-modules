from __future__ import (absolute_import, division, print_function)
from unittest import mock
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

    task_vars = {
        'inventory_hostname': 'testhost',
    }
    task_args = {
        'action': 'update'
    }
    try:
        args = ActionModule.supported_sdptool_args(task_args, task_vars)
        assert False
    except AnsibleError:
        assert True


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


def test_non_existent_cup_sup_file():
    zip_path = '/tmp/non_existent_sup_file.zip'
    task_vars = {
        'inventory_hostname': 'testhost',
        'ini_path': zip_path
    }
    task_args = {
        'action': 'cup_deploy'
    }
    try:
        ActionModule.supported_sdptool_args(task_args, task_vars)
        assert False
    except AnsibleError:
        assert True


def test_non_existent_custom_sup_file():
    zip_path = '/tmp/non_existent_sup_file.zip'
    task_vars = {
        'inventory_hostname': 'testhost'
    }
    task_args = {
        'action': 'custom_deploy'
    }
    try:
        ActionModule.supported_sdptool_args(task_args, task_vars)
        assert False
    except AnsibleError:
        assert True

    task_vars = {
        'inventory_hostname': 'testhost',
        'custom_sup_path': zip_path
    }
    try:
        ActionModule.supported_sdptool_args(task_args, task_vars)
        assert False
    except AnsibleError:
        assert True


def test_sdptoolcommand_without_action_arg():
    task_args = {
        'args': 'on'
    }
    try:
        ActionModule.check_task_args(task_args)
        assert False
    except AnsibleError:
        assert True


def test_supported_sdptool_args():
    task_vars = {
        'inventory_hostname': 'testhost'
    }
    task_args = {
        'action': 'set_biosconfig_all'
    }
    try:
        ActionModule.supported_sdptool_args(task_args, task_vars)
        assert False
    except AnsibleError:
        assert True

    task_vars = {
        'inventory_hostname': 'testhost'
    }
    task_args = {
        'action': 'vmedia'
    }
    try:
        ActionModule.supported_sdptool_args(task_args, task_vars)
        assert False
    except AnsibleError:
        assert True

    task_vars = {
        'inventory_hostname': 'testhost',
        'vmedia_iso_path': 'vmediaiso'
    }
    task_args = {
        'action': 'vmedia'
    }
    try:
        ActionModule.supported_sdptool_args(task_args, task_vars)
        assert True
    except AnsibleError:
        assert False


@mock.patch("sdptool.ActionModule._execute_module", return_value={'rc': 1})
def test_sdptool_installed(mock_obj):
    try:
        ActionModule(task='', connection='', play_context='', loader='', templar='', shared_loader_obj='').check_sdptool_installed(None, {})
        return False
    except Exception as e:
        return True


@mock.patch("sdptool.ActionModule._execute_module", return_value={'rc': 0})
def test_sdptool_installed1(mock_obj1):
    if ActionModule(task='', connection='', play_context='', loader='', templar='', shared_loader_obj='').check_sdptool_installed(None, {}):
        return True
    return False


class temp:
    def __init__(self) -> None:
        self.args = {
            'action': 'set_biosconfig'
        }


@mock.patch("sdptool.ActionModule._execute_module", return_value={'rc': 0, 'msg': 'success', 'failed': 'False', 'stdout_lines': "mocking success"})
@mock.patch("sdptool.ActionModule.check_pexpect_module")
@mock.patch("sdptool.ActionModule.check_sdptool_installed")
@mock.patch("sdptool.super")
def test_run(mock_super, mock_sdptool_installed, mock_pexpect, mock_execute):
    task_vars = {
        'inventory_hostname': '1.2.3.4',
        'bmc_username': 'uname',
        'bmc_password': 'passwordd'
    }
    test_dict = {'rc': 0, 'msg': 'success', 'failed': 'False', 'stdout_lines': 'mocking success'}
    try:
        return_dict = ActionModule(task=temp(), connection='', play_context='', loader='', templar='', shared_loader_obj='').run(None, task_vars)
        assert test_dict == return_dict
    except AnsibleError:
        assert False


@mock.patch("sdptool.super")
def test_run_without_credentials(mock_super):
    task_vars = {
        'inventory_hostname': '5.2.3.4'
    }
    try:
        ActionModule(task=temp(), connection='', play_context='', loader='', templar='', shared_loader_obj='').run(None, task_vars)
        assert False
    except AnsibleError:
        assert True
