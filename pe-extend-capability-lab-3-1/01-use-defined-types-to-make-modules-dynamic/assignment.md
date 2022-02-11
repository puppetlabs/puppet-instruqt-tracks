---
slug: use-defined-types-to-make-modules-dynamic
id: cpbzjzbgew4z
type: challenge
title: Use Defined Types to make Modules Dynamic
difficulty: basic
timelimit: 7200
---
1. Split the classes up:
# manifests/init.pp
# @summary A short summary of the purpose of this class
#
# A description of what this class does
#
# @example
#   include nginx
# @summary A short summary of the purpose of this class
#
# A description of what this class does
#
# @example
#   include nginx
class nginx (
  Optional[String] $package_provider,
  Optional[String] $version,
  Optional[String] $nginx_conf_template,
  Optional[String] $service_name,
  Optional[String] $package_name,
) {
  case $facts['os']['family'] {
    'windows': {
      $conf_dir = "c:/tools/nginx-${facts['nginx_version']}/conf"
    }
    'RedHat':  {
      $conf_dir = '/etc/nginx'
    }
    default: {
      fail("Unsupported osfamily: ${facts['os']['family']}")
    }
  }
  $sites_enabled_dir = "${conf_dir}/sites-enabled"
  contain nginx::package
  contain nginx::config
  contain nginx::service
  Class['nginx::package']
  -> Class['nginx::config']
  ~> Class['nginx::service']
}

# manifests/config.pp
# @summary A short summary of the purpose of this class
#
# A description of what this class does
#
# @example
#   include nginx::config
class nginx::config {
  $conf_dir            = $nginx::conf_dir
  $sites_enabled_dir   = $nginx::sites_enabled_dir
  $nginx_conf_template = $nginx::nginx_conf_template
  $nginx_conf          =  "${conf_dir}/nginx.conf"
  file { 'nginx_conf':
    ensure  => file,
    path    => $nginx_conf,
    content => epp($nginx_conf_template, {
      conf_dir          => $conf_dir,
      sites_enabled_dir => $sites_enabled_dir,
    }),
  }
  file { 'sites_enabled_dir':
    ensure => directory,
    path   => $sites_enabled_dir,
  }
}

# manifests/service.pp
# @summary A short summary of the purpose of this class
#
# A description of what this class does
#
# @example
#   include nginx::service
class nginx::service {
  service { $nginx::service_name:
    ensure => running,
    enable => true,
  }
}

# manifests/package.pp
# @summary A short summary of the purpose of this class
#
# A description of what this class does
#
# @example
#   include nginx::package
class nginx::package {
  package { $nginx::package_name:
    ensure   => $nginx::version,
    provider => $nginx::package_provider,
  }
}

2. PDK validate and run unit tests - this should fail:
Failures:

  1) nginx on centos-7-x86_64 is expected to compile into a catalogue without dependency cycles
     Failure/Error: it { is_expected.to compile }

       error during compilation: Evaluation Error: Error while evaluating a Function Call, Class[Nginx]:
         expects a value for parameter 'service_name'
         expects a value for parameter 'package_name' (line: 2, column: 1) on node desktop-klsbtep
     # ./spec/classes/nginx_spec.rb:9:in `block (4 levels) in <top (required)>'
3. Add default data for package and service name:
# data/common.yaml
nginx::service_name: 'nginx'
nginx::package_name: 'nginx'
4. PDK validate and run unit tests - some examples should fail:
Failures:

  1) nginx on centos-7-x86_64 is expected to contain Service[nginx] that requires Package[nginx]
     Failure/Error: it { is_expected.to contain_service('nginx').that_requires('Package[nginx]') }
       expected that the catalogue would contain Service[nginx] with that requires Package[nginx]
     # ./spec/classes/nginx_spec.rb:10:in `block (4 levels) in <top (required)>'
5. Modify the unit tests, remove the direct resource relationship - the relationship between the package and the service is now indirect, because it is separated by the config class:
# frozen_string_literal: true

require 'spec_helper'

