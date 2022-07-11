---
slug: working-with-puppets-trusted-facts
id: 0fmim6wrx8d8
type: challenge
title: Working with Puppet's trusted facts
teaser: Purge the agents and reinstall them with trusted facts.
notes:
- type: text
  contents: |-
    In this lab, you'll learn how to add trusted facts to agents. You will:

    1. Manually uninstall the agents and purge the nodes from the primary server.
    2. Reinstall your agents with two trusted facts: `pp_role` and `pp_datacenter`
    3. Re-sign the agent certificate with the trusted facts.

    This lab environment takes about 7 minutes to spin up. When the **Start** button appears, click it to begin.
tabs:
- title: PE Console
  type: service
  hostname: puppet
  path: /
  port: 443
- title: Linux Agent 1
  type: terminal
  hostname: nixagent1
- title: Linux Agent 2
  type: terminal
  hostname: nixagent2
- title: Primary Server
  type: terminal
  hostname: puppet
- title: Windows Agent
  type: service
  hostname: guac
  path: /#/client/c/winagent?username=instruqt&password=Passw0rd!
  port: 8080
- title: Lab Help Guide
  type: website
  url: https://puppet-kmo.gitbook.io/practice-lab-help/
difficulty: basic
timelimit: 1500
---
Uninstall Linux agents
========
*To view only the Windows instructions, collapse the Linux instruction blocks.*

⚠️ **Important:** The ****Linux Agent 1**** and ****Linux Agent 2**** tabs represent Linux nodes. Complete the following steps ****on each Linux agent node****.

1. On each node, retrieve the node's `certname` by running the following command:
    ```
    puppet config print certname
    ```
    🏆 **Extra credit:** Alternatively, see if you can find the certnames in the **PE console**. Log in with user `admin` and password `puppetlabs`.<br><br>

2. Copy each certname to a local text editor of your choice — you'll need them later in the lab.

3. Retire the nodes by running the *nix agent uninstall script on each node:
    ```
    /opt/puppetlabs/bin/puppet-enterprise-uninstaller -y -pd
    ```

4. Verify that the Puppet directory has been removed by running the following command on each node:
    ```
    ls /etc/puppetlabs
    ```
    ✅ **Result:** The output confirms that the agent no longer exists.

    ✏️ **Note:** Remember to complete these steps on each Linux agent node before continuing to the next section.


Remove nodes from the primary server on Linux
========
💭 **Why do this?**<br>
    Uninstalling the agent from a node does not remove the node from management by the primary server. You must also purge the node.

🔀 Switch to the **Primary Server** tab to run commands on the primary server.

2. Purge both Linux nodes by running the following command ****twice****, each time replacing `<CERTNAME>` with the certnames you gathered in the previous section:
    ```
    puppet node purge <CERTNAME>
    ```
    ✅ **Result:** In the output, notice the message: `Node <CERTNAME> was purged.`

    ✏️ **Note:** Remember to run this command for each Linux node before continuing to the next section.


Reinstall Linux agents with trusted facts and an autosign password
========
Now, replace `<DATACENTER>` and `<ROLE>` in the script with the correct trusted fact for each node:

|   | Data center | Role |
|-| :-----------: | :---------------: |
| ****Linux Agent 1**** | `dc-west` | `cmsweb`|
| ****Linux Agent 2**** | `dc-west` | `cmsloadbalancer`|
| ****Windows Agent**** | `dc-east` | `ecommerce` |

🔀 Switch to the ****Linux Agent 1**** tab.

1. Install an agent on the node by running the following installation script.

    ⚠️ **Important:** Remember to replace `<DATACENTER>` and `<ROLE>` with data from the table above.
    ```
    uri='https://puppet:8140/packages/current/install.bash'
    curl --insecure "$uri" | sudo bash -s custom_attributes:challengePassword=PASSWORD_FOR_AUTOSIGNER_SCRIPT extension_requests:pp_role=<ROLE> extension_requests:pp_datacenter=<DATACENTER>
    ```
1. 🔀 Switch to the ****Linux Agent 2**** tab and repeat step 1.
1. 🔀 Switch to the ****PE Console**** tab and click refresh inside the tab to see the attached nodes.
1. Click the Linux node names to view the trusted facts for each new node.

