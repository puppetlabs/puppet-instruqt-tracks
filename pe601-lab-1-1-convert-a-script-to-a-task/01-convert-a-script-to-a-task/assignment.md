---
slug: convert-a-script-to-a-task
id: 15gorgy0lbfm
type: challenge
title: Convert a script to a task
teaser: Convert a Bash script to a Bolt task.
notes:
- type: text
  contents: |-
    The first step in creating a Puppet task is to convert a script into a format Puppet knows how to work with. Here, you will use a Bash script to backup the log files on an NGINX installation.

    In this lab, you will:
     - Checkout NGINX code from source control.
     - Use the Puppet Development Kit (PDK) to create a new task.
     - Add a pre-written Bash script to the tasks folder, which will backup the NGINX logs on the target.
     - Use a metadata JSON file to describe the parameters in the backup script.
     - Run acceptance against a development node.

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
- title: Bug Zapper
  type: website
  hostname: guac
  url: https://docs.google.com/forms/d/e/1FAIpQLSfGpJOzuOk-N4L8TglPPUlPopT02Ok8zEvss62XdGMxAK_3gA/viewform?embedded=true
- title: Lab Help
  type: website
  hostname: guac
  url: https://puppet-kmo.gitbook.io/practice-lab-help/
difficulty: basic
timelimit: 3600
---
Pull down NGINX code and create a new Bolt task
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
7. Now, use the Puppet Development Kit (PDK) to create a new Bolt task to backup the logs:
    ```
    pdk new task backup_logs
    ```
    ✏️ **Note:** When prompted whether you consent to PDK collecting anonymous usage information, choose whichever option you prefer. This information is not stored after the lab expires.

    ✔️ **Result:** You created two files needed to setup the initial Bolt task: `backup_logs.sh` and `backup_logs.json`. ![cli output that shows files added](https://storage.googleapis.com/instruqt-images/files-added.png)

Edit the Bolt task and JSON file
========

1. In VS Code, open `backup_logs.sh` (**File** > **Open File...** > **CODE** > **nginx** > **tasks** > **backup_logs.sh**). Replace the contents of this existing backup script with the following script, which copies logs from `/var/log/nginx` to a subdirectory of `/var/backup` with the current timestamp as the directory name:

    ```
    #!/bin/bash
    # Sites backup script
    source_dir="/var/log/nginx"
    target_dir="/var/backup"

    # Target directory using a timestamp
    day=$(date +%Y%m%d-%H%M%S)
    target_dir_bkp="$target_dir/$day"
    mkdir -p $target_dir_bkp

    # Backup the files
    echo "$(date) Backing up $source_dir to $target_dir_bkp"
    cp -aR $source_dir/* $target_dir_bkp
    echo "$(date) Backup finished"

    # Diff to verify (diff returns a non-zero exit code if it finds any differences
    diff --recursive $source_dir $target_dir_bkp
    ```
3. In the same directory location, open `backup_logs.json`. Replace the contents of the file with the following JSON code which includes a description of the Bolt task, noop settings, and any included parameters:

    ```
    {
      "description": "Backs up nginx logs",
      "supports_noop": false,
      "parameters": {}
    }
    ```
4. In the VS Code terminal, run the following code to validate the new Bolt task using the PDK:
    ```
    pdk validate
    ```
    ✏️ **Note:** It may take a minute or two for the validation to complete.<br><br>
5. Now, run your Bolt task against `nixagent1` to confirm that it works:
    ```
    bolt task run nginx::backup_logs --targets nixagent1
    ```

✔️ **Result:** Notice the command line output which shows that the task ran successfully against nixagent1: `Successful on 1 target: nixagent1`

Modify the Bolt task to accept Bolt-supplied parameters
========
1. In the VS Code window, return to `backup_logs.sh` and replace the values for `source_dir` (line 3) and `target_dir` (line 4) with Bolt-supplied parameters:
    ```
    source_dir=$PT_source_dir
    ```
    ```
    target_dir=$PT_target_dir
    ```

2. Now, open `backup_logs.json`. Replace the previous contents with the following, which supplies default parameters for the Bolt task:
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
      }
    }
    ```
✔️ **Result:** The files were updated to accept new parameters.

Run the new Bolt task and push it to the Git server
========

1. Now that your Bolt task has been updated, it can run successfully. In the terminal window, run the Bolt task against `nixagent2`:
    ```
    bolt task run nginx::backup_logs --targets nixagent2
    ```
    ✔️ **Result:** Notice the command line output which shows that the task ran successfully against nixagent2:
    `Successful on 1 target: nixagent2`<br><br>

2. Since the Bolt task run was successful, you can now commit your new Bolt task to the Git repo and push it up to the Git server:
    ```
    git add .
    git commit -m "Add a task to backup logs"
    git push
    ```

    ✔️ **Result:** The output that follows the `git push` command indicates that the Bolt task to backup logs was successfully pushed to the Git server: ![git push output](https://storage.googleapis.com/instruqt-images/git-push-output.png)

----------

🎈 **Congratulations!** You took a backup script written for NGINX in Bash and converted it to a Bolt task. You supplied parameters via the command line, and added defaults in the JSON metadata file for the new Bolt task. If you want, you can spend some time exploring this environment.

**Find any bugs or have feedback? Click the **Bug Zapper** tab near the top of the page and let us know!**

When you are finished with this lab, click **Next**.