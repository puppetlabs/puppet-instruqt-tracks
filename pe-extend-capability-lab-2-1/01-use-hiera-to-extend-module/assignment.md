---
slug: use-hiera-to-extend-module
id: klwyzmbxsjtf
type: challenge
title: Use Hiera to extend Modul capabilitis
difficulty: basic
timelimit: 7200
---
Replace the case statement with a parameter block:
# manifests/init.pp
class nginx (
  Optional[String] $package_provider,
  Optional[String] $version,
) {
  service { 'nginx':
    ensure  => running,
    enable  => true,
    require => Package['nginx'],
  }
  package { 'nginx':
    ensure   => $version,
    provider => $package_provider,
  }
}
2. Ren facter on your nodes to check their os.family fact:
facter os.family
3. Move data into hiera
# data/osfamily/windows.yaml
---
nginx::package_provider: 'chocolatey'
# hiera.yaml
---
version: 5
defaults:  # Used for any hierarchy level that omits these keys.
  datadir: data         # This path is relative to hiera.yaml's directory.
  data_hash: yaml_data  # Use the built-in YAML backend.
hierarchy:
  - name: "osfamily"
    path: "osfamily/%{facts.os.family}.yaml"
  - name: 'common'
    path: 'common.yaml'
4. PDK validate & run unit tests - fail - missing defaults for optional parameters.
5. Add defaults in common.yaml:
# data/common.yaml
nginx::package_provider: ~   # undef
nginx::version: latest
6. PDK validate & run unit tests - success
Run options: exclude {:bolt=>true}
............
Finished in 9.71 seconds (files took 7.17 seconds to load)
12 examples, 0 failures
7. Use bolt to apply the module to the test nodes - success.
8. Create a custom fact to inspect the version, so that you can use it generate the install location:
# frozen_string_literal: true
Facter.add('nginx_version') do
  setcode do
    case Facter.value(:kernel)
    when 'windows'
      version_string = Facter::Core::Execution.execute('choco info nginx -r')
        # -r to limit output
      version_string.split('|').last
        # grab everything afer the last '|'
    else
      version_string = Facter::Core::Execution.execute('nginx -v 2>&1')
        # redirect to stdout & stderr
      %r{nginx version: (nginx|openresty)\/([\w\.]+)}.match(version_string)[2]
        # strip the version from the string
    end
  end
end
9. PDK validate and run unit tests - these should pass!
10. Use bolt to apply the module to the test nodes - success.
11. Log on to a test node and execute the custom fact:
> facter -p nginx_version