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

    Completing these steps will result in a workflow that deploys changes to test nodes after pull requests to the main branch from a feature branch are successful.

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
- title: Lab Help Guide
  type: website
  hostname: guac
  url: https://puppet-kmo.gitbook.io/practice-lab-help/
difficulty: basic
timelimit: 3600
---
Add a deployment to the Main pipeline for the control repo
========
1. On the **Windows Workstation** desktop, double-click the **CD4PE** shortcut.
    - If the browser window shows a connection privacy warning, bypass it by clicking **Advanced** > **Continue to cd4pe (unsafe)**.<br><br>
2. Log into CD4PE with username `puppet@puppet.com` and password `puppetlabs`.
    - If the browser isn't recognizing your keyboard input, copy and paste the username and password from these instructions.
    - To see the full CD4PE interface, expand the browser window to full-size.<br><br>
3. Navigate to **Control Repos** > **control-repo**.
4. Add a new deployment to the main pipeline. First, ensure **main** is selected in the drop-down menu. Then, click **Add Stage**:![add stage](https://storage.googleapis.com/instruqt-images/PE501-Continuously%20Deliver/add-stage.png)
1. In the modal that appears, enter the following for each field:

    <u>Create stage</u>
    - Stage Name: **Test Deployment**
    <u>Add to this stage</u>
    - Select Item: **Deployment**
    - Select a Puppet Enterprise Instance: **PE**
    - Select a Node Group: **Development environment**
    - Select a Deployment Policy: **Built-in deployment policies**
      - Choose **Direct deployment policy**
      - Leave existing settings as-is.<br><br>
1. Click **Add Stage** and then click **Done**.

✅ **Result:** A deployment has been added to the main pipeline for the control repo. <br><br>

Create a new feature branch and use Gitlab to trigger the Main pipeline
========
1. From the **Start** menu, open **Visual Studio Code**.
1. Enable autosave so that you don't have to remember to save your changes. Click **File** > **Auto Save**.
1. Open the `C:\CODE` directory. Click **File** > **Open Folder**, navigate to the `C:\CODE` directory and click **Select Folder**.
1. If prompted to trust the code in this directory, click **Accept**.
1. In VS Code, open a terminal. Click **Terminal** > **New Terminal**. Change directory to `C:\CODE`.
1. Clone the **control-repo** project:
    ```
    git clone git@gitlab:puppet/control-repo.git
    ```
1. Change directory into the **control-repo**:
    ```
    cd control-repo
    ```
2. Check out the **feature_test_motd** branch:
    ```
    git checkout -b feature_test_motd
    ```
3. Navigate to the **data** directory (**control-repo** > **data**).
4. Edit `common.yaml` to contain the following:
    ```
    # <control-repo>/data/common.yaml
    ---
    profile::base::login_message: 'Welcome to a new test server!'
    profile::apache::port: 80
    ```
5. In the VS Code terminal, add, commit, and push your changes to the `feature_test_motd` branch:
    ```
    git add .
    git commit -m "Updated base profile login message"
    git push origin feature_test_motd
    ```
6. Switch to the CD4PE browser window, navigate to Control Repos > control-repo and review events for the regex pipeline on the control repo. If nothing is happening, click the **New Events** button: ![new events](https://storage.googleapis.com/instruqt-images/PE501-Continuously%20Deliver/new-events.png)

1. The pipeline event will show as pending until the jobs finish running (which takes 1-2 minutes). Click the drop-down arrow at the right for a detailed look at the jobs as they run:![jobs running](https://storage.googleapis.com/instruqt-images/PE501-Continuously%20Deliver/jobs-running.png)

✅ **Result:**  Once the jobs finish running, the output shows that the **feature_test_motd** branch has been added: ![regex events](https://storage.googleapis.com/instruqt-images/PE501-Continuously%20Deliver/regex-events.png)

Create a Gitlab merge request to run the Main pipeline
========
1. On the **Windows Workstation** desktop, double-click the **Gitlab** desktop icon.
1. Log in with username `puppet`and password `puppetlabs`.
2. Navigate to the `control-repo` project, and then click the **Merge Requests** icon located in the left navigation bar: ![](https://storage.googleapis.com/instruqt-images/PE501-Continuously%20Deliver/merge-requests2.png)

3. Click **Create merge request**, and then click **Change branches** (next to `production` in the header).
1. Leave **Source branch** set to the `feature_test_motd`.
1. For **Target branch**, choose `main`.
1. Click **Compare branches and continue**. This will create a merge request to merge `feature_test_motd` to `main`.
4. Leave the title as-is and click **Create merge request**.
5. Click the **Merge** button to merge your change into the `main` branch.

✅ **Result:** The `feature_test_motd` branch was merged to `main` using a Gitlab merge request. <br><br>

Inspect the development environment impact analysis and promote pipeline to Deploy
========
1. Return to the CD4PE browser window (which may be a tab of the Gitlab browser), scroll down, and click **New Events**.
3. Observe the `main` pipeline as it runs the unit tests and syntax checks
4. Once the code verification stage has completed you may then click **Promote** (to the right of the jobs in the code verification stage of the pipeline). Click **Promote** and then click **Done**.
7. Click **New Events**, and then click the drop-down arrow to view the Deployment run progress.
8. Record the Job ID: Click on the green **1 Succeeded**, then click the blue job report under **Deployment Done**.
1. Navigate to **Deployment Steps** > **Orchestration Task** and click **View Jobs**. The job ID will be revealed.

    🔀 Switch to the **PE Console** tab<br><br>
9. Log in to PE with username `admin` and password `puppetlabs`.
1. Navigate to **Jobs**, and then click on the Job ID reported from CD4PE.
11. Review the changes to the nodes in the **Development** node group by clicking a node name and then clicking the link for the latest log. Review the changes made to the node.

✅ **Result:** New code was deployed directly to the Development environment by means of a Direct Deployment stage in your Main pipeline. This deployment was triggered by a Merge Request made when changes from your feature_test_motd code branch flagged a Merge Request in Gitlab.<br><br>

--------
🎈 **Congratulations!** In this lab you added a deployment step to the main pipeline for the control repo. You used Gitlab to trigger the Main pipeline. You then added a trigger based on a merge request from the main branch of the control repo. You also inspected the Impact Analysis of the jobs that you ran and promoted a pipeline to deply. This is a best-practice workflow for deploying changes to test nodes.

When you are ready to close out this lab, click **Next**.