====================================
Radware.Radware_Alteon Release Notes
====================================

.. contents:: Topics


v1.1.0
======

Minor Changes
-------------

- AL-13206 - add option to configure hname for virtual service.

Bugfixes
--------

- fix AL-141408 - Module alteon_config_ha_config_sync - incorrect parameters in sync_peer state.
- fix AL-141799 - Module alteon_software_vadc_default is not working on certified collection.
- fix lint errors.

New Modules
-----------

- radware.radware_alteon.alteon_config_secure_path_policy - create and manage secure path policy in Radware Alteon
- radware.radware_alteon.alteon_config_security_global - Manage security global parameters in Radware Alteon
- radware.radware_alteon.alteon_config_sideband_policy - create and manage sideband policy in Radware Alteon

v1.0.2
======

Minor Changes
-------------

- Add ansible lint to CI pipeline

v1.0.1
======

Minor Changes
-------------

- Fix as needed for ansible lint

v1.0.0
======

Major Changes
-------------

- Add initial modules
