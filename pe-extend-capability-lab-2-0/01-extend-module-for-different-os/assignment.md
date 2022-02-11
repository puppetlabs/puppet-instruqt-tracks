---
slug: extend-module-for-different-os
id: co8tnxi5znce
type: challenge
title: Extend a Module to Support Different OS Platforms
difficulty: basic
timelimit: 7200
---
1. Add "Windows" to the list of supported operating systems in metadata.json
...
    {
      "operatingsystem": "Scientific",
      "operatingsystemrelease": [
        "7"
      ]
    },
    {
      "operatingsystem": "Windows",
      "operatingsystemrelease": [
        "2016",
        "2019"
      ]
    }
  ],
  "requirements": [
    {
      "name": "puppet",
      "version_requirement": ">= 6.21.0 < 7.0.0"
...
2. Run pdk validate & pdk test unit - looks good.
3. Test your changes on a clean test node & inspect failed run output:
> bolt apply -e 'include nginx' -t windows
Starting: install puppet and gather facts on localhost:55985
Finished: install puppet and gather facts with 0 failures in 23.85 sec
Starting: apply catalog on localhost:55985
Started on localhost:55985...
Failed on localhost:55985:
  Resources failed to apply for localhost:55985
    Package[nginx]: change from 'absent' to '1.14.1' failed: Could not update: The source parameter is required when using the Windows provider.
  Err: /Stage[main]/Nginx/Package[nginx]/ensure: change from 'absent' to '1.14.1' failed: Could not update: The source parameter is required when using the Windows provider.
  Notice: /Stage[main]/Nginx/Service[nginx]: Dependency Package[nginx] has failures: true
  Warning: /Stage[main]/Nginx/Service[nginx]: Skipping because of failed dependencies
  changed: 0, failed: 1, unchanged: 0 skipped: 1, noop: 0
Finished: apply catalog with 1 failure in 18.28 sec
Failed on 1 target: localhost:55985
Ran on 1 target in 42.28 sec
"Windows" is default package provider on Windows; you need to specify a package source, or use a package provider that can resolve a source automatically - Chocolatey to the rescue!
4. nginx has already been manually installed on one of your windows nodes - run puppet resource to inspect the state and return the puppet code:
> puppet resource package nginx
package { 'nginx':
  ensure   => '1.21.4',
  provider => 'chocolatey',
}
> puppet resource service nginx
service { 'nginx':
  ensure       => 'running',
  enable       => 'true',
  logonaccount => 'LocalSystem',
  provider     => 'windows',
}

5. Fix your code by adding the chocolatey provider parameter for windows only, using a selector:
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
to:
# @summary A short summary of the purpose of this class
#
# A description of what this class does
#
# @example
#   include nginx
class nginx {
  $package_provider = $facts['os']['family'] ? {
    'windows' => 'chocolatey',
    default   => undef,
  }
  service { 'nginx':
    ensure  => running,
    enable  => true,
    require => Package['nginx'],
  }
  package { 'nginx':
    ensure   => latest,
    provider => $package_provider,
  }
}

6. Pdk validate & unit test:
....FF
Failures:
  1) nginx on windows-2016-x86_64 is expected to contain Service[nginx] that requires Package[nginx]
     Failure/Error: it { is_expected.to contain_service('nginx').that_requires('Package[nginx]') }
     Puppet::ResourceError:
       Parameter provider failed on Package[nginx]: Invalid package provider 'chocolatey' (file: C:/Users/David/pe401-lab/nginx/spec/fixtures/modules/nginx/manifests/init.pp, line: 26)
     # ./spec/classes/nginx_spec.rb:9:in `block (4 levels) in <top (required)>'
     # ------------------
     # --- Caused by: ---
     # ArgumentError:
     #   Invalid package provider 'chocolatey'
     #   ./spec/classes/nginx_spec.rb:9:in `block (4 levels) in <top (required)>'
  2) nginx on windows-2019-x86_64 is expected to contain Service[nginx] that requires Package[nginx]
     Failure/Error: it { is_expected.to contain_service('nginx').that_requires('Package[nginx]') }
     Puppet::ResourceError:
       Parameter provider failed on Package[nginx]: Invalid package provider 'chocolatey' (file: C:/Users/David/pe401-lab/nginx/spec/fixtures/modules/nginx/manifests/init.pp, line: 26)
     # ./spec/classes/nginx_spec.rb:9:in `block (4 levels) in <top (required)>'
     # ------------------
     # --- Caused by: ---
     # ArgumentError:
     #   Invalid package provider 'chocolatey'
     #   ./spec/classes/nginx_spec.rb:9:in `block (4 levels) in <top (required)>'
Finished in 6.31 seconds (files took 6.96 seconds to load)
6 examples, 2 failures
7. Add your module dependencies and fixtures:
# metadata.json
...
  "dependencies": [
    {
      "name": "puppetlabs/chocolatey",
      "version_requirement": ">= 6.0.1 < 7.0.0"
    },
    {
      "name": "puppetlabs/stdlib",
      "version_requirement": ">= 4.6.0 < 8.0.0"
    },
    {
      "name": "puppetlabs/powershell",
      "version_requirement": ">= 1.0.1 < 7.0.0"
    },
    {
      "name": "puppetlabs/registry",
      "version_requirement": ">= 1.0.0 < 5.0.0"
    }
  ],
  "operatingsystem_support": [
...
# fixtures.yml
---
fixtures:
  forge_modules:
    stdlib: "puppetlabs/stdlib"
    chocolatey: "puppetlabs/chocolatey"
    powershell: "puppetlabs/powershell"
    registry: "puppetlabs/registry"

  # NOTE TO DESIGNER: the above modules need to exist on a local git instance
  # at specific compatible module versions so that any external module updates
  # do not affect the lab.

8. re-run the unit test - success.
9. Re-run acceptance test on a clean test node, another fail...
> bolt apply --execute 'include nginx' -t windows
Starting: install puppet and gather facts on localhost:55985
Finished: install puppet and gather facts with 0 failures in 23.99 sec
Starting: apply catalog on localhost:55985
Started on localhost:55985...
Failed on localhost:55985:
  The task failed with exit code 1 and no stdout, but stderr contained:
  ruby.exe : C:/Program Files/Puppet Labs/Puppet/puppet/lib/ruby/vendor_ruby/puppet/type.rb:1910:in `block (2 levels) in providify': Parameter provider failed on Package[nginx]: Invalid package provider 'chocolatey' (Puppet::ResourceError)
10. You need to make sure the chocolatey module and dependencies are installed in order for puppet apply to compile a catalog locally (without a primary server). Add the chocolatey module to the module bolt project file (bolt will automatically take care of dependencies):
# bolt-project.yaml
---
name: nginx
modules:
  - name: puppetlabs/chocolatey
    version_requirement: '6.0.1'
> bolt module install
Installing project modules
  → Resolving module dependencies, this might take a moment
  → Writing Puppetfile at C:/Users/David/pe401-lab/nginx/Puppetfile
  → Syncing modules from C:/Users/David/pe401-lab/nginx/Puppetfile to
    C:/Users/David/pe401-lab/nginx/.modules
  → Generating type references
Successfully synced modules from
 C:/Users/David/pe401-lab/nginx/Puppetfile to C:/Users/David/pe401-lab/nginx/.modules

11. Apply the module to the same node...
> bolt apply -e 'include nginx' -t windows
12. Test on clean nodes windows & linux - success.
curl http://localhost:80 -usebasicparsing