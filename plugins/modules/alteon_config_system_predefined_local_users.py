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
module: alteon_config_system_predefined_local_users
short_description: Manage predefined local users in Radware Alteon
description:
  - Manage predefined local users in Radware Alteon.
version_added: '1.0.0'
author:
  - Leon Meguira (@leonmeguira)
  - Nati Fridman (@natifridman)
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
      - When C(present), guarantees that the object exists with the provided attributes.
      - When C(absent), when applicable removes the object.
      - When C(read), when exists read object from configuration to parameter format.
      - When C(overwrite), removes the object if exists then recreate it
      - When C(append), append object configuration with the provided parameters
    required: true
    default: null
    type: str
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
      - Parameters for predefined local users configuration.
    type: dict
    suboptions:
      current_admin_password:
        description:
          - The character string representing the current administrator password.
        required: false
        default: null
        type: str
      new_admin_password:
        description:
          - New user admin password.
        required: false
        default: null
        type: str
      new_l4_admin_password:
        description:
          - New user l4 admin password.
        required: false
        default: null
        type: str
      new_slb_admin_password:
        description:
          - New user slb admin password.
        required: false
        default: null
        type: str
      new_webapp_admin_password:
        description:
          - New user webapp admin password.
        required: false
        default: null
        type: str
      new_oper_password:
        description:
          - New user oper password.
        required: false
        default: null
        type: str
      new_l4_oper_password:
        description:
          - New user l4 oper password.
        required: false
        default: null
        type: str
      new_slb_viewer_password:
        description:
          - New user slb viewer password.
        required: false
        default: null
        type: str
      new_user_password:
        description:
          - New user user password.
        required: false
        default: null
        type: str
      global_language_display:
        description:
          - Sets the Alteon Web Based Management (WBM) interface language for a local user.
        required: false
        default: english
        choices:
        - english
        - chinese
        - korean
        - japanese
      user_lockout_state:
        description:
          - Globally enables user lockout upon authentication failure (when the user enters incorrect password).
        required: false
        default: disabled
        choices:
        - enabled
        - disabled
      user_lock_login_failed_attempts:
        description:
          - The number of failed login attempts (entering an incorrect password) during the lockout reset duration time, before user lockout.
        required: false
        default: 5
        type: int
      user_lockout_login_duration_minute:
        description:
          - The number of minutes that a user remains locked out due to failed login attempts (in minutes).
        required: false
        default: 10
        type: int
      user_lockout_login_reset_duration_minute:
        description:
          - The number of minutes within which failed login attempts must occur in order for the use to be locked out.
        required: false
        default: 10
        type: int
notes:
  - Requires the Radware alteon-sdk Python package on the host. This is as easy as
      C(pip3 install alteon-sdk)
requirements:
  - alteon-sdk
'''

EXAMPLES = r'''
- name: alteon configuration command
  radware.radware_alteon.alteon_config_system_predefined_local_users:
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
      current_admin_password: admin
      new_admin_password: radware
      new_slb_admin_password: radware
      new_l4_oper_password: radware
      new_slb_viewer_password: radware
      global_language_display: japanese
      user_lockout_state: enabled
      user_lock_login_failed_attempts: 5
      user_lockout_login_duration_minute: 20
      user_lockout_login_reset_duration_minute: 20
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
    from radware.alteon.sdk.configurators.system_predefined_local_users import PredefinedLocalUsersConfigurator
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
        super(ModuleManager, self).__init__(PredefinedLocalUsersConfigurator, **kwargs)


def main():
    spec = ArgumentSpec(PredefinedLocalUsersConfigurator)
    module = AnsibleModule(argument_spec=spec.argument_spec, supports_check_mode=spec.supports_check_mode)

    try:
        mm = ModuleManager(module=module)
        result = mm.exec_module()
        module.exit_json(**result)
    except RadwareModuleError as e:
        module.fail_json(msg=str(e), exception=traceback.format_exc())


if __name__ == '__main__':
    main()
