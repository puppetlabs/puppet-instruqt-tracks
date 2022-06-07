---
slug: hiera-and-puppet-lookup
id: pjzdkzqxxmfh
type: challenge
title: Use the Puppet lookup command on the primary server
teaser: Discover how Hiera looks for data based on the hiera.yaml configuration and
  node facts.
notes:
- type: text
  contents: |-
    In this lab you will use the `puppet lookup` command on your primary server to discover how Hiera looks for data based on your hiera.yaml configuration and your node facts.

    Click **Start** when you are ready to begin.
tabs:
- title: Windows Agent
  type: service
  hostname: guac
  path: /#/client/c/winagent?username=instruqt&password=Passw0rd!
  port: 8080
- title: Primary Server
  type: terminal
  hostname: puppet
- title: PE Console
  type: service
  hostname: puppet
  path: /
  port: 443
- title: Lab Help Guide
  type: website
  url: https://puppet-kmo.gitbook.io/practice-lab-help/
difficulty: basic
timelimit: 2400
---
Clone the control repo on your Windows development workstation
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
6. Check out the feature branch `webapp` to inspect some preconfigured Hiera data:
    ```
    cd control-repo
    git checkout webapp
    ```

Run the puppet lookup command to identify the login message for each node
========
🔀 Switch to the **Primary Server** tab.
1. Copy (but don't run) the following `puppet lookup` command into the Primary Server window. Again, **do not run the command yet**:
    ```
    puppet lookup profile::base::login_message --node <NODENAME> --environment webapp --explain
    ```
    🔀 Switch to the **PE Console** tab.<br><br>

2. Log into the PE console with username `admin` and password `puppetlabs`.
3. Navigate to the **Status** page, and then highlight and copy a node name.

    🔀 Switch to the **Primary Server** tab.<br><br>

4. On the Primary Server tab, replace **`<NODENAME>`** in the command with the name of the node you just copied, and then run the command on the selected node.
5. Review the login message in the output:
    `Found key: "profile::base::login_message" value: "<LOGIN MESSAGE HERE>"`

6. Repeat steps 1-5, replacing `<NODENAME>` with the name of the other node.

    ✅ **Result:** Review the output. Notice how it differs from the output for the previous node.

Run the puppet lookup command to identify other information for each node
========
1. Copy (but don't run) the following `puppet lookup` command into the Primary Server window. Again, **do not run the command yet**:
    ```
    puppet lookup profile::ntp::servers --node <NODENAME> --environment webapp --explain
    ```
    🔀 Switch to the **PE Console** tab.<br><br>

2. In the PE console, navigate to the **Status** page, and then highlight and copy a node name.

    🔀 Switch to the **Primary Server** tab.<br><br>

3. On the Primary Server tab, replace **`<NODENAME>`** in the command with the name of the node you just copied.
4. Run the command on the selected node and review the output.
5. Repeat steps 1-4, replacing `<NODENAME>` with the name of the other node, and then review the output. Notice how it differs from the output of the previous node.

    🔀 Switch to the **Windows Agent** tab.<br><br>

6. Review the contents of files at the following locations:
     - **control-repo** > **hiera.yaml**
     - **control-repo** > **data** > **datacenter**
     - **control-repo** > **data** > **department**

 ✅ **Result:** Verify the hierarchy of the contents in these files against the `puppet lookup` command output.

Identify which facts affected the lookup
========
🔀 Switch to the **Primary Server** tab.

1. Run the following `puppet query` command to check the facts that are used in the hierarchy of the `hiera.yaml` configuration file for all of your nodes:
    ```
    puppet query 'facts[certname,value] { name = "trusted" }'
    ```

    ✅ **Result:** Review the trusted facts and notice whether all facts are present on both nodes.

---
## 🎈 **Congratulations!**
In this lab, you used the `puppet lookup` command on the primary server to discover how Hiera looks for data based on the `hiera.yaml` configuration and node facts.