.. _gs_installing:

Installing |BRIDLE| manually
############################

.. contents::
   :local:
   :depth: 2

The recommended way to get started with |BRIDLE| is to use the Desktop
Installer. See the :ref:`gs_assistant` section for information about how
to install |BRIDLE| through Desktop Installer for Desktop.

.. note::

   If you use the Desktop Installer to install |BRIDLE|, you can skip
   this section of the documentation. If you prefer to install the
   toolchain manually, or if you run into problems during the installation
   process, see the following documentation for instructions.

To manually install |BRIDLE|, you must install all required tools and clone
the |BRIDLE| repositories. See the following sections for detailed instructions.

The first two steps, :ref:`gs_installing_tools` and
:ref:`gs_installing_toolchain`, are similar to the installation steps in
Zephyr's :zephyr:ref:`getting_started`. If you already have your system set up
to work with the Zephyr OS, you can skip these steps.

See :ref:`gs_installing_os` for information on the supported operating systems
and Zephyr features.

.. _gs_installing_tools:

.. rst-class:: numbered-step

Installing the required tools
*****************************

The current minimum required version for the main dependencies are:

.. list-table::
   :header-rows: 1

   * - Tool
     - Min. Version
   * - |python|_
     - |python_min_ver|
   * - |cmake|_
     - |cmake_min_ver|
   * - |dtc|_
     - |dtc_min_ver|

The installation process is different depending on your operating system.

.. tabs::

   .. group-tab:: Linux

      .. _install_dependencies_linux:

      If using an Ubuntu version older than 24.04, it is necessary to add extra
      repositories to meet the minimum required Python version listed above.
      In that case inspect, evaluate and then apply the `Deadsnakes PPA`_ from
      Canonical Launchpad:

         .. container:: highlight highlight-console notranslate

            .. parsed-literal::

               sudo add-apt-repository ppa:deadsnakes/ppa
               sudo apt update
               sudo apt install |python_bin|\ -dev |python_bin|\ -tk |python_bin|\ -venv

      To install the required tools on Ubuntu, complete the following steps:

      .. tsn-include:: develop/getting_started/index.rst
         :docset: zephyr
         :dedent: 6
         :start-after: .. _install_dependencies_ubuntu:
         :end-before: .. group-tab:: macOS

      For additional information and instructions for other Linux operating
      systems, see the :zephyr:ref:`linux_requirements` section in the Zephyr
      documentation.

   .. group-tab:: macOS

      .. _install_dependencies_macos:

      To install the required tools on macOS, complete the following steps:

      .. tsn-include:: develop/getting_started/index.rst
         :docset: zephyr
         :dedent: 6
         :start-after: .. _install_dependencies_macos:
         :end-before: .. group-tab:: Windows

      Also see :zephyr:ref:`mac-setup-alts` for additional information.

   .. group-tab:: Windows

      .. note::

         Due to issues finding executables or have easy access to USB devices,
         both the |ZEPHYR| and |TIAC| |BRIDLE| doesn't currently support
         application flashing using the `Windows Subsystem for Linux (WSL)
         <https://msdn.microsoft.com/en-us/commandline/wsl/install_guide>`_
         (WSL).

         **Therefore, we don't recommend using WSL when getting started!**

      In modern version of Windows (10 and later) it is recommended to install
      the Windows Terminal application from the Microsoft Store. Instructions
      are provided for a ``cmd.exe`` or PowerShell command prompts.

      .. _install_dependencies_windows:

      The recommended way for installing the required tools on Windows is
      to use `winget`_, Windows' official package manager. WinGet installs
      the tools so that you can use them from a Windows command prompt. If
      using WinGet isn't an option, you can either use the third party and
      also well known alternative package manager `Chocolatey`_ in similar
      way or you can install dependencies from their respective websites and
      ensure the command line tools are on your :envvar:`PATH`
      :zephyr:ref:`environment variable <env_vars>`.

      To install the required tools on Windows, complete the following steps:

      .. tsn-include:: develop/getting_started/index.rst
         :docset: zephyr
         :dedent: 6
         :start-after: .. _install_dependencies_windows:
         :end-before: .. _winget:

