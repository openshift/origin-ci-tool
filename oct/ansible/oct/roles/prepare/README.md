# Role: `prepare`

The purpose of the tasks in this role is to bring a new host from a bare operating system install to a state where all of the
pre-requisites for the Origin CI system are present. Some things that this role configures are:
 - configuring the package manager to be more robust for CI tasks
 - registering all the non-default repositories that the CI system needs to draw dependencies from
 - installing all of the dependencies using the package manager
 - configuring services that were installed in the above steps
 
As a general rule, this role will clobber any configuration that exists prior to it being run. If any manual patching has been
applied to `systemd` environment files or service definitions, those patches will need to be re-applied if they are on files that
this role touches.

This role is expected to be run as the first step on a new host, or as the first role after the `provision` role. It is expected
that the `docker` role is run after this step in order to bring relevant source code to the host.