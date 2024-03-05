.. _gs_nix:

Working with Bridle via Nix
###########################

.. contents::
   :local:
   :depth: 2

An alternative way to develop with Bridle is through `Nix
<https://nixos.org/>`_, a functional package managing system. This way, all
dependencies can be installed using a single tool. Packages installed this way
don't pollute your regular system, and can easily be removed later.

Installing the Nix Package Manager
**********************************

To get started using Nix, you will need to install the package manager itself.
Most distributions provide packages for installing it using their regular
package manager (e.g. Ubuntu provides a ``nix`` package that can be installed
using ``apt install nix``). If your distribution doesn't provide such a package,
see the instructions on `nixos.org <https://nixos.org/download>`_ to get a Nix
installation.

Enabling Flakes
***************

Flakes are an experimental feature that enables fully hermetic and reproducible
builds. To enable flakes, add::

   experimental-features = nix-command flakes

to your private Nix configuration in ``~/.config/nix/nix.conf`` (creating this
file if it doesn't exist).

Using the Bridle Flake
**********************

The Bridle flake provides a ``devShell`` output, which is a shell environment in
which all necessary tools and dependencies are present for developing Zephyr
applications with Bridle. By running ``nix develop`` within the bridle repository,
you enter this environment. You can then proceed to create a west workspace
ontop of your bridle directory and work as usual.

You can also use the build hooks provided by the ``west2nix`` input to perform
builds directly via Nix, without creating an explicit west workspace. In this
case, the workspace manifest used will be that provided by the ``west2nix.toml``
lockfile (see below on how to bring it up-to-date if required). For an example
of such a derivation, see ``doc.nix``, which builds this documentation. For
another example of a simpler build, see `the west2nix repository
<https://github.com/adisbladis/west2nix>`_.

Keeping the Bridle Flake Up-to-date
***********************************

Like all nix flakes, the Bridle flake has its inputs locked using the
``flake.lock`` file. Running ``nix flake update`` in the bridle directory will
check for upstream changes and bump any changed inputs in the lockfile. After
checking for breakages due to the update, e.g. via ``nix flake check``, and
confirming that ``nix develop`` drops you into a working shell, you should can
commit the updated ``flake.lock``. If you do notice breakage, you can simply
revert the update with ``git checkout flake.lock``.

The flake also relies on the manifest lockfile ``west2nix.toml``, which reflects
the state of a west workspace at a specific time. To update this lockfile, you
first need a full checkout of the workspace you want to lock:

.. code-block:: console

   mkdir workspace && cd workspace
   git clone https://github.com/tiacsys/bridle.git
   west init -l bridle
   west update

You can then run ``west2nix`` on this workspace and place the resulting lockfile
into the ``bridle`` directory:

.. code-block:: console

   nix run ./bridle#west2nix
   mv west2nix.toml bridle/

.. note::

   Running ``west2nix`` directly inside the ``bridle`` directory is
   likely to fail due to permission issues, hence running it from the workspace
   directory instead.

Finally, you can commit your new lockfile:

.. code-block:: console

   git add west2nix.toml
   git commit -m "Updated west2nix.toml"

Similarly to updating the flake inputs, this update can be reverted simply by
resetting ``west2nix.toml`` to an earlier state.
