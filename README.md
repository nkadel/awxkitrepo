awxkitrepo
==========

Wrapper for SRPM building tools for awxkit on RHEL 8 and RHEL 9.

Building awxkit
===============

Ideally, install "mock" and use that to build for both RHEL 8 and RHEL 9.

* make getsrc # Get source tarvalls for all SRPMs

* make cfgs # Create local .cfg configs for "mock".
* * centos-stream+epel-8-x86_64.cfg
* * centos-stream+epel-9-x86_64.cfg

* make repos # Creates local local yum repositories in $PWD/ansiblerepo
* * awxkitrepo/el/8
* * awxkitrepo/el/9

* make # Make all distinct versions using "mock"

Building a compoenent, without "mock" and in the local working system,
can also be done for testing.

* make build

awxkit has strong dependencies on other python modules that may, or may not,
be available in a particular OS. These are listed in the Makefile

Installing awxkit
=================

The relevant yum repository is built locally in awxkitreepo. To enable the repository, use this:

* make repo

Then install the .repo file in /etc/yum.repos.d/ as directed. This
requires root privileges, which is why it's not automated.

Awxkit RPM Build Security
====================

There is a significant security risk with enabling yum repositories
for locally built components. Generating GPG signed packages and
ensuring that the compneents are in this build location are securely
and safely built is not addressed in this test setup.

		Nico Kadel-Garcia <nkadel@gmail.com>
