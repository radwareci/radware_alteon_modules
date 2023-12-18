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
module: alteon_mng_device_reboot
short_description: Perform Alteon reboot
description:
  - Perform Alteon reboot with stateful option (device return)
version_added: '1.0.0'
author:
  - Leon Meguira (@leonmeguira)
  - Nati Fridman (@natifridman)
options:
  provider:
    description:
      - Radware Alteon connection details.
    required: true
    type: dict
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
  command:
    description:
      - Action to run.
    required: true
    default: null
    type: str
    choices:
    - reboot
    - reboot_stateful
  timeout_seconds:
    description:
      - Stateful Reboot timeout in seconds.
    required: false
    default: 600
    type: int
  fail_on_pending_cfg:
    description:
      - will not reboot the device if there is pending configuration
    required: false
    default: false
    type: bool
notes:
  - Requires the Radware alteon-sdk Python package on the host. This is as easy as
      C(pip3 install alteon-sdk)
requirements:
  - alteon-sdk
'''

EXAMPLES = r'''
- name: alteon device reboot
  radware.radware_alteon.alteon_mng_device_reboot:
    provider:
      server: 192.168.1.1
      user: admin
      password: admin
      validate_certs: false
      https_port: 443
      ssh_port: 22
      timeout: 5
    command: reboot
    timeout_seconds: 300
'''

RETURN = r'''
status:
  description: Message detailing run result
  returned: success
  type: str
  sample: Device Reset
'''

from ansible.module_utils.basic import AnsibleModule
import traceback

from ansible_collections.radware.radware_alteon.plugins.module_utils.common import RadwareModuleError
from ansible_collections.radware.radware_alteon.plugins.module_utils.alteon import \
    AlteonManagementFunctionArgumentSpec, AlteonManagementModule, fail_on_pending_arg_spec
try:
    from radware.alteon.sdk.alteon_managment import AlteonMngOper
except ModuleNotFoundError:
    if __name__ == '__main__':
        module_args = {'provider': {'type': 'dict', 'required': True},
                       'command': {'required': True, 'choices': ['reboot', 'reboot_stateful']},
                       'timeout_seconds': {'type': 'int', 'required': False, 'default': 600},
                       'fail_on_pending_cfg': {'type': 'bool', 'required': False, 'default': False}
                       }
        module = AnsibleModule(argument_spec=module_args, check_invalid_arguments=False)
        module.fail_json(msg="The alteon-sdk package is required")


class ModuleManager(AlteonManagementModule):
    def __init__(self, **kwargs):
        super(ModuleManager, self).__init__(AlteonMngOper, **kwargs)


def main():
    spec = AlteonManagementFunctionArgumentSpec(AlteonMngOper.reboot_stateful, AlteonMngOper.reboot)
    fail_on_pending_arg_spec(spec.argument_spec)
    module = AnsibleModule(argument_spec=spec.argument_spec, supports_check_mode=spec.supports_check_mode)

    try:
        mm = ModuleManager(module=module)
        result = mm.exec_module()
        result['changed'] = True
        module.exit_json(**result)
    except RadwareModuleError as e:
        module.fail_json(msg=str(e), exception=traceback.format_exc())


if __name__ == '__main__':
    main()
