.. _dm_adding_code:

Adding your own code
####################

.. contents::
   :local:
   :depth: 2

To maintain an application that uses |BRIDLE|, you should use the same tools
that |TIAC| members use to develop it. This section describes suggested user
workflows to develop and maintain an application based on |BRIDLE|.

See :ref:`dm_code_base` for detailed information on how the |BRIDLE|
repositories are organized.

.. _dm_user_workflows:

User workflows
**************

The following workflows present different ways of adding your own code to
|BRIDLE|. They describe the actual practicalities of developing an application
that is based on |BRIDLE| from a version control and maintenance point of view.

Which user workflow to choose depends on the type of application, the timeframe
to develop it, and the need to update |BRIDLE| version used.

All workflows are described under the following basic assumptions:

* One or more applications are to be developed using |BRIDLE|.
* Additional board definitions might be required by the user.
* Additional libraries might be required by the user.
* The term *application* refers to the application code and any board
  definitions and libraries it requires.
* The application(s) will require updates of the |BRIDLE| revision.

Workflow 1: Eschew Git and west
===============================

.. attention::

   This method of operation should be used only in the case of absolute
   necessity and should be avoided. Git and west are very powerful tools
   and cover almost every required workflow, including regulatory
   compliance with required traceability.

If you have your own version control tools, you might want to simply not use
Git or west at all, and instead rely on your own toolset. In such case, you
must obtain a copy of |BRIDLE| on your file system and then manage the source
code of both the SDK and your application yourself.

Since no downloadable packages of |BRIDLE| are currently available, the
simplest path to obtain the source code is to follow the instructions in the
:ref:`corresponding section <dm-wf-get-bridle>` of the documentation. This
requires you to install Git and west, but you can then ignore them from that
point onwards. If you need to update the copy of |BRIDLE| you are working with,
you can :ref:`obtain the source code <dm-wf-get-bridle>` again, or, if you
have kept the original set of repositories,
:ref:`update it instead <dm-wf-update-bridle>`. Once you have obtained a copy
of the |BRIDLE| source code, which is self-contained in a single folder, you
can then proceed to manage that code in any way you see fit.

Unless you take some :ref:`additional steps <zephyr:no-west>`, west itself must
still be installed in order to build applications.

Workflow 2: Out-of-tree application repository
==============================================

Another approach to maintaining your application is to completely decouple it
from the |BRIDLE| repositories and instead host it wherever you prefer - in
Git, another version control system, or simply on your hard drive. This is
typically also known as "out-of-tree" application, meaning that the
application, board definitions, and any other libraries are actually outside
any of the repositories provided by |TIAC| and can be placed anywhere at all.
As long as you do not need to make any changes to any of the repositories of
|BRIDLE|, you can use the procedures to
:ref:`get the source code <dm-wf-get-bridle>` and later
:ref:`update it <dm-wf-update-bridle>`, and manage your application separately,
inside or outside the top folder of |BRIDLE|.

If you choose to have your application outside of the folder hierarchy of
|BRIDLE|, the build system will find the location of the SDK through the
:makevar:`ZEPHYR_BASE` environment variable, which is set either through
a script or manually in an IDE. More information about application development
and the |BRIDLE| build and configuration system can be found in the
:ref:`app_build_system` documentation section.

The drawback with this approach is that any changes you make to the set of
|BRIDLE| repositories are not directly trackable using Git, since you do
not have any of the |BRIDLE| repositories forked. If you are tracking the
master branch of the |BRIDLE|, you can instead send the changes you require
to the official repositories as Pull Requests, so that they are incorporated
into the codebase.

Workflow 3: Application in a fork of `tiac-bridle`_
===================================================

Forking the `tiac-bridle`_ repository and adding the application to it is
another valid option to develop and maintain your application. This approach
also allows you to fork additional |BRIDLE| repositories and point to those.
This can be useful if you have to make changes to those repositories beyond
adding your own application to the manifest repository.

In order to use this approach, you first need to
:ref:`get the source code <dm-wf-get-bridle>`, and then
:ref:`fork the tiac-bridle repository <dm-wf-fork>`. Once you have your own
fork, you can start adding your application to your fork's tree and push it
to your own Git server. Every time you want to update the revision of the
|BRIDLE| that you want to use as a basis for your application, you must
follow the :ref:`instructions to update <dm-wf-update-bridle>` on your
own fork of ``tiac-bridle``.

If you have changes in additional repositories beyond `tiac-bridle`_ itself,
you can point to your own forks of those in the :file:`west.yml` included in
your fork.

Workflow 4: Application as the manifest repository
==================================================

An additional possibility is to take advantage of west to manage your own set
of repositories. This workflow is particularly beneficial if your application
is split among multiple repositories or, just like in the previous workflow,
if you want to make changes to one or more |BRIDLE| repositories, since it
allows you to define the full set of repositories yourself.

In order to implement this approach you first need to create a manifest
repository of your own, which just means a repository that contains
a :file:`west.yml` manifest file in its root. Next you must populate the
manifest file with the list of repositories and their revisions.

In general, the easiest thing to do is to import the :file:`west.yml` into
`tiac-bridle`_, using west's manifest imports feature. This is demonstrated
by the following code:

.. code-block:: yaml

   # Example application-specific west.yml, using manifest imports.
   manifest:
     remotes:
       - name: tiacsys
         url-base: https://github.com/tiacsys
     projects:
       - name: bridle
         repo-path: bridle
         remote: tiacsys
         revision: v0.1.5
         import: true
     self:
       path: application

Importing :file:`west.yml` also results in the addition of all the |BRIDLE|
projects, including those imported from Zephyr, into your workspace.

Then, make the following changes:

* Point the entries of any |BRIDLE| repositories that you have forked
  to your fork and fork revision, by adding them to the ``projects``
  list using a new remote.
* Add any entries for repositories that you need that are not part
  of |BRIDLE|.

For example:

.. code-block:: yaml

   # Example your-application/west.yml, using manifest imports, with
   # an BRIDLE fork and a separate module
   manifest:
     remotes:
       - name: tiacsys
         url-base: https://github.com/tiacsys
       - name: your-remote
         url-base: https://github.com/your-name
     projects:
       - name: bridle
         remote: tiacsys
         revision: v0.1.5
         import: true
       # Example for how to override a repository in the BRIDLE with your own:
       - name: mcuboot
         remote: your-remote
         revision: your-mcuboot-fork-SHA-or-branch
       # Example for how to add a repository not in BRIDLE:
       - name: your-custom-library
         remote: your-remote
         revision: your-library-SHA-or-branch
     self:
       path: application

The variable values starting with *your-* in the above code block are just
examples and you can replace them as needed. The above example includes
a fork of the ``mcuboot`` project, but you can fork any project in
:file:`bridle/west.yml`.

Once you have your new manifest repository hosted online, you can use
it with west just like you use the `tiac-bridle`_  repository when
:ref:`getting <dm-wf-get-bridle>` and later
:ref:`updating <dm-wf-update-bridle>` the source code. You just need to
replace ``tiac-bridle`` and ``bridle`` with the repository name and path
you have chosen for your manifest repository (*your-name/your-application*
and *your-ncs-fork*, respectively), as shown in the following code:

.. parsed-literal::
   :class: highlight

   west init -m https:\ //github.com/*your-name/your-application* *your-tiacsys-fork*
   cd *your-tiacsys-fork*
   west update

After that, to modify the |BRIDLE| version associated with your app,
change the ``revision`` value in the manifest file to the `tiac-bridle`_
Git tag, SHA, or the branch you want to use, save the file, and run
``west update``. See :ref:`zephyr:west-mr-model` for more details.
