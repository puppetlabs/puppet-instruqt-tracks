---
slug: acceptance-test-a-new-module
id: 8zq9jnuyjgr1
type: challenge
title: Acceptance Test a New Module
teaser: Acceptance Testing New Modules
difficulty: basic
timelimit: 7200
---
Run a manual acceptance test agains your nodes linux-2 and linux-3 (this should fail)...
> curl localhost:80
Started on localhost:2222...
Failed on localhost:2222:
  The command failed with exit code 7
    % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                   Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0curl: (7) Failed to connect to localhost port 80: Connection refused
Failed on 1 target: localhost:2222
Ran on 1 target in 10.43 sec
2. Use Puppet Bolt to apply your module to the clean test linux node (linux-2):
# Initialise a bolt project in your new module:
> bolt project init

# boly-project.yaml
---
name: nginx
modules: []


> bolt apply --execute 'include nginx' -t linux-2
Starting: install puppet and gather facts on localhost:2222
Running task 'puppet_agent::install' on localhost:2222
Finished: task puppet_agent::install with 0 failures in 10.89 sec
Finished: install puppet and gather facts with 0 failures in 24.57 sec
Starting: apply catalog on localhost:2222
Applying manifest block on ["localhost:2222"]
Compiling manifest block on ["localhost:2222"]
Running task 'apply_helpers::apply_catalog' on localhost:2222
Started on localhost:2222...
Failed on localhost:2222:
  Resources failed to apply for localhost:2222
    Service[nginx]: change from 'stopped' to 'running' failed: Systemd start for nginx failed!
  journalctl log for nginx:
  -- Logs begin at Thu 2021-12-09 15:01:52 UTC, end at Thu 2021-12-09 15:27:38 UTC. --
  -- No entries --
  Err: /Stage[main]/Nginx/Service[nginx]/ensure: change from 'stopped' to 'running' failed: Systemd start for nginx failed!
  journalctl log for nginx:
  -- Logs begin at Thu 2021-12-09 15:01:52 UTC, end at Thu 2021-12-09 15:27:38 UTC. --
  -- No entries --
  Notice: /Stage[main]/Nginx/Package[nginx]/ensure: created
  changed: 1, failed: 1, unchanged: 0 skipped: 0, noop: 0
Finished: apply catalog with 1 failure in 23.51 sec
Finished: apply catalog with 1 failure in 23.51 sec
Failed on 1 target: localhost:2222
Ran on 1 target in 48.23 sec
3. Notice the dependency fail - why does puppet need two runs to converge? Check to see if the nginx service is up and running:
> curl localhost:80
Started on localhost:2222...
Failed on localhost:2222:
  The command failed with exit code 7
    % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                   Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0curl: (7) Failed to connect to localhost port 80: Connection refused
Failed on 1 target: localhost:2222
Ran on 1 target in 10.43 sec
4. Run apply again:
> bolt apply --execute 'include nginx' -t linux-2
Starting: install puppet and gather facts on localhost:2222
Finished: install puppet and gather facts with 0 failures in 23.41 sec
Starting: apply catalog on localhost:2222
Started on localhost:2222...
Finished on localhost:2222:
  Notice: /Stage[main]/Nginx/Service[nginx]/ensure: ensure changed 'stopped' to 'running'
  changed: 1, failed: 0, unchanged: 1 skipped: 0, noop: 0
Finished: apply catalog with 0 failures in 16.1 sec
Successful on 1 target: localhost:2222
Ran on 1 target in 39.67 sec
5. The second run converges - the service is now running. Confirm with an acceptance test:
> curl localhost:80
Started on localhost:2222...
Finished on localhost:2222:
    % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                   Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">

  <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
      <head>
          <title>Test Page for the Nginx HTTP Server on Red Hat Enterprise Linux</title>
   ...
      </body>
  </html>
100  4057  100  4057    0     0  1980k      0 --:--:-- --:--:-- --:--:-- 1980k
Successful on 1 target: localhost:2222
Ran on 1 target in 10.44 sec
yay! it works! But you still have a bug - puppet agent attempts to manage the service before it is installed via the package.
6. Change the unit test for the resources package and service, replacing it with a relationship matcher:
From:
# spec/classes/init_spec.rb
# frozen_string_literal: true

require 'spec_helper'

describe 'nginx' do
  on_supported_os.each do |os, os_facts|
    context "on #{os}" do
      let(:facts) { os_facts }
      it { is_expected.to compile }
      it { is_expected.to contain_package('nginx') }
      it { is_expected.to contain_service('nginx') }
    end
  end
end

To:
# spec/classes/init_spec.rb
# frozen_string_literal: true
require 'spec_helper'
describe 'nginx' do
  on_supported_os.each do |os, os_facts|
    context "on #{os}" do
      let(:facts) { os_facts }
      it { is_expected.to compile }
      it { is_expected.to contain_service('nginx').that_requires('Package[nginx]') }
    end
  end
end

7. Run the unit test (it should fail, because the resource relationship does not yet exist):
> pdk test unit
FFFF
Failures:
  1) nginx on centos-7-x86_64 is expected to contain Service[nginx] that requires Package[nginx]
     Failure/Error: it { is_expected.to contain_service('nginx').that_requires('Package[nginx]') }
       expected that the catalogue would contain Service[nginx] with that requires Package[nginx]
     # ./spec/classes/nginx_spec.rb:9:in `block (4 levels) in <top (required)>'
8. Fix the bug by adding a resource relationship between the service and the package:
# manifests/init.pp
# @summary A short summary of the purpose of this class
#
# A description of what this class does
#
# @example
#   include nginx
class nginx {
  service { 'nginx':
    ensure  => running,
    enable  => true,
    require => Package['nginx'],
  }
  package { 'nginx':
    ensure => latest,
  }
}

9. Run a unit test (it should pass)

10. Apply & acceptance test your changes on a clean test node:
> bolt apply --execute 'include nginx' -t linux-3
Starting: install puppet and gather facts on localhost:2200
Finished: install puppet and gather facts with 0 failures in 23.16 sec
Starting: apply catalog on localhost:2200
Started on localhost:2200...
Finished on localhost:2200:
  Notice: /Stage[main]/Nginx/Package[nginx]/ensure: created
  Notice: /Stage[main]/Nginx/Service[nginx]/ensure: ensure changed 'stopped' to 'running'
  changed: 2, failed: 0, unchanged: 0 skipped: 0, noop: 0
Finished: apply catalog with 0 failures in 23.31 sec
Successful on 1 target: localhost:2200
Ran on 1 target in 46.62 sec
Notice the order in which the agent manages the resources - package before service.
11. Test the service:
> curl localhost:80
Started on localhost:2222...
Finished on localhost:2222:
    % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                   Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">

  <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
      <head>
          <title>Test Page for the Nginx HTTP Server on Red Hat Enterprise Linux</title>
   ...
      </body>
  </html>
100  4057  100  4057    0     0  1980k      0 --:--:-- --:--:-- --:--:-- 1980k
Successful on 1 target: localhost:2222
Ran on 1 target in 10.44 sec
Yay! it works! Nice