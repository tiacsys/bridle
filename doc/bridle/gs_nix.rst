.. _gs_nix:

Working with Bridle via Nix
###########################

.. contents::
   :local:
   :depth: 2

An alternative way to develop with Bridle is through `Nix <https://nixos.org/>`_, a functional package
managing system. This way, all dependencies can be installed using a single
tool. Packages installed this way don't pollute your regular system, and can
easily be removed later.

Installing the Nix Package Manager
**********************************

To get started using Nix, you will need to install the package manager itself.
Most distributions provide packages for installing it using their regular
package manager (e.g. Ubuntu provides a ``nix`` package that can be installed
using ``apt install nix``). If your distribution doesn't provide such a package, see the
instructions on `nixos.org <https://nixos.org/download>` to get a Nix
installation.

Enabling Flakes
***************

Flakes are an experimental feature that enables fully hermetic and reproducible
builds. To enable flakes, add

.. parsed-literal::
   :class: highlight

   experimental-features = nix-command flakes

to ``~/.config/nix/nix.conf`` (creating this file if it doesn't exist).

Using the Bridle Flake
**********************

The Bridle flake provides a ``devShell`` output, which is a shell environment in
which all necessary tools and dependencies are present for developing Zephyr
applications with Bridle. By running `nix develop` within the bridle repository,
you enter this environment. You can then proceed to create a west workspace
ontop of your bridle directory and work as usual.

Keeping the Bridle Flake Up-to-date
***********************************

Like all nix flakes, the Bridle flake has its inputs locked using the
``flake.lock`` file. Running ``nix flake update`` in the bridle directory will
check for upstream changes and bump any changed inputs in the lockfile.

The flake also relies on the manifest lockfile ``west2nix.toml``, which reflects
the state of a west workspace at a specific time. To update this lockfile, the
workspace you want to lock needs to be fully checked out. Within this workspace,
run ``nix run bridle#west2nix`` to generate a new ``west2nix.toml``, which can
then be placed in the bridle directory.
