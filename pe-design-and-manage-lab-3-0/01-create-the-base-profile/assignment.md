---
slug: create-the-base-profile
id: 2kemewf7bxic
type: challenge
title: Create a base profile
teaser: Create a base profile that shows a dynamic login message when you log into
  any node.
notes:
- type: text
  contents: |-
    In this lab you will:

    - Add a base profile to existing roles. You'll discover how Puppet cannot build a catalog until you create the classes that you include in your `.pp` files!
    - Use Puppet Development Kit (PDK) to create a base profile class.
    - Add a class to the base profile to show a dynamic, role-specific message of the day (motd) based on information retrieved from the node's trusted facts.
    - Log into nodes that have different roles to see the dynamic login message.

    Click **Start** when you're ready to begin.
tabs:
- title: Windows Agent
  type: service
  hostname: guac
  path: /#/client/c/winagent?username=instruqt&password=Passw0rd!
  port: 8080
- title: PE Console
  type: service
  hostname: puppet
  path: /
  port: 443
- title: Primary Server
  type: terminal
  hostname: puppet
- title: Linux Agent 1
  type: terminal
  hostname: nixagent1
- title: Linux Agent 2
  type: terminal
  hostname: nixagent2
- title: Git Server
  type: service
  hostname: gitea
  path: /
  port: 3000
- title: "Bug Zapper \U0001F99F⚡"
  type: website
  hostname: guac
  url: https://docs.google.com/forms/d/e/1FAIpQLSfQK4DblKykkrbbRRp9Wofb9ehFXf2YSmVgQFlaDYe0iDzT-A/viewform?embedded=true
