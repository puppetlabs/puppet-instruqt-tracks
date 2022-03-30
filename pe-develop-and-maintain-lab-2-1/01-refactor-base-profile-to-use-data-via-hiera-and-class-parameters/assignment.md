---
slug: refactor-base-profile-to-use-data-via-hiera-and-class-parameters
id: ajxi4la6m5kq
type: challenge
title: Refactor the base profile to use data via Hiera and class parameters
teaser: Refactor the base profile by moving variables to class parameters so that
  you can reuse the profile in another role without having to duplicate code.
notes:
- type: text
  contents: |-
    In this lab you will:
     - Refactor the base profile by moving variables to class parameters so that you can reuse the profile in another role without having to duplicate the code.

     - Externalize the finance department's login message in Hiera by creating a **department** directory and **finance.yaml** file so that Hiera can find the parameterized login message. The .yaml file path maps to the pp_department="finance" trusted fact key-value pair.

     - Run a PQL query to find out which servers have their **pp_department** trusted fact set to **finance**, so that you know which nodes are affected when you put the Hiera data in place.

    In this example, the nodes with pp_department="sales" get the login message defined in the common.yaml file because no sales.yaml file exists in the hierarchy.

     Click **Start** when you are ready to begin.
tabs:
- title: Windows Agent
  type: service
  hostname: guac
  path: /#/client/c/winagent?username=instruqt&password=Passw0rd!
  port: 8080
- title: PE Console
  type: service
  hostname: puppet
  path: /
  port: 443
- title: Primary Server
  type: terminal
  hostname: puppet
- title: Linux Agent 1
  type: terminal
  hostname: nixagent1
- title: Linux Agent 3
  type: terminal
  hostname: nixagent3
- title: Lab Help Guide
  type: website
  url: https://puppet-kmo.gitbook.io/practice-lab-help/
difficulty: basic
timelimit: 1500
---
Create a control repo on your Windows development workstation
========
1. On the **Windows Agent** tab, from the **Start** menu, open **Visual Studio Code**.
2. Enable autosave so that you don't have to remember to save your changes. Click **File** > **Auto Save**.
3. Open the `C:\CODE` directory. Click **File** > **Open Folder**, navigate to the `C:\CODE` directory and click **Select Folder**.

    ✏️ **Note:** If prompted to trust the code in this directory, click **Accept**.<br><br>


4. Open a new terminal. Click **Terminal** > **New Terminal**.
5. In the VS Code terminal window, run the following command:
```
git clone git@gitea:puppet/control-repo.git
```

Create and move a variable in your base profile to a parameter block
========
1. Check out the **webapp** feature branch:
      ```
      cd control-repo
      git checkout webapp
      ```
2. Navigate to **control-repo** > **site-modules** > **profile** > **manifests** > **base.pp** and replace the contents with the following code:
    ```
    # profile/manifests/base.pp
    class profile::base (
      $login_message
    ){
      class { 'motd':
        content => $login_message,
    }
    }
    ```
3. Externalize the data in Hiera for the `finance` department:
   1. Navigate to **control-repo** > **data**.
   2. Right-click the **data** directory, click **New Folder**, and name the new folder **department**.
   3. Right-click the **department** folder, click **New File**, and name the new file **finance.yaml**.
   4. Copy the following contents into **finance.yaml**:
   ```
   # data/department/finance.yaml
   ---
   profile::base::login_message: 'WARNING: This server is monitored by SecOps.'
   ```
4. From the VS Code terminal window, commit, push, and deploy your code:

    ```
    git add .
    git commit -m "Parameterize login message for finance nodes"
    git push
    ```

Run Puppet on nodes returned by a PQL query
========
🔀  Switch to the **PE Console** tab.
1. Log into the PE console with username `admin` and password `puppetlabs`.
2. Navigate to the **Nodes** page. From the **Filter by** list, select **PQL Query**.
3. From the **Common queries** list, select **Nodes with a specific fact and fact value**.
4. Replace the query text with the following text:
    ```
    inventory[certname] { trusted.extensions.pp_department = "finance" }
    ```
5. Click **Submit query**.

    ✅ **Result:** The query returns one node.<br><br>

6. Click the node name link to open the node data page for the **finance** node.
7. Click **Run > Puppet**.
8. You will be redirected to the **Run Puppet** page. Select the following options:

      - **Environment**: Click **Select an environment for nodes to run in** and choose **webapp** from the list.<br><br>