.. _gs_installing_toolchain:

.. rst-class:: numbered-step

Installing the toolchain
************************

.. important::

   Make sure to install the version that is mentioned below.
   Other versions might not work with this version of |BRIDLE|.
   Refere the :ref:`list of required tools <req_tools_table>`
   for the correct and tested version!

   Note that other versions of |BRIDLE| might require a different
   toolchain version.

.. _gs_toolchain_zephyr_sdk_install:

Preferred default toolchain
===========================

To be able to cross-compile your applications for all the various target
architectures, you must install at least version |zephyrsdk_recommended_ver|
of the |zephyrsdk|_. Refere the :ref:`list of required tools <req_tools_table>`
for the correct and tested version!

To set up the toolchain, complete the following steps (refere also Zephyr's
documentation in ":zephyr:ref:`toolchain_zephyr_sdk_install`"):

.. _toolchain_setup:

#. Download the `Zephyr SDK`_ bundle for your operating system.

      .. list-table::
         :header-rows: 1

         * - Operating System
           - Minimum version
           - Tested version
         * - Linux
           - |zephyrsdk_min_ver|
           - |zephyrsdk_recommended_ver_linux|
         * - macOS
           - |zephyrsdk_min_ver|
           - |zephyrsdk_recommended_ver_macos|
         * - Windows
           - |zephyrsdk_min_ver|
           - |zephyrsdk_recommended_ver_win10|

#. Extract the bundle into a folder of your choice. We recommend to use the
   folder ``/opt`` on Linux or macOS and ``%PROGRAMFILES%`` on Windows.

   Make sure that the folder name does not contain any spaces or special
   characters.

#. Run the Zephyr SDK setup script found in this new folder: ``setup.sh`` on
   Linux or macOS and ``setup.cmd`` on Windows.

There are no further configuration steps required when compiling, as the
Zephyr SDK is the preferred toolchain used by Bridle.

Alternative toolchain for ARM
=============================

.. _gs_toolchain_arm_gnu_install:

Arm GNU toolchain
-----------------

To be able to cross-compile your applications for ARM targets, you can use at
least version |armgnutc_recommended_ver| of the |armgnutc|_ too. The |armgnutc|
is the successor to the |gnuarmemb|, which has been considered obsolete since
2022 and should no longer be used.
Refere the :ref:`list of required tools <req_tools_table>` for the correct
and tested version!

For installation and handling of the |armgnutc| with Zephyr, the same steps
apply as for the |gnuarmemb|. From Zephyr's point of view, only the name has
changed. Therefore the same variable prefixes will be used (``GNUARMEMB``).
For more details, see the section :zephyr:ref:`toolchain_gnuarmemb` in the
Zephyr documentation.

To set up the toolchain, complete the following steps:

#. Download the `Arm GNU Toolchain`_ for your operating system.

      .. list-table::
         :header-rows: 1

         * - Operating System
           - Minimum version
           - Tested version
         * - Linux
           - |armgnutc_min_ver|
           - |armgnutc_recommended_ver_linux|
         * - macOS
           - |armgnutc_min_ver|
           - |armgnutc_recommended_ver_macos|
         * - Windows
           - |armgnutc_min_ver|
           - |armgnutc_recommended_ver_win10|

#. Extract the toolchain into a folder of your choice. We recommend to use the
   folder ``~/gnuarmemb`` on Linux or macOS and ``c:\gnuarmemb`` on Windows.

   Make sure that the folder name does not contain any spaces or special
   characters.

