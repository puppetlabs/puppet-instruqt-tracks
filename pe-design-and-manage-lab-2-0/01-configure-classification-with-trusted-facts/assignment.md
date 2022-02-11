---
slug: configure-classification-with-trusted-facts
id: ns2rbfx52q8q
type: challenge
title: Assign classes to nodes by using trusted facts
teaser: Write code that uses trusted facts to classify nodes, and then create and
  populate the placeholder classes for those roles.
notes:
- type: text
  contents: |-
    In this lab, you will:

     - Modify the `site.pp` file in your control repo to classify nodes and assign *role* classes to them by using trusted facts.
     - Create placeholder code to build out the initial roles (ecommerce, cmsweb, and cmsloadbalancer).
     - Test your changes by running Puppet.

     You'll complete these tasks on tabs that correspond to a Windows node and the PE console. Feel free to explore the other tabs - for example, check out the Linux nodes, which each run an agent.

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
- title: Lab Help Guide
  type: website
  url: https://puppet-kmo.gitbook.io/practice-lab-help/
difficulty: basic
timelimit: 3000
---
Create a local control repository and update site.pp in the webapp feature branch
========
1. Click the **Windows Agent** tab to go to the **Windows Agent** node. Then, click the **Start** menu and open **Visual Studio Code**.

2. Enable VS Code autosave by clicking **File** > **Auto Save**.<br><br>✏️ **Note:** This step isn’t required, but by enabling Auto Save, you don't need to remember to save your changes as you work, ensuring your edits won't be lost.<br><br>

3. Open the `CODE` directory. Click **File** > **Open Folder**, navigate to the `C:\CODE` directory and click **Select Folder**.

4. In VS Code, open a terminal. Click **Terminal** > **New Terminal**.

5. In the terminal window, run the following command to clone the control repo. When prompted, enter **yes** to add the Gitea server to known hosts.

    ```
    git clone git@gitea:puppet/control-repo.git
    ```

6. Configure a git username and email by running the following command:

    ```
    git config --global user.email "noreply@puppet.com"
    git config --global user.name "Puppet User"
    ```

7. Check out a new feature branch named <b>webapp</b>:

    ```
    cd control-repo
    git checkout -b webapp
    ```

    🔀 Switch to the **PE Console** tab.<br><br>

8. Log into the PE Console with username `admin` and password `puppetlabs`.

9. Navigate to the **Nodes** page. For each node, click its link and examine the contents of the node's facts (retrieved by Facter) on the **Facts** tab. Then, find the trusted facts by searching for the word **trusted** and notice the value shown for each node's `pp_role` trusted fact:<br>

    | Node      | Value             |
    | --------  |------             |
    | nixagent1 | "cmsweb"          |
    | nixagent2 | "cmsloadbalancer" |
    | winagent  | "ecommerce"       |

    🔀 Switch to the **Windows Agent** tab.<br><br>

10. In VS Code, open the `control-repo/manifests/site.pp` file. To classify your nodes by using the `pp_role` trusted fact, replace the content beneath `## Node Definitions ##` with the following code:

    ```
    # control-repo/manifests/site.pp
    node default {
      include "role::${trusted['extensions']['pp_role']}"
    }
    ```

11. In the VS Code terminal, commit and push your code to the <b>webapp</b> feature branch:

    ```
    git add .
    git commit -m "Add pp_role to site.pp"
    git push -u origin webapp
    ```

Run Puppet using the webapp environment branch and inspect the reports
========
🔀 <a name="run-puppet"> Switch to the **PE Console** tab.</a>

1. Navigate to the **Node groups** page; then, expand the **All Environments** group (click the plus sign (**+**) beside the group name) and click **Development environment**.

2. Click the **Classes** tab, and then click **Refresh** (on the right-hand side of the page) to reload the classes you just pushed.

3. On the **Matching nodes** tab, ensure all your nodes are listed for this group:

    - `nixagent1... svc.cluster.local`
    - `nixagent2... svc.cluster.local`
    - `winagent... svc.cluster.local`

4. In the upper-right corner, click **Run > Puppet**.

5. You will be redirected to the **Run Puppet** page. Select the following options:
    - **Environment**: Click **Select an environment for nodes to run in:** and choose **webapp** from the list.
    - **Schedule**: Accept the default settings.
    - **Run options**: Accept the default settings.

6. In the lower-right corner, click **Run Job** to run Puppet on all the nodes shown. You will be redirected to the **Job details** page.

7. When the jobs finish running, click the **winagent** node's report link in the **Report** column.

8. On the report page, click the **Log** tab to review the output contained in the error message: `Could not find class ::role::ecommerce`

