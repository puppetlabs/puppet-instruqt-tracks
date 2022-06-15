---
slug: develop-cross-platform-task
id: yebihva7cdsn
type: challenge
title: Develop a Cross-Platform Task
teaser: Develop your task to run on Windows machines.
notes:
- type: text
  contents: |-
    Puppet makes it easy to design tasks to work in a cross-platform environment. In this lab, you will expand the NGINX backup task code to enable the task code to run on Windows machines.

    Click **Start** when you're ready to begin.
tabs:
- title: Windows Workstation
  type: service
  hostname: guac
  path: /#/client/c/workstation?username=instruqt&password=Passw0rd!
  port: 8080
- title: PE Console
  type: service
  hostname: puppet
  port: 443
- title: PE Terminal
  type: terminal
  hostname: puppet
- title: Winagent1
  type: service
  hostname: guac2
  path: /#/client/c/winagent1?username=instruqt&password=Passw0rd!
  port: 8080
- title: Gitea
  type: service
  hostname: gitea
  path: /
  port: 3000
- title: Nixagent1
  type: terminal
  hostname: nixagent1
- title: Nixagent2
  type: terminal
  hostname: nixagent2
- title: Lab Help
  type: website
  hostname: guac
  url: https://puppet-kmo.gitbook.io/practice-lab-help/
- title: Bug Zapper
  type: website
  hostname: guac
  url: https://docs.google.com/forms/d/e/1FAIpQLSdpF19OgzY7HXS2nlGeI6y7kcVjVBzH9V_UaOP64478lOXZsQ/viewform?embedded=true
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

Extend the NGINX task
========

1. In VS Code, open **backup_logs.json** (**nginx** > **tasks** > **backup_logs.json**).
2. Replace the existing code with the following, which adds implementation requirements for the task:
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
3. In the VS Code terminal, run a syntax check using PDK:
    ```
    pdk validate
    ```
    ✏️ **Note:** When prompted whether you consent to PDK collecting anonymous usage information, choose whichever option you prefer. This information is not stored after the lab expires.<br><br>
4. In the same terminal window, run an acceptance test using Bolt:
    ```
    bolt task run nginx::backup_logs --target winagent1
    ```
    ✏️ **Note:** In the command line output, notice the execution failure:

    `Task metadata for task nginx::backup_logs specifies missing implementation backup_linux_logs.sh`

    This task failed because the task script `backup_windows_logs.ps1` and accompanying metadata file don't yet exist. The Bash script for Linux also needs to be renamed. In the next steps you will resolve this issue.<br><br>

5. In VS Code, navigate to the `tasks` directory and create a new file called **backup_windows_logs.ps1**. Populate it with the following PowerShell script which...:

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
6. In the same `/tasks` directory, create a metadata JSON file for the Windows task called **backup_windows_logs.json**. Add the following content to the file, which provides a name, description, and privacy settings for the task:
    ```
    {
      "name": "Windows backup",
      "description": "A task to perform web site log backups on Windows targets",
      "private": true
    }
    ```
7. In the same `/tasks` directory, create a metadata JSON file for the Linux task called **backup_linux_logs.json**. Add the following content to the file, which provides a name, description, and privacy settings for the task:
    ```
    {
      "name": "Linux backup",
      "description": "A task to perform web site log backups on Linux targets",
      "private": true
    }
    ```
8. Open **backup_logs.sh** and rename it to **backup_linux_logs.sh** so that it will match the implementation records in the **backup_logs.json** metadata file.

9. In the VS Code terminal, run `pdk validate` to...

Execute tasks against the Windows and Linux nodes
========
The task currently has defaults for the Linux node written into the main metadata file, **backup_logs.json**. When running the task against Windows nodes you must provide source and directory values at the command line.

1. From the VS Code terminal, run the following command to...:
    ```
    bolt task run nginx::backup_logs --target winagent1 "source_dir=c:\\tools\\nginx-1.21.6\\logs" "target_dir=c:\\temp\\"
    ```
🔀 Switch to the **Winagent1** tab.

1. Use **File Explorer** to navigate to `site_backup_<TIMESTAMP>` (**C:\temp\** > **site_backup_<TIMESTAMP>**)`. Inside this folder, notice a successful backup of the `access` and `error` logs.

✔️ **Result:** Great work! Your Windows task has been executed successfully. Now it's time to execute the Linux task. Remember that for the Linux nodes, the source and target directories have been set as defaults inside the **backup_logs.json** metadata file, so you don't need to supply values for the source and target directories from the command line.

🔀 Switch to the **Windows Workstation** tab.

1.  In the VS Code terminal window, run the following command which will...:
    ```
    bolt task run nginx::backup_logs --target nixagent1
    ```
🔀 Switch to the **Nixagent1** tab.

1. Change to the target directory, by running `cd /var/backup`, and then reveal the directory contents by running `ls`.
2. Locate and open a time-stamped directory, and then run `cat access.log` or `cat error.log`.

✔️ **Result:** Your Linux task has been successfully executed.

🎈 **Congratulations!** You extended the `nginx::backup_logs` task's functionality to include NGINX installations on the Windows platform. If you want to, you can spend some time exploring this environment.

---
**Find any bugs or have feedback? Click the **Bug Zapper** tab near the top of the page and let us know!**

When you're ready to close the lab, click **Next**.
