---
slug: configure-cd4pe
id: 5o3kmcd5aj3c
type: challenge
title: Configure Continuous Delivery for PE
teaser: Before you can build your continuous delivery pipelines, you must configure
  integrations with Puppet Enterprise and source control.
notes:
- type: text
  contents: |-
    In this lab, you will configure the Continuous Delivery for PE integrations you need to build your pipelines. You will:

     - Create a user and a workspace.
     - Configure integration with PE.
     - Configure integration with source control:
        - Integrate PE.
        - Integrate source control.
        - Add a job hardware node.

     Click **Start** when you're ready to begin.
tabs:
- title: PE Console
  type: service
  hostname: puppet
  port: 443
- title: PE Server
  type: terminal
  hostname: puppet
- title: Windows Workstation
  type: service
  hostname: guac
  path: /#/client/c/workstation?username=instruqt&password=Passw0rd!
  port: 8080
- title: CD4PE-Host
  type: terminal
  hostname: cd4pe-host
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
Create a Continuous Delivery user and user role in PE
========
You'll use this user and role to generate the PE authentication token required during the setup process and to view a centralized log of the activities Continuous Delivery for PE completes on your behalf.

<u>Create a Continuous Delivery user</u>
1. Log into the console with username `admin` and password `puppetlabs`.
1. Navigate to **Admin** > **Access Control**.
1. In the **Full name** field, enter `CD4PE User`.
1. In the **Login** field, enter `cd4pe_user`, and then click **Add local user**.
1. Click the new `CD4PE User` link in the list below.
1. In the top right corner, click **Generate password reset**.
1. Copy the password reset link into a new browser tab.
1. Enter the password `puppetlabs` in the new password box and click **Reset password**.
1. Close the tab, close the password reset box, and return to the PE console.

<u>Set the user's role and permissions</u>
1. Under the **User roles** tab, click **Manage roles**.
1. In the **Name** field, enter `CD4PE`. In the **Description** field, enter `CD4PE role`, and then click **Add role**.
1. Click the new `CD4PE` link in the list of roles below.
1. From the **User name** list, select `CD4PE User`, click **Add user**, and then click **Commit 1 change**.
1. Click the **Permissions** tab and add the following required permissions to the role (after selecting the options, click **Add** to set each permission):
    - **Job orchestrator:** Start, stop and view jobs.
    - **Node groups:** Create, edit, and delete child groups, All.
    - **Node groups:** Edit configuration data, All.
    - **Node groups:** Set environment, All.
    - **Node groups:** View, All.
    - **Nodes:** View node data from PuppetDB.
    - **Puppet agent:** Run Puppet on agent nodes.
    - **Puppet environment:** Deploy code, All.
    - **Puppet Server:** Compile catalogs for remote nodes.
    - **Tasks:** Run tasks, `cd4pe_jobs::run_cd4pe_job`.<br><br>
16. Click **Commit 10 changes** at the bottom right.

✅ **Result:** The system creates the CD4PE user and role.

Configure Code Manager in PE
========
You must enable and configure Code Manager to enable Continuous Delivery for PE to initiate code deployments as part of a pipeline job run.

1. On the **PE Server** tab, create an SSH key:
    ```
    ssh-keygen -t ed25519 -C "root@puppet" -f /etc/puppetlabs/puppetserver/ssh/id_ed25519 -q -P ""
    ```

    🔀  Switch to the Windows workstation tab<br><br>

2. On the desktop, double-click the **Gitlab** browser shortcut.
3. For username, enter `puppet`. For password, enter `puppetlabs`.
    - If prompted to save the password, choose either option.<br><br>
