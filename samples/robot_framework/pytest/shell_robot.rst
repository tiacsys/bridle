.. _shell_robot:

===========
shell_robot
===========

.. contents:: `Contents`
    :depth: 2
    :local:

test:

    :ref:`bridle-test-rqt:SWRQT-VERSION_RQT`

.. item:: CZM_LUZERN-SHOULD_READ_VERSION Should Read Version
    :validates: :ref:`bridle-test-rqt:SWRQT-VERSION_RQT` SWRQT-OTHER_RQT
    :ext_toolname: SYSRQT-VERSION_SYSTEM_RQT

    Test that the Zephyr version is correct.
       Zephyr version 3.5.99

.. item:: CZM_LUZERN-CHECK_I2C_INTERFACE Check I2C Interface
    :validates: SWRQT-I2C_RQT
    :ext_toolname: SYSRQT-I2C_SYSTEM_RQT

    Test that the I2C bus is configured.
       i2c@40005400 (READY)


Traceability Matrix
===================

The below table traces the qualification test cases to the validates requirements.

.. item-matrix:: Linking these qualification test cases to the validates requirements
    :source: CZM_LUZERN-
    :target: SWRQT-
    :sourcetitle: Qualification test case
    :targettitle: validates requirement
    :type: validates
    :stats:
    :group: top
    :nocaptions:

The below table traces the qualification test cases to the ext_toolname requirements.

.. item-matrix:: Linking these qualification test cases to the ext_toolname requirements
    :source: CZM_LUZERN-
    :target: SYSRQT-
    :sourcetitle: Qualification test case
    :targettitle: ext_toolname requirement
    :type: ext_toolname
    :stats:
    :group: top
    :nocaptions:
