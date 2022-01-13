---
slug: simulate-changes-with-noop
id: 8dcbrxcg3ex5
type: challenge
title: Run Puppet in no-op mode
teaser: Cause intentional drift and use no-op mode to see how Puppet would fix it.
  Then, run Puppet to implement those changes.
notes:
- type: text
  contents: |-
    In this lab you will:
    - Cause drift by making a breaking change to a Puppet component of your choosing (the `pxp-agent` or the uninstaller script).
    - Run Puppet with the `--noop` parameter to simulate a Puppet run without enforcing the agent catalog and making changes to the system.
    - Run Puppet normally to fix the drift you caused.

    In this lab, you'll use only the Linux agent (on the Linux Agent tab). Feel free to explore the PE console and primary server command line available on the other tabs. To log into the PE console, use userid `admin` and password `puppetlabs`.

    Click **Start** when you're ready to begin.
tabs:
- title: Linux Agent
  type: terminal
  hostname: nixagent
- title: PE Console
  type: service
  hostname: puppet
  path: /
  port: 443
- title: Primary Server
  type: terminal
  hostname: puppet
- title: Practice Lab Help
  type: website
  hostname: nixagent
  url: https://puppet-kmo.gitbook.io/practice-lab-help/
difficulty: basic
timelimit: 3000
---
## **First, let's break something.**
**What can we break?** Out of the box, Puppet manages only itself. So let's break Puppet!

Specifically, you'll cause drift on the agent node by making an unexpected change to one or more of the following components:

| # | Type | Component |
|:-:|:-:|-------|
|**1**| Service | ` [pxp-agent] ` |
|**2**| File | ` [pxp-agent.conf] ` |
|**3**| File | ` [puppet-enterprise-uninstaller] ` |

**Instructions**

1. Choose one or more components to break. Then, cause drift on the Linux agent node by running one of the following commands:<br><br>
     | # | How to cause drift |
     |:-:|------- |
     |**1**| Stop the service by running this command: <br> ``` service pxp-agent stop ```      |
     |**2**| Add text to the config file by running this command: <br> ``` echo hello > /etc/puppetlabs/pxp-agent/pxp-agent.conf ``` |
     |**3**| Remove the uninstall script by running this command: <br> ``` rm /opt/puppetlabs/bin/puppet-enterprise-uninstaller ```|

## **Next, let's see how Puppet would fix it.**

Run Puppet in no-op mode to simulate a Puppet run and understand what the Puppet agent would do.

## Instructions

1. Run the command you think would trigger a Puppet run in no-op mode. (Hint: Only one of these will work. You can run the `puppet agent --help` command to get clues.)<br><br>
     | # | Choose a command to run |
     |:-:|------- |
     |**1**| ```puppet agent run --noop``` |
     |**2**| ```puppet agent -t --noop``` |
     |**3**| ```puppet agent get_catalog --noop``` |

2. Examine the output for the mention of `noop` to see the changes Puppet would have made.<br><br>💡 **Tip:** Look for `/Stage[main]` in the output to quickly find the changes.

## **Finally, let's run Puppet to fix it.**

1. Run Puppet normally:
    ```puppet agent -t```

2. Examine the output to see the changes Puppet made to bring the node back into its desired state (all Puppet components fully functional).

🎈 **Congratulations!** How easy was that? Now imagine hundreds or thousands of these failures happening overnight — due to an automatic update, for instance — and you'll start to see the true power and potential of Puppet.

To continue, click **Next**.
