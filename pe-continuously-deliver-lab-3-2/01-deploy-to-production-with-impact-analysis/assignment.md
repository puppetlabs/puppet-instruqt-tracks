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
timelimit: 3600
---
Protect the production environment
========
1. On the **Windows Workstation** desktop, double-click the **CD4PE** shortcut.
    - If the browser window shows a connection privacy warning, bypass it by clicking **Advanced** > **Continue to cd4pe (unsafe)**.<br><br>
1. Log into CD4PE with username `puppet@puppet.com` and password `puppetlabs`.
    - If the browser isn't recognizing your keyboard input, copy and paste the username and password from these instructions.
    - To see the full CD4PE interface, expand the browser window to full-size.<br><br>
2. Navigate to **Settings** > **Puppet Enterprise**.
3. In the **Protected Envs** column click the `0`.
    - You may need to expand the CD4PE browser window to see the columns clearly.<br><br>
1. In the modal that opens, click **Add**. Then, select **Production environment** and toggle the switch to choose  **Administrators** for the approval role. ![designate approval](https://storage.googleapis.com/instruqt-images/PE501-Continuously%20Deliver/PE501-designate-approval.png)
1. Click **Add**, and then click **Done**.
1. Close the modal, return to the Puppet Enterprise settings page, and review the **Protected environments** column, which now shows one protected environment: ![protected environment](https://storage.googleapis.com/instruqt-images/PE501-Continuously%20Deliver/PE501-protectedenv.png)

    ✅   **Result:** The **production** environment is now protected.<br><br>

Create a new Deployment to Deploy to Production with Admin approval and Impact Analysis
========
1. In the left-hand sidebar, navigate to **Control Repos** > **control-repo**.
2. Add a new deployment step to deploy to **Production** with **Impact Analysis** after a successful deployment to **Development** environment.
3. Add a deployment step by clicking **Add a step** at the bottom of the pipeline.
4. Enter a name of **Deploy to Prod** in the **Stage Name** field. Under **Select a Node group**, select Production. Under **Select a deployment policy**, select the **Eventual Consistency policy**. Click **Add deployment to stage**. Click **Done**.
5. Edit the **main** pipeline to include an Impact Analysis step for the both the **developemt** and **production** environments <i>before</i> the **deployment** steps. First, click **Add Stage**.
1. In the modal that appears, enter the following for each field:

    <u>Create stage</u>
    - Stage Name: **IA for Test Deployment**
    <u>Add to this stage</u>
    - Select Item: **Impact Analaysis**
    <u>Select environments to analyze</u>
    - Leave as-is.
    - Click **Add Impact Analysis**, and then click **Done**.<br><br>

1. Click the ellipses (**...**) to the right of **IA for Test Deployment**, and then click **Reorder Pipeline**.
1. Click the blue arrows at the right to move **IA for Test Deployment** up the pipeline above **Test Deployment**. Click **Save changes** and then click **Done**.
1. Under the list of jobs, choose **Auto Promote**. (Do not select **Auto Promote** on the gate icon directly below **IA for Test Deployment**.) Your pipelines should now look like this:

✅   **Result:** You have added a new Deployment step that will require Admin approval to deploy changes to Production.<br><br> **ADD SCREENSHOT**

Merge the feature_new_config branch to the main branch
========
1. Open VScode. Open Folder to C:\CODE. Open a New Terminal. Change directory to C:\CODE. Clone the `control-repo` repository with the following command:

```
git clone git@gitlab:puppet/control-repo.git
```
Change directory in the `control-repo` by running `cd control-repo`.

On the workstation in the **control-repo** project run `git checkout main` and then `git checkout -b feature_new_config`.

2. Open `base.pp` file at **control-repo/site-modules/profile/manifests/base.pp** and edit it to include a new name for the config file. Copy the following code into the file:
```
class profile::base ($login_message){
  class {'motd':content => $login_message,}

  file {'/etc/new.config':
    content => 'this is a new config file'
  }
}
```
4. Git add, commit and push origin feature_new_motd: `git add .` then `git commit -m "Adding message of the day"` then `git push origin feature_new_config`
5. Merge to main: `git merge main`.
6. Switch over to the CD4PE browser to ensure your **Regex** `feature_new_config pipeline` runs. Wait until the run completes successfully before you continue.

✅   **Result:** The `feature_new_config` branch was merged to `main` using a Gitlab merge request. <br><br>

Create a new Gitlab merge request to run the Main pipeline
========
1. On the **Windows Workstation** desktop, double-click the **Gitlab** desktop icon.
1. Log in with username `puppet`and password `puppetlabs`.
2. Navigate to the `control-repo` project, and then click the **Merge Requests** icon located in the left navigation bar: ![](https://storage.googleapis.com/instruqt-images/PE501-Continuously%20Deliver/merge-requests2.png)

3. Click **Create merge request**, and then click **Change branches** (next to `production` in the header).
1. Leave **Source branch** set to the `feature_new_config`.
1. For **Target branch**, choose `main`.
1. Click **Compare branches and continue**. This will create a merge request to merge `feature_server` to `main`.
4. Leave the title as-is and click **Create merge request**.

✅   **Result:** The MR from Gitlab triggers the **Main** pipeline to run.<br><br>

Approve deployment to Production
========
1. Switch to the CD4PE browser.
2. Notice that the `main` pipeline has automatically deployed to the **Development** node group but does not automatically push changes and code to the **Production** node groups. Ensure all steps have completed successfully.
3. Review the Impact Analysis, by clicking the downward expansion arrow next to the latest **Main** pipeline run.
5. Click the # hyperlink in the **IA for Prod** step to view the Impact Analysis result page
6. Once you have reviewed the IA results return to the control repo main page by clicking `control-repo` link in the 'Control Repos\control-repo' breadcrumb trail
7. Back at the **Main** pipeline click the **Promote** link between the **IA to Prod** and **Deploy to Prod** stages
8. Click the **New Events** button when it appears
9. Click the downard expanion arrow and notice the Deployment to production step has a **Pending approval** bagdge
10. Click the # hyperlink under the text *Deployment pending approval* and then click the green **Approve** button on the next page
       🔀 Switch to the PE tab.
1. Log into Puppet Enterprise with username `admin` and password `puppetlabs` and navigate to the Jobs page.
1. Notice that there is no Job ID, as Eventual Consistency relies on normal Puppet runs to deploy your changes.

✅ **Result:** You new code has been deployed to the PE server and will be automatically rolled out during the normal Puppet Agent run lifecycle<br><br>

-------
🎈 **Congratulations!** In this lab you introduced an additonal deployment step to your **Main** pipeline. This step continued to move your Puppet code along to the **Production** environment after a successful deployment to the **Development** environment. You also configured **Impact Analysis** to show the potential changes to your environments and proteced the **Production** environment by requiring adminstrative approval prior to deployment.