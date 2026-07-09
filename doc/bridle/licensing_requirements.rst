.. _licensing_requirements:

Licensing
#########

Licensing is very important to open source projects. It helps ensure the
software continues to be available under the terms that the author desired.

.. _Apache 2.0 license:
   https://github.com/tiacsys/bridle/blob/main/LICENSE

.. _GitHub repo: https://github.com/tiacsys/bridle

Bridle uses the `Apache 2.0 license`_ (as found in the LICENSE file in
the project's `GitHub repo`_) to strike a balance between open
contribution and allowing you to use the software however you would like
to. The Apache 2.0 license is a permissive open source license that
allows you to freely use, modify, distribute and sell your own products
that include Apache 2.0 licensed software. (For more information about
this, check out articles such as `What is the rationale for (Zephyr)
choosing the Apache 2.0 license?`_ and `Top 10 Apache License Questions
Answered`_).

.. _What is the rationale for (Zephyr) choosing the Apache 2.0 license?:
   https://www.zephyrproject.org/faqs/#toggle-button-6aecde3bef611

.. _Top 10 Apache License Questions Answered:
   https://www.mend.io/blog/top-10-apache-license-questions-answered/

A license tells you what rights you have as a developer, as provided by the
copyright holder. It is important that the contributor fully understands the
licensing rights and agrees to them. Sometimes the copyright holder isn't the
contributor, such as when the contributor is doing work on behalf of a
company.

Components using other Licenses
*******************************

There are some imported or reused components of the Bridle Project that
use other licensing, as described in :ref:`Bridle_Licensing`.

Importing code into the Bridle code from other projects that use a license
other than the Apache 2.0 license needs to be fully understood in context
and approved by the Bridle maintainer.

By carefully reviewing potential contributions and also enforcing a
:ref:`DCO` for contributed code, we can ensure that the Bridle community
can develop products with the Bridle Project without concerns over patent
or copyright issues.

.. not yet

   See :ref:`external-contributions` for more information about
   this contributing and review process for imported components.

.. toctree::
   :maxdepth: 1

   LICENSING.rst

.. _copyrights:

Copyright and License Notices
*****************************

Bridle follows SPDX/REUSE-style file headers. Add a machine-readable copyright
notice and a license identifier at the top of each file so tooling can detect
them (for example :external+zephyr:ref:`west spdx <west-spdx>`, which uses the
`REUSE tool`_).

The Bridle Project follows the `Community Best Practice`_ for copyright notices
from the Linux Foundation, therefore we recommend using the following copyright
notice:

.. code-block:: none

   SPDX-FileCopyrightText: TiaC Systems

Include the license identifier alongside it:

.. code-block:: none

   SPDX-License-Identifier: Apache-2.0

Practical guidance:

- Place both lines at the very top of the file using the file's native comment syntax.
- If you authored substantial, original content, you *may* add an additional line for
  yourself or your organization.

.. _Community Best Practice:
   https://www.linuxfoundation.org/blog/copyright-notices-in-open-source-software-projects/

.. _REUSE tool:
   https://github.com/fsfe/reuse-tool

.. _DCO:

Developer Certification of Origin (DCO)
***************************************

To make a good faith effort to ensure licensing criteria are met, the Bridle
Project requires the Developer Certificate of Origin (DCO) process to be
followed.

The DCO is an attestation attached to every contribution made by every
developer. In the commit message of the contribution, the developer simply
adds a ``Signed-off-by`` statement and thereby agrees to the DCO.

When a developer submits a patch, it is a commitment that the contributor has
the right to submit the patch per the license. The DCO agreement is shown
below and at https://developercertificate.org/.

.. code-block:: none

    Developer's Certificate of Origin 1.1

    By making a contribution to this project, I certify that:

    (a) The contribution was created in whole or in part by me and I
        have the right to submit it under the open source license
        indicated in the file; or

    (b) The contribution is based upon previous work that, to the
        best of my knowledge, is covered under an appropriate open
        source license and I have the right under that license to
        submit that work with modifications, whether created in whole
        or in part by me, under the same open source license (unless
        I am permitted to submit under a different license), as
        Indicated in the file; or

    (c) The contribution was provided directly to me by some other
        person who certified (a), (b) or (c) and I have not modified
        it.

    (d) I understand and agree that this project and the contribution
        are public and that a record of the contribution (including
        all personal information I submit with it, including my
        sign-off) is maintained indefinitely and may be redistributed
        consistent with this project or the open source license(s)
        involved.

DCO Sign-Off
============

The "sign-off" in the DCO is a "Signed-off-by:" line in each commit's log
message. The Signed-off-by: line must be in the following format:

.. code-block:: none

   Signed-off-by: Your Name <your.email@example.com>

For your commits, replace:

- ``Your Name`` with your legal name (pseudonyms, hacker handles, and the
  names of groups are not allowed)

- ``your.email@example.com`` with the real email address you are using to
  author the commit. Pseudo or anonymized emails such as
  ``you-id+your-username@users.noreply.github.com`` are not allowed. The
  email must match the one you use to author the commit (CI will fail if
  there is no match).

You can automatically add the Signed-off-by: line to your commit body using
``git commit -s``. Use other commits in the Bridle git history as examples.
See Zephyr's :external+zephyr:ref:`git_setup` for instructions on configuring
user and email settings in Git.

Additional requirements:

- If you are altering an existing commit created by someone else, you must add
  your Signed-off-by: line without removing the existing one.
