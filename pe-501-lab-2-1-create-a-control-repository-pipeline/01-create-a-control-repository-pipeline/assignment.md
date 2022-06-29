---
slug: create-a-control-repository-pipeline
id: nchvmmpwwi6q
type: challenge
title: Create a control repository pipeline
teaser: Set up a control repo, and then set up a main and regexp pipeline for that
  control repo.
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
timelimit: 3300
---
Configure default control repo pipelines
========
1. On the **Windows Workstation** desktop, double-click the **CD4PE** shortcut.
    - If the browser window shows a connection privacy warning, bypass it by clicking **Advanced** > **Continue to cd4pe (unsafe)**.<br><br>
1. Log into CD4PE with username `puppet@puppet.com` and password `puppetlabs`.
    - If the browser isn't recognizing your keyboard input, copy and paste the username and password from these instructions.
    - To see the full CD4PE interface, expand the browser window to full-size.<br><br>
1. From the navigation menu, click **Control Repos**, and then click **Add control repo**.<br><br>
1. For each field, enter the following:

    <u>Select a source</u>
      - Source: **Gitlab|puppet**
      - Repository: **control-repo**
    <u>Select deployment branch</u>
      - Choose the **Create a main branch from an existing branch** option.
      - Base new main branch on: **production**<br><br>

1. Click **Add control repo**.<br><br>
1. Make sure that **main** is selected in the **Pipelines** dropdown and then click **+ Add default pipeline**.<br><br>
1. Click **Manage pipelines**.<br><br>
1. In the modal that opens, deselect the **Commit** trigger checkbox, and then select **PullRequest**. Click **Save Settings** and then click **Done**.<br><br>
1. On the main page, click the **Add Pipeline** icon:![add pipeline icon](https://storage.googleapis.com/instruqt-images/PE501-Continuously%20Deliver/Lab2.0-1-1.png)
1. In the modal that opens, select the **Branch regex** radio button, click **Add pipeline** and then click **Done**.<br><br>
1. Click **+ Add default pipeline**.<br><br>
1. Click **Manage pipelines**. Make sure that the **Commit** trigger checkbox is selected and that the **PullRequest** checkbox is deselected. Click **Save Settings** and then click **Done**.

    ✅ **Result:** A default control repo pipeline is created: ![pipeline created](https://storage.googleapis.com/instruqt-images/PE501-Continuously%20Deliver/lab2.1-pipeline-created.png)


Test the default pipelines
========
1. From the **Start** menu, open **Visual Studio Code**.<br><br>
1. Open the `C:\CODE` directory. Click **File** > **Open Folder**, navigate to the `C:\CODE` directory and click **Select Folder**.<br><br>
1. If prompted to trust the code in this directory, click **Accept**.<br><br>
1. In VS Code, open a terminal. Click **Terminal** > **New Terminal**.<br><br>
1. In the VS Code terminal window, run the following commands:

        git clone git@gitlab:puppet/control-repo.git
        cd control-repo
        git checkout -b feature_test

1. Commit your change and push to the remote repository:
    ```
    git commit --allow-empty -m "Initial branch commit"
    git push -u origin feature_test
    ```
1. Switch back to the CD4PE browser window and check the events for the regex pipeline on the control-repo. If nothing is happening, click the **New Events** button.<br><br>
1. The jobs may be in a **PENDING** state. Click the down-arrow icon to expand the list and then click into any of them to view their progress.<br><br>
1. There may be a delay for the jobs to complete the first time they are run, but after 2-3 minutes they should end in the **SUCCEEDED** state.
    ![code validation succeeded](https://storage.googleapis.com/instruqt-images/PE501-Continuously%20Deliver/Lab3.0-code-validation-succeeded.png)

    ✅ **Result:** The jobs run successfully.<br><br>

Add a unit test job type
========
1. In the left-hand navigation bar, click **Jobs** and then click **New job**.
    - If the **New job** button isn't not showing up, expand the CD4PE browser window.<br><br>
1. Enter the following:
    - **NAME**: **control-repo-onceover-show-puppetfile**
    - **Job commands**: `bundle exec onceover init && bundle exec onceover show puppetfile`
    - Select **Run on puppet hardware**.
    - For **Hardware capabilities**, select **docker** and then click **Apply**.
    - Toggle the option for **Run this job in a Docker container**. Leave the other settings as-is and then click **Save job**.<br><br>
1. In the left-hand navigation bar, click **Control Repos** and then click **control-repo**.<br><br>
1. In the **Pipelines** dropdown, select the **regex** pipeline:![regex pipeline](https://storage.googleapis.com/instruqt-images/regex-pipeline.png)


1. Click the ellipsis beside the **Code Validation stage** header:![3 dots](https://storage.googleapis.com/instruqt-images/PE501-Continuously%20Deliver/Lab3.0-3-dots.png)

1. Select **Add a stage after**.<br><br>
1. Enter the following:
    - In the **STAGE NAME** field, enter **Show Puppetfile module versions**.
    - From the **SELECT ITEM** dropdown, select **Jobs**.
    - Select the **control-repo-onceover-show-puppetfile** job, click **Add stage**, and then click **Done**.<br><br>
1. Repeat steps 4-7 for the **main** pipeline. Even though you won't trigger the main pipeline in this lab, other PE501 labs need this job in the main pipeline.

    ✅ **Result:** A unit test job type is created for both the **main** and **regex** pipelines: ![unit tests created](https://storage.googleapis.com/instruqt-images/PE501-Continuously%20Deliver/lab2.1-run-unit-tests-job.png)

Test the unit test job stage in your regex pipeline
========
1. Switch back to the VS Code window.<br><br>
1. Commit your change and push to the remote repository:
    ```
    git commit --allow-empty -m "Trigger Puppetfile show modules job"
    git push
    ```
1. Switch back to the CD4PE browser window and check the events for the regex pipeline on the control repo. Click the **New Events** button if it appears.<br><br>
1. The jobs may be in a **PENDING** state. To view their progress, click the down-arrow icon to expand the list and then click into any of them.<br><br>
1. Observe a new run of the regex pipeline jobs with the new custom job that displays the Puppetfile module statuses.
    ![unit tests successful](https://storage.googleapis.com/instruqt-images/PE501-Continuously%20Deliver/Lab3.0-run-unit-tests.png)

    ✅ **Result:** The unit test jobs run successfully.<br><br>

--------------
🎈 **Congratulations!** You set up a control repo and added the main and regex pipelines to it. Then, you tested the pipelines to make sure they work as expected.

When you are finished with this lab, click **Next**.