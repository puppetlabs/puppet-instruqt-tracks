---
slug: develop-cross-platform-task
id: yebihva7cdsn
type: challenge
title: Develop a Cross-Platform Task
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
timelimit: 3600
---
Clone the NGINX module to your workstation
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
Extend the nginx task
========

1. In VSCode, navigate to **nginx/tasks/backup_logs.json** and open file.
2. Edit the code so it looks like the block below:
```
{
  "description": "Backs up nginx logs",
  "supports_noop": false,
  "parameters": {
    "source_dir": {
      "description": "Source directory to backup.",
      "type": "String",
      "default": "/var/log/nginx"
    },
    "target_dir": {
      "description": "Target directory to save backup to.",
      "type": "String",
      "default": "/var/backup"
    }
  },
"implementations": [
  {"name": "backup_linux_logs.sh", "requirements": ["shell"]},
  {"name": "backup_windows_logs.ps1", "requirements": ["powershell"]}
]
}
```
3. From the VSCode terminal, run syntax checks with `pdk validate`.
4. As an acceptance test, run the following command in the terminal:
```
bolt task run nginx::backup_logs --target winagent1
```
Observe the execution failure:  we have not yet created the task script backup_windows_logs.ps1 and accompanying metadata file. Also the Bash script for linux needs to be renamed.

5. Create a new file called **backup_windows_logs.ps1** in the tasks directory with the following content:

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

# Create date stamp for backup sub directory
$date_stamp = Get-Date -UFormat "+%Y%m%d-%H%M%S"

# Create subdir with timestamp in target backup dir
$full_target_backup_path = Join-Path -Path $target_dir -ChildPath "site_backup_$date_stamp"

# Copy contents of source dir to full backup path target
Write-Output "Copying items from $source_dir to full backup path $full_target_backup_path"
Copy-Item -Recurse -Path $source_dir -Destination $full_target_backup_path
```
6. Create a new **backup_windows_logs.json** metadata file for the task with the following content:
```
{
  "name": "Windows backup",
  "description": "A task to perform web site log backups on Windows targets",
  "private": true
}
```
7.