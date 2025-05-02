.. _dm_code_base:

|BRIDLE| code base
##################

.. contents::
   :local:
   :depth: 2

The source code, libraries, and tools that compose |BRIDLE| are entirely hosted
in a set of `Git`_ repositories. Basic familiarity with Git is required to
understand the architecture of the repository set and to work with |BRIDLE|.

All |BRIDLE| repositories are publicly hosted on `GitHub`_, and accessible to
both individual users and companies.

Git basics
**********

Git is a distributed version control system that allows repositories to be
easily duplicated. Every time you take an existing Git repository and create
a copy of it, you are creating a *fork* of that repository. This means that
you create an identical copy that might diverge from the original over time,
since commits to the original will not be automatically reflected in the copy,
and commits to your copy will not be automatically reflected in the original.

.. note::

   When we talk about forks or copying Git repositories, we refer to the
   creation of a new repository hosted on a server and accessible to other
   users. If you clone a repository to your local machine using ``git clone``,
   that is referred to as a *clone* and not a fork.

When you create a fork by copying an existing repository, the original
repository is called the *upstream* repository and the newly created copy the
*downstream* repository.

A fork can be hosted on any server, including a public Git hosting site like
`GitHub`_. It is, however, important to differentiate between the generic
concept of a fork and GitHub's concept of a `GitHub fork`_. When you create
a GitHub fork, GitHub copies the original repository and tags the downstream
repository (the fork) with a flag that allows users to send pull requests
from the fork to its upstream repository. GitHub also supports creating forks
without linking them to the upstream respository. See the
`GitHub documentation <GitHub duplicate_>`_ for information
about how to do this.

.. _dm-branch-strategy:

Fork and branch strategy
************************

.. figure:: images/bridle-git-branches.svg
   :alt: A graphical depiction of the |BRIDLE| branch strategy

   The |BRIDLE| branch strategy.


.. _dm-repo-types:

Repository types
****************

There are two main type of Git repositories in the |BRIDLE| repository set:

:TIAC repositories:

   * Created, **developed**, and maintained by |TIAC|.
   * Usually permissively licensed for use by anyone interested,
     in both public or proprietary products.

:OSS repositories:

   * Created and maintained by |TIAC|.
   * Soft forks of open-source projects.
   * Typically contain a small set of changes that are specific to |BRIDLE|.
   * Updated ("upmerged") regularly with the latest changes
     from the open source project.

TIAC repositories are stand-alone and have no upstreams, since they are unique
to the |BRIDLE|. Some examples of repositories of this type are:

* `tiac-bridle`_: The |BRIDLE| main repository for |TIAC| developed software.

OSS repositories are typically soft forks of an upstream open source project,
which |TIAC| maintains in order to keep a small set of changes that do not
belong, or have not been merged, to the upstream official open source software
repository. For example:

* `tiac-zephyr`_ is a soft fork (and therefore a downstream) of the upstream
  official `Zephyr repository`_.

Repository structure
********************

In order to manage the combination of repositories and versions, |BRIDLE| uses
:external+zephyr:ref:`west <west>`, the same tool that the |ZEPHYR| uses to
manage its repository set. You can learn more about the reasons behind the
introduction of west in :external+zephyr:ref:`this section <west-history>`
of the |ZEPHYR| documentation.

A :external+zephyr:ref:`manifest repository <west-manifests>`, `tiac-bridle`_,
contains a file in its root folder, :file:`west.yml`, which lists all other
repositories (west projects) included in |BRIDLE|. The |BRIDLE| repository
structure has a star topology, with the `tiac-bridle`_ repository being the
center of the star and all other repositories being west projects that are
managed by :file:`west.yml`. This is equivalent to topology
:external+zephyr:ref:`T2 <west-t2>` in the
:external+zephyr:ref:`west documentation <west-topologies>` and more detailed
describe in :external+zephyr:ref:`west-mr-model`.

.. figure:: images/bridle-west-repos.svg
   :alt: A graphical depiction of the |BRIDLE| repository structure

   The |BRIDLE| repository structure.

