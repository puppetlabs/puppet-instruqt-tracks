---
slug: configure-a-control-repo-pipeline
id: nchvmmpwwi6q
type: challenge
title: Configure a Control Repo Pipeline
teaser: Configure a Control Repo Pipeline
notes:
- type: text
  contents: Configure a Control Repo Pipeline
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
timelimit: 14400
---
# Configure a Control Repo Pipeline

In this lab you are going to configure pipelines for your control-repo in order to automate the syntax checks of your code changes and introduce a new job type to additionally run unit tests. You have already configured the integrations with PE and Source Control, now you can configure the some basic pipelines for a control-repo project.


## Configure default control-repo pipelines
1. Double-click on the **CD4PE** shortcut on the desktop.
1. Log in to CD4PE with username `puppet@puppet.com` and password `puppetlabs`.
1. Click **Control Repos** from the navigation menu and click the **Add control repo** button.
1. Select **Gitlab | puppet** in the **SOURCE** dropdown.
1. Select **control-repo** in the **REPOSITORY** dropdown.
1. Select **Create a main branch...** in the **Select deployment branch** radio button group.
1. Select **production** in the **BASE NEW MAIN BRANCH ON** dropdown.
1. Click the **Add control repo** button.
1. Make sure that **main** is selected in the **Pipelines** dropdown and click the **+ Add default pipeline** button.
1. Click the **Manage pipelines** link, deselect the **Commit** trigger checkbox and select the **PullRequest** checkbox. Click **Save Settings** and **Done**.
1. Click the `add pipeline` icon (plus sign), select the **Branch regex** radio button, click **Add pipeline** and click **Done**.
1. Click the **+ Add default pipeline** button.
1. Click the **Manage pipelines** link, make sure the **Commit** trigger checkbox is selected and the **PullRequest** checkbox is deselected. Click **Save Settings** and **Done**.

## Test the default pipelines
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

1. Open the **control-repo** > **manifests** > **site.pp** file in VS Code and add a comment line to the file.
1. Commit your change and push to the remote repository:
    ```
    git add .
    git commit -m "Added some commenting to site.pp"
    git push origin feature_test
    ```
1. Switch back to the CD4PE browser window and check the events for the regex pipeline on the control-repo. Click the **New Events** button if needed.
1. The jobs may be in a **PENDING** state and you can click into any of them to view their progress after clicking the down arrow icon to expand the list.
1. There may be a delay for the jobs to complete the first time they are executed, but eventually they should end in the **COMPLETED** state.

## Add a unit test job type
1. Click **Jobs** in the leftside navigation bar and click **New job**.
1. Enter **control-repo-rspec-puppet** in the **NAME** field and the command **cd site-modules/profile && pdk test unit** in the **Job commands** text area.
1. Select **Run on puppet hardware**, select **docker** until **Hardware capabilities** and click **Apply**.
1. Select **Run this job in a Docker container** toggle button, keep the other defaults and click **Save job**.
1. Click **Control Repos** in the leftside navigation bar and click **control-repo**.
1. Select the **main** pipeline in the **Pipelines** dropdown and click the 3 dots next to the **Code Validation stage** header.
1. Select **Add a stage after**.
1. Enter **Run unit tests** in the **STAGE NAME** text box.
1. Select **Jobs** in the **SELECT ITEM** dropdown. Select the **control-repo-rspec-puppet** job, click **Add stage** and click **Done**.
1. Repeat the same steps for the **regex** pipeline.

## Test the unit test job stage in your Regex Pipeline
1. Switch back to the VS Code window
1. Add basic unit tests in the control-repo code and push to the `feature_` branch
1. Login to CD4PE
1. Click the events button for the `control-repo`

Observe a new run of the Regex pipeline with successful syntax checking and unit tests