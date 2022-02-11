---
slug: use-pdk-to-create-and-test-a-new-module
id: 7ubt77uaipci
type: challenge
title: Use PDK to create and test a new module
tabs:
- title: workstation
  type: service
  hostname: guac
  path: /#/client/c/winagent?username=instruqt&password=Passw0rd!
  port: 8080
- title: nixagent1
  type: terminal
  hostname: nixagent1
- title: nixagent2
  type: terminal
  hostname: nixagent2
difficulty: basic
timelimit: 7200
---
Use puppet resource commands to explore existing environment state
========
Steps
1. Use the puppet resource command to inspect the current state of your target linux servers and produce puppet code you can use in your new module; first explore installed packages:
# run on nixagent1
```
sudo -i puppet resource package nginx
```
Should produce output:
```
package { 'nginx':
  ensure => '1:1.20.1-9.el7',
}
```
2. Next explore the state of the service:
# run on nixagent1
```
sudo -i puppet resource service nginx
```
Should produce output:
```
service { 'nginx':
  ensure   => 'running',
  enable   => 'true',
  provider => 'systemd',
}
```

3. Compare to the output when running the same commands on nixagent2 first exploring the status of the installed package:
# run on nixagent2
```
sudo -i puppet resource package nginx
```
output:
```
package { 'nginx':
  ensure   => 'absent'
  provider => 'dnf',             # provider is redundant - a provider will be invoked automatically based on facts
}
```
4. Next inspect the service:
```
sudo -i puppet resource service nginx
```
output:
```
service { 'nginx':
  ensure   => 'stopped',
  enable   => 'false
  provider => 'systemd',
}
```
# nginx is not installed on nixagent2 this is our "clean" test node

Use PDK to create a new module
========
1. On the **Workstation** tab, from the **Start** menu, open **Visual Studio Code**.
2. Enable VS Code autosave by clicking **File** > **Auto Save**.

    ✏️ **Note:** This step isn’t required, but by enabling Auto Save, you don't need to remember to save your changes as you work, ensuring your edits won't be lost.<br><br>

3. Open the `C:\CODE` directory. Click **File** > **Open Folder**, navigate to the `C:\CODE` directory and click **Select Folder**.
4. In VS Code, open a terminal. Click **Terminal** > **New Terminal**.
5. Use the following PDK command to create a new module - select support only on RedHat only (for now):
```
pdk new module nginx
```
6. Accept the defaults for questions 1-3 by pressing **Enter**, but change the settings for question 4 to only leave RedHat selected using the arrows + space bar to de-select the other defaults.
7. In the file browser in VSCode select the newly created **nginx** module folder to expand its contents
8. Select the **metadata.json** to view the contents, notice the correct linux distros are listed under "operatingsystem_support":
```
# metadata.json
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

Use PDK to create a new class
========

1. In the VSCode terminal enter the root of your new class directory with:
```
cd nginx
```
2. From within the nginx module directory use PDK to reate the main class:
```
pdk new class nginx
```
3. Run PDK validate from within the same directory
```
pdk validate
```

Add test conditions to the unit test file created by PDK
========
1. Open the **nginx_spec.rb** unit test file file from the file browser in VSCode under the spec > classes directory
2. Edit to add addtional tests:
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

5. Run the newly created tests by invoking PDK from the root of the module directory:
```
pdk test unit
```
Our tests fail because no code has been written to actually install and configure the package and the resulting service yet. In this case we have written a test guranteed to fail first, so that we may later introduce the code that satisfies the tests as an example of *Red/Green* or *Test Driven* development.

Examine the output matching the following:
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
This is because the current state of the module code doesn't actually install or configure any packages/services. Lets fix it!

Use data gathered by puppet resource
========

1. Open the **init.pp** file under the manifests directory to add functionality to our module:
2. Edit the file to contain the following:
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
3. Run pdk validate to validate your syntax and lint
```
pdk validate
```

4. Ensure our tests added earlier now pass:
```
pdk test unit
```
We expected the final lines of output to be:

```
12 examples, 0 failures
```

Congratulations! You have just written your first module as well as a set of meangingful unit tests to go along with the functionality you introduced. The puppet resource command was used to explore an existing environment to gain insight into your current envionment as well as an easy way to generate some template code.