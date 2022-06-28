---
slug: run-a-pre-built-task
id: ajujjn3lbvm9
type: challenge
title: Run a pre-built task
teaser: Discover PE's pre-built tasks and get hands-on practice running tasks.
notes:
- type: text
  contents: |-
    Puppet Enterprise (PE) ships with several pre-built tasks and plans that you can run from both the command line and the PE Console.

    In this lab, you will run tasks that accomplish the following:

    - Reboot a node that's managed by Puppet.
    - Gather facts on a specific node.
    - Stop and start the **time** service.
    - Gather system information about the PuppetDB PostgreSQL installation.
tabs:
- title: Primary Server
  type: terminal
  hostname: puppet
- title: PE Console
  type: service
  hostname: puppet
  port: 443
- title: Windows Agent 1
  type: service
  hostname: guac2
  path: /#/client/c/winagent1?username=instruqt&password=Passw0rd!
  port: 8080
- title: Workstation
  type: service
  hostname: guac
  path: /#/client/c/workstation?username=instruqt&password=Passw0rd!
  port: 8080
- title: Git Server
  type: service
  hostname: gitea
  path: /
  port: 3000
- title: Linux Agent 1
  type: terminal
  hostname: nixagent1
- title: Bug Zapper
  type: website
  url: https://docs.google.com/forms/d/e/1FAIpQLSf2KZhuIGDq8Cu0n2BjQyVZgndh_cI3V-yZR7Lv7h_22P_mnw/viewform?embedded=true
- title: Lab Help
  type: website
  hostname: guac
  url: https://puppet-kmo.gitbook.io/practice-lab-help/
difficulty: basic
timelimit: 3600
---
Run tasks from the command line
========

1. Before you can run a task, you need to know which nodes you can run tasks against. On the **Primary Server** tab, run the following command to reveal the list of nodes to choose from:
    ```
    puppetserver ca list --all
    ```

    💡 Note the `winagent` machine name. You'll use this name when you run your first task.<br><br>

1. Run the `task show` command to see a list of available tasks:
    ```
    puppet task show --all
    ```
    💡 Notice the **reboot** task. You'll run this task first.<br><br>

1. Reboot the `winagent` node by running the **reboot** command, replacing `<winagent>` with the actual name of the node that appeared in the output for step 1:
    ```
    puppet task run reboot --nodes <winagent>
    ```
    🔀 Switch to the **Windows Agent 1** tab and notice that the node is now disconnected. <br><br>

1. When you see the **Reconnect** button (after approximately 30 seconds), click it to reconnect to the **Windows Agent 1** node and complete the reboot. ![reconnect button](https://storage.googleapis.com/instruqt-images/reconnect-100.png)

    ✔️ **Result:** Congratulations! You just ran a pre-built task — in this case, the task rebooted a specific node.

    🔀 Switch to the **Primary Server** tab.<br><br>
1. Now let's run another task — this time, to return facts about the Windows node. Remember to replace `<winagent>` with the name of the Windows node you used earlier:
    ```
    puppet task run facts --nodes <winagent>
    ```
1. Scroll through the output and observe the returned facts from your Windows node, including IP address, OS, kernel, and uptime. Note that the uptime was reset by the reboot.

    ✔️ **Result:** Congratulations! You ran two tasks from the command line: one to reboot the Windows node and one to return facts about the Windows node. Continue below to learn how to run a task from the PE console.

Run tasks from the PE console
========

🔀 Switch to the **PE Console** tab.

In this section, you'll run a task to stop and restart the time service on a Windows node in the development environment. In this lab, there's only one Windows node provisioned for development.

1. Login with username `admin` and password `puppetlabs`.<br><br>
2. Navigate to the **Tasks** page (**Orchestration** > **Tasks**).<br><br>
3. Notice that the two previous tasks that you ran on the command line are shown. These tasks have been recorded by the console.<br><br>
4. In the upper-right corner, click **Run a task**. ![run a task button](https://storage.googleapis.com/instruqt-images/run-a-task.png)
5. From the **Code environment** list, select `development`.<br><br>
6. In the **Task** field, scroll and select `service`.<br><br>
7. In the **Task parameters** section, enter the following:
    - For **action**, choose **stop**.
    - For **name**, enter `w32time`.<br><br>
8. In the **Select targets** section, from the **Select a target type** list, select **Node group**.<br><br>
1. In the **Choose a node group** field, select **Development environment (development)** and then click **Select**. Do not run the task yet.

    ✔️ **Result:** The name of your Windows node populates in the space below. This shows you the Windows node that's in the development environment node group.

    🔀 Switch to the Windows Agent 1 tab.<br><br>

1. Open a PowerShell window and run the following command to show the status of the w32time service:
    ```
    Get-Service -Name "w32time"
    ```
    💡 In the terminal output, under the **Status** header, notice that the service is **Running**.

    🔀 Switch to the **PE Console** tab.<br><br>

11. Click **Run task**. When the task run is complete, the page refreshes to show the task **Status** as **Stopped**. ![PE console task status stopped](https://storage.googleapis.com/instruqt-images/status-stopped.png)

    🔀 Switch to the **Windows Agent 1** tab.<br><br>

12. Run the PowerShell command again to show the status of the time service. Notice that the Status output in the terminal indicates **Stopped**.

    🔀 Switch to the **PE Console** tab.<br><br>

13. In the upper-right corner, click **Run again** > **All nodes** to restart the w32time service.<br><br>
14. In the **action parameter** list, select **start** and then click **Run task**.<br><br>
15. After the task completes, the page refreshes to show the task status as **Started**. ![PE console task status started](https://storage.googleapis.com/instruqt-images/status-started.png)

    🔀 Switch to the **Windows Agent 1** tab.<br><br>

1. Run the PowerShell command again. The service is now started.

    🔀 Switch to the **PE Console** tab.

By running this next task, you will get system information about the underlying database in the PuppetDB service, PostgreSQL. This task provides valuable operational information about the PostgreSQL installation.<br><br>
1. Go back to the **Tasks** page (**Orchestration** > **Tasks**) and click **Run a task**.<br><br>
1. Leave **Code environment** set to `production`.<br><br>
1. In the **Tasks** field, choose `pe_install::get_postgresql_info`.<br><br>
1. From the **Select a target type** list, select **Node group**.<br><br>
1. In the **Choose a node group** field, select `PE Master (production)` and then click **Select**.<br><br>
1. The primary Puppet server populates in the space below. Click **Run task**.<br><br>
1. After the task finishes, notice that the output provides details about the node run at a sysadmin level.<br><br>
---
🎈 **Congratulations!** In this lab, you ran pre-built PE tasks against the Windows node from both the command line and the PE console. You rebooted the Windows node under enforcement, retrieved Windows node facts, stopped and started the **w32time** service, and gathered system information about the PuppetDB PostgreSQL installation.

**Find any bugs or have feedback? Click the **Bug Zapper** tab near the top of the page and let us know!**

When you're ready to finish the lab, click **Next**.