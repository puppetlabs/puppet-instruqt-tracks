---
slug: acceptance-test-a-new-module
id: 8zq9jnuyjgr1
type: challenge
title: Acceptance test a new module
teaser: Run acceptance tests on your module using Bolt, and then establish resource
  relationships for your module.
notes:
- type: text
  contents: |-
    In this lab you will:

     - Run an acceptance test on a module by applying it to a test node using Bolt, and then run commands locally to verify that it works as expected.
     - Develop the module to use resource relationships, which will enable the Puppet agent to apply changes and converge in a single run.

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
- title: Linux Agent 3
  type: terminal
  hostname: nixagent3
- title: Lab Help Guide
  type: website
  url: https://puppet-kmo.gitbook.io/practice-lab-help/
difficulty: basic
timelimit: 1500
---
Manually test your new node starting state
========

1. On the **Windows Workstation** tab, from the **Start** menu, open **Visual Studio Code**.
2. Optional: Enable VS Code autosave by clicking **File** > **Auto Save**.

    ✏️ **Note:** By enabling autosave, you don't need to remember to save your changes as you work, ensuring your edits won't be lost.<br><br>

3. Open the `C:\CODE` directory. Click **File** > **Open Folder**, navigate to the `C:\CODE` directory and click **Select Folder**.
4. In VS Code, open a terminal. Click **Terminal** > **New Terminal**.
5. In the terminal window, run the following command:
    ```
    Invoke-WebRequest http://nixagent2:80
    ```
    ✏️ **Note:** Notice the failure message in the output, which tells you that nothing is responding on port 80 on your test nodes:
    ```
    Invoke-WebRequest : Unable to connect to the remote server
    ```

Create a Bolt project to help you test your module
========
1. In the VS Code terminal window, run the following command to navigate to the **nginx** module directory:
    ```
    cd nginx
    ```

2. Create a Bolt project:
    ```
    bolt project init
    ```

3. In VS Code Explorer, open the newly created **bolt-project.yaml** file (in **nginx** > **bolt-project.yaml**). Notice that your nginx module is automatically included in the file:
    ```
    # bolt-project.yaml
    ---
    name: nginx
    modules: []
    ```

4. In the VS Code terminal window, run `bolt apply` to test your module's functionality against **nixagent2**:
    ```
    bolt apply --execute 'include nginx' --no-host-key-check -u root --private-key C:\ProgramData\ssh\id_rsa --target nixagent2
    ```
    ✏️ **Note:** Notice the failure message in the output. This is a dependency failure:
    ```
    Resources failed to apply for nixagent2
    ...
    Failed on 1 target: nixagent2
    ```

5.  Run **bolt apply** a second time:
    ```
    bolt apply --execute 'include nginx' --no-host-key-check -u root --private-key C:\ProgramData\ssh\id_rsa --target nixagent2
    ```
    ✏️ **Note:** Notice the success message in the output. The second run converges and the service is now running:
    ```
    Successful on 1 target: nixagent2
    ```

6.  Confirm that the service is operational by running an acceptance test:
    ```
    Invoke-WebRequest http://nixagent2:80
    ```
    ✅ **Result:** It works! Notice the success message in the output:
    ```
    StatusCode        : 200
    StatusDescription : OK
    ```

    ⚠️ **Important:** Although the acceptance test worked, this is actually known as a convergance bug, which means that the order in which resources are managed causes initial runs to fail. Let's fix it!

Enhance unit tests to expose the failure point
========

1. In VS Code Explorer, open the **nginx_spec.rb** unit test file (in **spec** > **classes** > **nginx_spec.rb**). Replace the existing code with the following code, which updates the unit test for the resources package and service with a relationship matcher:
    ```
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
    ```

2. In the VS Code terminal window, run the updated test:
    ```
    pdk test unit
    ```
    ✏️ **Note:** Observe the failure output. You have added a clause for the test to expect the package to be before the service, but you have not yet updated the module code to enforce that rule:
    ```
      1) nginx on centos-7-x86_64 is expected to contain Service[nginx] that requires Package[nginx]
        Failure/Error: it { is_expected.to contain_service('nginx').that_requires('Package[nginx]') }
          expected that the catalogue would contain Service[nginx] with that requires Package[nginx]
        # ./spec/classes/nginx_spec.rb:10:in `block (4 levels) in <top (required)>'
    ```

3. In VS Code Explorer, navigate to the **init.pp** file (in **manifests** > **init.pp**). Replace the code with the following code, which fixes the bug by adding a resource relationship between the service and the package:
    ```
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
    ```

4. In the VS Code terminal window, run the unit tests again:
    ```
    pdk test unit
    ```
    ✅ **Result:** Notice the success message:
    ```
    8 examples, 0 failures
    ```

Test changes on a new node
========

1. In the VS Code terminal window, apply and run an acceptance test for your changes on **nixagent3**, which is a clean test node:
    ```
    bolt apply --execute 'include nginx' --no-host-key-check -u root --private-key C:\ProgramData\ssh\id_rsa --target nixagent3
    ```
    ✅ **Result:** Notice the success message in the output. This indicates that the resources were managed in the correct order, which allowed a single run to enforce your desired state:
    ```
    Successful on 1 target: nixagent3
    ```

2.  Test the service by running the following command:
    ```
    Invoke-WebRequest http://nixagent3:80
    ```
    ✅ **Result:** Notice the success message in the output:
    ```
    StatusCode        : 200
    StatusDescription : OK
    ```

---
🎈 **Congratulations!**
You used Bolt to test your module on a set of fresh test nodes. You also improved the unit tests that accompany the module to ensure all features work as expected.