#. If you want to build and program applications from the command line, define
   the environment variables for the *Arm GNU toolchain*. Depending on your
   operating system:

    .. tabs::

       .. group-tab:: Linux

          Open a terminal window and enter the following commands (assuming that
          you have installed the toolchain to ``~/gnuarmemb``; if not, change
          the value for ``GNUARMEMB_TOOLCHAIN_PATH``):

             .. code-block::

                export ZEPHYR_TOOLCHAIN_VARIANT=gnuarmemb
                export GNUARMEMB_TOOLCHAIN_PATH="${HOME}/gnuarmemb"

       .. group-tab:: macOS

          Open a terminal window and enter the following commands (assuming that
          you have installed the toolchain to ``~/gnuarmemb``; if not, change
          the value for ``GNUARMEMB_TOOLCHAIN_PATH``):

             .. code-block::

                export ZEPHYR_TOOLCHAIN_VARIANT=gnuarmemb
                export GNUARMEMB_TOOLCHAIN_PATH="${HOME}/gnuarmemb"

       .. group-tab:: Windows

          Open a command prompt and enter the following commands (assuming that
          you have installed the toolchain to ``c:\gnuarmemb``; if not, change
          the value for ``GNUARMEMB_TOOLCHAIN_PATH``):

             .. code-block::

                set ZEPHYR_TOOLCHAIN_VARIANT=gnuarmemb
                set GNUARMEMB_TOOLCHAIN_PATH=c:\gnuarmemb

.. _gs_toolchain_persistent_environment:

#. Set the environment variables persistently.
   Depending on your operating system:

    .. tabs::

       .. group-tab:: Linux

          Define the environment variables in the ``~/.zephyrrc`` file as
          described in :ref:`build_environment`. This will allow you to avoid
          setting them every time you open a terminal window.

       .. group-tab:: macOS

          Define the environment variables in the ``~/.zephyrrc`` file as
          described in :ref:`build_environment`. This will allow you to avoid
          setting them every time you open a terminal window.

       .. group-tab:: Windows

          Add the environment variables as system environment variables or
          define them in the ``%userprofile%\zephyrrc.cmd`` file as described
          in :ref:`build_environment`. This will allow you to avoid setting
          them every time you open a command prompt.

.. _gs_toolchain_gnu_arm_embedded_install:

GNU Arm Embedded toolchain
--------------------------

.. warning:: Obsolete and depricated since 2022! Do not use for new products.

To be able to cross-compile your applications for ARM targets, you can use
at least version |gnuarmemb_recommended_ver| of the |gnuarmemb|_ too. Refere
the :ref:`list of required tools <req_tools_table>` for the correct and tested
version!

For installation and handling of the |gnuarmemb| with Zephyr, the same steps
apply as for the |armgnutc|. For more details, see the section
:zephyr:ref:`toolchain_gnuarmemb` in the Zephyr documentation. The |gnuarmemb|
is the discontinued predecessor of the |armgnutc| and should no longer be used.

To set up the toolchain, complete the steps above for |armgnutc|.

   .. list-table::
      :header-rows: 1

      * - Operating System
        - Minimum version
        - Tested version
      * - Linux
        - |gnuarmemb_min_ver|
        - |gnuarmemb_recommended_ver_linux|
      * - macOS
        - |gnuarmemb_min_ver|
        - |gnuarmemb_recommended_ver_macos|
      * - Windows
        - |gnuarmemb_min_ver|
        - |gnuarmemb_recommended_ver_win10|

.. _gs_toolchain_stm32cubeclt_install:
.. _gs_toolchain_gnu_tools_for_stm32_install:

STM32CubeCLT (GNU tools for STM32)
----------------------------------

.. warning:: Special vendor specific toolchain for STM32 by STMicroelectronics.

To be able to cross-compile your applications for ARM targets or feel better
to use a special vendor toolchain for STM32 based platforms maintained by
STMicroelectronics, you can use at least version |stm32cubeclt_recommended_ver|
of the |stm32cubeclt|_ too.
Refere the :ref:`list of required tools <req_tools_table>` for the correct and
tested version!

The |stm32cubeclt| is an all-in-one multi-OS command-line toolset, which is
part of the STM32Cube ecosystem. It is a toolset for third-party integrated
development environment (IDE) providers, allowing the use of STMicroelectronics
proprietary tools within their own IDE frameworks.

