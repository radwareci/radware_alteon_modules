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
module: alteon_oper_ha_backup
short_description: Set Alteon to HA backup
description:
  - Set Alteon instance to HA backup
  - Validate HA state
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
  validate_backup_state:
    description:
      - when C(true) validate device in no longer in master state
      - when C(false) no ha state validation
    required: false
    default: no
    type: bool
notes:
  - Requires the Radware alteon-sdk Python package on the host. This is as easy as
      C(pip3 install alteon-sdk)
requirements:
  - alteon-sdk
'''

EXAMPLES = r'''
- name: alteon set ha backup
  radware.radware_alteon.alteon_oper_ha_backup:
    provider:
      server: 192.168.1.1
      user: admin
      password: admin
      validate_certs: false
      https_port: 443
      ssh_port: 22
      timeout: 5
    validate_backup_state: true
'''

RETURN = r'''
status:
  description: Message detailing run result
  returned: success
  type: str
  sample: HA peer state set to backup successfully
'''

from ansible.module_utils.basic import AnsibleModule
import traceback

from ansible_collections.radware.radware_alteon.plugins.module_utils.common import RadwareModuleError
from ansible_collections.radware.radware_alteon.plugins.module_utils.alteon import AlteonManagementModule, \
    AlteonManagementFunctionArgumentSpec
try:
    from radware.alteon.sdk.alteon_managment import AlteonMngOper
except ModuleNotFoundError:
    if __name__ == '__main__':
        module_args = {'provider': {'type': 'dict', 'required': True},
                       'validate_backup_state': {'required': False, 'type': 'bool', 'default': False}
                       }
        module = AnsibleModule(argument_spec=module_args, check_invalid_arguments=False)
        module.fail_json(msg="The alteon-sdk package is required")


class ArgumentSpecs(AlteonManagementFunctionArgumentSpec):
    def __init__(self):
        super().__init__(AlteonMngOper.set_ha_backup)


class ModuleManager(AlteonManagementModule):
    def __init__(self, **kwargs):
        super(ModuleManager, self).__init__(AlteonMngOper, command='set_ha_backup', **kwargs)

    def exec_module(self):
        res = super().exec_module()
        if res['status']:
            res['status'] = 'HA peer state set to Backup successfully'
        else:
            res['status'] = 'HA peer state is not Master'
        return res


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