4. In the top right corner, click the circular icon dropdown, and then click **Preferences**. ![drop-down button](https://storage.googleapis.com/instruqt-images/drop-down-icon.png)

5. In the icon menu at the left, click the upper key icon (for SSH keys). ![key icon](https://storage.googleapis.com/instruqt-images/key-top.png)

6. Copy the contents of the `id_ed25519.pub` file generated in the first step into the **Key** text area.
    - To find the contents, return to the PE Server tab and run the following:
        ```
        cat /etc/puppetlabs/puppetserver/ssh/id_ed25519.pub
        ```
    - Note the generated title, and select an expiration date in the future. Click **Add key**.<br><br>
7. Navigate to **Menu** > **Projects** > **Your projects**, and then click **puppet/control-repo**. ![menu projects with outlines](https://storage.cloud.google.com/instruqt-images/menu-projects-your-projects-amber.png)
8. Click the **Clone** dropdown, and then click the copy icon to the right of **Clone with SSH**. ![clone dropdown menu](https://storage.googleapis.com/instruqt-images/git-clone-amber-2.png)
 🔀 Switch to the PE Console tab<br><br>

9. Navigate to **Node groups**.
9. Click the plus (**+**) icon to the left of **PE Infrastructure** to expand the group, and then click **PE Master**.
9. Click the **Classes** tab and scroll to the bottom to find the **puppet_enterprise::profile::master** class.
10. For this class, set the following (click **Add to node group** to set each parameter):<br>
    **code_manager_auto_configure**:
    ```
    true
    ```
    **r10k_remote**:
    ```
    git@gitlab:puppet/control-repo.git
    ```
    **r10k_private_key**:
    ```
    /etc/puppetlabs/puppetserver/ssh/id_ed25519
    ```
11. Click **Commit 3 changes**.

    🔀 Switch to the **PE Server** tab<br><br>

12. To configure Code Manager, run `puppet agent -t` twice. Each run should take about 1-2 minutes.

✅ **Result:** Code Manager is enabled and configured. Continuous Delivery for PE can now initiate code deployments as part of a pipeline job run.

Integrate Continuous Delivery for PE with Puppet Enterprise
========

🔀 Switch to the Windows Workstation tab

1. On the desktop, double-click the **CD4PE** shortcut.
    - If the browser window shows a connection privacy warning, bypass it by clicking **Advanced** > **Continue to cd4pe (unsafe)**.
1. From the CD4PE login screen, click **Create an account**, then enter your information (remember the username and password you enter - you will need it later on), then click **Sign Up**.
    - To see the full interface, maximize the browser window.
2. On the next screen, click **+ Add new workspace**. Call it **Puppet** and then click **Create workspace**.
3. You'll be logged as your new user and will arrive at your main Workspace page. Under the **Set up Continuous Delivery for PE** header at the top, notice the steps listed. You will complete those steps next.

<u>Integrate Puppet Enterprise</u>

1. Click **Integrate Puppet Enterprise**, and then click **Add credentials**.
2. In the next window, set the following:
    - In the **Name** field, enter **Puppet Server**.
    - For the **Puppet Enterprise console address**, enter **https://puppet**.
    - Keep **Basic authorization** selected.
    - For **Puppet Enterprise username**, enter `cd4pe_user`.
    - For **Puppet Enterprise password**, enter `puppetlabs`.
3. Click **Save Changes**, and on the confirmation screen, click **Close**.
✅ **Result:** Puppet Enterprise is integrated.

<u>Integrate source control</u>

1. Click **Integrate source control**.
1. Click **GitLab**. In the **Host** field, enter **http://gitlab/**.
1. Switch to the **GitLab** tab in your browser and select **Settings** > **Access Tokens** from the left side navigation bar:![gitlab settings button](https://storage.googleapis.com/instruqt-images/PE501-Continuously%20Deliver/gitlab-settings-button.png)

1. In the **Token name** text box, enter **CD4PE**.
1. Choose an expiration date in the future, select **Maintainer** as the role, and then select all of the available scopes. Click **Create project access token**.
1. The page will automatically refresh and the project access token will be shown on the next page. Copy it by clicking the clipboard copy icon.
1. Switch to the **CD4PE** browser tab and paste the new token into the **Token** field.
1. Select **Clone via HTTP(S)** and then click **Add credentials**. After the credentials have been added, click **Done**.
✅ **Result:** Source control is integrated.

<u>Add a job hardware node</u>

1. Click **Set up job hardware**.
2. Click **+ Edit**.
3. From the **Puppet Enterprise Server** list, select the server you previously added (**Puppet-Server**) and then select the check box to the left of the node that begins with **CD4PE**.
4. Click **Save**, and then click **Done**.
✅ **Result:** A job hardware node has been added.

----------

🎈 **Congratulations!** You configured the necessary integrations for Continuous Delivery for PE! To learn how to add a control repository and configure a pipeline, continue to the next lab. Or, you can spend some time exploring this environment. When you are finished with this lab, click **Next**.