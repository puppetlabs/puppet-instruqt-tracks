---
slug: orchestrate-backups-with-plan
id: 3fyn29shttcx
type: challenge
title: Orchestrate backups with a plan
teaser: Expand the NGINX backup task code so that it includes a Puppet plan.
notes:
- type: text
  contents: |-
    In this lab, you will further expand the NGINX backup task code so that it includes a Puppet plan.

    Click **Start** when you're ready to begin.
tabs:
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
- title: Linux Agent 1
  type: terminal
  hostname: nixagent1
- title: Linux Agent 2
  type: terminal
  hostname: nixagent2
- title: PE Console
  type: service
  hostname: puppet
  port: 443
- title: PE Terminal
  type: terminal
  hostname: puppet
- title: Gitea
  type: service
  hostname: gitea
  path: /
  port: 3000
- title: Lab Help
  type: website
  url: https://puppet-kmo.gitbook.io/instruqt-platform-help/
- title: Bug Zapper
  type: website
  url: https://docs.google.com/forms/d/e/1FAIpQLScOPFhV7wpUQAOsjxd5tA7kEEfPVyFQ_AcKGV7AKwt5_UmF0g/viewform?embedded=true
difficulty: basic
timelimit: 3600
---
Create a plan in your module project
========

1. On the **Windows Workstation** tab, from the **Start** menu, open **Visual Studio Code**.<br><br>
2. Enable VS Code autosave by clicking **File** > **Auto Save**.<br><br>
3. Open the `C:\CODE` directory. Click **File** > **Open Folder**, navigate to the `C:\CODE` directory and click **Select Folder**.<br><br>
4. In VS Code, open a terminal. Click **Terminal** > **New Terminal**.<br><br>
5. In the terminal window, run the following command to clone the NGINX module:
    ```
    git clone git@gitea:puppet/nginx.git
    ```
6. Change directories into the NGINX module directory:
    ```
    cd .\nginx
    ```
7. Use Bolt to create a plan to orchestrate the tasks:
   ```
   bolt plan new nginx::backup_all_logs --pp
   ```
   ✔️ **Result:** Notice that a new **plans** folder appears in the VS Code explorer at the left.

Update the placeholder code
========

8. In the VS Code explorer, open `backup_all_logs.pp` (**nginx** > **plans** > **backup_all_logs.pp**) to see the placeholder code that Bolt created.<br><br>
9. Replace the placeholder code in **backup_all_logs.pp** with the plan code below. This plan looks for facts on the targets, and uses the fact's OS name to determine whether the OS is Windows or Linux. If the target is Windows, it applies the Windows values specified. Otherwise, if the target is Linux, it receives the default values. This is an example of how plans combine logic and tasks:
    ```
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
        run_task(nginx::backup_logs, $targ, {source_dir => $source_dir,target_dir => $target_dir})
      }
    }
    ```

10. Open `backup_logs.json` (**nginx** > **tasks** > **backup_logs.json**) and replace the existing code with the following metadata, which includes information about the task description, no-op settings, parameters, and implementations:

    ```
    {
        "description": "Backs up nginx logs",
        "supports_noop": false,
        "parameters": {
            "source_dir": {
                "description": "Source directory to back up.",
                "type": "String"
            },
            "target_dir": {
                "description": "Target directory to save the backup to.",
                "type": "String"
            }
        },
        "implementations": [
            {
                "name": "backup_linux_logs.sh",
                "requirements": [
                    "shell"
                ]
            },
            {
                "name": "backup_windows_logs.ps1",
                "requirements": [
                    "powershell"
                ]
            }
        ]
    }
    ```

11. Open `backup_windows_logs.ps1` (**nginx** > **tasks** > **backup_windows_logs.ps1**) and replace the code in the file with the script code below, which pauses the NGINX service and then restarts it after after the `backup_logs` task completes:

    ```
    [CmdletBinding()]
    Param(
    [Parameter(Mandatory = $True)]
    [String]
    $source_dir,

    [Parameter(Mandatory = $True)]
    [String]
    $target_dir
    )
    #Stop nginx service
    Stop-Service nginx

    # Create date stamp for backup sub directory
    $date_stamp = Get-Date -UFormat "+%Y%m%d-%H%M%S"

    # Create subdir with timestamp in target backup dir
    $full_target_backup_path = Join-Path -Path "c:\backups\" -ChildPath "site_backup_$date_stamp"

    # Copy contents of source dir to full backup path target
    Write-Output "Copying items from $source_dir to full backup path $full_target_backup_path"
    Copy-Item -Recurse -Path "c:\tools\nginx-1.23.0\logs\" -Destination $full_target_backup_path

    #Start nginx service
    Start-Service nginx
    ```

