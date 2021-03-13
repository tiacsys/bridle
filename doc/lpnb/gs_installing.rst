.. _gs_installing:

Installing the |LPNB| manually
##############################

.. contents::
   :local:
   :depth: 2

t.b.d.

.. _gs_installing_tools:

Installing the required tools
*****************************

t.b.d.

.. _gs_installing_toolchain:

Installing the toolchain
************************

t.b.d.

.. _cloning_the_repositories_win:
.. _cloning_the_repositories:

Getting the |LPNB| code
***********************

The |LPNB| consists of a set of Git repositories.

t.b.d.

To manage the combination of repositories and versions, the |LPNB|
uses :ref:`zephyr:west`. The main repository, `lpn-bridle`_, contains
a `west manifest file`_, :file:`west.yml`, that determines the revision
of all other repositories. This means that *lpn-bridle* acts as the
:ref:`manifest repository <zephyr:west-manifests>`, while the other
repositories are project repositories.

.. You can find additional information about the repository and development
   model in the :ref:`development model section <dev-model>`.

See the :ref:`west documentation <zephyr:west>` for detailed information
about the tool itself.

Setup Python Virtual Environment
================================

Create a new and complet empty workspace directory, change into this new
folder and execute:

.. tabs::

   .. group-tab:: Windows

      t.b.d.

   .. group-tab:: Linux

      .. parsed-literal::
         :class: highlight

         python3 -m venv --copies --prompt="$(basename $(pwd))[$(python3 --version)]" .env
         source .env/bin/activate
         pip3 install --upgrade pip
         pip3 install --upgrade setuptools

   .. group-tab:: macOS

      .. parsed-literal::
         :class: highlight

         python3 -m venv --copies --prompt="$(basename $(pwd))[$(python3 --version)]" .env
         source .env/bin/activate
         pip3 install --upgrade pip
         pip3 install --upgrade setuptools

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

Cloning the repositories
========================

t.b.d.

Updating the repositories
=========================

t.b.d.

.. _additional_deps:

Installing additional Python dependencies
*****************************************

The |LPNB| requires additional Python packages to be installed.

Use the following commands to install the requirements for each repository.

.. tabs::

   .. group-tab:: Windows

      Open a command prompt in the ``workspace`` folder and
      enter the following commands:

        .. parsed-literal::
           :class: highlight

           pip3 install --upgrade --requirement zephyr/scripts/requirements.txt
           pip3 install --upgrade --requirement bridle/scripts/requirements.txt

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

Installing ... t.b.d. (TBD) IDE
*******************************

t.b.d.

.. _build_environment:

Setting up the build environment
********************************

Before you start
:ref:`building and programming a sample application <gs_programming>`,
you must set up your build environment.

.. _setting_up_tbd:

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

Setting up the command line build environment
=============================================

If you want to build and program your application from the command line,
you must set up your build environment by defining the required environment
variables every time you open a new command prompt or terminal window.

See :ref:`zephyr:env_vars_important` information about the various relevant
environment variables.

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
