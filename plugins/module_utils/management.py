# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from abc import abstractmethod
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.radware.radware_alteon.plugins.module_utils.common import BaseAPI, RadwareModuleError, build_specs_from_annotation
try:
    from radware.sdk.exceptions import RadwareError
    from radware.sdk.beans_common import BaseBeanEnum
    from radware.sdk.common import get_type_hints, get_annotation_class
except ModuleNotFoundError:
    if __name__ == '__main__':
        AnsibleModule(argument_spec={}, check_invalid_arguments=False).fail_json(msg="The alteon-sdk package is required")


DOCUMENTATION = r'''
module: Device Management module
author:
  - Leon Meguira (@leonmeguira)
'''


class ManagementArgumentSpec(object):
    def __init__(self, mng_class):
        self.supports_check_mode = False
        command_spec = {"command": {"required": True, "choices": mng_class.api_function_names()}}
        self.argument_spec = {}
        self.argument_spec.update(command_spec)


class ManagementFunctionArgumentSpec(object):
    def __init__(self, mng_function):
        self.supports_check_mode = False
        self.argument_spec = {}
        self.argument_spec.update(build_specs_from_annotation(mng_function))


class ManagementModule(BaseAPI):
    def __init__(self, management_class, **kwargs):
        self._mng_instance = self._get_mng_class_instance(management_class)
        if 'command' in self._base.params:
            self._command = self._base.params['command']
        else:
            if 'command' in kwargs:
                self._command = kwargs.get('command')
            else:
                raise RadwareModuleError('missing management function name')

    @property
    @abstractmethod
    def _base(self):
        pass

    def exec_module(self, **kw):
        def translate(value, val_type):
            if issubclass(val_type, BaseBeanEnum):
                return val_type.enum(value)
            else:
                return value

        if self._command not in dir(self._mng_instance):
            raise RadwareModuleError(f'Management instance: {self._mng_instance} missing function: {self._command}')
        # try:
        #     self._device_mng.verify_device_accessible(retries=2)
        # except RadwareError as e:
        #     raise RadwareModuleError(e)

        try:
            func = getattr(self._mng_instance, self._command)
            if callable(func):
                annotations = get_type_hints(func)
                func_args = {}

                if annotations:
                    for k, v in annotations.items():
                        if k in self._base.params and self._base.params[k] is not None:
                            func_args.update({k: translate(self._base.params[k], get_annotation_class(annotations[k]))})
                        elif k in kw and kw[k] is not None:
                            func_args.update({k: translate(kw[k], get_annotation_class(annotations[k]))})

                func_result = func(**func_args)
            else:
                func_result = func
        except RadwareError as e:
            raise RadwareModuleError(e) from e

        # return dict(status=func_result)
        return {"status": func_result}

    def _get_mng_class_instance(self, mng_class):
        for k, v in self._device_mng.__dict__.items():
            if type(v) == mng_class:
                return v
        raise RadwareModuleError(f'unable to find SDK management class {mng_class}')
