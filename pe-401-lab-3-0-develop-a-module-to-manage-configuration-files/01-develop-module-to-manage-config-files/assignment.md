---
slug: develop-module-to-manage-config-files
id: 6u8xeegxuqfg
type: challenge
title: Develop a module to manage configuration files
teaser: Refactor a module to make it maintainable and easier to manage your configuration
  files.
notes:
- type: text
  contents: |-
    In this lab, you will:
     - Refactor a module to make it maintainable.
     - Use the template function with a file resource to manage content in the NGINX configuration file for Windows and Linux operating systems.
     - Use a file resource to manage the directory for NGINX configuration.

     Click **Start** when you're ready to begin.
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
Add a unit test to check for the presence of a configuration file
========

1. On the **Windows Workstation** tab, from the **Start** menu, open **Visual Studio Code**.
2. Optional: Enable VS Code autosave by clicking **File** > **Auto Save**.

    ✏️ **Note:** By enabling autosave, you don't need to remember to save your changes as you work, ensuring your edits won't be lost.<br><br>

3. Open the `C:\CODE` directory. Click **File** > **Open Folder**, navigate to the `C:\CODE` directory and click **Select Folder**.
4. In VS Code, open a terminal. Click **Terminal** > **New Terminal**.
5. In VS Code Explorer, open the **nginx** > **spec** > **classes** > **ngingx_spec.rb** file. Edit the file so it contains the following code:
    ```
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
    ```

2. From the VS Code terminal, navigate to the module root folder (nginx), and then run `pdk validate` followed by `pdk test unit`:
    ```
    pdk validate --parallel
    ```
    ```
    pdk test unit
    ```
    ✏️ **Note:** Notice that the tests fail. This is because the init.pp file still needs to be updated to include the file resources and relationships, as well as the custom fact **nginx_version**, to handle the differences between the desired results for Windows and Linux. You'll fix this in the next step.

Enhance the module to manage configuration files for Windows and Linux
========

1. In VS Code Explorer, open the **nginx** > **manifests** > **init.pp** file. Edit the file to contain the following code, which adds resources and relationships and the **nginx_version** custom fact:
    ```
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
    ```

4. In the VS Code terminal, run the unit tests again:
    ```
    pdk test unit
    ```
    ✏️ **Note:** The command fails because you haven't yet created any templates to populate the configuration files. You'll do that in the next step.

Create templates and configure Hiera to resolve them based on OS
========

1. In VS Code Explorer, open the **data** > **osfamily** > **windows.yaml** data file. Edit the file to contain the following code:
    ```
    # data/osfamily/windows.yaml
    ---
    nginx::package_provider: 'chocolatey'
    nginx::nginx_conf_template: 'nginx/nginx.conf_windows.epp'
    ```
2. Update **data** > **common.yaml** to handle non-Windows cases:
    ```
    # data/common.yaml
    ---
    nginx::package_provider: ~
    nginx::version: latest
    nginx::nginx_conf_template: 'nginx/nginx.conf_linux.epp'
    ```
6. In VS Code Explorer, navigate to the module root directory (nginx) and create a directory called **templates** (right-click > **New Folder**). Within that directory, create a file called **nginx.conf_linux.epp** (right-click > **New File**).
7. Edit the file to contain the following code:
    ```
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
    ```
8. In that same directory, create another template called **nginx.conf_windows.epp**. Edit it to contain the following code:
    ```
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
    ```
9. In the VS Code terminal, run `pdk validate`, and then run the unit tests again:
    ```
    pdk validate --parallel
    ```
    ```
    pdk test unit
    ```
    ✅ **Result:** Notice the success message that confirms that the unit tests now pass.

10. Run Bolt to apply the module to test nodes:
    Windows
    ```
    bolt apply -e "include nginx" --no-ssl-verify --user instruqt --password Passw0rd! --targets winrm://winagent
    ```
    Linux
    ```
    bolt apply --execute 'include nginx' --no-host-key-check -u root --private-key C:\ProgramData\ssh\id_rsa --target nixagent2
    ```
    ✅ **Result:** Notice the output indicating that the configuration files were created:
      ```
        Notice: /Stage[main]/Nginx/Package[nginx]/ensure: created
        Notice: /Stage[main]/Nginx/File[nginx_conf]/content: content changed '{md5}9ddf8423ce7d90df49548e387d6dfd4c' to '{md5}1eb037a21eb82e35d7e8b55bfcdda124'
        Notice: /Stage[main]/Nginx/Service[nginx]: Triggered 'refresh' from 1 event
        Notice: /Stage[main]/Nginx/File[sites_enabled_dir]/ensure: created
        changed: 4, failed: 0, unchanged: 0 skipped: 0, noop: 0
      ```

---

🎈 **Congratulations!**

You have extended this module to manage configuration files for the NGINX service by using templates. YOu also configured Hiera and the module code to correctly distribute the appropriate template to each OS supported in your fleet.