For installation the |stm32cubeclt|, see the accompanying original documentation
by STMicroelectronics. For handling the |stm32cubeclt| with Zephyr you have to
choose the same way as for other common cross-compilers. For more details, see
the section :zephyr:ref:`other_x_compilers` in the Zephyr documentation.

To set up the toolchain, complete the following steps:

#. Download the `STM32CubeCLT (GNU tools for STM32)`_ for your operating system.

      .. list-table::
         :header-rows: 1

         * - Operating System
           - Minimum version
           - Tested version
         * - Linux
           - |stm32cubeclt_min_ver|
           - |stm32cubeclt_recommended_ver_linux|
         * - macOS
           - |stm32cubeclt_min_ver|
           - |stm32cubeclt_recommended_ver_macos|
         * - Windows
           - |stm32cubeclt_min_ver|
           - |stm32cubeclt_recommended_ver_win10|

#. Extract the toolchain into a folder of your choice. We recommend to use the
   default as specified by STMicroelectronics, folder ``/opt/st/stm32cubeclt``
   on Linux, ``/Applications/STM32CubeCLT`` on macOS and ``C:\ST\STM32CubeCLT``
   on Windows.

   Make sure that the folder name does not contain any spaces or special
   characters.

#. If you want to build and program applications from the command line, define
   the environment variables for the *GNU tools for STM32*. Depending on your
   operating system:

    .. tabs::

       .. group-tab:: Linux

          Open a terminal window and enter the following commands (assuming that
          you have installed the toolchain to ``/opt/st/stm32cubeclt``; if not,
          change the value for ``CROSS_COMPILE``):

             .. code-block::

                export ZEPHYR_TOOLCHAIN_VARIANT=cross-compile
                export CROSS_COMPILE="/opt/st/stm32cubeclt/GNU-tools-for-STM32/bin/arm-none-eabi-"

       .. group-tab:: macOS

          Open a terminal window and enter the following commands (assuming that
          you have installed the toolchain to ``/Applications/STM32CubeCLT``; if
          not, change the value for ``CROSS_COMPILE``):

             .. code-block::

                export ZEPHYR_TOOLCHAIN_VARIANT=cross-compile
                export CROSS_COMPILE="/Applications/STM32CubeCLT/GNU-tools-for-STM32/bin/arm-none-eabi-"

       .. group-tab:: Windows

          Open a command prompt and enter the following commands (assuming that
          you have installed the toolchain to ``C:\ST\STM32CubeCLT``; if not,
          change the value for ``CROSS_COMPILE``):

             .. code-block::

                set ZEPHYR_TOOLCHAIN_VARIANT=cross-compile
                set CROSS_COMPILE="C:\ST\STM32CubeCLT\GNU-tools-for-STM32\bin\arm-none-eabi-"

#. Set the environment variables persistently, proceed as described above for
   the :ref:`Arm GNU Toolchain <gs_toolchain_persistent_environment>`.

.. _gs_toolchain_mcuxpressoide_install:
.. _gs_toolchain_mcuxpressoide_arm_gnu_install:

MCUXpresso IDE (Arm GNU Toolchain)
----------------------------------

.. warning:: Special vendor specific toolchain for General Purpose MCU by NXP.

To be able to cross-compile your applications for ARM targets or feel better
to use a special vendor toolchain for i.MX (RT), Kinetis or LPC based platforms
maintained by NXP, you can use at least version |mcuxpressoide_recommended_ver|
of the |mcuxpressoide|_ too.
Refere the :ref:`list of required tools <req_tools_table>` for the correct and
tested version!

The |mcuxpressoide| is the default integrated development environment for NXP
MCUs based on Arm Cortex-M cores and comes with a rich set of tools for debug
and compilation based on the standard :ref:`gs_toolchain_arm_gnu_install`.

For installation the |mcuxpressoide|, see the accompanying original documentation
by NXP. For handling the |mcuxpressoide| with Zephyr you have to choose the same
way as for other common cross-compilers. For more details, see the section
:zephyr:ref:`other_x_compilers` in the Zephyr documentation.

