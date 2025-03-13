.. _gs_devcontainer:

Working with Bridle via devcontainer
####################################

.. contents::
   :local:
   :depth: 2

An alternative way to develop with Bridle is by using `devcontainer <https://containers.dev/>`_.
Development containers bundle all necessary tools needed in a ready to use container
and take the effort of installing anything locally. Therefore if the development environment
is not needed anymore you can simply remove the container and have your system as clean
as before.

Prerequisites
*************

The Bridle devcontainer setup is created and tested with `docker <https://www.docker.com/>`_ and
`Visual Studio Code <https://code.visualstudio.com/>`_ with the `Dev Containers <https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers>`_
extension. So these three tools need to be installed on your system.

You should also be able to run ``docker`` commands as your user. To test this just run ``docker ps``
and it should print a list (might be empty) with all running containers. If you can't
access docker without root privileges it will exit with an error.

Using Bridle with devcontainer
******************************

All you have to do is checkout the bridle repository, open it in Visual Studio Code and if
prompted select ``Reopen in Container``. Then the referenced image in ``.devcontainer/devcontainer.json``
will be pulled and afterwards your workspace will be initialized using ``west`` automatically.
This will take a while – depending on your internet connection.

You can also start this process manually by opening the ``Command Palette`` (default shortcut
is ``Ctrl+Shif+P``) and then search for ``Dev Containers: Reopen in container``.

When this process is finished you can open up a new terminal inside of the container and get
started with your development. Go to ``Terminal > New Terminal`` and it appears in the ``TERMINAL``
section on the bottom of your screen.

Flashing and debugging
**********************

The devcontainer mounts the entire ``/dev`` folder from the host into the container. That way
the container is able to see new attached (or detached) devices. To be able to access those
devices it is necessary to have the proper udev rules on your **host machine**.

Windows users
*************

Visual Studio Code and docker are also available for Windows and therefore it is possible
to run this setup also on Windows. As filesystem access from the container to your Windows filesystem
is very slow (even on NVMe drives) it is recommended to checkout the repository in your WSL2
home folder and start your journey from there.

You can then start Visual Studio Code from your Windows machine, navigate via the ``Open Folder``
dialog to your WSL2 filesystem, open the repository and start your devcontainer. To access USB devices
for flashing and debugging you have to make them available in WSL2 by using `usbipd <https://learn.microsoft.com/en-us/windows/wsl/connect-usb>`_.
