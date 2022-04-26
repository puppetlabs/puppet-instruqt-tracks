---
slug: configure-a-deployment-to-a-test-environment
id: egfifhvyjeaw
type: challenge
title: Configure a Deployment to a Test Environment
teaser: Add a deployment to a pipeline and then add a trigger based on a merge request
  from the main branch of the control repo.
notes:
- type: text
  contents: Configure A Deployment to a Test Environment
tabs:
- title: Windows Workstation
  type: service
  hostname: guac
  path: /#/client/c/workstation?username=instruqt&password=Passw0rd!
  port: 8080
- title: CD4PE-Host
  type: terminal
  hostname: cd4pe-host
- title: PE Server
  type: terminal
  hostname: puppet
- title: PE Console
  type: service
  hostname: puppet
  port: 443
- title: Gitlab
  type: terminal
  hostname: gitlab
difficulty: basic
timelimit: 3600
---
Add a deployment to the main pipeline for the control repo
========
1. On the **Windows Workstation** desktop, double-click the **CD4PE** shortcut.
    - If the browser window shows a connection privacy warning, bypass it by clicking **Advanced** > **Continue to cd4pe (unsafe)**.<br><br>
1. Log into CD4PE with username `puppet@puppet.com` and password `puppetlabs`.
    - If the browser isn't recognizing your keyboard input, copy and paste the username and password from these instructions.<br><br>
1. From the navigation menu, click **Control Repos** > **control-repo**.

2. Edit the **main** pipeline to add a Pull Request trigger. Click... (tech team to add specific steps here)
3. Edit the **main** pipeline to include a new deployment. Click... (tech team to add specific steps here)
4. Edit the **Deployment** to use the **direct deployment** policy. Click... (tech team to add specific steps here)
5. Select the **Development** environment.
6. Edit the **main** pipeline to include an Impact Analysis step for the **development** environment before the **deployment** step. Click... (tech team to add specific steps here)
7. Ensure the **Auto-Promote** checkbox is NOT selected in the checkbox between the IA and Deployment.

✔️ **Result:** tbd. <br><br>

Create a new feature branch and use a Gitlab merge request to trigger the main pipeline
========
1. Log in to the Windows Workstation.
1. From the **Start** menu, open **Visual Studio Code**.
1. Enable autosave so that you don't have to remember to save your changes. Click **File** > **Auto Save**.
1. Open the `C:\CODE` directory. Click **File** > **Open Folder**, navigate to the `C:\CODE` directory and click **Select Folder**.
1. If prompted to trust the code in this directory, click **Accept**.
1. In VS Code, open a terminal. Click **Terminal** > **New Terminal**.
1. In the VS Code terminal window, in the **control-repo** project, run the following command:
        ```
        git checkout -b feature_server
        ```
3. Add a new role `server.pp` that includes only the `profile::base`. (add specific instructions here)
4. Open `base.pp` (**control-repo** > **manifests** > **base.pp**) and edit the file to include a new notify resource. (tech team to add specific steps here)
5. Open `site.pp` (**control-repo** > **manifests** > **site.pp**) in VS Code and edit the file so all servers get the `role::server`. (tech team to add specific steps here)
6. Git add, commit and push the `feature_server` branch:
    ```
    git add .
    git commit -m "Add notify resource to base.pp and added server role to site.pp"
    git push origin feature_server
    ```
7. Switch over to the CD4PE browser window and check the events for the regex pipeline on the control repo. If nothing is happening, click the **New Events** button.

✔️ **Result:** tbd. <br><br>

Create a Gitlab merge request to run the Main pipeline
========
1. Log into Gitlab. (tech team to add specific steps here)
2. In the `control-repo` project click **Merge Requests**.
3. Select the `feature_server` branch and then create a merge request to merge `feature_server` to main. (tech team to add specific steps here)
4. When prompted, click **Merge when pipeline completes**.

✔️ **Result:** tbd. <br><br>

Inspect the development environment impact analysis and promote pipeline to Deploy
========
1. Navigate to **CD4PE** > **control-repo** branch.
2. Click **New Events**.
3. Observe the `main` pipeline as it runs the unit tests and syntax checks and then runs the Impact Analysis.
4. Once Impact Analysis finishes running, notice that the pipeline stops. It is waiting for a manual promotion to run the Deployment step.
5. Click to inspect the IA output (tech team to add specific steps here)
6. Once satisfied with the output, click **Promote** (next to the `main` pipeline space between the IA step and the Deployment step).
7. Observe the Deployment runs.
8. Record the Job ID. (tech team to add specific steps here)

Switch tabs
9. Log in to PE.
1. Navigate to **Jobs**.
10. Look for the Job ID reported from CD4PE.
11. Observe the changes to the nodes in the Development node group.

✔️ **Result:** tbd. <br><br>

--------
🎈 **Congratulations!** In this lab you...