To set up the toolchain, complete the following steps:

#. Download the `MCUXpresso IDE (Arm GNU Toolchain)`_ for your operating system.

      .. list-table::
         :header-rows: 1

         * - Operating System
           - Minimum version
           - Tested version
         * - Linux
           - |mcuxpressoide_min_ver|
           - |mcuxpressoide_recommended_ver_linux|
         * - macOS
           - |mcuxpressoide_min_ver|
           - |mcuxpressoide_recommended_ver_macos|
         * - Windows
           - |mcuxpressoide_min_ver|
           - |mcuxpressoide_recommended_ver_win10|

#. Extract the toolchain into a folder of your choice. We recommend to use the
   default as specified by NXP, folder ``/usr/local/mcuxpressoide`` on Linux,
   ``/Applications/MCUXpressoIDE`` on macOS and ``C:\NXP\MCUXpressoIDE``
   on Windows.

   Make sure that the folder name does not contain any spaces or special
   characters.

#. If you want to build and program applications from the command line, define
   the environment variables for the *Arm GNU Toolchain*. Depending on your
   operating system:

    .. tabs::

       .. group-tab:: Linux

          Open a terminal window and enter the following commands (assuming that
          you have installed the toolchain to ``/usr/local/mcuxpressoide``; if not,
          change the value for ``CROSS_COMPILE``):

             .. code-block::

                export ZEPHYR_TOOLCHAIN_VARIANT=cross-compile
                export CROSS_COMPILE="/usr/local/mcuxpressoide/ide/tools/bin/arm-none-eabi-"

       .. group-tab:: macOS

          Open a terminal window and enter the following commands (assuming that
          you have installed the toolchain to ``/Applications/MCUXpressoIDE``; if
          not, change the value for ``CROSS_COMPILE``):

             .. code-block::

                export ZEPHYR_TOOLCHAIN_VARIANT=cross-compile
                export CROSS_COMPILE="/Applications/MCUXpressoIDE/ide/tools/bin/arm-none-eabi-"

       .. group-tab:: Windows

          Open a command prompt and enter the following commands (assuming that
          you have installed the toolchain to ``C:\NXP\MCUXpressoIDE``; if not,
          change the value for ``CROSS_COMPILE``):

             .. code-block::

                set ZEPHYR_TOOLCHAIN_VARIANT=cross-compile
                set CROSS_COMPILE="C:\NXP\MCUXpressoIDE\ide\tools\bin\arm-none-eabi-"

#. Set the environment variables persistently, proceed as described above for
   the :ref:`Arm GNU Toolchain <gs_toolchain_persistent_environment>`.

.. _cloning_the_repositories_win:
.. _cloning_the_repositories:

.. rst-class:: numbered-step

Getting the |BRIDLE| code
*************************

|BRIDLE| consists of a set of Git repositories. Every |BRIDLE| release consists
of a combination of these repositories at different revisions. The revision of
each of those repositories is determined by the current revision of the main
(or manifest) repository, `tiac-bridle`_.

.. note::

   The latest state of development is on the main branch of the `tiac-bridle`_
   repository. To ensure a usable state, the `tiac-bridle`_ repository defines
   the compatible states of the other repositories. However, this state is not
   necessarily tested. For a higher degree of quality assurance, check out a
   tagged release.

   Therefore, unless you are familiar with the development process, you should
   always work with a specific release of |BRIDLE|.

To manage the combination of repositories and versions, |BRIDLE|
uses :zephyr:ref:`west`. The main repository, `tiac-bridle`_, contains
a `west manifest file`_, :file:`west.yml`, that determines the revision
of all other repositories. This means that *bridle* acts as the
:zephyr:ref:`manifest repository <west-manifests>`, while the other
repositories are project repositories.

You can find additional information about the repository and development
model in the :ref:`development model section <dev-model>`.

See the :zephyr:ref:`west documentation <west>` for detailed information
about the tool itself.

