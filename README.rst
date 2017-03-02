Client Library for OpenStack Rating Service (Distil)


How to release code/tarballs/pypi
=================================

1. Add release tag, for example, “0.2.0” with the following description:
“Release disitilclient version 0.2.0”; it should be signed by your personal
gpg key:

.. code-block:: shell

  git tag -s 0.2.0


2. Check that tag is in the repo: “git tag -v 0.2.0”, you should see something
like:

.. code-block:: shell

  object 1466c71d0e9a8fd2cc6e0610587ca0bb2d451ad3
  type commit
  tag 0.2.0
  tagger Fei Long Wang <flwang@catalyst.net.nz> 1488405992 +1300
  
  Release distilclient 0.2.0
  
  Since this release, Distil V2 API is supported.

3. Push tag to the gerrit, you should be in the core team to do it, here is
the command to do it:

.. code-block:: shell

  git push gerrit 0.2.0

4. Check the build status on http://status.openstack.org/zuul/ by search
distilclient.

5. Release wil be available when openstack/python-distilclient disappear,
check the following links for the right versions:

  * https://pypi.python.org/pypi/python-distilclient/
  * http://tarballs.openstack.org/python-distilclient/

6. Check pypi release on https://pypi.python.org/pypi/python-distilclient
