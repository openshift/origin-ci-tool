# Role: `docker`

The purpose of the tasks in this role is to configure Docker on the host system for use by the Origin CI. It is expected that 
the correct version of Docker be installed on the system prior to this role being applied. As a general rule, this role will 
clobber any configuration that exists prior to it being run. If any manual patching has been applied to `systemd` environment 
files or service definitions, those patches will need to be re-applied if they are on files that this role touches.