.. _gs_setup_pyvenv:

.. rst-class:: numbered-step

Setup Python Virtual Environment
================================

**Create a new and complet empty workspace directory** (e.g. :ugn:`workspace`),
change into this new folder and execute:

.. tabs::

   .. group-tab:: Linux

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            |python_bin| -m venv --clear --copies --prompt="$(basename $(pwd))[$(|python_bin| --version)]" .env
            source .env/bin/activate
            |pip_bin| install --upgrade pip
            |pip_bin| install --upgrade setuptools

   .. group-tab:: macOS

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            |python_bin| -m venv --clear --copies --prompt="$(basename $(pwd))[$(|python_bin| --version)]" .env
            source .env/bin/activate
            |pip_bin| install --upgrade pip
            |pip_bin| install --upgrade setuptools

   .. group-tab:: Windows

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            for /f "delims=" %A in ('|python_bin| --version') do set PV=%A
            |python_bin| -m venv --clear --copies --prompt="%CD%[%PV%]" .env
            .env\Scripts\activate
            |pip_bin| install --upgrade pip
            |pip_bin| install --upgrade setuptools

.. _gs_installing_west:

.. rst-class:: numbered-step

Installing west
===============

Install west by entering the following command:

.. tabs::

   .. group-tab:: Linux

         .. container:: highlight highlight-console notranslate

            .. parsed-literal::

               |pip_bin| install west

   .. group-tab:: macOS

         .. container:: highlight highlight-console notranslate

            .. parsed-literal::

               |pip_bin| install west

   .. group-tab:: Windows

         .. container:: highlight highlight-console notranslate

            .. parsed-literal::

               |pip_bin| install west

You only need to do this once.

.. _west_update:

Like any other Python package, the west tool is updated regularly.
Therefore, remember to regularly check for updates:

.. tabs::

   .. group-tab:: Linux

         .. container:: highlight highlight-console notranslate

            .. parsed-literal::

               |pip_bin| install --upgrade west

   .. group-tab:: macOS

         .. container:: highlight highlight-console notranslate

            .. parsed-literal::

               |pip_bin| install --upgrade west

   .. group-tab:: Windows

         .. container:: highlight highlight-console notranslate

            .. parsed-literal::

               |pip_bin| install --upgrade west

.. _cloning_with_west:

.. rst-class:: numbered-step

Cloning the repositories
========================

To clone the repositories, complete the following steps:

#. Open a command window and **go into the workspace directory** (e.g.
   :ugn:`workspace`). This folder will hold all |BRIDLE| repositories
   together with the Python Virtual Environment that is already created
   and setup as described above.

#. Determine what revision of |BRIDLE| you want to work with. The recommended
   way is to work with a specific release.

   * To work with a specific release, the revision is the corresponding
     tag (for example, |release_tt|). You can find the tag in the
     :ref:`release_notes` of the release.
   * To work with a development tag, the revision is the corresponding
     tag (for example, ``1.0.99-dev1``)
   * To work with a branch, the revision is the branch name (for example,
     ``main`` to work with the latest state of development).
   * To work with a specific state, the revision is the SHA (for example,
     ``4b44408145d4843f2bf13952a7723680240d0f95``).

#. Initialize west with the revision of |BRIDLE| that you want to check out,
   replacing :ird:`BRIDLE_revision` with the revision:

   .. container:: highlight highlight-console notranslate

      .. parsed-literal::

         west init -m https\://github.com/tiacsys/bridle --mr :ird:`BRIDLE_revision`

   For example, to check out the |release_em| release, enter the following command:

   .. container:: highlight highlight-console notranslate

      .. parsed-literal::

         west init -m https\://github.com/tiacsys/bridle --mr |release_em|

   To check out the :brd:`latest state of development`, enter the following command:

   .. container:: highlight highlight-console notranslate

      .. parsed-literal::

         west init -m https\://github.com/tiacsys/bridle --mr :brd:`main`

   .. west-error-start

   .. note::

      If you get an error message when running west,
      :ref:`update west <west_update>` to the latest version. See
      :zephyr:ref:`west-troubleshooting` if you need more information.

      .. west-error-end

      Initializing west with a specific revision of the manifest file does not
      lock your repositories to this version. Checking out a different branch
      or tag in the `tiac-bridle`_ repository and running ``west update``
      changes the version of |BRIDLE| that you work with.

   This will clone the manifest repository `tiac-bridle`_ into :file:`bridle`.