❔ **Question: Why did Puppet fail to compile the catalog?**
The compiler tried to autoload the `role::ecommerce` class, but this class doesn't exist yet.

To return to the job's report page (for example, to run the job again or explore errors on other nodes), click **Jobs** in the left navigation, and on the **Puppet run** tab, click the job in the **Job ID** column.

Create the role::<ROLE NAME> classes
========
🔀 Switch to the **Windows Agent** tab.

1. From the VS Code terminal, navigate to your role directory:
    ```
    cd site-modules\role
    ```

2. Run the following PDK command to create the `role::ecommerce` class. This command creates the `site-modules\role\manifests\ecommerce.pp` manifest file.
    ```
    pdk new class role::ecommerce
    ```
    💡 **Tip:** When prompted whether or not you consent to anonymous PDK usage information, choose whichever option you prefer.<br><br>

4. Modify the new `ecommerce.pp` file to include placeholder code for your new role, as in this example:
    ```
    # @summary A short summary of the purpose of this class
    #
    # A description of what this class does
    #
    # @example
    #   include role::ecommerce
    class role::ecommerce {
      notify { 'Hello! my role is: ${trusted[\'extensions\'][\'pp_role\']} \
        and I\'ve been running for ${facts[\'uptime\']}':
      }
    }
    ```
5. In the `site-modules\role` directory from your terminal, run the `pdk validate` command.

    ✔️ **Result:** You'll receive an error message: `pdk (ERROR): puppet-lint: single quoted string containing a variable found`.

    ❔ **Why did this happen?**<br>Remember, you must interpolate the string for the value of the `$trusted['extensions']['pp_role']` variable. Fix this by replacing the single quotes with double quotes and removing the backslashes so that your code looks like this example:
    ```
    class role::ecommerce {
      notify { "Hello! my role is: ${trusted['extensions']['pp_role']} \
         and I've been running for ${facts['uptime']}":
      }
    }
    ```

6. From the `site-modules\role` directory in the terminal, run `pdk validate` again.

7. Commit and push your changes to the <b>webapp</b> branch.
    ```
    git add .
    git commit -m "Add ecommerce role"
    git push origin webapp
    ```

   🔀 Switch to the **PE Console** tab.<br><br>

8. Run Puppet using your environment branch <b>webapp</b> again, and then inspect the node reports.
    💡 **Need a refresher?** Review the steps shown in the "[**Run Puppet ...**](#run-puppet)" section above.

    ✔️ **Result:** The Windows agent succeeds but the two Linux agents still fail. Fix this by assigning roles to each of the nodes.

    🔀 Switch to the **Windows Agent** tab.<br><br>

9. In the VS Code terminal, from the `control-repo\site-modules\role` directory, run `pdk new class role::cmsweb`. Then, run `pdk new class role::cmsloadbalancer`.

10. Add the following code to the `cmsweb.pp` file:

    ```
    # @summary A short summary of the purpose of this class
    #
    # A description of what this class does
    #
    # @example
    #   include role::cmsweb
    class role::cmsweb {
      notify { "Hello! my role is: ${trusted['extensions']['pp_role']} \
      and I've been running for ${facts['uptime']}": }
    }
    ```

11. Add the following code to the `cmsloadbalancer.pp` file:

    ```
    # @summary A short summary of the purpose of this class
    #
    # A description of what this class does
    #
    # @example
    #   include role::cmsloadbalancer
    class role::cmsloadbalancer {
      notify { "Hello! my role is: ${trusted['extensions']['pp_role']} \
      and I've been running for ${facts['uptime']}": }
    }
    ```

12. Push your code to the `webapp` branch:
    ```
    git add .
    git commit -m "Add cmsweb and cmsloadbalancer roles"
    git push origin webapp
    ```

    🔀 Switch to the **PE Console** tab.<br><br>

13. Run the job again against all the nodes in one of these ways:
    - On the **Jobs** page, click the **Puppet run** tab and click the most recent job. Then, click **Run again** > **All nodes** in the upper-right corner, and click **Run job** near the bottom of the page.
    - On the **Node groups** page, open the `Development environments` group and run Puppet against all three nodes in the **webapp** environment.<br><br> ✔️ **Result:** All three nodes finish successfully when their respective report link is inspected.

---

## 🎈 **Congratulations!**
You created a local repo and updated the webapp feature branch. You then identified each node's `pp_role` trusted fact and modified the site.pp file to classify your nodes by using that fact. After running Puppet and reviewing the error messages in the reports, you created the `role::ecommerce` class and added placeholder code. Then, you created the `role::cmsweb` and `role::cmsloadbalancer` classes for the other servers in this simulated production environment.

To continue, click **Next**.