9. Select the checkbox beside the node name to run the job on that node only.
10. Click **Run job** and wait for the job to finish.
✅ **Result:** The job fails. Click the report link at the right of the page and go to the **Log** tab to find out why.

Troubleshoot using the puppet lookup command
========
🔀 Switch to the **Primary Server** tab.
1. Troubleshoot the failure by running the `puppet lookup` command. Copy (but don't run) the following command to the Primary Server tab. Again, **do not run it yet**:
    ```
    puppet lookup profile::base::login_message --node <CERTNAME> --environment webapp --explain
    ```
    🔀 Switch to the **PE Console** tab.<br><br>

2. On the **Status** page, select and copy the node name.

    🔀 Switch to the **Primary Server** tab.<br><br>

3. Replace `<CERTNAME>` with the name of the failing node that you copied, and then run the command.

    ✅ **Result:** Read the failure message: The lookup command didn't find a login message in the base profile for the node.

Fix the Hiera data configuration
========
🔀 Switch to the **Windows Agent** tab.
1. Configure the required domain-level Hiera data. Navigate to **control-repo** > **hiera.yaml** and replace the existing code with the following code, which adds the department-specific yaml file to the Hiera lookup path:
    ```
    # <control-repo>/hiera.yaml
    ---
    version: 5
    hierarchy:
      - name: Yaml data
        datadir: data
        data_hash: yaml_data
        paths:
          - "nodes/%{trusted.certname}.yaml"
          - "department/%{trusted.extensions.pp_department}.yaml"
          - "common.yaml"
    ```
2. From the VS Code terminal window, push your new changes:
    ```
    git add .
    git commit -m "Edit hiera.yaml to support department facts"
    git push
    ```
    🔀 Switch to the **PE Console** tab.<br><br>

3. Run Puppet on the `finance` department node only:
    1. Navigate to the **Nodes** page.
    2. Click the node name link to open the node data page for the `finance` node.
    3. Click **Run > Puppet**.
    4. You will be redirected to the **Run Puppet** page. Select the following options:
        - **Environment**: Click **Select an environment for nodes to run in** and choose **webapp** from the list.
    5. Select the checkbox beside the node name to run the job on that node only.
    6. Click **Run job** and wait for job to finish.

        ✅ **Result:** In the log, notice that the job completed successfully.<br><br>

4. Run Puppet on the `sales` department node only:
    1. Navigate to the **Nodes** page.
    2. Click the node name link to open the node data page for the `sales` node.

        💡 **Tip:** You can find the `sales` department node by modifying the PQL query you ran previously:

        ```
        inventory[certname] { trusted.extensions.pp_department = "sales" }
        ```

    3. Click **Run > Puppet**.
    4. You will be redirected to the **Run Puppet** page. Select the following options:
        - **Environment**: Click **Select an environment for nodes to run in** and choose **webapp** from the list.
    5. Select the checkbox beside the node name to run the job on that node only.
    6. Click **Run job** and wait for the job to finish.

    ✅ **Result:** In the log, notice that the job failed.

    🔀 Switch to the **Windows Agent** tab.<br><br>

5. Navigate to **control-repo** > **data** > **common.yaml** and replace the existing content with the following required default data:
    ```
    # data/common.yaml
    ---
    profile::base::login_message: 'Welcome!'
    ```
6. From the terminal window, add, commit, and push your changes:
    ```
    git add .
    git commit -m "Add base profile login message to common.yaml"
    git push
    ```
    🔀 Switch to the **PE Console** tab.<br><br>

7. Run Puppet on the `sales` department node only:
    1. From the PE Console, navigate to the **Nodes** page.
    2. Click the node name link to open the node data page for the `sales` node.
        💡 **Tip:** You can find the `sales` department node by modifying the PQL query you ran previously:
        ```
        inventory[certname] { trusted.extensions.pp_department = "sales" }
        ```
    3. Click **Run > Puppet**.
    4. You will be redirected to the **Run Puppet** page. Select the following options:
        - **Environment**: Click **Select an environment for nodes to run in** and choose **webapp** from the list.
    5. Select the checkbox beside the node name to run the job on that node only.
    6. Click **Run job** and wait for the jobs to finish.

    ✅ **Result:** Notice that the jobs ran successfully.

---
## 🎈 **Congratulations!**
In this lab, you refactored the base profile by moving variables to class parameters so that you can reuse the profile in another role without having to duplicate the code.
