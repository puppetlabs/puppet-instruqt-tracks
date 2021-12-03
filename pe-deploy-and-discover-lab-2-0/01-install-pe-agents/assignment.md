---
slug: install-pe-agents
id: yn5tswpkuyaq
type: challenge
title: Install Puppet agents
teaser: Install the Puppet agent by using both the local and remote installation methods.
notes:
- type: text
  contents: |-
    In this lab, you will:

    * Install an agent locally on a node by using the agent installation script.
    * Install an agent remotely on a node by using the PE console.
    * For both methods, sign the new agent certificate by using the console.


    Click **Start** when you're ready to begin.
tabs:
- title: PE Console
  type: service
  hostname: puppet
  port: 443
- title: Linux Agent
  type: terminal
  hostname: nixagent
- title: Windows Agent
  type: service
  hostname: guac
  path: /#/client/c/winagent?username=instruqt&password=Passw0rd!
  port: 8080
- title: Lab Aid
  type: website
  hostname: guac
  url: https://puppet-kmo.gitbook.io/lab-aids/-MZKPjwKRKKFuXxxy7ge/pe101/install-puppet-agents
difficulty: basic
timelimit: 3599
---
<a name="linux"><img src="https://storage.googleapis.com/instruqt-images/install-local-linux.png"></a>

## Run the agent installation script from the node’s command line.

1. Log into the PE console with username `admin` and password `puppetlabs`.

1. From the console sidebar, navigate to the **Nodes** page.

1. In the upper-right corner, click **Add Nodes**.

1. On the **Add nodes to inventory** page, click **Install Agents**.

1. Copy the curl command shown in the ***nix nodes** field at the right of the console.<br><br>💡 **Tip:** Select the text and right-click to copy.

1. ![swtich tabs](https://storage.googleapis.com/instruqt-images/Instruct%20Icons/icon_switch_tabs_white_32.png) Switch to the **Linux Agent** tab. Then, paste and run the curl command.<br><br>✔️ **Result:** This command installs the Puppet agent.

1. ![swtich tabs](https://storage.googleapis.com/instruqt-images/Instruct%20Icons/icon_switch_tabs_white_32.png) Switch back to the **PE Console** tab when the installation is complete.

1. Click **Refresh** at the top right of the console.

1. Now you have to sign the agent's certificate. From the console sidebar, navigate to the **Certificates** page and click the **Unsigned certificates** tab.

1. In the list of nodes, find the node name containing `nixagent` and click **Accept**.

1. ![swtich tabs](https://storage.googleapis.com/instruqt-images/Instruct%20Icons/icon_switch_tabs_white_32.png) Switch back to the **Linux Agent** tab.

1. Trigger a Puppet run:<br><br>
     ```
     puppet agent -t
     ```

13. ![swtich tabs](https://storage.googleapis.com/instruqt-images/Instruct%20Icons/icon_switch_tabs_white_32.png) Switch back to the **PE Console** tab.

14. From the console sidebar, navigate to the **Nodes** page. Click the node name containing `nixagent`.

1. On the **Facts** tab, inspect the facts about the `nixagent` node.

<br>🎈 **Congratulations!**  You installed Puppet agents locally from the command line on Linux. Continue below to learn how to install the agent from the PE console using Windows.

---


<a name="windows"><img src="https://storage.googleapis.com/instruqt-images/install-remote-windows.png"></a>

## Install the agent from the PE console.

1. ![swtich tabs](https://storage.googleapis.com/instruqt-images/Instruct%20Icons/icon_switch_tabs_white_32.png) Switch to the **PE Console** tab if needed.

2. From the console sidebar, navigate to the **Nodes** page. In the upper-right corner, click **Add Nodes**.

3. On the **Add nodes to inventory** page, click **Install Agents**.

4. From the **Transport method** list, select **WinRM**. Enter the following information:

     - WinRM hosts: `winagent`
     - User: `Administrator`
     - password: `Puppetlabs!`
     - Test connection: checked

5. Click **Add nodes**.

6. To check the status of the installation, navigate to the **Tasks** page, and then click the ID number of the **pe_bootstrap** task. When the installation is complete, you'll see a certname in the output at the bottom of the page.

✏️ **Note:** The installation might take a few minutes to complete. Don't move on until step 6 has finished.

7. When the certificate is ready to sign, a blue decoration is shown on the **Certificates** page link.<br><br>💡 **Tip:** If the decoration isn't shown after the `pe_bootstrap` task has finished running, click the refresh icon at the top right of the PE console.

8. Sign the agent's certificate. Navigate to the **Certificates** page and click the **Unsigned certificates** tab.

9. In the list of nodes, find the node name containing `winagent` and click **Accept**.

10. ![swtich tabs](https://storage.googleapis.com/instruqt-images/Instruct%20Icons/icon_switch_tabs_white_32.png) Switch to the **Windows Agent** tab.

11. From the Windows Start Menu, click **Puppet**, and then click **Start Command Prompt with Puppet**. Then, trigger a Puppet run at the command prompt:<br><br>
     ````
     puppet agent -t
     ````

12. Click the **PE Console** tab, and from the console sidebar, navigate to the **Nodes** page. Click the node name containing `winagent`.

1. On the **Facts** tab, inspect the facts about the `winagent` node.

<br>🎈 **Congratulations!**  You installed Puppet agents remotely from the PE console on Windows.

<br>To close this lab, click **Next**.