#. Enter the following command to clone the project repositories:

   .. container:: highlight highlight-console notranslate

      .. parsed-literal::

         west update

#. Export the :zephyr:ref:`Zephyr CMake package <cmake_pkg>` and also for
   |BRIDLE|. This allows CMake to automatically load the boilerplate code
   required for building |BRIDLE| applications:

   .. container:: highlight highlight-console notranslate

      .. parsed-literal::

         west zephyr-export
         west bridle-export

Your directory structure now looks similar to this:

   .. parsed-literal::
      :class: highlight-console notranslate

      :ugn:`workspace`
       ├── :ibl:`.env`
       ├── :ibl:`.west`
       ├── :brd:`bridle`
       ├── modules
       │   ├── fs
       │   │   ├── fatfs
       │   │   └── ...
       │   ├── hal
       │   │   ├── altera
       │   │   ├── cmsis
       │   │   ├── espressif
       │   │   ├── stm32
       │   │   ├── xtensa
       │   │   └── ...
       │   ├── lib
       │   │   ├── canopennode
       │   │   └── ...
       │   └── ...
       ├── tools
       │   ├── net-tools
       │   └── ...
       ├── ...
       ├── :brd:`zephyr`
       └── ...

Note that there are additional folders, and that the structure might change.
The full set of repositories and folders is defined in the manifest file.

.. _updating_with_west:

.. rst-class:: numbered-step

Updating the repositories
=========================

If you work with a specific release of |BRIDLE|, you do not need to
update your repositories, because the release will not change. However,
you might want to switch to a newer release or check out the latest state
of development.

To manage the ``bridle`` repository (the manifest repository), use Git.
To make sure that you have the latest changes, run ``git fetch origin``
to :ref:`fetch the latest code <dm-wf-update-bridle>` from the `tiac-bridle`_
repository. Checking out a branch or tag in the ``bridle`` repository
gives you a different version of the manifest file. Running ``west update``
will then update the project repositories to the state specified in this
manifest file.

.. include:: gs_installing.rst
   :start-after: west-error-start
   :end-before: west-error-end

For example, to switch to release |release_em| of |BRIDLE|, enter the
following commands in the :ugn:`workspace/bridle` directory:

   .. container:: highlight highlight-console notranslate

      .. parsed-literal::

         git fetch origin
         git checkout |release_em|
         west update

To update to :brd:`a particular revision (SHA)`, make sure that you have that
particular revision locally before you check it out (by running
``git fetch origin``):

   .. container:: highlight highlight-console notranslate

      .. parsed-literal::

         git fetch origin
         git checkout :brd:`4b44408145d4843f2bf13952a7723680240d0f95`
         west update

To switch to the :brd:`latest state of development`, enter the
following commands:

   .. container:: highlight highlight-console notranslate

      .. parsed-literal::

         git fetch origin
         git checkout :brd:`origin/main`
         west update

   .. note::

      Run ``west update`` every time you change or modify the current
      working branch (for example, when you pull, rebase, or check out
      a different branch). This will bring the project repositories to
      the matching revision defined by the manifest file.

.. _additional_deps:

.. rst-class:: numbered-step

Installing additional Python dependencies
*****************************************

The |BRIDLE| requires additional Python packages to be installed.

Use the following commands to install the requirements for each repository.

