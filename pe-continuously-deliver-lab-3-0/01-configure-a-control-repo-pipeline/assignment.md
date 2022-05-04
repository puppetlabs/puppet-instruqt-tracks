---
slug: configure-a-control-repo-pipeline
id: nchvmmpwwi6q
type: challenge
title: Configure a Control Repo Pipeline
teaser: Set up a control repo, and then set up a main and regexp pipeline for the
  control repo you built.
notes:
- type: text
  contents: |-
    In this lab you will:

     - Set up a control repo to work with, and then set up a main and regexp pipeline for the control repo.

     Click **Start** when you are ready to begin.
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
Configure default control repo pipelines
========
1. On the **Windows Workstation** desktop, double-click the **CD4PE** shortcut.
    - If the browser window shows a connection privacy warning, bypass it by clicking **Advanced** > **Continue to cd4pe (unsafe)**.<br><br>
1. Log into CD4PE with username `puppet@puppet.com` and password `puppetlabs`.
    - If the browser isn't recognizing your keyboard input, copy and paste the username and password from these instructions.
    - To see the full CD4PE interface, expand the browser window to full-size.<br><br>
1. From the navigation menu, click **Control Repos**, and then click **Add control repo**.
1. For each field, enter the following:

    <u>Select a source</u>
      - Source: **Gitlab|puppet**
      - Repository: **control-repo**
    <u>Select deployment branch</u>
      - Choose the **Create a main branch from an existing branch** option.
      - Base new main branch on: **production**<br><br>

1. Click **Add control repo**.
1. Make sure that **main** is selected in the **Pipelines** dropdown and then click **+ Add default pipeline**.
1. Click **Manage pipelines**.
1. In the modal that opens, deselect the **Commit** trigger checkbox, and then check the box for **PullRequest**. Click **Save Settings** and then click **Done**.
1. On the main page, click the **Add Pipeline** icon:![add pipeline icon](https://storage.googleapis.com/instruqt-images/PE501-Continuously%20Deliver/Lab2.0-1-1.png)
1. In the modal that opens, select the **Branch regex** radio button, click **Add pipeline** and then click **Done**.
1. Click **+ Add default pipeline**.
1. Click **Manage pipelines**. Make sure that the **Commit** trigger checkbox is selected and that the **PullRequest** checkbox is deselected. Click **Save Settings** and then click **Done**.

✅ **Result:** A default control repo pipeline is created.<br><br>

Test the default pipelines
========
1. From the **Start** menu, open **Visual Studio Code**.
1. Enable autosave so that you don't have to remember to save your changes. Click **File** > **Auto Save**.
1. Open the `C:\CODE` directory. Click **File** > **Open Folder**, navigate to the `C:\CODE` directory and click **Select Folder**.
1. If prompted to trust the code in this directory, click **Accept**.
1. In VS Code, open a terminal. Click **Terminal** > **New Terminal**.
1. In the VS Code terminal window, run the following commands:

        cd code
        git clone git@gitlab:puppet/control-repo.git
        cd control-repo
        git checkout -b feature_test

1. Open `site.pp` (**control-repo** > **manifests** > **site.pp**) in VS Code and add a comment line to the file.
1. Commit your change and push to the remote repository:
    ```
    git add .
    git commit -m "Added some commenting to site.pp"
    git push origin feature_test
    ```
1. Switch back to the CD4PE browser window and check the events for the regex pipeline on the control-repo. If nothing is happening, click the **New Events** button.
1. The jobs may be in a **PENDING** state. Click the down-arrow icon to expand the list and then click into any of them to view their progress.
1. There may be a delay for the jobs to complete the first time they are executed, but eventually they should end in the **SUCCEEDED** state.
    ![code validation succeeded](https://storage.googleapis.com/instruqt-images/PE501-Continuously%20Deliver/Lab3.0-code-validation-succeeded.png)

✅  **Result:** The jobs run successfully.<br><br>

Add a unit test job type
========
1. In the left-hand navigation bar, click **Jobs** and then click **New job**.
    - If the **New job** button isn't not showing up, expand the CD4PE browser window.
1. Enter the following:
    - **NAME**: **control-repo-onceover-show-puppetfile**
    - **Job commands**: `bundle exec onceover init && bundle exec onceover show puppetfile`<br><br>
1. Select **Run on puppet hardware**.
1. For **Hardware capabilities**, select **docker** and then click **Apply**.
1. Toggle the option for **Run this job in a Docker container**. Leave the other settings as-is and then click **Save job**.
1. In the left-hand navigation bar, click **Control Repos** and then click **control-repo**.
1. In the **Pipelines** dropdown, select the **main** pipeline:![main branch](https://storage.googleapis.com/instruqt-images/PE501-Continuously%20Deliver/Lab3.0-main-branch.png)

1. Click the 3 dots next to the **Code Validation stage** header:![3 dots](https://storage.googleapis.com/instruqt-images/PE501-Continuously%20Deliver/Lab3.0-3-dots.png)

1. Select **Add a stage after**.
1. In the **STAGE NAME** field enter **Run unit tests**.
1. From the **SELECT ITEM** dropdown, select **Jobs**.
1. Select the **control-repo-onceover-show-puppetfile** job, click **Add stage** and then click **Done**.
1. Repeat the same steps for the **regex** pipeline.

✅  **Result:** A unit test job type is created.<br><br>

Test the unit test job stage in your Regex Pipeline
========
1. Switch back to the VS Code window.
1. Open `site.pp` (**control-repo** > **manifests** > **site.pp**) and add a comment line somewhere in the file.
1. Commit your change and push to the remote repository:
    ```
    git add .
    git commit -m "Added some commenting to site.pp"
    git push origin feature_test
    ```
1. Switch back to the CD4PE browser window and check the events for the regex pipeline on the control repo. Click the **New Events** button if needed.
1. The jobs may be in a **PENDING** state. To view their progress, click the down-arrow icon to expand the list and then click into any of them.
1. Observe a new run of the regex pipeline jobs with the new custom job that displays the Puppetfile module statuses.
    ![unit tests successful](https://storage.googleapis.com/instruqt-images/PE501-Continuously%20Deliver/Lab3.0-run-unit-tests.png)
✅  **Result:** The unit test jobs run successfully.<br><br>

--------------
🎈 **Congratulations!** You set up a control repo and then added main and regexp pipelines to it, before finally testing the pipelines to ensure they work as expected.

To close this lab, click **Next**.