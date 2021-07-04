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
Zephyr's :ref:`zephyr:getting_started`. If you already have your system set up
to work with the Zephyr OS, you can skip these steps.

See :ref:`gs_installing_os` for information on the supported operating systems
and Zephyr features.

.. _gs_installing_tools:

.. rst-class:: numbered-step

Installing the required tools
*****************************

The installation process is different depending on your operating system.

.. tabs::

   .. group-tab:: Windows

      The recommended way for installing the required tools on Windows is
      to use `Chocolatey`_, a package manager for Windows. Chocolatey installs
      the tools so that you can use them from a Windows command prompt.

      To install the required tools, complete the following steps:

      .. tsn-include:: getting_started/index.rst
         :docset: zephyr
         :dedent: 6
         :start-after: .. _install_dependencies_windows:
         :end-before: _get_the_code:

   .. group-tab:: Linux

      To install the required tools on Ubuntu, complete the following steps:

      .. tsn-include:: getting_started/index.rst
         :docset: zephyr
         :dedent: 6
         :start-after: .. _install_dependencies_ubuntu:
         :end-before: group-tab:: macOS

      For additional information and instructions for other Linux operating
      systems, see the :ref:`zephyr:linux_requirements` section in the Zephyr
      documentation.

      .. note::

         You do not need to install the Zephyr SDK. We recommend
	 to install the compiler toolchain separately, as detailed
	 in :ref:`gs_installing_toolchain`.

         **But you can still using the ready-to-use, full-featured, and
	 multiple-arch-supported Zephyr SDK in parallel!**

   .. group-tab:: macOS

      To install the required tools on macOS, complete the following steps:

      .. tsn-include:: getting_started/index.rst
         :docset: zephyr
         :dedent: 6
         :start-after: .. _install_dependencies_macos:
         :end-before: group-tab:: Windows

      Also see :ref:`zephyr:mac-setup-alts` for additional information.

.. _gs_installing_toolchain:

.. rst-class:: numbered-step

Installing the toolchain
************************

To be able to cross-compile your applications for ARM targets, you must install
version **10-2020-q4-major** of the `GNU Arm Embedded Toolchain`_.

.. important::

   Make sure to install the version that is mentioned above.
   Other versions might not work with this version of |BRIDLE|.

   Note that other versions of |BRIDLE| might require a different
   toolchain version.

To set up the toolchain, complete the following steps:

.. _toolchain_setup:

#. Download the `GNU Arm Embedded Toolchain`_ for your operating system.

#. Extract the toolchain into a folder of your choice. We recommend to use the
   folder ``c:\gnuarmemb`` on Windows and ``~/gnuarmemb`` on Linux or macOS.

   Make sure that the folder name does not contain any spaces or special
   characters.

#. If you want to build and program applications from the command line, define
   the environment variables for the *GNU Arm Embedded toolchain*. Depending on
   your operating system:

    .. tabs::

       .. group-tab:: Windows

          Open a command prompt and enter the following commands (assuming that
          you have installed the toolchain to ``c:\gnuarmemb``; if not, change
          the value for GNUARMEMB_TOOLCHAIN_PATH):

            .. parsed-literal::
               :class: highlight

               set ZEPHYR_TOOLCHAIN_VARIANT=gnuarmemb
               set GNUARMEMB_TOOLCHAIN_PATH=\ c:\\gnuarmemb

       .. group-tab:: Linux

          Open a terminal window and enter the following commands (assuming that
          you have installed the toolchain to ``~/gnuarmemb``; if not, change
          the value for GNUARMEMB_TOOLCHAIN_PATH):

            .. parsed-literal::
              :class: highlight

              export ZEPHYR_TOOLCHAIN_VARIANT=gnuarmemb
              export GNUARMEMB_TOOLCHAIN_PATH=\ "~/gnuarmemb"

       .. group-tab:: macOS

          Open a terminal window and enter the following commands (assuming that
          you have installed the toolchain to ``~/gnuarmemb``; if not, change
          the value for GNUARMEMB_TOOLCHAIN_PATH):

            .. parsed-literal::
              :class: highlight

              export ZEPHYR_TOOLCHAIN_VARIANT=gnuarmemb
              export GNUARMEMB_TOOLCHAIN_PATH=\ "~/gnuarmemb"

