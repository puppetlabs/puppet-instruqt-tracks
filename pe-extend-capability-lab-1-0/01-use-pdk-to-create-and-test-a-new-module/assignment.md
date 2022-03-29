---
slug: use-pdk-to-create-and-test-a-new-module
id: 7ubt77uaipci
type: challenge
title: Use PDK to create and test a new module
teaser: Use PDK to create, test, and validate a new module and a new class.
notes:
- type: text
  contents: |
    In this lab, you will:

    - Use the **puppet resource** command to explore the current state of your test nodes and produce Puppet code that you will use to develop your module.

    - Use **pdk new module** and **pdk new class** to create a module, a class, and a simple unit test. These commands save you time, eliminating the need for you to write boilerplate code. Then, you'll extend the unit tests to fail first before adding code to make them pass.

    - Use **pdk validate** to validate your code for syntax and style, and then run **pdk test unit** to run your unit tests to make sure your code compiles and the class behaves as expected.

    - Add the Puppet code you obtained from step one to manage the resources for the NGINX package and service. Then, run **pdk validate** to validate the code for syntax and style before running your unit test to ensure your code compiles and functions as expected.
tabs:
- title: Linux Agent 1
  type: terminal
  hostname: nixagent1
- title: Linux Agent 2
  type: terminal
  hostname: nixagent2
- title: Windows Workstation
  type: service
  hostname: guac
  path: /#/client/c/workstation?username=instruqt&password=Passw0rd!
  port: 8080
- title: Lab Help Guide
  type: website
  url: https://puppet-kmo.gitbook.io/practice-lab-help/
difficulty: basic
timelimit: 1500
---
Run the puppet resource command to explore the state of resources on the system.
========
🔀 Start on the **Linux Agent 1** tab.

1. Use the `puppet resource` command to inspect the state of resources on the target Linux servers and produce Puppet code that you can use in your new module. Start by exploring the installed nginx package. On `Linux Agent 1`, run the following command:

    ```
    sudo -i puppet resource package nginx
    ```

    ✅ **Result:** The command returns what it discovers about the installed package — in this case, the package version number.

    ```
    package { 'nginx':
      ensure => '1:1.20.1-9.el7',
    }
    ```

2. Now, explore the state of the nginx service:
    ```
    sudo -i puppet resource service nginx
    ```
    ✅ **Result:** The command produces the following output, indicating the service is running and starts when the system starts up:
    ```
    service { 'nginx':
      ensure   => 'running',
      enable   => 'true',
    }
    ```

🔀 Switch to the **Linux Agent 2** tab.

1. Run the same commands on `Linux Agent 2` and compare the results to the previous output. First, explore the status of the nginx package:
    ```
    sudo -i puppet resource package nginx
    ```
    ✅ **Result:** The output indicates the package is absent from the system. Some package providers don't distinguish between 'purged' and 'absent' — that's okay.
    ```
    package { 'nginx':
      ensure   => 'purged'
    }
    ```

2. Inspect the nginx service:
    ```
    sudo -i puppet resource service nginx
    ```
    ✅ **Result:** The output indicates the service doesn't exist or isn't running:
    ```
    service { 'nginx':
      ensure   => 'stopped',
      enable   => 'false
    }
    ```
    ✏️ **Note:** Notice the differences in the output. This output shows that nginx is not installed on Linux Agent 2. This will be your "clean" test node.

Use PDK to create a module
========

🔀 Switch to the **Windows Workstation** tab.

1. From the **Start** menu, open **Visual Studio Code**.
2. Optional: Enable VS Code autosave by clicking **File** > **Auto Save**.

    ✏️ **Note:** By enabling Auto Save, you don't need to remember to save your changes as you work, ensuring your edits won't be lost.<br><br>

3. Open the `C:\CODE` directory. Click **File** > **Open Folder**, navigate to the `C:\CODE` directory and click **Select Folder**.
4. In VS Code, open a terminal. Click **Terminal** > **New Terminal**.
1. Run the following PDK command to create a new module - select **support only on RedHat** (for now):
    ```
    pdk new module nginx
    ```
    - When prompted whether you consent to the collection of anonymous PDK usage information, choose either option.
    - For questions 1-3 (Q 1/4, Q 2/4, and so on), press **Enter** to accept the default settings.
    - For question 4, leave only **RedHat** selected. Use the up/down arrows to move between selections and use the spacebar to clear the other selected options; then, press **Enter**.
    - At the **Metadata will be generated...** prompt, press **Enter**.<br><br>
