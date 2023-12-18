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
module: alteon_config_system_vx_peer_sync
short_description: Manage VX peer sync in Radware Alteon
description:
  - Manage VX peer sync in Radware Alteon.
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
      - Parameters for VX peer sync configuration.
    type: dict
    suboptions:
      auto_sync:
        description:
          - The vADC ID.
        required: false
        default: enabled
        choices:
        - enabled
        - disabled
      sync_authentication_mode:
        description:
          - Enable authentication passphrase.
        required: false
        default: null
        choices:
        - admin
        - passphrase
      sync_authentication_passphrase:
        description:
          - Authentication Passphrase.
        required: false
        default: null
        type: str
      peer_switches:
        description:
          - Peer Switch configuration.
        required: false
        default: null
        type: list
        elements: dict
        suboptions:
          id:
            description:
              - Peer Switch ID.
            required: true
            default: null
            type: int
          ip4_address:
            description:
              - The IP address of the peer switch.
            required: false
            default: null
            type: str
          ip6_address:
            description:
              - The IP address of the peer switch.
            required: false
            default: null
            type: str
          ip_ver:
            description:
              - The IP version of the Peer Switch Address.
            required: false
            default: null
            choices:
            - ipv4
            - ipv6
          state:
            description:
              - Specifies whether the peer is enabled.
            required: false
            default: disabled
            choices:
            - enabled
            - disabled
          vadc_ids:
            description:
              - vADC ID.
            required: false
            default: null
            type: list
            elements: int
notes:
  - Requires the Radware alteon-sdk Python package on the host. This is as easy as
      C(pip3 install alteon-sdk)
requirements:
  - alteon-sdk
'''

EXAMPLES = r'''
- name: alteon configuration command
  radware.radware_alteon.alteon_config_system_vx_peer_sync:
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
      auto_sync: enabled
      sync_authentication_mode: passphrase
      sync_authentication_passphrase: secret_123
      peer_switches:
        - id: 2
          state: enabled
          ip4_address: 8.8.8.8
          vadc_ids:
            - 4
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
    from radware.alteon.sdk.configurators.system_vx_peer_syncronization import VXPeerSyncConfigurator
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
        super(ModuleManager, self).__init__(VXPeerSyncConfigurator, **kwargs)


def main():
    spec = ArgumentSpec(VXPeerSyncConfigurator)
    module = AnsibleModule(argument_spec=spec.argument_spec, supports_check_mode=spec.supports_check_mode)

    try:
        mm = ModuleManager(module=module)
        result = mm.exec_module()
        module.exit_json(**result)
    except RadwareModuleError as e:
        module.fail_json(msg=str(e), exception=traceback.format_exc())


if __name__ == '__main__':
    main()
