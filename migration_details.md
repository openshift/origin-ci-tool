# `vagrant-openshift` Feature Migration Details

## `vagrant-openshift` Features By Command

### `build-atomic-host`
 - [AtomicHostUpgrade](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/atomic_host_upgrade.rb):
   - `atomic host upgrade`: TODO
 
### `build-origin`
 - [BuildOrigin](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/build_origin.rb):
   - `make release{,-binaries}`: TODO
   - install etcd: TODO
   
### `build-origin-base`
 - [CreateYumRepositories](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/yum_update.rb):
   - `yum install deltarpm augeas`: [install_dependencies.yml](./oct/prepare/roles/prepare/tasks/install_dependencies.yml)
   - update `openshift-deps.repo` with the pub mirror link: TODO, should be in Origin install step
   - install EPEL if not Fedora: [register_repositories.yml](./oct/prepare/roles/prepare/tasks/register_repositories.yml)
   - [BZ 707364](https://bugzilla.redhat.com/show_bug.cgi?id=707364) workaround: this was for RHEL 6, we can drop it
 - [YumUpdate](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/.rb):
   - remove previous Origin repository: TODO, should be in Origin install step
   - `yum clean all`: [install_dependencies.yml](./oct/prepare/roles/prepare/tasks/install_dependencies.yml)
   - `yum update --exclude=kernel*`: [install_dependencies.yml](./oct/prepare/roles/prepare/tasks/install_dependencies.yml)
   - add configuation to `yum`: [configure_yum.yml](./oct/prepare/roles/prepare/tasks/configure_yum.yml)
   - update `metadata_expire` to `never`: won't implement unless convinced
 - [SetHostName](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/set_host_name.rb):
   - update `/etc/sysconfig/network` and `/etc/hostname`: @sdodson says this is not needed
 - [InstallOriginBaseDependencies](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/.rb):
   - `vagrant` and Fedora/`systemd` `eth*` naming workaround: even RHEL is on sytemd219, this fix was for systemd197, we can 
   drop it
   - `yum install`: [install_dependencies.yml](./oct/prepare/roles/prepare/tasks/install_dependencies.yml)
   - install of `facter` but not on Fedora: [install_dependencies.yml](./oct/prepare/roles/prepare/tasks/install_dependencies.yml)
   - install Chrome and Chromedriver: [install_dependencies.yml](./oct/prepare/roles/prepare/tasks/install_dependencies.yml)
   - install `openshift-rhel7-dependencies.repo`: [register_repositories.yml](./oct/prepare/roles/prepare/tasks/register_repositories.yml)
   - install Go: TODO
   - install Docker: TODO
   - install `rhaos3{1,2}.repo`: [register_repositories.yml](./oct/prepare/roles/prepare/tasks/register_repositories.yml)
   - configure system: [post_install.yml](./oct/prepare/roles/prepare/tasks/post_install.yml)
   - configure Docker daemon: [configure_docker_daemon.yml](./oct/prepare/roles/prepare/tasks/configure_docker_daemon.yml),
   [configure_docker_daemon_storage.yml](./oct/prepare/roles/prepare/tasks/configure_docker_daemon_storage.yml),
   [configure_openshift_storage.yml](./oct/prepare/roles/prepare/tasks/configure_openshift_storage.yml)
   
### `build-origin-base-images`
 - [BuildOriginBaseImages](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/build_origin_base_images.rb):
   - shell out to a `make` task to build base images: TODO
   
### `build-origin-images`
 - [BuildOriginImages](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/build_origin_images.rb):
   - shell out to `docker build`: ????
   
### `build-origin-rpm-test`
 - [BuildOriginRPMTest](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/build_origin_rpm_test.rb):
   - shell out to `tito`: TODO
   
### `build-sti`
 - [BuildSTI](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/build_sti.rb):
   - shell out to a `make` task or tasks to build STI binary: TODO
   
### `checkout-repositories`
 - [CheckoutRepositories](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/checkout_repositories.rb):
   - given a repo name, remote location and branch, clone it and check it out: TODO
   
### `clone-upstream-repositories`
 - [CloneUpstreamRepositories](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/clone_upstream_repositories.rb):
   - turn off `StrictHostKeyChecking` so we don't get interactive prompts from GitHub: TODO
   - for each repo, `git clone --bare`: TODO
   - make sure the user calling this owns the repo: TODO
   
### `create-ami`
 - [CleanNetworkSetup](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/clean_network_setup.rb):
   - overwrite `/etc/udev/rules.d/70-persistent-net.rules`: ???? (maybe, see if ansible AMI stuff can do it for us)
   - remove the `mlocate` database: ????
 - ConfigValidate:
   - `vagrant` builtin: ????
 - VagrantPlugins::AWS::Action::ConnectAWS:
   - `vagrant` builtin: ????
 - [CreateAMI](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/create_ami.rb):
   - use AWS EC2 API to create an AMI: TODO
   
### `create-local-yum-repo`
 - [CreateLocalYumRepo](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/create_local_yum_repo.rb):
   - install `createrepo`: TODO
   - create local repo pointing to RPMs: TODO
   
### `download-artifacts-origin`
 - [DownloadArtifactsOrigin](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/download_artifacts_origin.rb):
   - get logs from Docker and stuff using `journalctl`
   - build list of sources & targets, then `rsync`: TODO
   
### `download-artifacts-origin-aggregated-logging`
 - [DownloadArtifactsOriginAggregatedLogging](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/download_artifacts_origin_aggregated_logging.rb):
   - see [above](#download-artifacts-origin)
   
### `download-artifacts-origin-console`
 - [DownloadArtifactsOriginConsole](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/download_artifacts_origin_console.rb):
   - see [above](#download-artifacts-origin)
   
### `download-artifacts-origin-metrics`
 - [DownloadArtifactsOriginMetrics](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/download_artifacts_origin_metrics.rb):
   - see [above](#download-artifacts-origin)
   
### `download-artifacts-sti`
 - [DownloadArtifactsOriginSTI](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/download_artifacts_origin_sti.rb):
   - see [above](#download-artifacts-origin)
   
### `install-origin`
 - [YumUpdate](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/yum_update.rb):
   - see [above](#build-origin-base)
 - [SetHostName](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/set_host_name.rb):
   - see [above](#build-origin-base)
 - [InstallOrigin](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/install_origin.rb):
   - set up the OpenShift `systemd` service and start it, etc: TODO (use `openshift-ansible`)
 - [InstallOriginRHEL7](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/install_origin_rhel7.rb):
   - build a `rhel7.2` Docker image to base everything else off of: TODO
 - [InstallOriginAssetDependencies](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/install_origin_asset_dependencies.rb):
   - install & update `npm`: [install_dependencies.yml](./oct/prepare/roles/prepare/tasks/install_dependencies.yml)
   - shell out to a `make` task to install and configure the console: TODO

### `install-origin-assets-base`
 - [InstallOriginAssetDependencies](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/install_origin_asset_dependencies.rb):
   - see [above](#install-origin)
 
### `local-origin-checkout`
 - [LocalOriginCheckout](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/local_origin_checkout.rb):
   - looking for repositories in `$GOPATH`: TODO (???? - many repos don't use Go)
   - if repo is cloned, check out the given branch: TODO
   - clone repo if necessary: ????
   
### `modify-ami`
 - ConfigValidate:
   - `vagrant` builtin: ????
 - VagrantPlugins::AWS::Action::ConnectAWS:
   - `vagrant` builtin: ????
 - [ModifyAMI](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/modify_ami.rb):
   - use AWS EC2 API to add a tag to an AMI: TODO

### `modify-instance`
 - ConfigValidate:
   - `vagrant` builtin: ????
 - VagrantPlugins::AWS::Action::ConnectAWS:
   - `vagrant` builtin: ????
 - [ModifyInstance](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/modify_instance.rb):
   - allow a user to rename, stop or terminate AWS instances: TODO

### `origin-init`
 - [GenerateTemplate](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/generate_template.rb):
   - generate a template for AWS (??) to define the instance that will be spawned: TODO
   
### `push-openshift-images`
 - [PushOpenshiftImages](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/push_openshift_images.rb):
   - ensure Docker daemon has registry as insecure: ????
   - tag and push Docker images: TODO (using `make` from Origin?)
 
### `push-openshift-release`
 - [PushOpenshiftRelease](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/push_openshift_release.rb):
   - shell out to a `make` target in Origin to push the release: TODO
   
### `sync-origin`
 - [PrepareSSHConfig](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/prepare_ssh_config.rb):
   - update `ssh` configuration: TODO
   - sync user's `.openshiftdev/home.d` files: ????
 - [Clean](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/clean.rb):
   - remove bare directories from prior clones: ????
 - [CloneUpstreamRepositories](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/clone_upstream_repositories.rb):
   - use `git clone --bare` on each repo: TODO, but not on sync?
 - [SyncLocalRepository](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/sync_local_repository.rb):
   - make some temp commits locally, push from local to VM to update VM code, then remove tmp commmits locally: TODO
   - also allow a re-sync from a given branch or otherwise internet-accessible repo: TODO
 - [CheckoutRepositories](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/checkout_repositories.rb):
   - see [above](#checkout-repositories)
 - [BuildOriginBaseImages](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/build_orign_base_images.rb):
   - see [above](#build-origin-base-images)
 - [BuildOrigin](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/build_origin.rb):
   - see [above](#build-origin)
 - [RunSystemctl](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/run_systemctl.rb):
   - shell out to `systemctl` to restart the daemon: TODO
 
### `sync-origin-aggregated-logging`
 - [PrepareSSHConfig](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/prepare_ssh_config.rb):
   - see [above](#sync-origin)
 - [Clean](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/clean.rb):
   - see [above](#sync-origin)
 - [CloneUpstreamRepositories](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/clone_upstream_repositories.rb):
   - see [above](#sync-origin)
 - [SyncLocalRepository](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/sync_local_repository.rb):
   - see [above](#sync-origin)
 - [CheckoutRepositories](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/checkout_repositories.rb):
   - see [above](#checkout-repositories)

### `sync-origin-console`
 - [PrepareSSHConfig](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/prepare_ssh_config.rb):
   - see [above](#sync-origin)
 - [Clean](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/clean.rb):
   - see [above](#sync-origin)
 - [CloneUpstreamRepositories](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/clone_upstream_repositories.rb):
   - see [above](#sync-origin)
 - [SyncLocalRepository](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/sync_local_repository.rb):
   - see [above](#sync-origin)
 - [CheckoutRepositories](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/checkout_repositories.rb):
   - see [above](#checkout-repositories)
 - [InstallOriginAssetDependencies](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/install_origin_asset_dependencies.rb):
   - see [above](#install-origin-assets-base)
 
### `sync-origin-metrics`
 - [PrepareSSHConfig](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/prepare_ssh_config.rb):
   - see [above](#sync-origin)
 - [Clean](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/clean.rb):
   - see [above](#sync-origin)
 - [CloneUpstreamRepositories](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/clone_upstream_repositories.rb):
   - see [above](#sync-origin)
 - [SyncLocalRepository](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/sync_local_repository.rb):
   - see [above](#sync-origin)
 - [CheckoutRepositories](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/checkout_repositories.rb):
   - see [above](#checkout-repositories)
 
### `sync-sti`
 - [PrepareSSHConfig](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/prepare_ssh_config.rb):
   - see [above](#sync-origin)
 - [Clean](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/clean.rb):
   - see [above](#sync-origin)
 - [CloneUpstreamRepositories](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/clone_upstream_repositories.rb):
   - see [above](#sync-origin)
 - [SyncLocalRepository](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/sync_local_repository.rb):
   - see [above](#sync-origin)
 - [CheckoutRepositories](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/checkout_repositories.rb):
   - see [above](#checkout-repositories)
 - [BuildSTI](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/build_sti.rb):
   - see [above](#build-sti)
 
### `test-origin`
 - [RunOriginTests](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/run_origin_tests.rb):
   - interpret input from the robot to invoke the correct `make` targets: TODO
   - shell out to the correct `make` target from user input: TODO
 - [DownloadArtifactsOrigin](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/download_artifacts_origin.rb):
   - see [above](#download-artifacts-origin)
 
### `test-origin-aggregated-logging`
 - [RunOriginAggregatedLoggingTests](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/run_origin_aggregated_logging_tests.rb):
   - see [above](#test-origin)
 - [DownloadArtifactsOriginAggregatedLogging](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/download_artifacts_origin_aggregated_logging.rb):
   - see [above](#download-artifacts-origin-aggregated-logging)
 
### `test-origin-console`
 - [RunOriginConsoleTests](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/run_origin_console_tests.rb):
   - see [above](#test-origin)
 - [DownloadArtifactsOriginConsole](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/download_artifacts_origin_console.rb):
   - see [above](#download-artifacts-origin-console)
 
### `test-origin-image`
 - [TestOriginImage](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/command/test_origin_image.rb):
   - pull down latest `openshift/base` images and run `make` targets on them: ????
 - [DownloadArtifactsOrigin](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/download_artifacts_origin.rb):
   - see [above](#download-artifacts-origin)
 
### `test-origin-metrics`
 - [RunOriginMetricsTests](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/run_origin_metrics_tests.rb):
   - see [above](#test-origin)
 - [DownloadArtifactsOriginMetrics](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/download_artifacts_origin_metrics.rb):
   - see [above](#download-artifacts-origin-metrics)

### `test-origin-sti`
 - [RunSTITests](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/run_sti_tests.rb):
   - see [above](#test-origin)
 - [DownloadArtifactsSTI](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/download_artifacts_sti.rb):
   - see [above](#download-artifacts-sti)
 
### `try-restart-origin`
 - [RunSystemctl](https://github.com/openshift/vagrant-openshift/blob/master/lib/vagrant-openshift/action/run_systemctl.rb):
   - see [above](#test-origin)