---
## 🎈 **Congratulations!**
You uninstalled the agent from your Linux nodes and purged them from the primary server so that you can reuse their node licenses. You then securely assigned each server's role and data center in your environment by installing the Puppet agent with trusted facts and provided an autosign password to enable certificate signing so that primary server can authenticate the agent.

Uninstall Windows agents
========
1. 🔀 Switch to the **Windows Agent** tab.

1. Open a PowerShell terminal: **Start** —> **Windows PowerShell** —> **Windows PowerShell 5.1**

    💡 Make sure you are using the correct version of Windows PowerShell (version 5.1).<br><br>

1. Retrieve the node's `certname` by running the following command:
    ```
    puppet config print certname
    ```
    🏆 **Extra credit:** Alternatively, see if you can find the certname in the **PE Console**. Log in with user `admin` and password `puppetlabs`.<br><br>

1. Copy the certname to a local text editor of your choice — you'll need it later in the lab.

1. Launch the **Windows Add or Remove Programs** interface by running the following command in PowerShell:
    ```
    appwiz
    ```
1. Right-click __Puppet Agent (64-bit)__, select __Uninstall__, and follow the prompts to uninstall. Click OK on the dialog box that indicates a reboot is necessary, but do not reboot.
    ✏️ **Note:** Uninstalling the agent removes the Puppet program directory, the agent service, and all related registry keys. This might take a couple of minutes.
    ⚠️ **Important:** The `data` directory remains intact, including all SSL keys. Completely remove the agent from the node in the next step.<br><br>

1. In the PowerShell terminal, run the following command:
    ```
    remove-item C:\ProgramData\PuppetLabs\puppet -Recurse -Confirm:$false
    ```

Remove the node from the primary server on Windows
========
💭 **Why do this?**<br>
    Uninstalling the agent from a node does not remove the node from management by the primary server. You must also purge the node.

1. 🔀 Switch to the **Primary Server** tab to run commands on the primary server.

2. Purge the Windows node by running the following command, replacing `<CERTNAME>` with the certname you gathered in a previous step:
    ```
    puppet node purge <CERTNAME>
    ```
✅ **Result:** In the output, notice the message: `Node <CERTNAME> was purged.`<br><br>


Reinstall Windows agents with trusted facts and an autosign password
========
Now, replace `<DATACENTER>` and `<ROLE>` in the script with the correct trusted fact for the Windows node:

|   | Data Center | Role |
|-| :-----------: | :---------------: |
| ****Linux Agent 1**** | `dc-west` | `cmsweb`|
| ****Linux Agent 2**** | `dc-west` | `cmsloadbalancer`|
| ****Windows Agent**** | `dc-east` | `ecommerce` |


1. 🔀 Switch to the ****Windows Agent**** tab.

1. Install an agent by using the following installation script, passing in the corresponding role and data center for the last command. Run the following four commands one at a time:

    💡 Make sure you are using the correct version of Windows PowerShell (version 5.1).<br><br>

    Command 1
    ```
    [Net.ServicePointManager]::ServerCertificateValidationCallback = {$true};
    ```
    Command 2
    ```
    $webClient = New-Object System.Net.WebClient;
    ```
    Command 3
    ```
    $webClient.DownloadFile('https://puppet:8140/packages/current/install.ps1', 'install.ps1');
    ```
    Command 4
    ```
    .\install.ps1 custom_attributes:challengePassword=PASSWORD_FOR_AUTOSIGNER_SCRIPT extension_requests:pp_role=<ROLE> extension_requests:pp_datacenter=<DATACENTER>
    ```

    ✏️ **Note:** A rescue command is built into the Windows image; as an alternative to running steps 1-3, you can run the following in a new PowerShell prompt:
    ```
    Get-PuppetInstallerScript
    ```

1. 🔀 Switch to the **PE Console** tab and log in with user `admin` and password `puppetlabs`.

1. On the **Nodes** page, click the Windows node name to view the trusted facts for the new node.

---
## 🎈 **Congratulations!**
You uninstalled the Puppet agent from your Windows node and purged it from the primary server so that you can reuse its node license. You securely assigned the server's role and data center in your environment by installing the agent with trusted facts and provided an autosign password to enable certificate signing so that primary server can authenticate the agent.

To continue, click **Next**.