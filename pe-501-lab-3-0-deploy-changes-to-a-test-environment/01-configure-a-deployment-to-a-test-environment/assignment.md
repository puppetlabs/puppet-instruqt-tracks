---
slug: configure-a-deployment-to-a-test-environment
id: egfifhvyjeaw
type: challenge
title: Deploy changes to a test environment
teaser: Add a deployment to a pipeline, and then add a trigger based on a merge request
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
timelimit: 3300
---
Add a test deployment to the main pipeline
========
1. On the **Windows Workstation** desktop, double-click the **CD4PE** shortcut.
    - If the browser window shows a connection privacy warning, bypass it by clicking **Advanced** > **Continue to cd4pe (unsafe)**.<br><br>
2. Log into Continuous Delivery for PE with username `puppet@puppet.com` and password `puppetlabs`.
    - If the browser doesn't recognize your keyboard input, copy the username and password from these instructions.
    - To see the full Continuous Delivery for PE interface, maximize the browser window.<br><br>
3. Navigate to **Control Repos** > **control-repo**.<br><br>
4. Add a new deployment to the main pipeline. First, ensure **main** is selected in the drop-down menu:![main pipeline](https://storage.googleapis.com/instruqt-images/pipelines-main.png) Then, click **Add Stage**:![add stage](https://storage.googleapis.com/instruqt-images/PE501-Continuously%20Deliver/add-stage.png)
1. In the **Add new stage** window, enter the following:

    - In the **Stage Name** field, enter **Test Deployment**.
    - For **Select a Node Group** choose **Development environment**.
    - Under **Select a Deployment Policy** choose **Direct deployment policy**.
    - Leave all other settings as is.<br><br>
1. Click **Add Stage** and then click **Done**.

    ✅ **Result:** A test deployment has been added to the **main** pipeline for the control repo: ![test deployment created](https://storage.googleapis.com/instruqt-images/PE501-Continuously%20Deliver/Lab3.0-test-deployment-created.png)

Update the MOTD on a new feature test branch
========
1. From the **Start** menu, open **Visual Studio Code**.<br><br>
1. Open the `C:\CODE` directory. Click **File** > **Open Folder**, navigate to the `C:\CODE` directory and click **Select Folder**.
    - If prompted to trust the code in this directory, click **Accept**.<br><br>
1. In VS Code, open a terminal. Click **Terminal** > **New Terminal**.<br><br>
1. Clone the **control-repo** project:
    ```
    git clone git@gitlab:puppet/control-repo.git
    ```
    💡 After pasting the code in the terminal, remember to click Enter.<br><br>
1. Change directory into the **control-repo**:
    ```
    cd control-repo
    ```
2. Check out the **feature_test_motd** branch:
    ```
    git checkout -b feature_test_motd
    ```
3. Navigate to the **data** directory (**control-repo** > **data**).<br><br>
4. Edit `common.yaml` and replace the login message with the following:
    ```
    'Welcome to a new test server!'
    ```
5. In the VS Code terminal, add, commit, and push your changes to the `feature_test_motd` branch:
    ```
    git add .
    git commit -m "Update base profile login message"
    git push -u origin feature_test_motd
    ```
6. Switch to the CD4PE browser window, navigate to **Control Repos** > **control-repo**, and review events for the regex pipeline on the control repo. If nothing happens, click the **New Events** button: ![new events](https://storage.googleapis.com/instruqt-images/PE501-Continuously%20Deliver/new-events.png)

1. The pipeline event will show as pending until the jobs finish running (which should take about 2-3 minutes). Click the drop-down arrow at the right for a detailed look at the jobs as they run:![jobs running](https://storage.googleapis.com/instruqt-images/PE501-Continuously%20Deliver/lab3.0-updated-base-profile-message-pending.png)

    ✅ **Result:**  The job rus successfully to include the updated login message: ![updated motd](https://storage.googleapis.com/instruqt-images/PE501-Continuously%20Deliver/lab3.0-base-message-updated-complete.png)

Create a Gitlab merge request to run the main pipeline
========
1. On the **Windows Workstation** desktop, double-click the **Gitlab** desktop icon.<br><br>
1. Log in with username `puppet`and password `puppetlabs`.<br><br>
2. Navigate to the `control-repo` project, and then click the **Merge Requests** icon located in the left navigation bar: ![](https://storage.googleapis.com/instruqt-images/PE501-Continuously%20Deliver/merge-requests2.png)

1. Click **Create merge request**, and then click **Change branches** (next to `production` in the header).<br><br>
1. Leave **Source branch** set to `feature_test_motd`.<br><br>
1. For **Target branch**, select `main`.<br><br>
1. Click **Compare branches and continue**.<br><br>
1. Leave the title as is and click **Create merge request**.<br><br>
1. After the page refreshes, click the **Merge** button. This will merge your `feature_test_motd` change into the `main` branch.

    ✅ **Result:** The `feature_test_motd` branch was merged to `main` using a Gitlab merge request: ![Gitlab merge request](https://storage.googleapis.com/instruqt-images/PE501-Continuously%20Deliver/lab3.0-gitlab-merge.png)

Promote the main pipeline to Deploy and locate the job ID
========
1. Return to the CD4PE browser window (which may be a tab of the Gitlab browser), scroll down, and click **New Events** if shown.<br><br>
3. Observe the `main` pipeline as it runs the unit tests and syntax checks.<br><br>
4. After the code verification stage is complete, click **Promote** (to the right of the page under **Pipeline stage 1**). ![promote](https://storage.googleapis.com/instruqt-images/promote.png)
1. Click **Promote** and then click **Done**.<br><br>
7. Click the **New Events** button if shown, and then click the drop-down arrow to the right of the running pipeline: ![drop-down arrow](https://storage.googleapis.com/instruqt-images/downward-arrow-2.png)

    Review the merge run progress: ![merge run progress](https://storage.googleapis.com/instruqt-images/PE501-Continuously%20Deliver/lab3.0-merge-branch-deploy-progress.png)

8. After the job completes, record the Job ID. Click on the green **1 Succeeded**, and then click the blue job report link (**#1**) under **Deployment Done**: ![1 succeeded](https://storage.googleapis.com/instruqt-images/PE501-Continuously%20Deliver/1-succeeded.png) ![deployment done](https://storage.googleapis.com/instruqt-images/PE501-Continuously%20Deliver/deployment-done.png)
1. Scroll down to **Deployment events** > **3. Orchestration task** and click **View jobs**: ![view jobs](https://storage.googleapis.com/instruqt-images/PE501-Continuously%20Deliver/view-jobs.png)

    ✅ **Result:** The job ID will appear under the job column at the left: ![job ID](https://storage.googleapis.com/instruqt-images/PE501-Continuously%20Deliver/job-id.png)

Review the job run reports
=======
🔀 Switch to the **PE Console** tab<br><br>

1. Log into PE with username `admin` and password `puppetlabs`.<br><br>
1. Navigate to **Jobs**, and then click on the Job ID reported from Continuous Delivery for PE. This shows you the jobs that ran on nodes in the **Development** node group.<br><br>
1. Under the **Report** column at the right, click one of the links shown, and then click the **Log** tab to review the changes.

    ✅ **Result:** New code was deployed directly to the Development environment by means of a Direct Deployment stage in your main pipeline. This deployment was triggered by a merge request made when changes from your **feature_test_motd** code branch flagged a merge request in Gitlab.<br><br>

--------
🎈 **Congratulations!** In this lab you added a deployment step to the main pipeline for the control repo. You used Gitlab to trigger the main pipeline. You then added a trigger based on a merge request from the main branch of the control repo. This is a best-practice workflow for deploying changes to test nodes.

When you are finished with this lab, click **Next**.