.. tabs::

   .. group-tab:: Linux

      Open a terminal window in the :ugn:`workspace` folder and
      enter the following commands:

         .. container:: highlight highlight-console notranslate

            .. parsed-literal::

               |pip_bin| install --upgrade --requirement zephyr/scripts/requirements.txt
               |pip_bin| install --upgrade --requirement bridle/scripts/requirements.txt

   .. group-tab:: macOS

      Open a terminal window in the :ugn:`workspace` folder and
      enter the following commands:

         .. container:: highlight highlight-console notranslate

            .. parsed-literal::

               |pip_bin| install --upgrade --requirement zephyr/scripts/requirements.txt
               |pip_bin| install --upgrade --requirement bridle/scripts/requirements.txt

   .. group-tab:: Windows

      Open a command prompt in the :ugn:`workspace` folder and
      enter the following commands:

         .. container:: highlight highlight-console notranslate

            .. parsed-literal::

               |pip_bin| install --upgrade --requirement zephyr\\scripts\\requirements.txt
               |pip_bin| install --upgrade --requirement bridle\\scripts\\requirements.txt

.. _installing_tbd:

.. rst-class:: numbered-step

Installing ... t.b.d. (TBD) IDE
*******************************

t.b.d.

.. _build_environment:

.. rst-class:: numbered-step

Setting up the build environment
********************************

Before you start
:ref:`building and programming a sample application <gs_programming>`,
you must set up your build environment.

.. _setting_up_tbd:

.. rst-class:: numbered-step

Setting up the ... t.b.d. (TBD) IDE environment
===============================================

t.b.d.

Setting up executables
======================

The process is different depending on your operating system.

.. tabs::

   .. group-tab:: Linux

      Make sure the locations of tools are added to the PATH variable.
      On Linux, ... t.b.d. (TBD) IDE uses the PATH variable to find
      executables if they are not set in ... t.b.d. (TBD) IDE.

   .. group-tab:: macOS

      If you start ... t.b.d. (TBD) IDE on macOS by running the file
      :file:`bin/tbdIDE`, make sure to complete the following steps:

      #. Specify the path to all executables under ... t.b.d.
      #. Specify the ... t.b.d.

      If you start ... t.b.d. (TBD) IDE from the command line, it uses the
      global PATH variable to find the executables. You do not need to
      explicitly configure the executables in ... t.b.d. (TBD) IDE.

      Regardless of how you start ... t.b.d. (TBD) IDE, if you get an error
      that a tool or command cannot be found, first make sure that the tool
      is installed. If it is installed, verify that its path is configured
      correctly in the ... t.b.d. (TBD) IDE settings or in the PATH variable.

   .. group-tab:: Windows

      Make sure the locations of tools are added to the PATH variable.
      On Windows, ... t.b.d. (TBD) IDE uses the PATH variable to find
      executables if they are not set in ... t.b.d. (TBD) IDE.

.. _build_environment_cli:

.. rst-class:: numbered-step

Setting up the command line build environment
=============================================

If you want to build and program your application from the command line,
you must set up your build environment by defining the required environment
variables every time you open a new command prompt or terminal window.

See :zephyr:ref:`env_vars` and :zephyr:ref:`important-build-vars` information
about the various relevant environment variables.

Define the required environment variables as follows, depending on your
operating system:

.. tabs::

   .. group-tab:: Linux

      Navigate to the :ugn:`workspace` folder and enter the following command:
      ``source zephyr/zephyr-env.sh``

      If you need to define additional environment variables, create the file
      ``~/.zephyrrc`` and add the variables there. This file is loaded
      automatically when you run the above command.

   .. group-tab:: macOS

      Navigate to the :ugn:`workspace` folder and enter the following command:
      ``source zephyr/zephyr-env.sh``

      If you need to define additional environment variables, create the file
      ``~/.zephyrrc`` and add the variables there. This file is loaded
      automatically when you run the above command.

   .. group-tab:: Windows

      Navigate to the :ugn:`workspace` folder and enter the following command:
      ``zephyr\zephyr-env.cmd``

      If you need to define additional environment variables, create the file
      ``%userprofile%\zephyrrc.cmd`` and add the variables there. This file is
      loaded automatically when you run the above command.
