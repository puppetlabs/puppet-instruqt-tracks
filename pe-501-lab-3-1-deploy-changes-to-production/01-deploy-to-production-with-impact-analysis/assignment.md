---
slug: deploy-to-production-with-impact-analysis
id: hhyo5oaxazf5
type: challenge
title: Deploy changes to Production
teaser: Deploy changes to Production
notes:
- type: text
  contents: |-
    In this lab you will:

     - Add and configure a new pipeline for the Production branch that requires impact analysis and manual deployment.
     - Configure the Development pipeline to deploy to Production.
     - Protect the Production environment and require privileged deployment step approval.
     - Adjust the Main pipeline to automatically deploy to the Development branch from a git commit.
     - Use a rolling deployment policy that requries logic between each step.

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
Protect the production environment
========
1. On the **Windows Workstation** desktop, double-click the **CD4PE** shortcut.
    - If the browser window shows a connection privacy warning, bypass it by clicking **Advanced** > **Continue to cd4pe (unsafe)**.<br><br>
1. Log into CD4PE with username `puppet@puppet.com` and password `puppetlabs`.
    - If the browser isn't recognizing your keyboard input, copy and paste the username and password from these instructions.
    - To see the full CD4PE interface, expand the browser window to full-size.<br><br>
1. Navigate to **Settings** > **Puppet Enterprise**.<br><br>
1. In the **Protected Environments** column, click the `0`.
    - You may need to expand the CD4PE browser window to see the columns clearly.<br><br>