12. Open `backup_windows_logs.json` (**nginx** > **tasks** > **backup_windows_logs.json**) and replace the existing metadata in the file with the content below, which adds a line to use Powershell as the input method:
    ```
    {
      "name": "Windows backup",
      "description": "A task to perform web site log backups on Windows targets",
      "input_method": "powershell",
      "private": true
    }
    ```
13. Open `backup_linux_logs.json` (**nginx** > **tasks** > **backup_linux_logs.json**) and replace the existing metadata in the file with the content below, which adds a line to use both input methods:
    ```
    {
      "name": "Linux backup",
      "description": "This task performs website log backups on Linux targets",
      "input_method": "both",
      "private": true
    }
    ```
14. Lastly, open `backup_linux_logs.sh` (**nginx** > **tasks** > **backup_linux_logs.sh**) and replace the existing code with the following Bash script which identifies source and target directories, pauses the NGINX service while the `backup_logs` task runs, and runs a diff to identify any changes since it last ran before restarting the NGINX service:
    ```
    #!/bin/bash
    # Sites backup script
    source_dir=$PT_source_dir
    target_dir=$PT_target_dir
    ​
    # Target directory using a timestamp
    day=$(date +%Y%m%d-%H%M%S)
    target_dir_bkp="$target_dir/$day"
    mkdir -p $target_dir_bkp

    # Stop nginx service
    systemctl stop nginx
    ​
    # Back up the files
    echo "$(date) Backing up $source_dir to $target_dir_bkp"
    cp -aR $source_dir/* $target_dir_bkp
    echo "$(date) Backup finished"
    ​
    # Diff to verify (diff returns a non-zero exit code if it finds any differences)
    diff --recursive $source_dir $target_dir_bkp

    # Start nginx service
    systemctl start nginx
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
    Finished: task facts with 0 failures in 27.26 sec
    Finished: plan facts in 27.34 sec
    Starting: task nginx::backup_logs on nixagent1
    Finished: task nginx::backup_logs with 0 failures in 0.9 sec
    Starting: task nginx::backup_logs on winagent1
    Finished: task nginx::backup_logs with 0 failures in 4.72 sec
    Finished: plan nginx::backup_all_logs in 33.03 sec
    ```
Verify the NGINX service stopped and restarted on Windows
========
🔀 Switch to the **Windows Agent 1** tab.

✏️ **Note:** If you've been disconnected, click **Reconnect** to connect to the Windows agent.

1. From the **Start** menu, open **Windows Powershell**.<br><br>
2. In the Powershell terminal window, run the following command to locate the `nginx` backup folder:
    ```
    Get-ChildItem -Path C:\backups\
    ```
    ✔️ **Result:** In the output, notice the backup folder, `site_backup_<date-time>`. This verifies that a backup was made.<br><br>
    💡 **Tip:** To verify that the `access` and `error` logs have been backed up successfully, you can navigate to the timestamped backup folder to view the logs. <br><br>
3. To verify that the NGINX service stopped and started, run `eventvwr`. This command opens the **Event Viewer** interface.<br><br>
4. Click the square in the top right of the interface header to enlarge the Event Viewer to full size.<br><br>
5. In the left-hand pane of the **Event Viewer**, navigate to **Windows Logs** > **Application**.

    ✔️ **Result:** In the **Source** column, locate the entries with the value `nssm`. These lines show the start and stop times for the NGINX service. This verifies that the service was successfully stopped and restarted.

Verify the NGINX service stopped and restarted on Linux
========
🔀 Switch to the **Linux Agent 1** tab.

1. Run `ls /var/backup` and notice the timestamped folder in the output.
    ```
    ls /var/backup
    ```
    💡 **Tip:** To verify that the logs were backed up successfully, you can navigate to the timestamped folder and then run `cat` into either the `error` or the `access` log.<br><br>
5. Verify that the NGINX service was stopped and started:
    ```
    systemctl show nginx
    ```
1. In the output, locate the lines with the value `ExecStartPre=`. These lines show `stop_time=` which indicates that the service successfully stopped and restarted.

---
🎈 **Congratulations!** You built a Puppet plan! If you want to, you can spend some time exploring this environment.
To learn more about writing Puppet plans, visit [Puppet documentation](http://pup.pt/bolt-puppet-plans).
---
**Find any bugs or have feedback? Click the **Bug Zapper** tab near the top of the page and let us know!**

When you're ready to close the lab, click **Next**.