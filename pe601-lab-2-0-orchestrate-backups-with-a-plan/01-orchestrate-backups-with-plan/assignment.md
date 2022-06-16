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
9. Run the sample plan against your test nodes:
    ```
    bolt plan run nginx::backup_all_logs -targets nixagent1,winagent1
    ```

Create new tasks to pause and restart the nginx service during log backups
========

1.