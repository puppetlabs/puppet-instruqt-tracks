---
slug: deploy-to-production-with-impact-analysis
id: hhyo5oaxazf5
type: challenge
title: Deploy to Production with Impact Analysis
teaser: Deploy to Production with Impact Analysis
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
timelimit: 3600
---
Protect the production environment
========
1. On the **Windows Workstation** desktop, double-click the **CD4PE** shortcut.
    - If the browser window shows a connection privacy warning, bypass it by clicking **Advanced** > **Continue to cd4pe (unsafe)**.<br><br>
1. Log into CD4PE with username `puppet@puppet.com` and password `puppetlabs`.
    - If the browser isn't recognizing your keyboard input, copy and paste the username and password from these instructions.<br><br>
2. Navigate to **Settings** > **Puppet Enterprise**.
3. In the **Protected Envs** column click the `0`.
    - You may need to expand the CD4PE browser window to see the columns clearly.<br><br>
1. In the modal that opens, click **Add**. Then, select **Production environment** and toggle the switch to choose  **Administrators** for the approval role. ![designate approval](https://storage.googleapis.com/instruqt-images/PE501-Continuously%20Deliver/PE501-designate-approval.png)
1. Click **Add**, and then click **Done**.
1. Close the modal, return to the Puppet Enterprise settings page, and review the **Protected environments** column, which now shows one protected environment: ![protected environment](https://storage.googleapis.com/instruqt-images/PE501-Continuously%20Deliver/PE501-protectedenv.png)

    ✔️ **Result:** The **production** environment is now protected.<br><br>

Create a new pipeline to run on the Development environment
========
1. In the left-hand sidebar, navigate to **Control Repos** > **control-repo**.
2. Add a new pipeline to run on the **Development** environment. Click the **Add Pipeline** icon:![add pipeline icon](https://storage.googleapis.com/instruqt-images/PE501-Continuously%20Deliver/Lab2.0-1-1.png)
1. In the modal that opens, select **Development**, click **Add pipeline**, and then click **Done**.
3. Configure the pipeline to run triggered by a merge request. With the **development** pipeline showing in the dropdown list, click... (add steps here)
4. Add the unit test step to the Code Validation stage. (add steps here)
5. Add an Impact Analysis stage for the Production environment. (add steps here)
6. Add a deployment step using the Eventual Consistency policy to the Production environment. (add steps here)
7. Make sure the promotion to the deployment step requires manual promotion. (add steps here)

✔️ **Result:** tbd.<br><br>

Edit the Main pipeline to automatically deploy to Development
========
1. Edit the **main** pipeline. (add steps here)
2. Select **Auto-Approve** (between the IA step and Deployment step).

✔️ **Result:** tbd.<br><br>

Merge the feature_new_motd branch to the main branch
========
1. On the workstation in the **control-repo** project run
        ```
        git checkout main
        ```
        ```
        git checkout -b feature_new_motd
        ```
2. Open `common.yaml` file (filepath) and edit it to include a new string for message of the day.
4. Git add, commit and push origin feature_new_motd:
        ```
        (insert command here)
        ```
5. Merge to main. (add steps here)
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