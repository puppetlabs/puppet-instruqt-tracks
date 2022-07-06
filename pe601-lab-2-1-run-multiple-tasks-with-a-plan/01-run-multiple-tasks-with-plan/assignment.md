---
slug: run-multiple-tasks-with-plan
id: yxmghjbr7fps
type: challenge
title: Run Multiple Tasks with a Plan
teaser: Add tasks to the Puppet plan to stop and start the Puppet agent
notes:
- type: text
  contents: |-
    ## Scenario
    Your Puppet plan is failing because the Puppet agent is running in the background and starting your service during the backup.

    In this lab, you will resolve this issue by adding tasks to the Puppet plan that will stop the Puppet agents during backups, and restart them after the backups complete.
tabs:
- title: PE Console
  type: service
  hostname: puppet
  port: 443
- title: PE terminal
  type: terminal
  hostname: puppet
- title: Windows Workstation
  type: service
  hostname: guac
  path: /#/client/c/workstation?username=instruqt&password=Passw0rd!
  port: 8080
- title: Windows Agent 1
  type: service
  hostname: guac2
  path: /#/client/c/winagent1?username=instruqt&password=Passw0rd!
  port: 8080
- title: Git Server
  type: service
  hostname: gitea
  path: /
  port: 3000
- title: Linux Agent 1
  type: terminal
  hostname: nixagent1
- title: Linux Agent 2
  type: terminal
  hostname: nixagent2
- title: Lab Help
  type: website
  url: https://puppet-kmo.gitbook.io/instruqt-platform-help/
- title: Bug Zapper
  type: website
  url: https://docs.google.com/forms/d/e/1FAIpQLSd_z5iIJUvLrAwYCwDchDoF3ncy5TsCCDSiA_7SWFOPrFbKog/viewform?embedded=true
difficulty: basic
timelimit: 3600
---
Clone the NGINX module
========

1. On the **Windows Workstation** tab, from the **Start** menu, open **Visual Studio Code**.<br><br>
1. Enable VS Code autosave by clicking **File** > **Auto Save**.<br><br>
1. Open the `C:\CODE` directory. Click **File** > **Open Folder**, navigate to the `C:\CODE` directory and click **Select Folder**.<br><br>
1. In VS Code, open a terminal. Click **Terminal** > **New Terminal**.<br><br>
1. In the terminal window, run the following command to clone the NGINX module:
    ```
    git clone git@gitea:puppet/nginx.git
    ```
1. Change directories into the NGINX module directory:
    ```
    cd .\nginx
    ```

Update the plan to disable and re-enable the Puppet agent
========

1. In the VS Code explorer, open `backup_all_logs.pp` (**nginx** > **plans** > **backup_all_logs.pp**) to open the current version of the plan.<br><br>The plan must be updated to disable the Puppet agent before running the log backup and then re-enable it after the backup finishes. Doing this prevents the Puppet agent from restarting the NGINX server while the backup is running and ensures a consistent set of backup files.<br><br>
1. Replace the code in **backup_all_logs.pp** with the plan code below. The two additional `run_task` function calls ensure that the Puppet agent is disabled before the log backup starts and is re-enabled after it finishes.
    ```
    # This is the structure of a simple plan. To learn more about writing
    # Puppet plans, see the documentation: http://pup.pt/bolt-puppet-plans
    # The summary sets the description of the plan that will appear
    # in 'bolt plan show' output. Bolt uses puppet-strings to parse the
    # summary and parameters from the plan.
    # @summary A plan created with bolt plan new.
    # @param targets The targets to run on.
    plan nginx::backup_all_logs (
      TargetSpec $targets
    ) {
      run_plan(facts, targets=>$targets)
      get_targets($targets).each |Target $targ| {
        case $targ.facts['os']['name'] {
          'windows': {
              $source_dir ='C:\tools\nginx-1.23.0\logs'
              $target_dir = 'C:\backups'
            }
          default: {
            $source_dir = '/var/log/nginx'
            $target_dir = '/var/backup'
          }
        }
        run_task(service, $targ, { name => 'puppet', action => 'stop' })
        run_task(nginx::backup_logs, $targ, {source_dir => $source_dir,target_dir => $target_dir})
        run_task(service, $targ, { name => 'puppet', action => 'start' })
      }
    }
    ```

Run the new backup plan against Windows and Linux nodes
========
1. In the VS Code terminal, run the the new backup plan against both the Linux and Windows nodes:
    ```
    bolt plan run nginx::backup_all_logs --targets nixagent1,winagent1
    ```

    ✔️ **Result:** Once the plan completes, you will see similar output to the following on the command line:
    ```
    Starting: plan nginx::backup_all_logs
    Starting: plan facts
    Starting: task facts on nixagent1, winagent1
    Finished: task facts with 0 failures in 15.88 sec
    Finished: plan facts in 15.96 sec
    Starting: task service on nixagent1
    Finished: task service with 0 failures in 1.11 sec
    Starting: task nginx::backup_logs on nixagent1
    Finished: task nginx::backup_logs with 0 failures in 0.8 sec
    Starting: task service on nixagent1
    Finished: task service with 0 failures in 0.93 sec
    Starting: task service on winagent1
    Finished: task service with 0 failures in 2.99 sec
    Starting: task nginx::backup_logs on winagent1
    Finished: task nginx::backup_logs with 0 failures in 4.28 sec
    Starting: task service on winagent1
    Finished: task service with 0 failures in 8.04 sec
    Finished: plan nginx::backup_all_logs in 34.16 sec
    Plan completed successfully with no result
    ```

Verify the Puppet service stopped and restarted on Windows
========
🔀 Switch to the **Windows Agent 1** tab.

✏️ **Note:** If you've been disconnected, click **Reconnect** to connect to the Windows agent.

1. From the **Start** menu, open **Windows Powershell**.<br><br>
1. In the Powershell terminal window, run the following command to show recent service activity on the node:
    ```
    Get-WinEvent -FilterHashtable @{logname='System';id=7036} -MaxEvents 4
    ```
1. Notice that reading from bottom to top that the Puppet agent service stops, then the NGINX service stops, and then they are restarted in the correct order. This ensures that the log files are backed up in a consistent state.

Verify the Puppet service stopped and restarted on Linux
========
🔀  Switch to the **Linux Agent 1** tab.

1. Verify that the Puppet service was stopped and started:
    ```
    systemctl status puppet
    ```
1. In the output, note the timestamp of the line that contains the text `Started Puppet agent`, and it should show the time when the plan restarted the service after the log file backup process completed.

---
🎈 **Congratulations!** You enhanced your Puppet plan to create a consistent set of backup files! If you want to, you can spend some time exploring this environment.
To learn more about writing Puppet plans, visit [Puppet documentation](http://pup.pt/bolt-puppet-plans).
---
**Find any bugs or have feedback? Click the **Bug Zapper** tab near the top of the page and let us know!**

When you're ready to close the lab, click **Next**.