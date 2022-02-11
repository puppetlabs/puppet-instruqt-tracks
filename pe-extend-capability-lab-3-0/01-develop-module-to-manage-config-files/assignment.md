---
slug: develop-module-to-manage-config-files
id: 6u8xeegxuqfg
type: challenge
title: Develop a Module to Manage Configuration Files
difficulty: basic
timelimit: 7200
---
1. Modify the unit tests:
# spec/classes/nginx_spec.rb
# frozen_string_literal: true

require 'spec_helper'

describe 'nginx' do
  on_supported_os.each do |os, os_facts|
    context "on #{os}" do
      let(:facts) { os_facts }
      it { is_expected.to compile }
      it { is_expected.to contain_service('nginx').that_requires('Package[nginx]') }
      it { is_expected.to contain_service('nginx').that_subscribes_to('File[nginx_conf]') }
      it { is_expected.to contain_file('nginx_conf').with('content' => %r{worker_processes}) }
      it { is_expected.to contain_file('sites_enabled_dir') }
    end
  end
end

2. PDK validate and run unit tests - these should fail
3. Add the file resources and relationships, use the custom fact nginx_version you created in the previous lab to construct the file path for conf_dir.
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
) {
 case $facts['os']['family'] {
    'windows': {
      $conf_dir = "c:/tools/nginx-${facts['nginx_version']}/conf"
    }
    'RedHat':  { $conf_dir = '/etc/nginx'  }
    default: { fail("Unsupported osfamily: ${facts['os']['family']}") }
  }
  $sites_enabled_dir = "${conf_dir}/sites-enabled"
  $nginx_conf        = "${conf_dir}/nginx.conf"
  service { 'nginx':
    ensure    => running,
    enable    => true,
    require   => Package['nginx'],
    subscribe => File[$nginx_conf],
  }
  package { 'nginx':
    ensure   => $version,
    provider => $package_provider,
  }
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

4. PDK validate and run unit tests - these should fail:
 1) nginx on centos-7-x86_64 is expected to compile into a catalogue without dependency cycles
     Failure/Error: it { is_expected.to compile }
       error during compilation: Evaluation Error: Error while evaluating a Function Call, Class[Nginx]: expects a value for parameter 'nginx_conf_template' (line: 2, column: 1) on node desktop-klsbtep
     # ./spec/classes/nginx_spec.rb:9:in `block (4 levels) in <top (required)>'
5. Add per-osfamily and common hiera data:
# data/osfamily/windows.yaml
---
nginx::package_provider: 'chocolatey'
nginx::nginx_conf_template: 'nginx/nginx.conf_windows.epp'
# data/common.yaml
---
nginx::package_provider: ~
nginx::version: latest
nginx::nginx_conf_template: 'nginx/nginx.conf_linux.epp'
6.  PDK validate and run unit tests - these should fail:
Failures:

  1) nginx on centos-7-x86_64 is expected to compile into a catalogue without dependency cycles
     Failure/Error: it { is_expected.to compile }
       error during compilation: Evaluation Error: Error while evaluating a Function Call, Could not find template 'nginx/nginx.conf_linux.epp' (file: C:/Users/David/pe401-lab/nginx/spec/fixtures/modules/nginx/manifests/init.pp, line: 38, column: 16) on node desktop-klsbtep
     # ./spec/classes/nginx_spec.rb:9:in `block (4 levels) in <top (required)>'
7. Add two templates, one for each OS:
# templates/nginx.conf_linux.epp
<%- |
  Stdlib::Absolutepath $conf_dir,
  Stdlib::Absolutepath $sites_enabled_dir,
| -%>

user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;

# Load dynamic modules. See /usr/share/doc/nginx/README.dynamic.
include /usr/share/nginx/modules/*.conf;

events {
    worker_connections 1024;
}

http {
    include       mime.types;
    default_type  application/octet-stream;
    sendfile        on;
    keepalive_timeout  65;
    include <%= $sites_enabled_dir %>/*.conf;
    server {
        listen       80 default_server;
        listen       [::]:80 default_server;
        server_name  _;
        root         /usr/share/nginx/html;
        # Load configuration files for the default server block.
        include <%= $conf_dir %>/default.d/*.conf;
        location / {
        }
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
    }

}

# templates/nginx.conf_windows.epp
<%- |
  Stdlib::Absolutepath $conf_dir,
  Stdlib::Absolutepath $sites_enabled_dir,
| -%>

worker_processes  1;
events {
    worker_connections  1024;
}
http {
    include       mime.types;
    default_type  application/octet-stream;
    sendfile        on;
    keepalive_timeout  65;
    include <%= $sites_enabled_dir %>/*.conf;
    server {
        listen       80;
        server_name  localhost;
        # Load configuration files for the default server block.
        include <%= $conf_dir %>/default.d/*.conf;
        location / {
            root   html;
            index  index.html index.htm;
        }
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
    }
}

8. PDK validate and run unit tests - these should pass!
9. Use bolt to apply the module to test nodes - this should pass!