The figure above depicts the |BRIDLE| repository structure. A central concept
with this repository structure is that each revision (in Git terms) of the
`tiac-bridle`_ repository completely determines the revisions of all other
repositories (i.e. the west projects). This means that the linear Git history
of this manifest repository also determines the history of the repository set
in its entirety, thanks to the :file:`west.yml` `west manifest file`_ being
part of the manifest repository. West reads the contents of the manifest file
to find out which revisions of the project repositories are to be checked out
every time ``west update`` is run. In this way, you can decide to work with a
specific |BRIDLE| release either by initializing a new west installation at a
particular tag or by checking out the corresponding tag for a release in an
existing installation and then updating your project repositories to the
corresponding state with ``west update``. Alternatively, you can work with
the latest state of development by using the main branch of the `tiac-bridle`_
repository, updating it with Git regularly and using ``west update`` to update
the project repositories every time the manifest repository changes. More
information about manifests can be found in the
:external+zephyr:ref:`west manifest section <west-manifests>`
of the |ZEPHYR| documentation.

Revisions
*********

.. attention::

   A proper release planning has not been established so far. The information
   given here is in planning and not yet implemented!

There are two fundamental revisions that are relevant to most |BRIDLE| users:

* The ``main`` branch of the `tiac-bridle`_ repository.
* Any Git tag (i.e. release) of the `tiac-bridle`_ repository.

As discussed above, the revision of the manifest repository, `tiac-bridle`_,
uniquely determines the revisions of all other repositories, so a discussion
about |BRIDLE| revisions can be essentially limited to the manifest repository
revision.

The ``main`` branch of the `tiac-bridle`_ repository always contains the
latest development state of the |BRIDLE|. Since all development is done openly,
you can use it if you are not particularly concerned about stability and want
to track the latest changes that are being merged continuously into the different
repositories.

The Git tags correspond to official releases tested and signed by the |TIAC|
engineers. The format is as follows::

   vX.Y.Z(-rcN)

Where X, Y, and Z are the major, minor, and patch version respectively and,
optionally, a release candidate postfix ``-rcN`` is attached if the tag
identifies a candidate instead of the actual release.

The Git tags are composed as follows::

   vX.Y.Z(-rcN|-devN)

X, Y, and Z are the major, minor, and patch version, respectively.
Tags without a suffix correspond to official releases tested and signed
by |TIAC| engineers. A release candidate suffix ``-rcN`` is attached if
the tag identifies a candidate instead of the actual release. In between
releases, there might be development tags. These are identified by a
``-devN`` suffix.

.. _dm-oss-downstreams:

OSS repositories downstream project history
*******************************************

As described in :ref:`dm-repo-types`, |BRIDLE| contains OSS repositories,
which are based on third-party, open-source Git repositories and may contain
additional patches not present upstream. Examples include `tiac-zephyr`_,
which have upstream open-source projects used as a basis for downstream
repositories distributed with |BRIDLE|. This section describes how the
history of these OSS repositories is maintained, and how they are synchronized
with their upstreams.

The short logs for these downstream patches contain ``[tcs xyz]`` at the
beginning, for different ``xyz`` strings. This makes their different purposes
downstream clearer, and makes them easier to search for and see in ``git log``.
The current values of ``[tcs xyz]`` are:

* ``[tcs mergeup]``:
  periodic merges of the upstream tree (if really needed)
* ``[tcs fromlist]``:
  patches which have upstream pull requests, including any later revisions
* ``[tcs fromtree]``:
  patches which have been cherry-picked from an upstream tree
* ``[tcs toup]``:
  patches which |TIAC| developers intend to submit upstream later
* ``[tcs noup]``:
  patches which are specific to |BRIDLE|
* ``[tcs temphack]``:
  temporary patches with some known issues
* ``[backport-<NUM>]``:
  patches which have been cherry-picked from an upstream backport pull request

.. note::

   The downstream project history is periodically rewritten. This is important
   to prevent the number of downstream patches included in a specific |BRIDLE|
   release from increasing forever. A repository's history is typically only
   rewritten once for every |BRIDLE| release.

To make incorporating new history into your own forks easier, a new point in the
downstream |BRIDLE| history is always created which has an empty ``git diff``
with the previous version. The empty diff means you can always use:

* ``git merge``
  to get the rewritten history merged into your own fork without errors
* ``git rebase --onto`` or ``git cherry-pick``
  to reapply any of your own patches cleanly before and after
  the history rewrite
* ``git cherry``
  to list any additional patches you may have applied to these projects
  to rewrite history as needed

Additionally, both the old and new histories are committed sequentially into
the ``revision`` fields for these projects in the :file:`bridle/west.yml`
west manifest file. This means you can always combine ``git bisect`` in the
``bridle`` repository with ``west update`` at each bisection point to diagnose
regressions, etc.
