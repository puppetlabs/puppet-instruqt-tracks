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
Create a Plan in your Module project
========

1. On the **Windows Workstation** tab, from the **Start** menu, open **Visual Studio Code**.
2. Enable VS Code autosave by clicking **File** > **Auto Save**.

    ✏️ **Note:** This step isn’t required, but by enabling Auto Save, you don't need to remember to save your changes as you work, ensuring your edits won't be lost.<br><br>

3. Open the `C:\CODE` directory. Click **File** > **Open Folder**, navigate to the `C:\CODE` directory and click **Select Folder**.
4. In VS Code, open a terminal. Click **Terminal** > **New Terminal**.
5. In the terminal window, run the following command to clone the NGINX module:
    ```
    git clone git@gitea:puppet/nginx.git
    ```
6. Change directories into the NGINX module:
    ```
    cd .\nginx
    ```
7. Create a Plan to orchestrate our tasks:
   ```
   bolt plan new nginx::backup_all_logs --pp
   ```
8. Open the ../nginx/plans/backup_all_logs.pp plan file in the editor to see the placeholder code created by Bolt.

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
          $source_dir ='C:\tools\nginx-1.21.6\logs'
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
10. Navigate to **/nginx/tasks/backup_logs.json** and open the file. Replace the code in the file with the following block:

```
{
    "description": "Backs up nginx logs",
    "supports_noop": false,
    "parameters": {
        "source_dir": {
            "description": "Source directory to backup.",
            "type": "String"
        },
        "target_dir": {
            "description": "Target directory to save backup to.",
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

11. Navigate to **/nginx/tasks/backup_windows_logs.ps1**. Replace the code in the file with the block below:

```
[CmdletBinding()]
Param(
[Parameter(Mandatory = $True)]
[String]
$source_dir,
​
[Parameter(Mandatory = $True)]
[String]
$target_dir
)
​
# Create date stamp for backup sub directory
$date_stamp = Get-Date -UFormat "+%Y%m%d-%H%M%S"
​
# Create subdir with timestamp in target backup dir
$full_target_backup_path = Join-Path -Path "c:\backups\" -ChildPath "site_backup_$date_stamp"
New-Item -ItemType Directory -Force -Path $full_target_backup_path
​
# Copy contents of source dir to full backup path target
Write-Output "Copying items from $source_dir to full backup path $full_target_backup_path"
Copy-Item -Recurse -Path "c:\tools\nginx-1.21.6\logs\*" -Destination $full_target_backup_path -Force
```

12. Navigate to **/nginx/tasks/backup_windows_logs.json**. Replace the code in the file with the code block below:
```
{
  "name": "Windows backup",
  "description": "A task to perform web site log backups on Windows targets",
  "input_method": "powershell",
  "private": true
}
```
13. Navigate to **/nginx/tasks/backup_linux_logs.json**. Replace the code in the file with the code block below:
```
{
  "name": "Linux backup",
  "description": "A task to perform web site log backups on Linux targets",
  "input_method": "both",
  "private": true
}
```
14. Lastly, navigate to **/nginx/tasks/backup_linux_logs.sh** and replace the code there with the following block:
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
​
# Backup the files
echo "$(date) Backing up $source_dir to $target_dir_bkp"
cp -aR $source_dir/* $target_dir_bkp
echo "$(date) Backup finished"
​
# Diff to verify (diff returns a non-zero exit code if it finds a4ny differences
diff --recursive $source_dir $target_dir_bkp
```
15.