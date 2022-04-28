---
slug: configure-a-deployment-to-a-test-environment
id: egfifhvyjeaw
type: challenge
title: Deploy changes to a test environment
teaser: Add a deployment to a pipeline and then add a trigger based on a merge request
  from the main branch of the control repo.
notes:
- type: text
  contents: |-
    In this lab you will:
     - Add a deployment step to a pipeline and ensure deployments to nodes (including test nodes) use a best practice approach.
     - Add a trigger based on a merge request from the main branch of the control repo.

    Completing these steps will result in a workflow that deploys changes to test nodes after pull requests to the main branch from a feature_ branch are successful.

    Click **Start** when you're ready to begin.
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
2. Log into CD4PE with username `puppet@puppet.com` and password `puppetlabs`.
    - If the browser isn't recognizing your keyboard input, copy and paste the username and password from these instructions.<br><br>
3. From the navigation menu, click **Control Repos** > **control-repo**.

4. Under **Pipelines**, select **main** from the dropdown menu to include a new deployment:
- Click Add Stage
- For Stage Name, Type in **Test Deployment**
- Under Select Item, choose **Deployment**
- For Select a Puppet Enterprise Instance, leave **PE** selected
- For Select a Node Group, choose **Development**
- In the Select A Deployment Policy, select **Direct deployment policy**
- Click **Add Stage** then click **Done**


**5.** Edit the **main** pipeline to include an Impact Analysis step for the **development** environment before the **deployment** step:
- Click **Add Stage**
- For Stage Name, type in **IA for Test Deployment**
- In the Select Item pulldown menu, select Impact Analaysis
- Click **Add Impact Analysis**, then click **Done**
- Click on the ellipses icon for **IA for Test Deployment**. Select **Reorder Pipeline** from the popout
- With the blue up arrow icon, move **IA for Test Deployment** before the **Test Deployment** Stage
- Under the jobs list select the **Auto Promote** box on the first gate icon. Do not select **Auto Promote** on the gate icon directly below **IA for Test Deployment**
- Click **Save Changes**, Click **Done**

✔️ **Result:** tbd. <br><br>

Create a new feature branch and use a Gitlab merge request to trigger the main pipeline
========
1. Log in to the Windows Workstation.
1. From the **Start** menu, open **Visual Studio Code**.
1. Enable autosave so that you don't have to remember to save your changes. Click **File** > **Auto Save**.
1. Open the `C:\CODE` directory. Click **File** > **Open Folder**, navigate to the `C:\CODE` directory and click **Select Folder**.
1. If prompted to trust the code in this directory, click **Accept**.
1. In VS Code, open a terminal. Click **Terminal** > **New Terminal**. Change directory to `C:\CODE`. Run the following command: `git clone git@gitlab:puppet/control-repo.git`. Change directory into the **control-repo**: `cd control-repo`.
1. In the terminal window, in the **control-repo** project, run the following commands:
        ```
        git checkout -b feature_server
        ```
3. At `control-repo/site-modules/role/manifests`, create a new file called `server.pp` that includes only the `profile::base`. Copy the following code into the file:

```
class role::server {
  class { 'profile::base':
    login_message => 'Welcome to the server',
  }
}
```
4. Open `control-repo/manifests/site.pp`  in VS Code and edit the file so all servers get the `role::server`. Copy in the following code:

```
node default {
  if $trusted['extensions']['pp_role'] {
      include "role::${trusted['extensions']['pp_role']}"
  }
  else {
    include role::server
  }
}
```
5. Git add, commit and push the `feature_server` branch:
    ```
    git add .
    git commit -m "Add server role to site.pp"
    git push origin feature_server
    ```
6. Switch over to the CD4PE browser window and check the events for the regex pipeline on the control repo. If nothing is happening, click the **New Events** button.

✔️ **Result:** tbd. <br><br>

Create a Gitlab merge request to run the Main pipeline
========
1. Log into Gitlab by clicking the desktop idon **Gitlab**. User/pass is `puppet/puppetlabs`.
2. In the `control-repo` project click **Merge Requests** in the left navigation bar.
3. Click the blue **Create Merge Request** button, then select **Change branches**. In the Source Branch dropdown select the `feature_server` branch. In the Target Branch, select `main` and then create a merge request to merge `feature_server` to `main` by clicking the **Compare Branches and Continue** button.
4. Click **Create Merge Request**.

✔️ **Result:** tbd. <br><br>

Inspect the development environment impact analysis and promote pipeline to Deploy
========
1. Navigate to **CD4PE** > **control-repo** branch.
2. Click **New Events**.
3. Observe the `main` pipeline as it runs the unit tests and syntax checks and then runs the Impact Analysis.
4. Once Impact Analysis finishes running, notice that the pipeline stops. It is waiting for a manual promotion to run the Deployment step.
5. Click to inspect the IA output: Click **6 Succeeded**, then click the blue **#1** analysis report. Then click **View Analysis**.
6. Once satisfied with the output, click **Promote** (next to the `main` pipeline space between the IA step and the Deployment step).
7. Observe the Deployment runs.
8. Record the Job ID: Click on the green **#1 Succeeded**, then the blue job report under **Deployment Done**. Navigate to Deployment Steps-->Orchestration Task and click **View Jobs**. The job id will be revealed.

Switch tabs
9. Log in to PE.
1. Navigate to **Jobs**.
10. Look for the Job ID reported from CD4PE.
11. Observe the changes to the nodes in the Development node group.

✔️ **Result:** tbd. <br><br>

--------
🎈 **Congratulations!** In this lab you...