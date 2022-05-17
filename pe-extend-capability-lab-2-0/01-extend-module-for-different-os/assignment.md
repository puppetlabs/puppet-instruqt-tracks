---
slug: extend-module-for-different-os
id: co8tnxi5znce
type: challenge
title: Extend a Module to Support Different OS Platforms
teaser: Enhance your module to support Windows and Red Hat.
notes:
- type: text
  contents: |-
    In this lab, you will:
     - Enhance your module to support Windows in addition to Red Hat by introducing logic to handle different package managers across the various operating systems running in your fleet.
     - Learn how to manage local module dependencies in the module `metadata.json` file and with Bolt to easily test changes during development.

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
Add Windows support to the module
========
1. On the **Windows Workstation** tab, from the **Start** menu, open **Visual Studio Code**.
2. Optional: Enable VS Code autosave by clicking **File** > **Auto Save**.

    ✏️ **Note:** By enabling autosave, you don't need to remember to save your changes as you work, ensuring your edits won't be lost.<br><br>

3. Open the `C:\CODE` directory. Click **File** > **Open Folder**, navigate to the `C:\CODE` directory, and click **Select Folder**.
4. In VS Code, open a terminal. Click **Terminal** > **New Terminal**.
5. Using VS Code Explorer, open **metadata.json** (in **nginx** > **metadata.json**).
1. Replace the existing code with the following to add "Windows" to the list of supported operating systems:
    ```
    {
      "name": "instruqt-nginx",
      "version": "0.1.0",
      "author": "instruqt",
      "summary": "",
      "license": "Apache-2.0",
      "source": "",
      "dependencies": [

      ],
      "operatingsystem_support": [
        {
          "operatingsystem": "CentOS",
          "operatingsystemrelease": [
            "7"
          ]
        },
        {
          "operatingsystem": "OracleLinux",
          "operatingsystemrelease": [
            "7"
          ]
        },
        {
          "operatingsystem": "RedHat",
          "operatingsystemrelease": [
            "8"
          ]
        },
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
          "version_requirement": ">= 6.21.0 < 8.0.0"
        }
      ],
      "pdk-version": "2.3.0",
      "template-url": "pdk-default#2.3.0",
      "template-ref": "tags/2.3.0-0-g8aaceff"
    }
    ```
2. In the VS Code terminal, navigate to the root of the module folder (nginx). Then, run `pdk validate` followed by `pdk test unit`:
    ```
    cd nginx
    ```
    ```
    pdk validate --parallel
    ```
    ```
    pdk test unit
    ```
    ✏️ **Note:** In the output, notice that the unit tests fail against the Windows environments that you introduced:
    ```
    12 examples, 4 failures
    ```

3. Investigate what happened. Use Bolt to test against a Windows test node:
    ```
    bolt apply -e "include nginx" --no-ssl-verify --user instruqt --password Passw0rd! --targets winrm://winagent
    ```
    ✏️ **Note:** Notice the failure message in the output:
    ```
    Parameter ensure failed on Package[nginx]: Provider windows must have features 'upgradeable' to set 'ensure' to 'latest'
    ```

⚠️ **Important:** "Windows" is the default package provider on Windows. To fix the failure, you must specify a package source or use a package provider that can resolve a source automatically. Chocolatey to the rescue!

Dynamically add the Chocolately provider parameter to Windows nodes
========

1. In VS Code Explorer, navigate to **init.pp** (in **nginx** > **manifests** > **init.pp**). Replace the existing code with the following code, which adds the Chocolatey provider parameter for Windows only, using a selector:
    ```
    # @summary A short summary of the purpose of this class
    # A description of what this class does
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
    ```
6. In the VS Code terminal, run `pdk validate` and then `pdk test unit`:
    ```
    pdk validate --parallel
    ```
    ```
    pdk test unit
    ```
    ✏️ **Note:** In the output message, notice the failures related to the Windows OS:
    ```
    12 examples, 4 failures
    ```
