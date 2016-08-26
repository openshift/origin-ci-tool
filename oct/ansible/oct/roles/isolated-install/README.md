# Role: `isolated-install`

The purpose of the tasks in this role is to install a package, whether that installation results in a downgrade, fresh install, or
upgrade. This role is in general _not_ idempotent: as it is an intractable problem to determine if, in general, a downgrade or 
upgrade to a system package will be safe, we instead remove any trace of the package on the system if it already exists before 
attempting to install the version requested.

This role supports installation of the package RPM from any currently-configured repository or from any repository that is 
reachable from the internet. Repositories installed from URLs will have a `.repo` file created for them automatically. The name of
the repository will be the given URL with all non-alphanumeric characters (`/[^a-zA-Z0-9]/`) stripped out. Then, the URL and 
name will be inserted into the following definition, where `<reponame>` is the stripped URL and `<url>` is the given URL:
```
[<reponame>]
name=<reponame>
baseurl=<url>
enabled=1
gpgcheck=0
sslverify=0
sslclientcert=/var/lib/yum/client-cert.pem
sslclientkey=/var/lib/yum/client-key.pem
```
    
The `sslclient{cert,key}` fields are provided to allow for the repositories to be non-public. As the `sslclient{cert,key}` are not
used unless the RPM repository responds to a request with auth headers, these fields are ignored unless the repository needs 
them and therefore repositories that do not need them are not broken and it is safe to append them always.

Any repositories that are installed from given URLs will be enabled only for the installation of the package requested, and their
`.repo` file will be deleted immediately afterword.