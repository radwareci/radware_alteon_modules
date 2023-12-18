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
module: alteon_config_l3_interface
short_description: Manage l3 interface in Radware Alteon
description:
  - Alteon needs an IP interface for each subnet to which it is connected so it can communicate with the real servers and other devices
    attached to it that receive switching services.
  - Alteon can be configured with up to 256 IP interfaces. Each IP interface represents Alteon on an IP subnet on your network.
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
      - Parameters for l3 interafce configuration.
    type: dict
    suboptions:
      index:
        description:
          - Interface ID.
        required: true
        default: null
        type: int
      description:
        description:
          - Interface description.
        required: false
        default: null
        type: str
      ip4_address:
        description:
          - IPv4 address.
        required: false
        default: null
        type: str
      ip4_subnet:
        description:
          - IPv4 subnet mask.
        required: false
        default: null
        type: str
      vlan:
        description:
          - VLAN ID.
        required: false
        default: null
        type: int
      state:
        description:
          - Gateway state.
        required: false
        default: enabled
        choices:
        - enabled
        - disabled
      bootp_relay:
        description:
          - Specifies whether to enable BOOTP relay.
          - In the DHCP environment, Alteon acts as a relay agent.
          - This BOOTP relay feature enables Alteon to forward a client request for an IP address to two BOOTP servers with configured IP addresses.
        required: false
        default: enabled
        choices:
        - enabled
        - disabled
      ip_ver:
        description:
          - IP version.
        required: false
        default: ipv4
        choices:
        - ipv4
        - ipv6
      ip6_address:
        description:
          - IPv6 address.
        required: false
        default: null
        type: str
      ip6_prefix:
        description:
          - IPv6 prefix.
        required: false
        default: null
        type: str
      peer_ip:
        description:
          - The peer interface IP address used in high availability unicast session failover.
          - Radware recommends that you configure a peer IP address for all IP interfaces participating in session failover.
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
- name: alteon configuration command
  radware.radware_alteon.alteon_config_l3_interface:
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
      index: 10
      state: enabled
      ip4_address: 8.8.8.8
      ip_ver: ipv4
      vlan: 10
      bootp_relay: enabled
      peer_ip: 8.8.8.9
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
    from radware.alteon.sdk.configurators.l3_interface import L3InterfaceConfigurator
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
        super(ModuleManager, self).__init__(L3InterfaceConfigurator, **kwargs)


def main():
    spec = ArgumentSpec(L3InterfaceConfigurator)
    module = AnsibleModule(argument_spec=spec.argument_spec, supports_check_mode=spec.supports_check_mode)

    try:
        mm = ModuleManager(module=module)
        result = mm.exec_module()
        module.exit_json(**result)
    except RadwareModuleError as e:
        module.fail_json(msg=str(e), exception=traceback.format_exc())


if __name__ == '__main__':
    main()