1. In the **Puppet Enterprise protected environments** window, click **Add**. Then, select **production** and toggle the switch to choose  **Administrators** for the approval role. ![designate approval](https://storage.googleapis.com/instruqt-images/PE501-Continuously%20Deliver/PE501-designate-approval.png)
1. Click **Add**, and then click **Done**.<br><br>
1. Close the window, return to the Puppet Enterprise settings page, and review the **Protected environments** column, which now shows one protected environment: ![protected environment](https://storage.googleapis.com/instruqt-images/PE501-Continuously%20Deliver/PE501-protectedenv.png)

    ✅ **Result:** The **production** environment is now protected.<br><br>

Add a deployment step that requires admin approval and impact analysis
========
1. In the left-hand sidebar, navigate to **Control Repos** > **control-repo**.<br><br>
1. Add a new deployment step to deploy to **Production** with **Impact Analysis** after a successful deployment to the **Development** environment. First, select the **main** pipeline from the **Pipelines** dropdown. ![main pipeline selected](https://storage.googleapis.com/instruqt-images/pipelines-main.png)
1. Add a new deployment stage by clicking **+ Add stage** at the bottom of the pipeline. ![add stage button](https://storage.googleapis.com/instruqt-images/add-stage.png)
1. Enter the following:
    - In the **Stage Name** field, enter **Deploy to Production**.
    - For **Select a Node group**, select **Production environment**.
    - Under **Select a deployment policy**, select the **Eventual Consistency policy**.
    - Click **Add stage** and then click **Done**.<br><br>
1. Edit the **main** pipeline to include an Impact Analysis step for both the **development** and **production** environments <i>before</i> the **deployment** steps. First, click **Add Stage**.<br><br>
1. Enter the following:
    - In the **Stage Name** field, enter **IA for Deployment**.
    - For **Select Item**, select **Impact Analaysis**.
    - Leave other settings as-is.
    - Click **Add impact analysis** and then click **Done**.<br><br>

1. Click the ellipses (**...**) to the right of **IA for Deployment**, and then click **Reorder Pipeline**.![reorder pipeline](https://storage.googleapis.com/instruqt-images/reorder-pipeline.png)
1. Click the blue arrow to the right of **IA for Deployment** two times to move **IA for Deployment** up the pipeline above **Deploy to Dev**.![blue arrow](https://storage.googleapis.com/instruqt-images/blue-arrow.png)
    Your pipeline should now look like this (click and drag this sidebar to increase image size): ![updated pipeline](https://storage.googleapis.com/instruqt-images/reorder-pipeline-updated.png)
1. Click **Save changes** and then click **Done**.<br><br>
1. Under the list of jobs (**Pipeline stage 1**) and under **IA for Deployment**, click the checkbox for **Auto Promote**. Do not select **Auto Promote** under **Deploy to Dev**. Your pipelines should now look like this: ![pipelines auto promote](https://storage.googleapis.com/instruqt-images/PE501-Continuously%20Deliver/lab3.1-pipelines-set.png)

    ✅ **Result:** You added a new deployment step that will require Admin approval to deploy changes to Production.<br><br>

Create a new branch to test a code change
========
1. From the **Start** menu, open **Visual Studio Code**.<br><br>
1. Open the `C:\CODE` directory. Click **File** > **Open Folder**, navigate to the `C:\CODE` directory and click **Select Folder**.
    - If prompted to trust the code in this directory, click **Accept**.<br><br>
1. In VS Code, open a terminal. Click **Terminal** > **New Terminal**.<br><br>
1. Clone the `control-repo` repository with the following command:
    ```
    git clone git@gitlab:puppet/control-repo.git
    ```
1. Change directory in the `control-repo` by running `cd control-repo`.<br><br>
1. On the workstation in the **control-repo** project, run:
    ```
    git checkout main
    git checkout -b feature_new_config
    ```
    💡 After pasting the code in the terminal, remember to click Enter.<br><br>
2. Open the `base.pp` file (**control-repo** > **site-modules** > **profile** > **manifests** > **base.pp**). Edit it to point from `/etc/old.config` to `/etc/new.config` by replacing the code in the file with the following:
    ```
    class profile::base ($login_message){
      class {'motd':content => $login_message,}

      file {'/etc/new.config':
        content => 'this is a new config file'
      }
    }
    ```
3. In the terminal, run the following command to add, commit, and push changes to origin `feature_new_motd`:
    ```
    git add .
    git commit -m "Update base profile with new config file"
    git push -u origin feature_new_config
    ```
    💡 After pasting the code in the terminal, remember to click Enter.<br><br>
4. Switch over to the CD4PE browser window to ensure your **Regex** `feature_new_config` pipeline is running (jobs will show as **In Progress**).
    - If nothing is showing, click **New Events**: ![new events button](https://storage.googleapis.com/instruqt-images/new-events.png)
    - Wait until the run completes successfully before you continue (about 2-3 minutes).<br><br>

    ✅ **Result:** Code was pushed to a new `feature_new_config` branch and the regex pipeline tested the change: ![base profile job completed](https://storage.googleapis.com/instruqt-images/PE501-Continuously%20Deliver/lab3.1-base-profile-job-completed.png)

Create a Gitlab merge request to run the main pipeline
========
1. On the **Windows Workstation** desktop, double-click the **Gitlab** desktop icon.<br><br>
1. Log in with username `puppet`and password `puppetlabs`.<br><br>
1. Navigate to the `control-repo` project, and then click the **Merge Requests** icon located in the left navigation bar:![merge requests](https://storage.googleapis.com/instruqt-images/PE501-Continuously%20Deliver/merge-requests2.png)
1. Click **Create merge request**, and then click **Change branches** (next to `production` in the header).<br><br>
1. Leave **Source branch** set to the `feature_new_config` branch.<br><br>
1. For **Target branch**, choose `main`.<br><br>
1. Click **Compare branches and continue**.<br><br>
1. Leave the title as-is and click **Create merge request**.<br><br>
1. After the page refreshes, click **Merge**. This will create a merge request to merge `feature_new_config` to `main`: ![base profile merged](https://storage.googleapis.com/instruqt-images/PE501-Continuously%20Deliver/lab3.1-base-profile-merged.png)

    ✅ **Result:** The merge request from Gitlab triggers the **Main** pipeline to run.<br><br>

Approve deployment to production
========
1. Switch to the CD4PE browser (this may be a tab in your browser window).<br><br>
1. If nothing is showing as running, click **New Events**: ![new events button](https://storage.googleapis.com/instruqt-images/new-events.png)
2. Notice that the `main` pipeline has automatically deployed to the **Development** environment but does not automatically push changes and code to the **Production** environment. Wait for all steps to complete before proceeding (2-3 minutes).<br><br>
3. Review Impact Analysis. Click the downward arrow to the right of the latest **Main** pipeline run.![downward arrow](https://storage.googleapis.com/instruqt-images/downward-arrow-2.png)
4. In the **IA for Deployment** row, click the blue link that starts with a hash (#): ![IA link](https://storage.googleapis.com/instruqt-images/PE501-Continuously%20Deliver/lab3.1-ia-link.png)
5. Review the Impact Analysis results. Once you are done, return to the control repo main page by clicking the `control-repo` link in the **Control Repos\control-repo** breadcrumb trail at the top of the page.<br><br>
6. Back at the **Main** pipeline, between the **Deploy to Dev** and **Deploy to Prod** stages, click **Promote**:![promote](https://storage.googleapis.com/instruqt-images/deploy-to-dev-deploy-to-prod.png)
1. Click **Promote** and then click **Done**.<br><br>
7. When it appears, click **New Events**.<br><br>
8. Click the downard expanion arrow to the right of the running job and notice the Deployment to production step has a **Pending approval** badge: ![pending approval](https://storage.googleapis.com/instruqt-images/PE501-Continuously%20Deliver/pending-approval.png)
9. Under **Deployment pending approval**, click the blue link that starts with a #. ![](https://storage.googleapis.com/instruqt-images/PE501-Continuously%20Deliver/deployment-pending-approval.png)

1. Click the **Approve** button, and then click **Approve** and **Done**. ![](https://storage.googleapis.com/instruqt-images/PE501-Continuously%20Deliver/approve.png)

    🔀 Switch to the PE Console tab.<br><br>

1. Log into Puppet Enterprise with username `admin` and password `puppetlabs`, and then navigate to the **Jobs** page.<br><br>
2. Notice that there is no Job ID, as Eventual Consistency relies on normal Puppet runs to deploy your changes.

    ✅ **Result:** You new code has been deployed to the PE server and will be automatically rolled out during the normal Puppet Agent run lifecycle.<br><br>

-------
🎈 **Congratulations!** In this lab you introduced an additonal deployment step to your **Main** pipeline. This step continued to move your Puppet code along to the **Production** environment after a successful deployment to the **Development** environment. You also configured **Impact Analysis** to show the potential changes to your environments and protected the **Production** environment by requiring adminstrative approval prior to deployment.

When you are finished with this lab, click **Next**.