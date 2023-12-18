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
module: alteon_config_ssl_client_auth_policy
short_description: Manage SSL Authentication Policy in Radware Alteon
description:
  - SSL client authentication enables a server to confirm a client's identity as part of the SSL handshake process.
    Similarly, SSL server authentication enables a client to confirm the identity of the server. Authentication
    of a client or server requires checking their certificate validity. If the certificate is valid, the
    handshake process is completed, otherwise the session is terminated.
  - The same Authentication Policy can be associated with multiple SSL Policies.
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
      - Parameters for SSL Authentication Policy configuration.
    type: dict
    suboptions:
      index:
        description:
          - The authentication policy name (key id) as an index.
        required: true
        default: null
        type: str
      description:
        description:
          - An optional descriptive name of the policy in addition to the policy ID.
        required: false
        default: null
        type: str
      state:
        description:
          - Specifies whether to enable/disable the authentication policy.
        required: false
        default: null
        choices:
        - enabled
        - disabled
      ca_chain_lookup_depth:
        description:
          - Specifies the maximum number of certificates to be traversed in a certificate chain while attempting
            to validate the link between the certificate and the configured trusted CA.
        required: false
        default: 2
        type: int
      ca_verification:
        description:
          - Specifies whether to verify that a client certificate is trusted.
        required: false
        default: null
        choices:
        - enabled
        - disabled
      failure_redirection_url:
        description:
          - Specifies the URL to which a client should be redirected when its authentication fails.
        required: false
        default: null
        type: str
      trusted_ca_chain_name:
        description:
          - Trusted CA certificate name.
        required: false
        default: null
        type: str
      trusted_ca_chain_type:
        description:
          - Specifies one or more (group) Certificate Authority (CA) certificates that are trusted as issuers of
            regular (client/server) certificates.
        required: false
        default: null
        choices:
        - group
        - cert
      advertised_ca_chain_name:
        description:
          - Specifies the certificate authority name that should be included in the Certificate Request message,
            providing greater control over the configuration information shared with unknown clients.
        required: false
        default: null
        type: str
      advertised_ca_chain_type:
        description:
          - Advertised CA type
        required: false
        default: null
        choices:
        - group
        - cert
        - default
        - none
      cert_validation_method:
        description:
          - Specifies the method for validating whether a certificate, that was already validated as issued by a
            trusted entity, has not been revoked.
        required: false
        default: none
        choices:
        - none
        - ocsp
      ocsp_validation_static_uri:
        description:
          - Specifies the static URI for OCSP validation requests.
        required: false
        default: null
        type: str
      ocsp_uri_priority:
        description:
          - The OCSP access point can be configured (static URI) or can be provided in the certificate (in the
            Authority Information Access extension). The OCSP URI priority defines whether to check
            first if the location is provided in the certificate or not.
        required: false
        default: clientcert
        choices:
        - clientcert
        - staticuri
      ocsp_response_cache_time_second:
        description:
          - Specifies the length of time for which the OCSP response is cached, in seconds.
        required: false
        default: null
        type: int
      ocsp_response_deviation_time_second:
        description:
          - Allows to overlook small deviations, in seconds, between Alteon and OCSP server timestamps when
            performing OCSP signature verification.
        required: false
        default: 75
        type: int
      ocsp_cert_chain_validation:
        description:
          - Specifies whether to enable validation of every certificate in the certificate chain, or only of the
            authenticated element (client/server) certificate.
        required: false
        default: disabled
        choices:
        - enabled
        - disabled
      ocsp_response_secure:
        description:
          - Specifies whether to verify that the certificate status information received from the OCSP responder is
            up-to-date by sending a random nonce (a random sequence of 20 bytes) in the OCSP request. The OCSP
            responder must use its secret key to sign the response containing this nonce.
        required: false
        default: enabled
        choices:
        - enabled
        - disabled
      pass_cert_info_version_header_name:
        description:
          - Specifies the header name pass certificate version information to the back-end server.
        required: false
        default: CCRT-Version
        type: str
      pass_cert_info_version_header:
        description:
          - Specifies whether to pass certificate version information to the back-end server.
        required: false
        default: disabled
        choices:
        - enabled
        - disabled
      pass_cert_info_serial_number_header_name:
        description:
          - Specifies the header name pass certificate serial number to the back-end server.
        required: false
        default: CCRT-SN
        type: str
      pass_cert_info_serial_number_header:
        description:
          - Specifies whether to pass certificate serial number to the back-end server.
        required: false
        default: disabled
        choices:
        - enabled
        - disabled
      pass_cert_info_sign_algorithm_header_name:
        description:
          - Specifies the header name pass certificate Signature Algorithm to the back-end server.
        required: false
        default: CCRT-SignatureAlgo
        type: str
      pass_cert_info_sign_algorithm_header:
        description:
          - Specifies whether to pass certificate Signature Algorithm to the back-end server.
        required: false
        default: disabled
        choices:
        - enabled
        - disabled
      pass_cert_info_issuer_header_name:
        description:
          - Specifies the header name pass certificate issuer information to the back-end server.
        required: false
        default: CCRT-Issuer
        type: str
      pass_cert_info_issuer_header:
        description:
          - Specifies whether to pass certificate issuer information to the back-end server.
        required: false
        default: disabled
        choices:
        - enabled
        - disabled
      pass_cert_info_not_before_header_name:
        description:
          - Specifies the header name pass certificate Not Before Validity Date to the back-end server.
        required: false
        default: CCRT-NotBefore
        type: str
      pass_cert_info_not_before_header:
        description:
          - Specifies whether to pass certificate Not Before Validity Date to the back-end server.
        required: false
        default: disabled
        choices:
        - enabled
        - disabled
      pass_cert_info_not_after_header_name:
        description:
          - Specifies the header name pass certificate Not After Validity Date to the back-end server.
        required: false
        default: CCRT-NotAfter
        type: str
      pass_cert_info_not_after_header:
        description:
          - Specifies whether to pass certificate Not After Validity Date to the back-end server.
        required: false
        default: disabled
        choices:
        - enabled
        - disabled
      pass_cert_info_subject_header_name:
        description:
          - Specifies the header name pass certificate subject information to the back-end server.
        required: false
        default: CCRT-Subject
        type: str
      pass_cert_info_subject_header:
        description:
          - Specifies whether to pass certificate subject information to the back-end server.
        required: false
        default: disabled
        choices:
        - enabled
        - disabled
      pass_cert_info_public_key_type_header_name:
        description:
          - Specifies the header name pass certificate Public Key Type information to the back-end server.
        required: false
        default: CCRT-publicKeyType
        type: str
      pass_cert_info_public_key_type_header:
        description:
          - Specifies whether to pass certificate Public Key Type information to the back-end server.
        required: false
        default: disabled
        choices:
        - enabled
        - disabled
      pass_cert_info_md5_header_name:
        description:
          - Specifies the header name pass certificate MD5 hash information to the back-end server.
        required: false
        default: CCRT-MD5Hash
        type: str
      pass_cert_info_md5_header:
        description:
          - Specifies whether to pass certificate MD5 hash information information to the back-end server.
        required: false
        default: disabled
        choices:
        - enabled
        - disabled
      pass_cert_info_cert_header_name:
        description:
          - Specifies the header name pass certificate information to the back-end server.
        required: false
        default: CCRT-Certificate
        type: str
      pass_cert_info_cert_header:
        description:
          - Specifies whether to pass certificate information information to the back-end server.
        required: false
        default: disabled
        choices:
        - enabled
        - disabled
      pass_cert_info_2424ssl_compliance_header:
        description:
          - Specifies whether to enable 2424SSL Headers Compliance Mode.
        required: false
        default: disabled
        choices:
        - enabled
        - disabled