7. Return to the **metadata.json** file and replace the existing code with the following code, which adds your module dependencies:
    ```
    {
      "name": "instruqt-nginx",
      "version": "0.1.0",
      "author": "instruqt",
      "summary": "",
      "license": "Apache-2.0",
      "source": "",
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
        {
          "operatingsystem": "CentOS",
          "operatingsystemrelease": [
            "7"
          ]
        },
        {
          "operatingsystem": "OracleLinux",
          "operatingsystemrelease": [
            "7"
          ]
        },
        {
          "operatingsystem": "RedHat",
          "operatingsystemrelease": [
            "8"
          ]
        },
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
          "version_requirement": ">= 6.21.0 < 8.0.0"
        }
      ],
      "pdk-version": "2.3.0",
      "template-url": "pdk-default#2.3.0",
      "template-ref": "tags/2.3.0-0-g8aaceff"
    }

    ```
8. In the VS Code terminal window, run the unit tests again:
    ```
    pdk test unit
    ```
    ✏️ **Note:** In the output message, notice that the catalog for Windows environments still fails - this is because we need to add additional configuration for module dependencies during unit testing.<br><br>
9. In VS Code Explorer, navigate to the **.fixtures.yaml** file. Replace the existing code with the following code, which ensures that dependencies are handled correctly during unit testing:
    ```
    # .fixtures.yml
    ---
    fixtures:
      forge_modules:
        stdlib: "puppetlabs/stdlib"
        chocolatey: "puppetlabs/chocolatey"
        powershell: "puppetlabs/powershell"
        registry: "puppetlabs/registry"
    ```

8. From the VS Code terminal window, run the unit tests again:
    ```
    pdk test unit
    ```
    ✅ **Result:** Notice the success message in the output:
    ```
    12 examples, 0 failures
    ```

9.  In the VS Code terminal window, run the acceptance test on a clean test node again:
    ```
    bolt apply -e "include nginx" --no-ssl-verify --user instruqt --password Passw0rd! --targets winrm://winagent
    ```
    ✏️ **Note:** In the output message, notice that Bolt fails to run the module against your Windows test node:
    ```
    ...
    Failed on winrm://winagent:
      The task failed with exit code 1 and no stdout, but stderr contained:
      ruby.exe : C:/Program Files/Puppet Labs/Puppet/puppet/lib/ruby/vendor_ruby/puppet/type.rb:1986:in `block (2 levels) in providify': Parameter provider failed on Package[nginx]: Invalid package provider 'chocolatey' (Puppet::ResourceError)
    ...
    ```
10. In VS Code Explorer, navigate to the **bolt-project.yaml** file and replace the existing code with the following code to add module dependencies to correctly handle dependencies when testing with Bolt:
    ```
    # bolt-project.yaml
    ---
    name: nginx
    modules:
      - name: puppetlabs/chocolatey
        version_requirement: '6.0.1'
    ```
    ✏️ **Note:** Notice that in this case you don't need to include all the dependencies. Bolt will handle these for you in the next step.<br><br>
11. In the VS Code terminal, run `bolt module install` to install the required modules:
    ```
    bolt module install
    ```
12. Apply the module to the same node again to check for success:
    ```
    bolt apply -e "include nginx" --no-ssl-verify --user instruqt --password Passw0rd! --targets winrm://winagent
    ```
13. Manually test the node to ensure the nginx service is running:
    ```
    Invoke-WebRequest http://winagent:80
    ```

✅ **Result:** Notice the success message in the output:
```
StatusCode: 200
StatusDescription: OK
```
---
🎈 **Congratulations!**
In this lab, you enhanced your module to support Windows in addition to Red Hat by introducing logic to handle different package managers across the various operating systems running in your fleet. In this case Windows does not ship with a default package manager capable of downloading installation media from the internet, and we extended our code base to use Chocolately on Windows nodes to solve that problem. You also learned how to manage local module dependencies in the module `metadata.json` file and how to use Bolt to easily test changes during development.
