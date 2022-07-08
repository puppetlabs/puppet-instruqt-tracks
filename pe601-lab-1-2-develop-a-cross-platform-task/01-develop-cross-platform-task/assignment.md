---
slug: develop-cross-platform-task
id: yebihva7cdsn
type: challenge
title: Develop a cross-platform task
teaser: Extend a task that runs on Linux nodes to also run on Windows nodes.
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
- title: Windows Agent 1
  type: service
  hostname: guac2
  path: /#/client/c/winagent1?username=instruqt&password=Passw0rd!
  port: 8080
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
- title: Linux Agent 1
  type: terminal
  hostname: nixagent1
- title: Linux Agent 2
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
timelimit: 2700
---
Clone the NGINX module to your workstation
========
1. On the **Windows Workstation** tab, from the **Start** menu, open **Visual Studio Code**.<br><br>
2. Enable VS Code autosave by clicking **File** > **Auto Save**.<br><br>
3. Open the `C:\CODE` directory. Click **File** > **Open Folder**, navigate to the `C:\CODE` directory, and click **Select Folder**.<br><br>
4. In VS Code, open a terminal. Click **Terminal** > **New Terminal**.<br><br>
5. In the terminal window, run the following command to clone the NGINX module:
    ```
    git clone git@gitea:puppet/nginx.git
    ```
6. Change directories into the NGINX module directory:
    ```
    cd .\nginx
    ```

Extend the NGINX task
========

1. In VS Code, open the task metadata file, **backup_logs.json** (**nginx** > **tasks** > **backup_logs.json**).<br><br>
2. Replace the code with the following code, which adds implementation requirements for the task (starting on line 16):
    ```
    {
        "description": "Backs up nginx logs",
        "supports_noop": false,
        "parameters": {
            "source_dir": {
                "description": "Source directory to back up.",
                "type": "String",
                "default": "/var/log/nginx"
            },
            "target_dir": {
                "description": "Target directory to save the backup to.",
                "type": "String",
                "default": "/var/backup"
            }
        },
        "implementations": [{
                "name": "backup_linux_logs.sh",
                "requirements": ["shell"]
            },
            {
                "name": "backup_windows_logs.ps1",
                "requirements": ["powershell"]
            }
        ]
    }
    ```
3. In the VS Code terminal, run a syntax check using Puppet Development Kit (PDK):
    ```
    pdk validate
    ```
    ✏️ **Note:** When prompted whether you consent to PDK collecting anonymous usage information, choose whichever option you prefer. This information is not stored after the lab expires.<br><br>
4. In the same terminal window, run an acceptance test using Bolt:
    ```
    bolt task run nginx::backup_logs --target winagent1
    ```
    ✏️ **Note:** In the command-line output, notice the run failure:

    ```
    Task metadata for task nginx::backup_logs specifies missing implementation backup_linux_logs.sh
    ```

    This task failed because the task script `backup_windows_logs.ps1` and accompanying metadata file don't exist yet. The Bash script for Linux also needs to be renamed. You'll resolve these issues in the next steps.<br><br>

5. In the VS Code explorer, you should already be in the **tasks** directory. If not, navigate there first, then create a file (**File** > **New File**).<br><br>

1. Create a new file called **backup_windows_logs.ps1** and then add the following content, which creates date stamps and timestamps:

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

    # Create a date stamp for backup subdirectory
    $date_stamp = Get-Date -UFormat "+%Y%m%d-%H%M%S"

    # Create a subdirectory with a timestamp in the target backup directory
    $full_target_backup_path = Join-Path -Path $target_dir -ChildPath "site_backup_$date_stamp"

    # Copy the contents of source directory to full backup path target
    Write-Output "Copying items from $source_dir to full backup path $full_target_backup_path"
    Copy-Item -Recurse -Path $source_dir -Destination $full_target_backup_path
    ```
6. In the same **tasks** directory, create a file for the Windows task metadata called **backup_windows_logs.json**. Add the following content to the file, which provides a name, description, and privacy settings for the Windows task:
    ```
    {
      "name": "Windows backup",
      "description": "A task to perform web site log backups on Windows targets",
      "private": true
    }
    ```
7. In the same **tasks** directory, create a file for the Linux task metadata called **backup_linux_logs.json**. Add the following content to the file, which provides a name, description, and privacy settings for the Linux task:
    ```
    {
      "name": "Linux backup",
      "description": "A task to perform website log backups on Linux targets",
      "private": true
    }
    ```
8. Change the **backup_logs.sh** filename to match the implementation records in the **backup_logs.json** metadata file. In the VS Code explorer, find **backup_logs.sh** and rename it to **backup_linux_logs.sh** (right-click > **Rename**).<br><br>

9. In the VS Code terminal, run another syntax check using PDK:
    ```
    pdk validate
    ```
    ✔️ **Result:** Nice job! The required task script and metadata files were created, the **backup_linux_logs.sh** file was renamed to match the implementation records in the **backup_logs.json** metadata file, and a syntax check ran successfully using PDK. Now it's time to run the tasks against the Windows and Linux nodes.

Run tasks against the Windows and Linux nodes
========
The task currently has defaults for only the Linux node written into the main metadata file, **backup_logs.json**. To run the task against Windows nodes, you must provide source and directory values at the command line, which you'll do next.

1. In the VS Code terminal, run the task against the Windows node using Bolt:
    ```
    bolt task run nginx::backup_logs --target winagent1 "source_dir=c:\\tools\\nginx-1.23.0\\logs" "target_dir=c:\\temp\\"
    ```
    ✏️ **Note:** Wait until the task run completes before you continue.

    🔀 Switch to the **Windows Agent 1** tab.<br><br>

1. Use **File Explorer** to navigate to the **site_backup_< TIMESTAMP >** directory (**Local Disc (C:)** > **temp** > **site_backup_< TIMESTAMP >**). In this directory, you'll see a successful backup of the `access` and `error` logs.

    ✔️ **Result:** Great work! Your Windows task ran successfully. Now it's time to run the Linux task. Remember that for the Linux nodes, the source and target directories have been set as defaults in the **backup_logs.json** metadata file, so you don't need to supply values for the source and target directories on the command line.

    🔀 Switch to the **Windows Workstation** tab.<br><br>

1.  In the VS Code terminal window, run the task against the Linux node using Bolt:
    ```
    bolt task run nginx::backup_logs --target nixagent1
    ```
    🔀 Switch to the **Linux Agent 1** tab.<br><br>

1. Change to the target directory by running `cd /var/backup` and list the directory contents by running `ls`.<br><br>
2. Locate and open the timestamped directory and then run `cat access.log` or `cat error.log`.

    ✔️ **Result:** You verified that the logs were backed up, so you know that your Linux task ran successfully.
---
🎈 **Congratulations!** You extended the `nginx::backup_logs` task functionality to include NGINX installations on the Windows platform. If you want to, you can spend some time exploring this environment.

---
**Find any bugs or have feedback? Click the **Bug Zapper** tab near the top of the page and let us know!**

When you're ready to close the lab, click **Next**.
