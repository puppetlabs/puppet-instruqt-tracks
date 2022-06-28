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
- title: Winagent1
  type: service
  hostname: guac2
  path: /#/client/c/winagent1?username=instruqt&password=Passw0rd!
  port: 8080
- title: Nixagent1
  type: terminal
  hostname: nixagent1
- title: Nixagent2
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
difficulty: basic
timelimit: 3600
---
Create a plan in your module project
========

1. On the **Windows Workstation** tab, from the **Start** menu, open **Visual Studio Code**.
2. Enable VS Code autosave by clicking **File** > **Auto Save**.
3. Open the `C:\CODE` directory. Click **File** > **Open Folder**, navigate to the `C:\CODE` directory and click **Select Folder**.
4. In VS Code, open a terminal. Click **Terminal** > **New Terminal**.
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

Replace the existing code that Bolt created
========

8. In the VS Code explorer, open `backup_all_logs.pp` (**nginx** > **plans** > **backup_all_logs.pp**) to see the placeholder code that Bolt created.

9. Replace the placeholder code in **backup_all_logs.pp** with the code block below, which contains the structure for a simple plan:
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

12. Open `backup_windows_logs.json` (**nginx** > **tasks** > **backup_windows_logs.json**) and replace the existing metadata in the file with the content below, which includes information for the task name, description, input method and privacy settings:
    ```
    {
      "name": "Windows backup",
      "description": "A task to perform web site log backups on Windows targets",
      "input_method": "powershell",
      "private": true
    }
    ```
13. Open `backup_linux_logs.json` (**nginx** > **tasks** > **backup_linux_logs.json**) and replace the existing metadata in the file with the content below, which includes information for the task name, description, input method and privacy settings:
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
15. In the VS Code terminal, run the the new backup plan:
    ```
    bolt plan run nginx::backup_all_logs --targets nixagent1,winagent1
    ```

    Once the plan completes, you will see similar output to the following on the command line:
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
🔀 Switch to the **Winagent1** tab.

1. To see your `nginx` backup folder, run `Get-ChildItem -Path C:\backups\`
1. Change directories into the timestamped backup folder to verify that the `access` and `error` logs have been backed up successfully.
2. To verify that the NGINX service stopped and started, run `eventvwr`. This command opens the **Event Viewer**.
3. In the left-hand pane of the **Event Viewer**, click **Windows Logs** > **Application**. In the **Source** column, look for entries that have `nssm` value (NGINX service). Verify that the service has been stopped and started.

Verify the NGINX service stopped and restarted on Linux
========
🔀  Switch to the **Nixagent1** tab.

1. Run `ls /var/backup` and notice the timestamped folder.
1. To verify the logs were backed up successfully, change directories into the timestamped folder and then run `cat` into either the `error` or the `access` log.
5. To verify that the NGINX service was stopped and started, run `systemctl show nginx`.
1. In the output, look for the value `ExecStartPre=`. This indicates that the service successfully stopped and restarted.

🎈 **Congratulations!** You built a Puppet plan! If you want to, you can spend some time exploring this environment.
To learn more about writing Puppet plans, visit the Puppet [documentation](http://pup.pt/bolt-puppet-plans).
---
**Find any bugs or have feedback? Click the **Bug Zapper** tab near the top of the page and let us know!**

When you're ready to close the lab, click **Next**.