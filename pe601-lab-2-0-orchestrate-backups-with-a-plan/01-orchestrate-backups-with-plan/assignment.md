---
slug: orchestrate-backups-with-plan
id: 3fyn29shttcx
type: challenge
title: Orchestrate Backups with a Plan
notes:
- type: text
  contents: PLACEHOLDER
tabs:
- title: PE Console
  type: service
  hostname: puppet
  port: 443
- title: PE terminal
  type: terminal
  hostname: puppet
- title: Workstation
  type: service
  hostname: guac
  path: /#/client/c/workstation?username=instruqt&password=Passw0rd!
  port: 8080
- title: winagent1
  type: service
  hostname: guac2
  path: /#/client/c/winagent1?username=instruqt&password=Passw0rd!
  port: 8080
- title: gitea
  type: service
  hostname: gitea
  path: /
  port: 3000
- title: nixagent1
  type: terminal
  hostname: nixagent1
- title: nixagent2
  type: terminal
  hostname: nixagent2
difficulty: basic
timelimit: 7200
---
Create a plan in your module project
========

1. On the **Windows Workstation** tab, from the **Start** menu, open **Visual Studio Code**.
2. Enable VS Code autosave by clicking **File** > **Auto Save**.

    ✏️ **Note:** This step isn’t required, but by enabling Auto Save, you don't need to remember to save your changes as you work. This ensures your edits won't be lost.<br><br>

3. Open the `C:\CODE` directory. Click **File** > **Open Folder**, navigate to the `C:\CODE` directory and click **Select Folder**.
4. In VS Code, open a terminal. Click **Terminal** > **New Terminal**.
5. In the terminal window, run the following command to clone the NGINX module:
    ```
    git clone git@gitea:puppet/nginx.git
    ```
6. Go to the NGINX module directory:
    ```
    cd .\nginx
    ```
7. Create a plan to orchestrate our tasks:
   ```
   bolt plan new nginx::backup_all_logs --pp
   ```
8. Open the ../nginx/plans/backup_all_logs.pp plan file in the editor to see the placeholder code that Bolt created.

9. Replace the placeholder code in **backup_all_logs.pp** with the code block below:

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
    run_task(nginx::backup_logs, $targ, {source_dir => $source_dir,target_dir => $target_dir})
  }
}
```
10. Open **/nginx/tasks/backup_logs.json** and replace the code in the file with the following block:

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

11. Open **/nginx/tasks/backup_windows_logs.ps1** and replace the code in the file with the block below:

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

12. Open **/nginx/tasks/backup_windows_logs.json** and replace the code in the file with the code block below:
```
{
  "name": "Windows backup",
  "description": "A task to perform web site log backups on Windows targets",
  "input_method": "powershell",
  "private": true
}
```
13. Open **/nginx/tasks/backup_linux_logs.json** and replace the code in the file with the code block below:
```
{
  "name": "Linux backup",
  "description": "This task performs website log backups on Linux targets",
  "input_method": "both",
  "private": true
}
```
14. Lastly, open **/nginx/tasks/backup_linux_logs.sh** and replace the code with the following block:
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
# Diff to verify (diff returns a non-zero exit code if it finds a4ny differences
diff --recursive $source_dir $target_dir_bkp
# Start nginx service
systemctl start nginx
```
15. Run the the new backup plan:
```
bolt plan run nginx::backup_all_logs --targets nixagent1,winagent1
```

On the command line, you will see output similar to the block below as the plan completes:
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
Verification
========
1. **Windows:** Switch to the **winagent1** tab. Run `Get-ChildItem -Path C:\backups\` to see your `nginx` backup folder. Go to the timestamped backup folder the `access` and `error` logs have been backed up successfully.
2. To verify that the nginx service stopped and started, type `eventvwr` at the command line and enter. This command opens the Event Viewer.
3. In the left-hand pane of the Event Viewer, click **Windows Logs** > **Application**. In the **Source** column, look for entries that have `nssm` value (nginx service). Verify that the service has been stopped and started.
4. **Linux:** Switch to the **nixagent1** tab. Run `ls /var/backup` and notice the timestamped folder. To verify the logs were backed up successfully, go into the timestamped folder and `cat` either the `error` or the `access` log.
5. To verify that the nginx service was stopped and started, run `systemctl show nginx`. In the output, look for the value `ExecStartPre=`. This indicates that the service successfully stopped and restarted.

🎈 **Congratulations!** You built a Puppet plan! If you want to, you can spend some time exploring this environment.

---
**Find any bugs or have feedback? Click the **Bug Zapper** tab near the top of the page and let us know!**

When you're ready to close the lab, click **Next**.