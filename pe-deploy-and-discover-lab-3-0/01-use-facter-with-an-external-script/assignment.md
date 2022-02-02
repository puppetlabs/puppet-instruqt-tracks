---
slug: use-facter-with-an-external-script
id: br8duqywypho
type: challenge
title: Use Facter with an external script
teaser: Create an external fact in a script and discover what Facter returns.
notes:
- type: text
  contents: |-
    It's your first day on the job in your new sysadmin role, and your boss sent you an email asking you to tag each node with its corresponding data center.

    To read the email, click the arrow (**>**) at the right.
- type: text
  contents: |-
    <img src="https://storage.googleapis.com/instruqt-images/PE-deploy-and-discover/lab-3.0-boss-memo.png" width="90%">

    Read the email above, and then click the arrow (**>**) at the right to continue.
- type: text
  contents: |-
    With this new information, you'll extend Facter by defining an external fact that identifies and tags each server with its corresponding data center location.

    Facter — a component of the Puppet agent — gathers built-in (core) facts that are packaged within it. It can also gather custom or external facts by using scripts that you or a third party have written.

    Facter collects these facts on each Puppet run and sends them to the primary server. The primary server uses facts to build each agent's catalog.

    Click the arrow (**>**) at the right to continue.
- type: text
  contents: |-
    In this lab, you will:
     * Run Facter to retrieve a node's `timezone` fact to discover which time zone a node is located in.
     * Create a `datacenter` external fact that marks a node with its corresponding data center based on its time zone.

    Click **Start** when you're ready to begin.
tabs:
- title: Linux Agent
  type: terminal
  hostname: nixagent
- title: Windows Agent
  type: service
  hostname: guac
  path: /#/client/c/winagent?username=instruqt&password=Passw0rd!
  port: 8080
- title: PE Console
  type: service
  hostname: puppet
  port: 443
- title: Lab Aid
  type: website
  hostname: guac
  url: https://puppet-kmo.gitbook.io/lab-aids/-MZKPjwKRKKFuXxxy7ge/pe101/identify-your-nodes-by-using-external-facts
- title: Practice Lab Help
  type: website
  hostname: guac
  url: https://puppet-kmo.gitbook.io/practice-lab-help/
difficulty: basic
timelimit: 3000
---
Create an external fact on a Linux node
========
*To view only the Windows instructions, collapse this instruction block.*

🔀 Switch to the **Linux Agent** tab if needed.

2. Ensure there isn't already a fact called `datacenter` on the Linux node:

    ✏️ **Tip:** Click the code block to copy it, and then right-click and paste it on the command line.
    ```
    facter datacenter
    ```
    ✔️ **Result:** Facter returns no value.

    Before creating the `datacenter` external fact, you need to know what value you're going to assign it. It can be anything of course, but for this example, you'll assign a data center name based on the node's time zone.<br><br>

3. Retrieve the value of the `timezone` core fact:
    ```
    facter timezone
    ```
    ✔️ **Result:** Puppet outputs the node's time zone. You will use this to create the `datacenter` fact in the coming steps.

    | Time Zone     | Data Center Name |
    |---------------|-------------|
    | Eastern / EDT | dc-east     |
    | Pacific / PDT | dc-west     |


4. We've provided a simple external fact script below. To put it into place, create the Facter location directory and external fact script:
    ```
    mkdir -p /etc/puppetlabs/facter/facts.d
    ```
5. Open the script in the vi editor:
    ```
    vi /etc/puppetlabs/facter/facts.d/datacenter.sh
    ```
6. Copy the code below into the file.

    💡 **Tip:** To do this, type `:set paste`, press **Enter**, and then press `i`. Then, click the code below to copy it, and paste it into the file.
    ```
    #!/usr/bin/env bash
    echo "datacenter=<DATACENTER>"
    ```

7. Using the information from the table above, replace `<DATACENTER>` with the ****Data Center Name**** that corresponds to the output of the node's `timezone` fact.

8. Save and exit vi by pressing `ESC` and typing `:wq`.

9. Run the following command make the script executable:
    ```
    chmod +x /etc/puppetlabs/facter/facts.d/datacenter.sh
    ```

## Verify that the fact was installed and is accessible by Facter:

10. Run `facter datacenter` again and notice the new output.

    ✔️ **Result:** Facter returns `dc-west`.<br><br>

11. Run Puppet to send all facts (built-in and external) to the primary Puppet server:
    ```
    puppet agent -t
    ```
    🔀 Switch to the **PE Console** tab.<br><br>

12. Login using `admin` and `puppetlabs`. Then, navigate to the **Nodes** page.

13. Click the Linux node (the name that contains `nixagent`).

14. On the **Facts** tab, scroll to view the `datacenter` fact displayed in the list.

🎈 **Congratulations!**  You installed an external fact script to create a `datacenter` fact, and then verified that Facter can retrieve the data in the fact.

Create an external fact on a Windows node
========
🔀  Switch to the **Windows Agent** tab.

2. Ensure there isn't already a fact called `datacenter` on the Windows node: Open a ****Powershell**** window from the ****Start**** menu, and then run the following command:

    ✏️ Tip: Click the code block to copy it, and then right-click and paste it.

    ```
    facter datacenter
    ```
    ✔️ **Result:** Facter returns no value.

    Before creating the `datacenter` external fact, you need to know what value you're going to assign it. It can be anything of course, but for this example, you'll assign a data center name based on the node's time zone.<br><br>

3. See the value of the `timezone` core fact:
    ```
    facter timezone
    ```
    ✔️ **Result:** Puppet outputs the node's time zone. You will use this to create the `datacenter` fact in the coming steps.
    | Time Zone     | Data Center Name |
    |---------------|-------------|
    | Eastern / EDT | dc-east     |
    | Pacific / PDT | dc-west     |

4. We've provided a simple external fact script below. To put it into place, create the following file:

    ⚠️ **Important:** Click ****Yes**** when prompted to create the file.

    ```
    notepad C:\ProgramData\PuppetLabs\facter\facts.d\datacenter.ps1
    ```

5. Using the information from the table above, replace `<DATACENTER>` with the ****Data Center Name**** that corresponds to the output of the node's `timezone` fact.
    ```
    write-host "datacenter=<DATACENTER>"
    ```
6. Save the file and exit Notepad.

## Verify that the fact was installed and is accessible by Facter:

7. In Powershell, run `facter datacenter` again and notice the new output.

    ✔️ **Result:** : Facter should return `dc-east`.<br><br>

1. Run Puppet to send all facts (built-in and external) to the primary Puppet server:
    ```
    puppet agent -t
    ```
    🔀 Switch to the **PE Console** tab.<br><br>

1. Navigate to the **Nodes** page.

1. Click the Windows node (the name that contains `winagent`).

1. On the **Facts** tab, scroll to view the `datacenter` fact displayed in the list.

🎈 **Congratulations!**  You installed an external fact script to create a `datacenter` fact, and then verified that Facter was able to retrieve the data in the fact.

To continue, click **Next**.