1. In the VS Code file browser, click the newly created **nginx** module folder to expand its contents.
8. Click the **metadata.json** file to open it. Notice the correct Linux distributions (distros) are listed under "operatingsystem_support":
    ```
      "operatingsystem_support": [
        {
          "operatingsystem": "CentOS",
          "operatingsystemrelease": [
            "7"
          ]
        },
    ```

Use PDK to create a new class
========

1. In the VS Code terminal, navigate to the new class directory:
    ```
    cd nginx
    ```
2. Create the main class for the module:
    ```
    pdk new class nginx
    ```
    ✏️ **Note:** Notice the new files.<br><br>

3. From within the same directory, run `pdk validate`:
    ```
    pdk validate --puppet-version=6
    ```
    ✏️ Note: Wait for the `pdk validate` command to finish before continuing.

Add test conditions to the unit test file created by PDK
========

1. In VS Code Explorer, open the `nginx_spec.rb` unit test file (in **spec** > **classes**).
1. Replace the existing content with the following code, which adds additional tests:
    ```
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
    ```

1. In the VS Code terminal window, run the new tests by invoking PDK from the root of the module directory:
    ```
    pdk test unit
    ```
1. A section of the command output will look like this:
    ```
    Finished in 8.11 seconds (files took 18.38 seconds to load)
    12 examples, 8 failures

    Failed examples:

    rspec './spec/classes/nginx_spec.rb[1:1:2]' # nginx on centos-7-x86_64 is expected to contain Package[nginx]
    rspec './spec/classes/nginx_spec.rb[1:1:3]' # nginx on centos-7-x86_64 is expected to contain Service[nginx]
    rspec './spec/classes/nginx_spec.rb[1:2:2]' # nginx on oraclelinux-7-x86_64 is expected to contain Package[nginx]
    rspec './spec/classes/nginx_spec.rb[1:2:3]' # nginx on oraclelinux-7-x86_64 is expected to contain Service[nginx]
    rspec './spec/classes/nginx_spec.rb[1:3:2]' # nginx on redhat-8-x86_64 is expected to contain Package[nginx]
    rspec './spec/classes/nginx_spec.rb[1:3:3]' # nginx on redhat-8-x86_64 is expected to contain Service[nginx]
    rspec './spec/classes/nginx_spec.rb[1:4:2]' # nginx on scientific-7-x86_64 is expected to contain Package[nginx]
    rspec './spec/classes/nginx_spec.rb[1:4:3]' # nginx on scientific-7-x86_64 is expected to contain Service[nginx]
    ```

The tests fail because you haven't written code to install and configure the package and the resulting service. **This is intentional!** Next, you will add code that satisfies the tests. This is an example of doing **red/green** or **test-driven** development.<br><br>

Use data gathered by the puppet resource command to fix the test
========

1. In VS Code Explorer, open the **init.pp** file (in **manifests**).
1. Replace the existing content with the following code, which will add functionality to your module:
    ```
    # @summary A short summary of the purpose of this class
    # A description of what this class does
    # @example
    #   include nginx
    class nginx {
      service { 'nginx':
        ensure => running,
        enable => true,
      }
      package { 'nginx':
        ensure => latest,
      }
    }
    ```
1. In the VS Code terminal window, run `pdk validate` to validate your syntax and lint:
    ```
    pdk validate --parallel
    ```

1. Run the following command to ensure the tests you added earlier will now pass:
    ```
    pdk test unit
    ```

✅ **Result:** The output shows `0 failures` — the test now passes!

---

🎈 **Congratulations!**
You wrote your first module and a set of meaningful unit tests to go along with the functionality you introduced. You also used the `puppet resource` command to explore an existing environment to gain insight into your current environment and learned how to use PDK to easily generate templates.
