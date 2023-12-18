#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2020, Radware LTD.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'certified'}

DOCUMENTATION = r'''
module: alteon_config_ha_service
short_description: Manage HA services in Radware Alteon
description:
  - Manage HA services in Radware Alteon
version_added: '1.0.0'
author:
  - Nofar Livkind (@nofarlivkind)
options:
  provider:
    description:
      - Radware Alteon connection details.
    type: dict
    required: true
    suboptions:
      server:
        description:
          - Radware Alteon IP.
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
      - When C(present), guarantees that the object exists with the provided attributes.
      - When C(absent), when applicable removes the object.
      - When C(read), when exists read object from configuration to parameter format.
      - When C(overwrite), removes the object if exists then recreate it
      - When C(append), append object configuration with the provided parameters
    type: str
    required: true
    default: null
    choices:
    - present
    - absent
    - read
    - overwrite
    - append
  revert_on_error:
    description:
      - If an error occurs, perform revert on alteon.
    required: false
    default: false
    type: bool
  write_on_change:
    description:
      - Executes Alteon write calls only when an actual change has been evaluated.
    required: false
    default: false
    type: bool
  parameters:
    description:
      - Parameters for Altoen HA services configuration.
    type: dict
    suboptions:
      index:
        description:
          - The service ID number in alphanumeric.
        required: true
        default: null
        type: str
      state:
        description:
          - The state of the HA group.
        required: false
        default: disabled
        choices:
        - enabled
        - disabled
      pref:
        description:
          - The preferred initial state.
        required: false
        default: standby
        choices:
        - active
        - standby
      failBackMode:
        description:
          - The fail back mode.
        required: false
        default: onfailure
        choices:
        - onfailure
        - always
      advertise_Interval:
        description:
          - The advertisement interval.
        required: false
        default: 1
        type: int
      interfaces:
        description:
          - List of IP interfaces for HA communication between the devices.
        required: false
        default: null
        type: list
        elements: int
      floating_IPs:
        description:
          - Floating IP index to add to the HA group.
        required: false
        default: null
        type: list
        elements: str
      vips:
        description:
          - VIP index to add to the HA group.
        required: false
        default: null
        type: list
        elements: str
      trig_gwtrck_state:
        description:
          - The Gateway tracking state.
        required: false
        default: disabled
        choices:
        - enabled
        - disabled
      trig_gwtrck_list:
        description:
          - The list of tracking interface.
        required: false
        default: null
        type: list
        elements: int
      trig_ifs_list:
        description:
          - The Gateway tracking list.
        required: false
        default: null
        type: list
        elements: int
      trig_reals_state:
        description:
          - Enable or disable real tracking.
        required: false
        default: disabled
        choices:
        - enabled
        - disabled
      trig_reals_list:
        description:
          - The list of real to HA group.
        required: false
        default: null
        type: list
        elements: str
notes:
  - Requires Radware alteon Python SDK.
requirements:
  - Radware alteon Python SDK.
'''

EXAMPLES = r'''
- name: alteon configuration command
  radware.radware_alteon.alteon_config_ha_service:
    provider:
      server: 192.168.1.1
      user: admin
      password: admin
      validate_certs: false
      https_port: 443
      ssh_port: 22
      timeout: 5
    state: present
    parameters:
      index: 1
      state: enabled
      pref: active
      failBackMode: always
      interfaces: 1 2
'''

RETURN = r'''
status:
  description: Message detailing run result
  returned: success
  type: str
  sample: object deployed successfully
obj:
  description: parameters object type
  returned: changed, read
  type: dict
'''

from ansible.module_utils.basic import AnsibleModule
import traceback

from ansible_collections.radware.radware_alteon.plugins.module_utils.common import RadwareModuleError
from ansible_collections.radware.radware_alteon.plugins.module_utils.alteon import AlteonConfigurationModule, \
    AlteonConfigurationArgumentSpec as ArgumentSpec
try:
    from radware.alteon.sdk.configurators.ha_service import HaServiceConfigurator
except ModuleNotFoundError:
    if __name__ == '__main__':
        module_args = {'parameters': {'type': 'dict', 'required': False},
                       'provider': {'type': 'dict', 'required': True},
                       'revert_on_error': {'required': False, 'type': 'bool', 'default': False},
                       'write_on_change': {'required': False, 'type': 'bool', 'default': False},
                       'state': {'required': True, 'choices': ['present', 'absent', 'read', 'overwrite', 'append']}
                       }
        module = AnsibleModule(argument_spec=module_args, check_invalid_arguments=False)
        module.fail_json(msg="The alteon-sdk package is required")


class ModuleManager(AlteonConfigurationModule):
    def __init__(self, **kwargs):
        super(ModuleManager, self).__init__(HaServiceConfigurator, **kwargs)


def main():
    spec = ArgumentSpec(HaServiceConfigurator)
    module = AnsibleModule(argument_spec=spec.argument_spec, supports_check_mode=spec.supports_check_mode)

    try:
        mm = ModuleManager(module=module)
        result = mm.exec_module()
        module.exit_json(**result)
    except RadwareModuleError as e:
        module.fail_json(msg=str(e), exception=traceback.format_exc())


if __name__ == '__main__':
    main()
