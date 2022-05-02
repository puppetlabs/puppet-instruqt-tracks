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
difficulty: basic
timelimit: 10800
---
Protect the production environment
========
1. On the **Windows Workstation** desktop, double-click the **CD4PE** shortcut.
    - If the browser window shows a connection privacy warning, bypass it by clicking **Advanced** > **Continue to cd4pe (unsafe)**.<br><br>
1. Log into CD4PE with username `puppet@puppet.com` and password `puppetlabs`.
    - If the browser isn't recognizing your keyboard input, copy and paste the username and password from these instructions.
2. Navigate to **Settings** > **Puppet Enterprise**.
3. In the **Protected Envs** column click the `0`.
    - You may need to expand the CD4PE browser window to see the columns clearly.<br><br>
1. In the modal that opens, click **Add**. Then, select **Production environment** and toggle the switch to choose  **Administrators** for the approval role. ![designate approval](https://storage.googleapis.com/instruqt-images/PE501-Continuously%20Deliver/PE501-designate-approval.png)
1. Click **Add**, and then click **Done**.
1. Close the modal, return to the Puppet Enterprise settings page, and review the **Protected environments** column, which now shows one protected environment: ![protected environment](https://storage.googleapis.com/instruqt-images/PE501-Continuously%20Deliver/PE501-protectedenv.png)

    ✔️ **Result:** The **production** environment is now protected.<br><br>

Create a new Deployment to Deploy to Production with Admin approval and Impact Analysis
========
1. In the left-hand sidebar, navigate to **Control Repos** > **control-repo**.
2. Add a new deployment step to deploy to **Production** with **Impact Analysis** after a successful deployment to **Development** environment.
3. Add a deployment step by clicking **Add a step** at the bottom of the pipeline.
4. Enter a name of **Deploy to Prod** in the **Stage Name** field. Under **Select a Node group**, select Production. Under **Select a deployment policy**, select the **Eventual Consistency policy**. Click **Add deployment to stage**. Click **Done**.
5. Add an **Impact Analysis** step
1. In the modal that appears, enter the following for each field:

    <u>Create stage</u>
    - Stage Name: **IA for Deployment to Dev and Prod**
    <u>Add to this stage</u>
    - Select Item: **Impact Analaysis**
    <u>Select environments to analyze</u>
    - Leave as-is.
    - Click **Add Impact Analysis**, and then click **Done**.<br><br>

1. Click the ellipses (**...**) to the right of **IA for Deployment to Dev and Prod**, and then click **Reorder Pipeline**.
1. Click the blue arrows at the right to move **IA for Deployment to Dev and Prod** up the pipeline above **Test Deployment**. Click **Save changes** and then click **Done**.
1. Under the list of jobs, choose **Auto Promote**. (Do not select **Auto Promote** on the gate icon directly below **IA for Deployment to Dev and Prod**.)

✔️ **Result:** You have added a new Deployment step that will require Admin approval to deploy changes to Production.<br><br>

Merge the feature_new_motd branch to the main branch
========
1. Open VScode. Open Folder to C:\CODE. Open a New Terminal. Change directory to C:\CODE. Clone the `control-repo` repository with the following command:

```
git clone git@gitlab:puppet/control-repo.git
```
Change directory in the `control-repo` by running `cd control-repo`.

On the workstation in the **control-repo** project run `git checkout main` and then `git checkout -b feature_new_motd`.

2. Open `common.yaml` file at **control-repo/data/common.yaml** and edit it to include a new string for message of the day. Copy the following code into the file:
4. Git add, commit and push origin feature_new_motd: `git add .` then `git commit -m "Adding message of the day"` then `git push origin feature_new_motd`
5. Merge to main: `git merge main`.
6. Switch over to the CD4PE browser to ensure your `feature_ pipeline` runs. Wait until the run completes successfully before you continue.

Switch to Gitlab tab.

1. Log in to Gitlab with username ___ and password ___ (add instructions here).
1. Create a new merge request merging `feature_new_motd` to `main`.
8. When prompted, choose `merge when pipeline succeeds`.

✔️ **Result:** tbd.<br><br>

Approve deployment to Production
========
1. Switch to the CD4PE browser.
2. Notice that the `main` pipeline does not automatically push changes and code to the Development node groups and development branch in Gitlab.
3. Notice that the Development pipeline now runs triggered by the commit made from the `main` pipeline.
4. Review the Impact Analysis, and then approve the deployment to Production.(add steps here)

    Switch to the PE tab.

1. Log into Puppet Enterprise and navigate to (?).
1. Notice that there is no Job ID, as Eventual Consistency relies on normal Puppet runs to deploy your changes.

✔️ **Result:** tbd.<br><br>

-------
🎈 **Congratulations!** In this lab you...