#. Set the environment variables persistently.
   Depending on your operating system:

    .. tabs::

       .. group-tab:: Windows

          Add the environment variables as system environment variables or
          define them in the ``%userprofile%\zephyrrc.cmd`` file as described
          in :ref:`build_environment`. This will allow you to avoid setting
          them every time you open a command prompt.

       .. group-tab:: Linux

          Define the environment variables in the ``~/.zephyrrc`` file as
          described in :ref:`build_environment`. This will allow you to avoid
          setting them every time you open a terminal window.

       .. group-tab:: macOS

          Define the environment variables in the ``~/.zephyrrc`` file as
          described in :ref:`build_environment`. This will allow you to avoid
          setting them every time you open a terminal window.

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
uses :ref:`zephyr:west`. The main repository, `tiac-bridle`_, contains
a `west manifest file`_, :file:`west.yml`, that determines the revision
of all other repositories. This means that *bridle* acts as the
:ref:`manifest repository <zephyr:west-manifests>`, while the other
repositories are project repositories.

You can find additional information about the repository and development
model in the :ref:`development model section <dev-model>`.

See the :ref:`west documentation <zephyr:west>` for detailed information
about the tool itself.

.. _gs_setup_pyvenv:

.. rst-class:: numbered-step

Setup Python Virtual Environment
================================

**Create a new and complet empty workspace directory** (e.g. ``workspace``),
change into this new folder and execute:

.. tabs::

   .. group-tab:: Windows

      .. parsed-literal::
         :class: highlight

         for /f "delims=" %A in ('python --version') do set PV=%A
         python -m venv --clear --copies --prompt="%CD%[%PV%]" .env
         .env\Scripts\activate
         python -m pip install --upgrade pip
         python -m pip install --upgrade setuptools

   .. group-tab:: Linux

      .. parsed-literal::
         :class: highlight

         python3 -m venv --clear --copies --prompt="$(basename $(pwd))[$(python3 --version)]" .env
         source .env/bin/activate
         pip3 install --upgrade pip
         pip3 install --upgrade setuptools

   .. group-tab:: macOS

      .. parsed-literal::
         :class: highlight

         python3 -m venv --clear --copies --prompt="$(basename $(pwd))[$(python3 --version)]" .env
         source .env/bin/activate
         pip3 install --upgrade pip
         pip3 install --upgrade setuptools

.. _gs_installing_west:

.. rst-class:: numbered-step

Installing west
===============

Install west by entering the following command:

.. tabs::

   .. group-tab:: Windows

      .. parsed-literal::
         :class: highlight

         pip3 install west

   .. group-tab:: Linux

      .. parsed-literal::
         :class: highlight

         pip3 install west

   .. group-tab:: macOS

      .. parsed-literal::
         :class: highlight

         pip3 install west

You only need to do this once.

.. _west_update:

Like any other Python package, the west tool is updated regularly.
Therefore, remember to regularly check for updates:

.. tabs::

   .. group-tab:: Windows

      .. parsed-literal::
         :class: highlight

         pip3 install --upgrade  west

   .. group-tab:: Linux

      .. parsed-literal::
         :class: highlight

         pip3 install --upgrade  west

   .. group-tab:: macOS

      .. parsed-literal::
         :class: highlight

         pip3 install --upgrade  west

.. _cloning_with_west:

.. rst-class:: numbered-step

Cloning the repositories
========================

To clone the repositories, complete the following steps:

#. Open a command window and **go into the workspace directory.** This folder
   will hold all |BRIDLE| repositories together with the Python Virtual
   Environment that is already created and setup as described above.

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
   replacing *BRIDLE_revision* with the revision:

   .. parsed-literal::
      :class: highlight

      west init -m https\://github.com/tiacsys/bridle --mr *BRIDLE_revision*

   For example, to check out the |release| release, enter the following command:

   .. parsed-literal::
      :class: highlight

      west init -m https\://github.com/tiacsys/bridle --mr |release|

   To check out the latest state of development, enter the following command:

   .. parsed-literal::
      :class: highlight

      west init -m https\://github.com/tiacsys/bridle --mr main

   .. west-error-start

   .. note::

      If you get an error message when running west,
      :ref:`update west <west_update>` to the latest version. See
      :ref:`zephyr:west-troubleshooting` if you need more information.

      .. west-error-end

      Initializing west with a specific revision of the manifest file does not
      lock your repositories to this version. Checking out a different branch
      or tag in the `tiac-bridle`_ repository and running ``west update``
      changes the version of |BRIDLE| that you work with.

   This will clone the manifest repository `tiac-bridle`_ into :file:`bridle`.

