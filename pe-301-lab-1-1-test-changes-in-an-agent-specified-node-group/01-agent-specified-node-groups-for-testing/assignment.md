---
slug: agent-specified-node-groups-for-testing
id: byvczbgv7ity
type: challenge
title: Use an agent-specified node group for testing
teaser: Configure PE so you can implement environment-based testing using a one-time
  run exception environment group.
notes:
- type: text
  contents: |-
    In this lab you will configure PE so that you can implement environment-based testing using a one-time run exception environment group.

    By making a breaking change to the one-time exception environment, you'll discover the relationship (through inheritance) between the development environment and the one-time exception environment.

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
- title: Linux Agent 3
  type: terminal
  hostname: nixagent3
- title: Git Server
  type: service
  hostname: gitea
  path: /
  port: 3000
- title: Lab Help Guide
  type: website
  url: https://puppet-kmo.gitbook.io/practice-lab-help/
difficulty: basic
timelimit: 2400
---
Create a control repo on your Windows development workstation
========
1. On the **Windows Agent** tab, from the **Start** menu, open **Visual Studio Code**.
2. Enable autosave so that you don't have to remember to save your changes. Click **File** > **Auto Save**.
3. Open the `C:\CODE` directory. Click **File** > **Open Folder**, navigate to the `C:\CODE` directory and click **Select Folder**.

    ✏️ **Note:** If prompted to trust the code in this directory, click **Accept**.<br><br>

4. In VS Code, open a terminal. Click **Terminal** > **New Terminal**.
5. In the VS Code terminal window, run the following command:
    ```
    git clone git@gitea:puppet/control-repo.git
    ```

Add a debug message to all nodes by updating site.pp
========
1. Check out the `webapp` feature branch:
    ```
    cd control-repo
    git checkout webapp
    ```
2. Navigate to **control-repo** > **manifests** > **site.pp** and replace the existing code with the following code:
    ```
    # control-repo/manifests/site.pp
    node default {
        include "role::${trusted['extensions']['pp_role']}"
        notify { 'It worked! This is experimental code on your feature branch!': }
    }
    ```
3. Push your changes to the control repo via Git:
    ```
    git add .
    git commit -m "Add debug message to site.pp"
    git push
    ```

Make a breaking change to the Development one-time run group to show agent-specifed environment inheritance
========

  🔀 Switch to the **PE Console** tab.

1. Log into PE with username `admin` and password `puppetlabs`.
2. Navigate to the **Node groups** page.
3. Expand the **All Environments** group, expand the **Development environment** group, and click **Development one-time run exception**.
4. Make a breaking change to this group's rules. This will show you how runtime evaluation occurs during the Puppet run with an agent-specifed environment as a result of inheritance from the **Development** group. Add a new rule that has the following values, click **Add rule**, and commit your changes (click **Commit** at the bottom of the page):

    |Fact                            |Operator    |Value      |
    |--------------------------------|------------|-----------|
    |`agent_specified_environment`   |     `= `   |`devapp`   |

    <br>
6. Return to the **Node groups** page and click **Development environment**.

7. On the **Classes** tab, click **Refresh** (on the right-hand side of the page) to reload the classes you just pushed.

    ✏️ **Note:** After the classes reload, notice the text near the **Refresh** link: "Class definitions updated: a few seconds ago".<br><br>

8. In the upper-right corner, click **Run > Puppet**.

9. On the **Run Puppet** page, select the following options:

      - **Environment**: Click **Select an environment for nodes to run in:** and choose **webapp** from the list.


10. Click **Run job** and wait for jobs to complete.

✅ **Result:** Notice that none of the jobs were successful. This is because the selection of an environment causes the nodes to "fall into" the **Development one-time run exception group** during the Puppet run. In this case, the rule that you introduced means that you can only apply the nonexistent **devapp** branch. In the next steps, you'll fix those rules.

Fix the broken rule and then run Puppet against the development group, specifying the webapp branch
========
1. In the PE console, navigate to the **Node groups** page.
2. Expand the **All Environments** group; then, expand **Development environment** and click **Development one-time run exception**.
3. Remove the `agent_specified_environment = devapp` rule by clicking **Remove** (shown to the right) and commit the change.
4. Return to the **Node groups** page and click **Development environment**.
5. In the upper-right corner, click **Run > Puppet**.
6. You will be redirected to the **Run Puppet** page. Select the following options:

      - **Environment**: Click **Select an environment for nodes to run in:** and choose **webapp** from the list.



7. Click **Run job** and wait for jobs to complete.

✅ **Result:** Your infrastructure includes three Linux nodes and a Windows node. When the run is complete, notice that you have log entries for all nodes except Nixagent3. Next, you will explore why that is.

Investigate missing facts on new nodes
========
1. Navigate to the **Nodes** page.
2. From the **Filter by** list, select **PQL Query**.
3. From the **Common queries** list, select **Nodes with a specific fact and fact value**.
4. Replace the query text with the following text, and then click **Submit query**:
    ```
    inventory[certname] { trusted.extensions.pp_environment = "development" }
    ```
✅ **Result:**  Notice that the nixagent3 node is missing from the results. Go to the **Status** page and then select and copy the full name of the nixagent3 node. This node isn't in the list because it's missing the pp_environment fact. You will fix this issue by pinning the node to the **Development environment** group.

Pin the node with the missing fact to the Development environment group
========
1. Navigate to the **Node Groups** page and click **Development environment**.
2. In the **Certname** field, paste the name of the node you just copied, click **Pin node**, and commit the change.
3. Kick off another Puppet run for the **Development** group, specifying the `webapp` branch environment. In the upper-right corner, click **Run > Puppet** with the following options:

      - **Environment**: Click **Select an environment for nodes to run in** and choose **webapp** from the list.


4. Click **Run job** and wait for jobs to complete.

✅ **Result:** When the run finishes, notice that you have a log and a successful run for the new node that was pinned to the **Development** node group.

---
## 🎈 **Congratulations!**
In this lab you configured PE so that you could implement environment-based testing using a one-time run exception environment group.