describe 'nginx' do
  on_supported_os.each do |os, os_facts|
    context "on #{os}" do
      let(:facts) { os_facts }
      it { is_expected.to compile.with_all_deps }
      it { is_expected.to contain_class('nginx::service').that_subscribes_to('Class[nginx::config]') }
      it { is_expected.to contain_class('nginx::config').that_requires('Class[nginx::package]') }
      it { is_expected.to contain_service('nginx').that_subscribes_to('File[nginx_conf]') }
      it { is_expected.to contain_file('nginx_conf').with('content' => %r{worker_processes}) }
      it { is_expected.to contain_file('sites_enabled_dir') }
    end
  end
end

6. PDK validate and run unit test - this should pass...
> pdk test unit
pdk (INFO): Using Ruby 2.5.9
pdk (INFO): Using Puppet 6.25.0
[*] Preparing to run the unit tests.
....................................

Finished in 13.61 seconds (files took 7.52 seconds to load)
36 examples, 0 failures
Add defined types for the website instances
Your module must not make assumptions, it must also be flexible. You must design your module to be consumed by profiles in a customizable way.
Creating new websites with their own static content is not part of the module's responibility, this is left to the end user, to be declared at the profile layer.
1. Add some example code to demonstrate how you intend to use the module to manage multiple websites:
# examples/websites.pp
# Example profile
class profile::nginx {
  case $facts['os']['family'] {
    'windows': {
      $sites_dir = 'c:/sites'
    }
    'RedHat':  {
      $sites_dir = '/var/sites'
    }
    default: {
      fail("Unsupported osfamily: ${facts['os']['family']}")
    }
  }
  $sites = [
    {
      name => 'puppet.com',
      port => 81,
    },
    {
      name => 'forge.com',
      port => 82,
    },
  ]
  file { $sites_dir:
    ensure => directory,
  }
  $sites.each |$site| {
    $site_root = "${sites_dir}/${$site['name']}"
    nginx::website { $site['name']:
      port      => $site['port'],
      site_root => $site_root,
      require   => File[$site_root, $sites_dir]  # puppet does not assume; does not create parent dirs
    }
    file { $site_root:
      ensure => directory,
    }
    file { "${site_root}/index.html":
      content => "hello from ${site['name']}!",
    }
  }
}

include profile::nginx

2. Add unit tests:
# spec/defines/website_spec.rb
# frozen_string_literal: true

require 'spec_helper'

describe 'nginx::website' do
  let(:title) { 'nginx.local' }
  let(:params) do
    {
      port: 81,
      site_root: '/var/sites',
    }
  end

  on_supported_os.each do |os, os_facts|
    context "on #{os}" do
      let(:facts) { os_facts }
      it { is_expected.to compile }
    end
  end
end

3. PDK validate and run unit tests - these should fail:
....................................FFFFFF

Failures:

  1) nginx::website on centos-7-x86_64 is expected to compile into a catalogue without dependency cycles
     Failure/Error: it { is_expected.to compile }
       error during compilation: Evaluation Error: Error while evaluating a Resource Statement, Un
4. Add a new defined type, website:
# manifests/website.pp
# @summary A short summary of the purpose of this defined type.
#
# A description of what this defined type does
#
# @example
#   nginx::website { 'namevar': }
#
#   nginx::website { 'puppet.com':
#     port => 80,
#   }
#
define nginx::website (
  String                  $server_name = $title,
  Stdlib::Port            $port        = undef,
  Stdlib::Absolutepath    $site_root   = undef,
  Optional[Array[String]] $index       = ['index.html', 'index.htm'],
) {
  include nginx
  $sites_enabled_dir = $nginx::sites_enabled_dir
  $nginx_service     = $nginx::service_name
  file { "${sites_enabled_dir}/${server_name}.conf":
    ensure  => file,
    notify  => Service[$nginx_service],
    content => epp('nginx/website.conf.epp', {
      index       => $index,
      port        => $port,
      root        => $site_root,
      server_name => $server_name,
    })
  }
}

5. PDK validate and run unit tests - it should pass!
6. Use bolt to apply the example in your module to some test nodes:
> bolt apply examples/website.pp -t windows-1,linux-1 --noop
7. Use bolt to run a simple acceptance test agains each website instance (this should pass):
> bolt command run 'curl http://localhost:81 ; curl http://localhost:82' -t windows-1,linux-1