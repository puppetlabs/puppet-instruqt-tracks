---
slug: configure-additional-agent-package-platforms
id: znr1665vsmzt
type: challenge
title: Configure Puppet Enterprise to support additional agent platforms
teaser: Add agent packages for the platforms in your infrastructure.
notes:
- type: text
  contents: |-
    In this lab, you will:

    1. Attempt an agent installation on a node with a different OS than the primary server.
    2. Configure the primary server to provide OS-specific agent packages so that you can install agents across a variety of nodes.
    3. Attempt the agent installation again and autosign the agent certificate by providing a challenge password.

    Click **Start** when you're ready to begin.
tabs:
- title: Linux Agent
  type: terminal
  hostname: nixagent1
- title: Primary Server
  type: terminal
  hostname: puppet
- title: PE Console
  type: service
  hostname: puppet
  port: 443
- title: Lab Help Guide
  type: website
  url: https://puppet-kmo.gitbook.io/practice-lab-help/
difficulty: basic
timelimit: 1500
---
1. On the Linux node, install an agent by running the installation script with the `custom_attributes:challengePassword` parameter:
    ```
    uri='https://puppet:8140/packages/current/install.bash'
    curl --insecure "$uri" | bash -s custom_attributes:challengePassword=PASSWORD_FOR_AUTOSIGNER_SCRIPT
    ```
    ✅ **Result:** The installation script will fail.<br><br>

2. In the output, notice the failure message:
    ```
    The agent packages needed to support ubuntu-20.04-amd64 are not present are not present on your        primary  server. To add them, apply the pe_repo::platform::ubuntu_2004_amd64 class to your master node, and then run Puppet. The required agent packages should be retrieved when puppet runs on the master, after which you can run the install.bash script again.
    ```

    💭  **Why did the installation fail?**<br>
    The Ubuntu 20.04 package isn't present on the primary server — the primary server isn't running Ubuntu. To ensure that the packages are present, you must add the `pe_repo::platform:<AGENT_OS_VERSION_ARCHITECTURE>` classes to the primary server.

    🔀  Switch to the **PE Console** tab.<br><br>
1. Log in with username `admin` and password `puppetlabs`.

4. From the console sidebar, navigate to the **Node groups** page. Expand **PE Infrastructure** (click **+**) and then click **PE Master**.

5. Add the repository class for the agent node OS that you want to support.
    1. On the **Classes** tab, in the **Add new class** field, enter `pe_repo`.
    2. From the list of classes, select the `pe_repo::platform::ubuntu_2004_amd64` repo class.
    3. Click **Add class**.<br><br>

6. Commit your change: Click **Commit** in the bottom right of the page.

    🔀 Switch to the **Primary Server** tab.<br><br>

8. Run Puppet to manually trigger the download of the new agent package to the primary server:
    ```
    puppet agent -t
    ```

    🔀 Switch to the **Linux Agent** tab.<br><br>

10. Install the agent on the Linux node by running the following installation script, which includes the `custom_attributes:challengePassword` parameter to autosign the agent certificate:
    ```
    uri='https://puppet:8140/packages/current/install.bash'
    curl --insecure "$uri" | sudo bash -s custom_attributes:challengePassword=PASSWORD_FOR_AUTOSIGNER_SCRIPT
    ```
    In the output, notice the success message. (You may need to scroll up).
    ```
    The following NEW packages will be installed: puppet-agent
    ```

## 🎈 **Congratulations!**
You configured Puppet Enterprise to support installing agents that run a different OS than the primary server.

<br>To continue, click **Next**.