difficulty: basic
timelimit: 7200
---
# Create a control repo on your Windows development workstation
1. ![switch tabs](https://storage.googleapis.com/instruqt-images/Instruct%20Icons/icon_switch_tabs_white_32.png) Switch to the **Windows Agent** tab.
2. From the **Start** menu, open **Visual Studio Code**.
3. Enable autosave so that you don't have to remember to save your changes. Click **File** > **Auto Save**.
4. Open the `C:\CODE` directory. Click **File** > **Open Folder**, navigate to the `C:\CODE` directory and click **Select Folder**.
5. If prompted to trust the code in this directory, click **Accept**.
6. In VS Code, open a terminal. Click **Terminal** > **New Terminal**.
7. In the VS Code terminal window, run the following command:

        git clone git@gitea:puppet/control-repo.git
---
# Include a base profile in your roles
1. Check out the **webapp** feature branch:
      ```
      cd control-repo
      git checkout webapp
      ```

3. Open the `site-modules/role/manifests/cmsweb.pp` role file and include an initial base profile by replacing the existing code with the following code:
    ```
    # site-modules/role/manifests/cmsweb.pp
    class role::cmsweb {
      include profile::base
    }
    ```

4. Repeat for the `ecommerce.pp` role in the same directory.
    ```
    # site-modules/role/manifests/ecommerce.pp
    class role::ecommerce {
      include profile::base
    }
    ```
5. Repeat for the `cmsloadbalancer.pp` role in the same directory.
    ```
    # site-modules/role/manifests/cmsloadbalancer.pp
    class role::cmsloadbalancer {
      include profile::base
    }
    ```
6. Validate your code by running `pdk validate`.

    💡 **Tip:** When prompted whether or not you consent to anonymous PDK usage information, choose whichever option you prefer.
     ```
    cd site-modules\role
    pdk validate
    ```
    ✔️ **Result:** PDK indicates that your code is valid.
6. Commit and push your code to your feature branch.
    ```
    git add .
    git commit -m "Add base profile to roles"
    git push
    ```
---
# Trigger a Puppet run against your environment branch
1. ![switch tabs](https://storage.googleapis.com/instruqt-images/Instruct%20Icons/icon_switch_tabs_white_32.png) Switch to the **PE Console** tab and log in with username `admin` and password `puppetlabs`.

2. Navigate to the **Node groups** page; then, expand the **All Environments** group and click **Development environment**.
3. On the **Classes** tab, click **Refresh** (on the right-hand side of the page) to reload the classes you just pushed.
4. On the **Matching nodes** tab, ensure that all your nodes are listed for this group.
5. Run Puppet in the `webapp` environment.
    1. In the upper-right corner, click **Run** > **Puppet**. You will be redirected to the **Run Puppet** page.
    2. Under **Environment**, click **Select an environment for nodes to run in**.
    3. Select **webapp**.
    4. Click **Run Job** at the lower right to kick off a Puppet run.
1. When the jobs finish running, click any node's report link in the **Report** column.
1. On the **Log** tab, notice the following error:

    ```
    Error: Error while evaluating a Function Call, Could not find class ::profile::base
    ```

    ❔ **Why did Puppet fail to compile the catalog?**<br>The base profile class you included in your roles doesn't exist yet.
---
# Create a base profile
1. ![switch tabs](https://storage.googleapis.com/instruqt-images/Instruct%20Icons/icon_switch_tabs_white_32.png) Switch to the **Windows Agent** tab.

2. In the Visual Studio Code terminal, navigate to the `site-modules\profile` directory and create a base profile using PDK.

    ```
    cd ..\profile
    pdk new class profile::base
    ```

3. Replace the code in the base profile (`site-modules/profile/manifests\base.pp`) with code that declares the motd class:
    ```
    # site-modules/profile/manifests/base.pp
    # @summary A short summary of the purpose of this class
    #
    # A description of what this class does
    #
    # @example
    #   include profile::base
    class profile::base {
      class { 'motd':
          content => "Hello! You are in ${trusted['extensions']['pp_datacenter']}.\n"
      }
    }
    ```
4. Validate your code.
    ```
    pdk validate
    ```
    ✔️ **Result:** Your code passes validation.


5. Commit and push your code to your feature branch.
    ```
    git add .
    git commit -m "Add base profile to roles"
    git push
    ```
    ✔️ **Result:** Your code will be automatically deployed to the primary server.

![switch tabs](https://storage.googleapis.com/instruqt-images/Instruct%20Icons/icon_switch_tabs_white_32.png) Switch to the **PE Console** tab.

6. Trigger a Puppet run against your environment branch, and then inspect the report. If you don't recall the steps, refer back to the preceding section.<br><br>💡 **Tip:** You can also go to the **Jobs** page, click the **Puppet run** tab and click the most recent job. Then, click **Run again** > **All nodes** in the upper-right corner, and click **Run job** near the bottom of the page.
---
# See the change
Follow the instructions for each OS below to verify that your changes took effect.

|Windows             |Linux            |
|--------------------|--------------------|
|<ol><li>![swtich tabs](https://storage.googleapis.com/instruqt-images/Instruct%20Icons/icon_switch_tabs_white_32.png) Switch to the **Windows Agent** tab.</li><br><li>Click the **Start** menu.</li><br><li>Click the user icon.</li><br><li>Select **Sign Out**.</li><br><li>When presented with the **Reconnect** option, click **Reconnect**.<br><br>✔️ **Result:** The message of the day appears on the login screen.</li></ol>|<ol><li>![swtich tabs](https://storage.googleapis.com/instruqt-images/Instruct%20Icons/icon_switch_tabs_white_32.png) Switch to the **Linux Agent** tab.</li><br><li>In the terminal, type the command `ssh root@localhost`.</li><br><li>Type `yes` when prompted.<br><br>✔️ **Result:** The message of the day appears.</li></ol><br><br><br><br><br>|

🎈 **Congratulations!**
Using the roles and profiles pattern, you built a base profile — a building block that defines a shared feature set across many nodes — to customize the login message of your nodes.
---

**Find any bugs or have feedback? Click the **Bug Zapper** tab near the top of the page and let us know!**

To close this lab, click **Next**.