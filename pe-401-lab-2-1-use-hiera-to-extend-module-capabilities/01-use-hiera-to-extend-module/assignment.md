---
slug: use-hiera-to-extend-module
id: klwyzmbxsjtf
type: challenge
title: Use Hiera to extend module capabilities
teaser: Move your data into Hiera and then create a custom fact to determine the installation
  directory location.
notes:
- type: text
  contents: |-
    In this lab, you will:
     - Refactor your module by moving data into Hiera.
     - Create a custom fact in the module to return the NGINX version so that it can be used to determine the installation directory location.

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
timelimit: 1500
---
Gather information about your node types by using Facter
========
1. On the **Linux Agent 1** tab, run Facter to visualize the OS fingerprint:
    ```
    sudo -i facter os.family
    ```
    🔀 Switch to the **Windows Agent** tab.<br><br>
2. From the **Start** menu, open a new **Powershell** prompt, and then run Facter again:
    ```
    facter os.family
    ```

Replace the case statement with a parameter block and configure Hiera to handle new parameters
========
1. On the **Windows Workstation** tab, from the **Start** menu, open **Visual Studio Code**.
2. Optional: Enable VS Code autosave by clicking **File** > **Auto Save**.

    ✏️ **Note:** By enabling Auto Save, you don't need to remember to save your changes as you work, ensuring your edits won't be lost.<br><br>

3. Open the `C:\CODE` directory. Click **File** > **Open Folder**, navigate to the `C:\CODE` directory and click **Select Folder**.
4. In VS Code, open a terminal. Click **Terminal** > **New Terminal**.
5. In VS Code Explorer, open the **nginx** > **manifests** > **init.pp** file and replace the case statement with a parameter block:
    ```
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
    ```

6. In VS Code Explorer, navigate to the **data** directory and create a directory called **osfamily** (right-click the **data** directory, and then click **New Folder**). In that directory, create a file named **windows.yaml** (right-click the **osfamily** directory and click **New File**).
7. Copy the following code into the file. This code sets the nginx package provider to Chocolatey:
    ```
    # data/osfamily/windows.yaml
    ---
    nginx::package_provider: 'chocolatey'
    ```

8. In VS Code Explorer, navigate to the **hiera.yaml** file in the base module directory. Update the contents of the file to include a search path based on the **os.family** fact:
    ```
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
    ```
9. In the VS Code terminal, navigate to the root of the module directory (nginx). Then, run `pdk validate` followed by `pdk test unit`:
    ```
    pdk validate --parallel
    ```
    ```
    pdk test unit
    ```
    ✏️ **Note:** In the output, notice that the unit tests fail:
    ```
    12 examples, 12 failures
    ```
    ⚠️ **Important:** The tests failed because you haven't set any defaults to handle cases where the **os.family** fact is not Windows. You also haven't provided a way look up the data for the **package_provider** parameter that you introduced. You'll fix this in the next step.<br><br>
10. In VS Code Explorer, open the **nginx** > **data** > **common.yaml** > **common.yaml**  and the following code, which adds defaults for both parameters:
    ```
    # data/common.yaml
    ---
    nginx::package_provider: ~   # undef
    nginx::version: latest
    ```
11. In the VS Code terminal, run the unit tests again:
    ```
    pdk test unit
    ```
    ✅ **Result:** Notice the success message in the output:
    ```
    12 examples, 0 failures
    ```
12. Use Bolt to apply the module to the Windows test node:
    ```
    bolt apply -e "include nginx" --no-ssl-verify --user instruqt --password Passw0rd! --targets winrm://winagent
    ```
13. Use Bolt to apply the module to a Linux test node as well:
    ```
    bolt apply --execute 'include nginx' --no-host-key-check -u root --private-key C:\ProgramData\ssh\id_rsa --target nixagent2
    ```
    ✅ **Result:** In the output, notice the successful runs on each of the target nodes.<br><br>

Create a custom fact to enable more module features
========

⚠️ **Important:** It is common to need additional data from Facter to enable more customization and flexibility using Hiera. Create a custom fact to inspect the version of your service to support additional feature enhancements.<br><br>

1. On the **Windows Workstation** tab, in VS Code Explorer, create the following directory structure and file:  **lib** > **facter** > **nginx_version.rb**. Alternatively, you can create the file from the terminal window: Navigate to the root folder (nginx) and run the following command:
    ```
    New-Item -Type File -Path lib\facter\nginx_version.rb -Force
    ```
3. Open **nginx_version.rb** and populate it with the following code:
    ```
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
    ```
    ⚠️ **Important:** Bolt doesn't store custom fact code on target nodes, so you will need to add a notify resource to test the output of your custom fact when applying your module to your test nodes.
1. Navigate to **init.pp** and add the notify resource to print out the fact value:
    ```
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
        before   => Notify['nginx_version_debug']
      }

      notify { 'nginx_version_debug':
        message => "${facts[nginx_version]}"
      }
    }
    ```
5. In the terminal, run validate and unit tests:
    ```
    pdk validate --parallel
    ```
    ```
    pdk test unit
    ```
    ✅ **Result:** Notice the success message in the output:
    ```
    12 examples, 0 failures
    ```
6.  Use Bolt to apply the module to the your test nodes:

    Windows:
      ```
      bolt apply -e "include nginx" --no-ssl-verify --user instruqt --password Passw0rd! --targets winrm://winagent
      ```
    Linux:
      ```
      bolt apply --execute 'include nginx' --no-host-key-check -u root --private-key C:\ProgramData\ssh\id_rsa --target nixagent2
      ```
✅ **Result:** The module is successfully applied to both target nodes.

---

🎈 **Congratulations!**
You have successfully enhanced the module to handle different use cases using Hiera and introduced a custom fact to enable future module features!