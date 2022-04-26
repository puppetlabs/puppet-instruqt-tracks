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
- title: workstation
  type: service
  hostname: guac
  path: /#/client/c/workstation?username=instruqt&password=Passw0rd!
  port: 8080
difficulty: basic
timelimit: 3600
---
Add a Deployment to the ‘main’ pipeline for the control-repo
========
1. On the **Windows Workstation** desktop, double-click the **CD4PE** shortcut.
    - If the browser window shows a connection privacy warning, bypass it by clicking **Advanced** > **Continue to cd4pe (unsafe)**.<br><br>
1. Log into CD4PE with username `puppet@puppet.com` and password `puppetlabs`.
    - If the browser isn't recognizing your keyboard input, copy and paste the username and password from these instructions.<br><br>
1. From the navigation menu, click **Control Repos**.

2. Edit the **main** pipeline to add a Pull Request trigger. Click...
3. Edit the **main** pipeline to include a new deployment. Click...
4. Edit the **Deployment** to use the **direct deployment** policy. Click...
5. Select the **Development** environment
6. Edit the **main** pipeline to include an Impact Analysis step for the **development** environment before the **deployment** step. Click...
7. Ensure the ‘Auto-Promote’ checkbox is NOT selected in the checkbox between the IA and Deployment

Create a new feature branch and use a Gitlab MR to trigger the ‘main’ pipeline
========
1. Login to the workstation
2. In VSCode in the ‘control-repo’ project run ‘git checkout -b feature_server
3. Add a new role server.pp that includes only the profile::base
4. Edit the base.pp profile to include a new notify resource
5. Edit the site.pp file so all servers get the role::server
6. Git add, commit and push the feature_server branch
7. Login to CD4PE to observe a successful pipeline run for the Regex ‘feature_’ branch

Create a Gitlab MR to run the Main pipeline
========
1. Login to Gitlab
2. In the ‘control-repo’ project click Merge Requests
3. Select the feature_server branch and create a MR to merge feature_server to main
4. When prompted click the ‘Merge when pipeline completes’ button

Inspect the ‘development’ environment impact analysis and promote pipeline to Deploy
========
1. Login to CD4PE
2. Select the ‘control-repo’ and click the New Events button
3. Observe the ‘main’ pipeline runs the unit tests and syntax checks and then runs the Impact Analysis
4. Once the IA runs notice the pipeline stops, it is waiting for a manual promotion to run the Deployment step
5. Click to inspect the IA output
6. Once satisfied with the output, click the Promote button next to the ‘main’ pipeline space between the IA step and the Deployment step
7. Observe the Deployment runs
8. Record the Job ID
9. Login to PE and click the Jobs menu
10. Look for the Job ID reported from CD4PE
11. Observe the changes to the nodes in the Development node group

--------
🎈 **Congratulations!** In this lab you...