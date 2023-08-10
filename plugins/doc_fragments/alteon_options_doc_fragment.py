# -*- coding: utf-8 -*-
#
# Copyright: (c) 2023, Radware LTD.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


class ModuleDocFragment(object):
    # Standard documentation
    DOCUMENTATION = r'''
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
            type: str
          user:
            description:
              - Radware Alteon username.
            required: true
            default: null
            type: str
          password:
            description:
              - Radware Alteon password.
            required: true
            default: null
            type: str
            aliases:
            - pass
            - pwd
          validate_certs:
            description:
              - If C(no), SSL certificates will not be validated.
              - This should only set to C(no) used on personally controlled sites using self-signed certificates.
            required: true
            default: null
            type: bool
          https_port:
            description:
              - Radware Alteon https port.
            required: true
            default: null
            type: int
          ssh_port:
            description:
              - Radware Alteon ssh port.
            required: true
            default: null
            type: int
          timeout:
            description:
              - Timeout for connection.
            required: true
            default: null
            type: int
    notes:
    - Requires the Radware alteon-sdk Python package on the host. This is as easy as
        C(pip3 install alteon-sdk)
    requirements:
      - alteon-sdk
    '''

    # Additional section
    OTHER = r'''
    options:
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
    '''

    # Additional section
    STATE_TYPE1 = r'''
    options:
      state:
        description:
          - When C(present), guarantees that the object exists with the provided attributes.
          - When C(absent), when applicable removes the object.
          - When C(read), when exists read object from configuration to parameter format.
          - When C(overwrite), removes the object if exists then recreate it.
        required: true
        default: null
        type: str
        choices:
        - present
        - absent
        - read
        - overwrite
        - append
    '''

    # Additional section
    STATE_TYPE2 = r'''
    options:
      state:
        description:
          - When C(present), guarantees that the object exists with the provided attributes.
          - When C(absent), when applicable removes the object.
          - When C(read), when exists read object from configuration to parameter format.
          - When C(overwrite), removes the object if exists then recreate it. This state can be used only before applying the entry.
            If the entry was already applied you must delete, apply and recreate the entry.
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
    '''
