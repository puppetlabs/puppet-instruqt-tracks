---
slug: use-defined-types-to-make-modules-dynamic
id: cpbzjzbgew4z
type: challenge
title: Use defined types to make modules dynamic
teaser: Break your module class into smaller classes. Then, use class inclusion to
  make the code base more maintainable.
notes:
- type: text
  contents: |-
    In this lab, you will:
     - Use the `contain` function and class relationships to split a module into separate classes and manifest files.
     - Create a defined type to manage separate website instances.

     Click **Start** when you are ready to begin.
tabs:
- title: Windows Workstation
  type: service
  hostname: guac
  path: /#/client/c/workstation?username=instruqt&password=Passw0rd!
  port: 8080
- title: Linux Agent 1
  type: terminal
  hostname: nixagent1
- title: Linux Agent 2
  type: terminal
  hostname: nixagent2
- title: Windows Agent 1
  type: service
  hostname: guac2
  path: /#/client/c/winagent?username=instruqt&password=Passw0rd!
  port: 8080
- title: Lab Help Guide
  type: website
  hostname: guac
  url: https://puppet-kmo.gitbook.io/practice-lab-help/
difficulty: basic
timelimit: 2400
---
Refactor the module class into smaller classes to improve maintainability
========

1. On the **Windows Workstation** tab, from the **Start** menu, open **Visual Studio Code**.
2. Optional: Enable VS Code autosave by clicking **File** > **Auto Save**.

    ✏️ **Note:** By enabling autosave, you don't need to remember to save your changes as you work, ensuring your edits won't be lost.<br><br>

3. Open the `C:\CODE` directory. Click **File** > **Open Folder**, navigate to the `C:\CODE` directory and click **Select Folder**.
4. In VS Code, open a terminal. Click **Terminal** > **New Terminal**.
5. In VS Code Explorer, open the **nginx** > **manifests** > **init.pp** file. Edit the file to contain the following code:
    ```
    # @summary A short summary of the purpose of this class
    # A description of what this class does
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
    ```
2. In the same directory, create a configuration class file named **config.pp** (right-click > **New File**). Edit the file to contain the following code:
    ```
    # manifests/config.pp
    # @summary A short summary of the purpose of this class
    # A description of what this class does
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
    ```
4. In the same directory, create a service class file named **service.pp** and edit it to contain the following code:
    ```
    # manifests/service.pp
    # @summary A short summary of the purpose of this class
    # A description of what this class does
    # @example
    #   include nginx::service
    class nginx::service {
      service { $nginx::service_name:
        ensure => running,
        enable => true,
      }
    }
    ```
5. In the same directory, create a package class file called **package.pp**. Edit it to contain the following code:
    ```
    # manifests/package.pp
    # @summary A short summary of the purpose of this class
    # A description of what this class does
    # @example
    #   include nginx::package
    class nginx::package {
      package { $nginx::package_name:
        ensure   => $nginx::version,
        provider => $nginx::package_provider,
      }
    }
    ```

7. From the VS Code terminal, navigate to the root folder (nginx), and then run `pdk validate` followed by `pdk test unit`:
    ```
    pdk validate --parallel
    ```
    ```
    pdk test unit
    ```
    ✏️ **Note:** Notice the failure message:
    ```
    30 examples, 30 failures
    ```

Refactor Hiera to handle new classes
========
1. In VS Code Explorer, open the **data** > **common.yaml** > **common.yaml** file and update it to handle the newly created classes:
    ```
    # data/common.yaml
    ---
    nginx::package_provider: ~
    nginx::version: latest
    nginx::nginx_conf_template: 'nginx/nginx.conf_linux.epp'
    nginx::service_name: 'nginx'
    nginx::package_name: 'nginx'
    ```

5.  The relationship between the package and the service is now indirect because it is separated by the configuration class. To fix this, you must modify the unit tests to remove the direct resource relationship. In VS Code Explorer, open the **spec** > **classes** > **nginx_spec.rb** > **nginx_spec.rb** file and edit it to contain the following code:
    ```
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
    ```

6. In the VS Code terminal, run the unit tests again:
    ```
    pdk test unit
    ```
    ✅ **Result:** Notice the success message in the output:
    ```
    36 examples, 0 failures
    ```

Add example usage and unit tests for the website instances
========

1. In VS Code Explorer, navigate to the nginx root directory; then, create a directory called **examples** (right-click > **New Folder**).
2. In the **examples** directory, create a file called **websites.pp** (right-click > **New File**). Edit the file to contain the following code:
    ```
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

    ```

2. Navigate to **nginx** > **spec**> **defines** and create a unit test file named **website_spec.rb** to support this example. Edit the file to contain the following code:
    ```
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
    ```

3. In the VS Code terminal, run `pdk validate`; then, run the unit tests again:
    ```
    pdk validate --parallel
    ```
    ```
    pdk test unit
    ```
    ✏️ **Note:** Notice the failure message in the output:
    ```
    42 examples, 6 failures
    ```
    The tests failed because you have not created a type to handle website content. You'll fix this in the next step.


Add a defined type to handle website content
========
1. In VS Code Explorer, navigate to the **manifests** directory and create a file named **website.pp**. Edit the file to contain the following code:
    ```
    # manifests/website.pp
    # @summary A short summary of the purpose of this defined type.
    # A description of what this defined type does
    # @example
    #   nginx::website { 'namevar': }
    #   nginx::website { 'puppet.com':
    #     port => 80,
    #   }
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
    ```
2. Navigate to the **templates** directory and create a new template file named **website.conf.epp**. Edit it to contain the following content, which will power websites created by the profile:
    ```
    <%- | String $server_name,
          Stdlib::Port $port,
          Stdlib::Absolutepath $root,
          Array[String] $index
    | -%>
    server {
        listen         <%= $port %> default_server;
        listen         [::]:<%= $port %> default_server;
        server_name    <%= $server_name %>;
        root           <%= $root %>;
        index          <%= join($index, " ") %>;
        try_files $uri /index.html;
    }
    ```

3. In the VS Code terminal, run `pdk validate` and `pdk test unit` again.

    ✅ **Result:** Notice the success message in the output:
    ```
    42 examples, 0 failures
    ```

4. Run Bolt to apply the example in your module to some test nodes:

    Windows
    ```
    bolt apply "examples\websites.pp" --no-ssl-verify --user instruqt --password Passw0rd! --targets winrm://winagent
    ```
    Linux
    ```
    bolt apply "examples\websites.pp" --no-host-key-check -u root --private-key C:\ProgramData\ssh\id_rsa --target nixagent2
    ```
5. Run simple acceptance test commands:
    Windows
    ```
    Invoke-WebRequest -Uri http://winagent:81
    ```
    ```
    Invoke-WebRequest -Uri http://winagent:82
    ```
    Linux
    ```
    Invoke-WebRequest -Uri http://nixagent2:81
    ```
    ```
    Invoke-WebRequest -Uri http://nixagent2:82
    ```

    ✅ **Result:** Notice the success message on each node:
    ```
    hello from puppet.com!
    ```
    ```
    hello from forge.com!
    ```

---

🎈 **Congratulations!**

You have successfully split a large initial module main class into smaller classes to enable better maintainability and seperation of concerns. You also created a **defined type** that enables the creation of static web content when used in a profile.