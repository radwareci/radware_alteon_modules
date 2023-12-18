#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2020, Radware LTD.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['stableinterface'],
                    'supported_by': 'certified'}

DOCUMENTATION = r'''
module: alteon_software_install_vadc
short_description: Install software image on vadc
description:
  - Install software image on Alteon device
  - applicable on VX
version_added: '1.0.0'
author:
  - Leon Meguira (@leonmeguira)
options:
  provider:
    description:
      - Radware Alteon connection details.
    type: dict
    required: true
    suboptions:
      server:
        description:
          - Radware Alteon IP address.
        required: true
        default: null
      user:
        description:
          - Radware Alteon username.
        required: true
        default: null
      password:
        description:
          - Radware Alteon password.
        required: true
        default: null
      validate_certs:
        description:
          - If C(false), SSL certificates will not be validated.
          - This should only set to C(false) used on personally controlled sites using self-signed certificates.
        required: true
        default: null
        type: bool
      https_port:
        description:
          - Radware Alteon https port.
        required: true
        default: null
      ssh_port:
        description:
          - Radware Alteon ssh port.
        required: true
        default: null
      timeout:
        description:
          - Timeout for connection.
        required: true
        default: null
  state:
    description:
      - When C(installed), ensure the vadc software installed on the device and the is set to be booted
        from. the vadcs are not rebooted into the new software if needed.
      - When C(activated), performs the same operation as C(installed), but the vadcs are rebooted into the new software
    type: str
    required: false
    default: activated
    choices:
      - installed
      - activated
  version:
    description:
      - software version
    required: true
    default: null
    type: str
  vadc_id:
    description:
      - vadc id
    required: true
    default: null
    type: int
  reboot_wait:
    description:
      - when C(yes) wait for vadc to return after reboot.
      - when C(no) no wait for vadc to return after reboot
    required: false
    default: yes
    type: bool
  reboot_timeout:
    description:
      - Stateful Reboot timeout in seconds.
    required: false
    default: 180
    type: int
  vadc_user:
    description:
      - vadc login user name for software installation validation
      - if unspecified, vx login user is used
    required: false
    default: null
    type: str
  vadc_password:
    description:
      - vadc login password for software installation validation
      - if unspecified, vx login password is used
    required: false
    default: null
    type: str
notes:
  - Requires the Radware alteon-sdk Python package on the host. This is as easy as
      C(pip3 install alteon-sdk)
requirements:
  - alteon-sdk
'''

EXAMPLES = r'''
- name: alteon software installation on vadc
  radware.radware_alteon.alteon_software_install_vadc:
    provider:
      server: 192.168.1.1
      user: admin
      password: admin
      validate_certs: false
      https_port: 443
      ssh_port: 22
      timeout: 5
    state: activated
    vadc_id: 2
    version: 31.0.10.50
    reboot_timeout: 180
'''

RETURN = r'''
status:
  description: Message detailing run result
  returned: success
  type: str
  sample: Software Installed successfully
'''

from ansible.module_utils.basic import AnsibleModule
import traceback

from ansible_collections.radware.radware_alteon.plugins.module_utils.common import RadwareModuleError
from ansible_collections.radware.radware_alteon.plugins.module_utils.alteon import AlteonManagementModule, AlteonManagementFunctionArgumentSpec
try:
    from radware.alteon.sdk.alteon_managment import AlteonMngOper
except ModuleNotFoundError:
    if __name__ == '__main__':
        module_args = {'provider': {'type': 'dict', 'required': True},
                       'state': {'required': False, 'choices': ['installed', 'activated'], 'default': 'activated'},
                       'version': {'required': True, 'type': 'str'},
                       'reboot_wait': {'required': False, 'type': 'bool', 'default': True},
                       'reboot_timeout': {'required': False, 'type': 'int', 'default': 180},
                       'vadc_id': {'required': True, 'type': 'int'},
                       'vadc_user': {'required': False, 'type': 'str'},
                       'vadc_password': {'required': False, 'type': 'str', 'no_log': True},
                       }
        module = AnsibleModule(argument_spec=module_args, check_invalid_arguments=False)
        module.fail_json(msg="The alteon-sdk package is required")


class ArgumentSpecs(AlteonManagementFunctionArgumentSpec):
    def __init__(self):
        super().__init__(AlteonMngOper.software_install_vadc)
        self.argument_spec.update(state=dict(
            choices=['installed', 'activated'],
            default='activated'
        ))


class ModuleManager(AlteonManagementModule):
    def __init__(self, **kwargs):
        super(ModuleManager, self).__init__(AlteonMngOper, command='software_install_vadc', **kwargs)

    def exec_module(self):
        if self.params['state'] == 'installed':
            res = super().exec_module(reboot=False)
            mode = 'Installed'
        else:
            res = super().exec_module(reboot=True)
            mode = 'Activated'

        if res['status']:
            return dict(status=f'Software {mode} successfully', changed=True)
        else:
            return dict(status=f'No Software {mode}', changed=False)


def main():
    spec = ArgumentSpecs()
    module = AnsibleModule(argument_spec=spec.argument_spec, supports_check_mode=spec.supports_check_mode)

    try:
        mm = ModuleManager(module=module)
        result = mm.exec_module()
        module.exit_json(**result)
    except RadwareModuleError as e:
        module.fail_json(msg=str(e), exception=traceback.format_exc())


if __name__ == '__main__':
    main()