#. Enter the following command to clone the project repositories:

   .. parsed-literal::
      :class: highlight

      west update

#. Export a :ref:`Zephyr CMake package <zephyr:cmake_pkg>`. This allows CMake
   to automatically load the boilerplate code required for building |BRIDLE|
   applications:

   .. parsed-literal::
      :class: highlight

      west zephyr-export

Your directory structure now looks similar to this::

   workspace
    ├── .env
    ├── .west
    ├── bridle
    ├── modules
    │   ├── fs
    │   │   └── fatfs
    │   ├── hal
    │   │   ├── altera
    │   │   ├── cmsis
    │   │   ├── espressif
    │   │   ├── stm32
    │   │   └── xtensa
    │   └── lib
    │       └── canopennode
    ├── tools
    │   └── net-tools
    ├── zephyr
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

For example, to switch to release |release| of |BRIDLE|, enter the
following commands in the ``workspace/bridle`` directory:

.. parsed-literal::
   :class: highlight

   git fetch origin
   git checkout |release|
   west update

To update to a particular revision (SHA), make sure that you have that
particular revision locally before you check it out (by running
``git fetch origin``):

.. parsed-literal::
   :class: highlight

   git fetch origin
   git checkout 4b44408145d4843f2bf13952a7723680240d0f95
   west update

To switch to the latest state of development, enter the
following commands:

.. parsed-literal::
   :class: highlight

   git fetch origin
   git checkout origin/main
   west update

.. note::

   Run ``west update`` every time you change or modify the current working
   branch (for example, when you pull, rebase, or check out a different
   branch). This will bring the project repositories to the matching revision
   defined by the manifest file.

.. _additional_deps:

.. rst-class:: numbered-step

Installing additional Python dependencies
*****************************************

The |BRIDLE| requires additional Python packages to be installed.

Use the following commands to install the requirements for each repository.

.. tabs::

   .. group-tab:: Windows

      Open a command prompt in the ``workspace`` folder and
      enter the following commands:

        .. parsed-literal::
           :class: highlight

           pip3 install --upgrade --requirement zephyr\\scripts\\requirements.txt
           pip3 install --upgrade --requirement bridle\\scripts\\requirements.txt

   .. group-tab:: Linux

      Open a terminal window in the ``workspace`` folder and
      enter the following commands:

        .. parsed-literal::
           :class: highlight

           pip3 install --upgrade --requirement zephyr/scripts/requirements.txt
           pip3 install --upgrade --requirement bridle/scripts/requirements.txt

   .. group-tab:: macOS

      Open a terminal window in the ``workspace`` folder and
      enter the following commands:

        .. parsed-literal::
           :class: highlight

           pip3 install --upgrade --requirement zephyr/scripts/requirements.txt
           pip3 install --upgrade --requirement bridle/scripts/requirements.txt

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

   .. group-tab:: Windows

      Make sure the locations of tools are added to the PATH variable.
      On Windows, ... t.b.d. (TBD) IDE uses the PATH variable to find
      executables if they are not set in ... t.b.d. (TBD) IDE.

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

.. _build_environment_cli:

.. rst-class:: numbered-step

Setting up the command line build environment
=============================================

If you want to build and program your application from the command line,
you must set up your build environment by defining the required environment
variables every time you open a new command prompt or terminal window.

See :ref:`zephyr:env_vars` and :ref:`zephyr:important-build-vars` information
about the various relevant environment variables.

Define the required environment variables as follows, depending on your
operating system:

.. tabs::

   .. group-tab:: Windows

      Navigate to the ``workspace`` folder and enter the following command:
      ``zephyr\zephyr-env.cmd``

      If you need to define additional environment variables, create the file
      ``%userprofile%\zephyrrc.cmd`` and add the variables there. This file is
      loaded automatically when you run the above command.

   .. group-tab:: Linux

      Navigate to the ``workspace`` folder and enter the following command:
      ``source zephyr/zephyr-env.sh``

      If you need to define additional environment variables, create the file
      ``~/.zephyrrc`` and add the variables there. This file is loaded
      automatically when you run the above command.

   .. group-tab:: macOS

      Navigate to the ``workspace`` folder and enter the following command:
      ``source zephyr/zephyr-env.sh``

      If you need to define additional environment variables, create the file
      ``~/.zephyrrc`` and add the variables there. This file is loaded
      automatically when you run the above command.