notes:
  - Requires the Radware alteon-sdk Python package on the host. This is as easy as
      C(pip3 install alteon-sdk)
requirements:
  - alteon-sdk
'''

EXAMPLES = r'''
- name: alteon configuration command
  radware.radware_alteon.alteon_config_ssl_client_auth_policy:
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
      index: ssl_server_auth_pol
      description: test_auth_policy
      state: enabled
      ca_verification: require
      advertised_ca_chain_type: default
      cert_validation_method: ocsp
      ocsp_validation_static_uri: http://uri.ocsp.com
      ocsp_response_secure: enabled
      trusted_ca_chain_name: ca_group_1
      trusted_ca_chain_type: group
      pass_cert_info_version_header_name: CCRT-ver
      pass_cert_info_version_header: enabled
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
    from radware.alteon.sdk.configurators.ssl_client_auth_policy import SSLClientAuthPolicyConfigurator
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
        super(ModuleManager, self).__init__(SSLClientAuthPolicyConfigurator, **kwargs)


def main():
    spec = ArgumentSpec(SSLClientAuthPolicyConfigurator)
    module = AnsibleModule(argument_spec=spec.argument_spec, supports_check_mode=spec.supports_check_mode)

    try:
        mm = ModuleManager(module=module)
        result = mm.exec_module()
        module.exit_json(**result)
    except RadwareModuleError as e:
        module.fail_json(msg=str(e), exception=traceback.format_exc())


if __name__ == '__main__':
    main()
