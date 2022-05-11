---
slug: configure-module-pipeline
id: zh7rsvzlgxrc
type: challenge
title: Create a Module Pipeline
teaser: Put together a basic pipeline built for module testing and gain a familiarity
  with building pipelines.
notes:
- type: text
  contents: |
    In this lab you will put together a basic pipeline built for module testing and gain a familiarity with building pipelines. You will:

     - Create a module pipeline.
     - Create breaking changes to unit and syntax tests in order to test your pipeline.
     - Fix the breaking changes and then run your pipeline successfully.

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
Create a module pipeline
========

1. On the Windows Workstation desktop, double-click the CD4PE shortcut.
     - If the browser window shows a connection privacy warning, bypass it by clicking **Advanced** > **Continue to cd4pe (unsafe)**.<br><br>
1. Enter username `puppet@puppet.com` and password `puppetlabs`.
    - If the browser doesn't recognize your keyboard input, copy the username and password from these instructions.
    - To see the full CD4PE interface, expand the browser window to full-size.<br><br>
1. From the left navigation menu, navigate to **Code delivery** > **Modules**, and then click **Add module**.
1. For each field, enter the following:

    <u>Select a source</u>
      - Source: **Gitlab|puppet**
      - Repository: **module**
    <u>Select deployment branch</u>
      - Use this branch for deployments: **main**<br><br>

1. Assign the module a display name of **module**.
1. Click **Add Module**.
1. On the main Modules page, click the **Add Pipeline** icon:![add pipeline icon](https://storage.googleapis.com/instruqt-images/PE501-Continuously%20Deliver/Lab2.0-1-1.png)
1. In the modal pop-up, choose **Branch Regex**. In **Configure regex**, keep the default of `feature_.*`:![modal screenshot](https://storage.googleapis.com/instruqt-images/PE501-Continuously%20Deliver/Lab2.0-2-2.png)
1. Click **Add pipeline**, and then click **Done**. After returning to main modules page, observe that the branch name has changed to regex.![branch regex](https://storage.googleapis.com/instruqt-images/PE501-Continuously%20Deliver/Lab2.0-3-2.png)
1. Click **+Add default pipeline**.
✅   **Result:** A pipeline is created: ![pipeline created](https://storage.googleapis.com/instruqt-images/PE501-Continuously%20Deliver/lab2.0-pipeline-created.png)

Test your module pipeline
========

1. From the **Start** menu, open **Visual Studio Code**.<br><br>
    💡 **Tip:** Enable VS Code autosave by clicking **File** > **Auto Save**. By enabling autosave, you don't need to remember to save your changes as you work, ensuring your edits won't be lost.<br><br>

1. Open the `C:\CODE` directory. Click **File** > **Open Folder**, navigate to the `C:\CODE` directory, and click **Select Folder**.
1. In VS Code, open a terminal. Click **Terminal** > **New Terminal**.
1. In the VS Code terminal window, run the following command:
    ```
    git clone git@gitlab:puppet/module.git
    ```
1. Check out a new feature branch `feature_test` to use with the new regex pipeline:
    ```
    cd module
    git checkout -b feature_test
    ```

1. Push your new feature branch up to Gitlab:
    ```
    git commit --allow-empty -m "Initial branch commit"
    git push -u origin feature_test
    ```

1. Navigate to the CD4PE window and observe the pipeline job and failure output as it appears in the **Events** section at the bottom of the page. The first time you run these jobs, Docker downloads and builds the images on the back end. It will take a couple of minutes to get a full run. If nothing is showing, click **New Events** to see the running jobs: ![new events button](https://storage.googleapis.com/instruqt-images/PE501-Continuously%20Deliver/new-events.png)

✅   **Result:** The errors in the code have successfully (and temporarily!) broken the pipeline. Click **1 Failed** to see details about the job failure. ![pipeline failure](https://storage.googleapis.com/instruqt-images/PE501-Continuously%20Deliver/lab2.0-job-failure.png)

Fix the module repository code to run the pipeline successfully
========

1. Switch back to the VS Code window to fix the syntax.  Run the following command in the terminal to automatically correct the syntax errors:
    ```
    pdk validate --auto-correct
    ```
1. In the VS Code terminal window, commit and push your code to your feature branch:
    ```
    git add .
    git commit -m "Autocorrect syntax and style errors"
    git push
    ```
1. Switch back to the CD4PE browser window. Click the **New Events** button if it appears.
1. Observe pipeline success.

✅   **Result:** You fixed the errors in the code and now the pipeline works as expected.

----------

🎈 **Congratulations!**

You created a module pipeline, intentionally broke the unit and syntax tests to show the pipeline executing, and then fixed your code to run the pipeline successfully. When you are finished with this lab, click **Next**.