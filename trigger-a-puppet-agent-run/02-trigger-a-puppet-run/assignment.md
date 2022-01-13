---
slug: trigger-a-puppet-run
id: xbnzl6tqkedg
type: challenge
title: "Trigger a Puppet run \U0001F4BB"
teaser: Discover the high-level steps the agent takes during a Puppet run.
notes:
- type: text
  contents: |-
    # Manual vs. automatic Puppet runs
    By default, the agent initiates a Puppet run every 30 minutes. Because it's difficult to demonstrate Puppet with these scheduled background runs, we disabled the Puppet agent service on your agent system.

    Running Puppet manually is helpful when you're developing code — you can observe the agent output as it makes the required changes to the system.

    In these challenges, you’ll use the `puppet agent -t` command to manually trigger a Puppet run.

    When you’re ready to begin, click **Start**.
tabs:
- title: Primary Server
  type: terminal
  hostname: puppet
- title: Agent Node
  type: terminal
  hostname: linux-node
- title: Practice Lab Help
  type: website
  url: https://puppet-kmo.gitbook.io/practice-lab-help/
difficulty: basic
timelimit: 600
---
Now that the agent node's certificate is signed, on its next run the agent can request a catalog from the primary server. Here, you'll explore the high-level steps the agent completes during a Puppet run.

# Step 1: Switch to the agent node
Switch to the **Agent node** tab to the right so that you can run tasks from the node's command line.

# Step 2: Trigger the run
Run the following command to trigger another Puppet run. The output will be easier to read now that `pluginsyc` did its work in the previous challenge:
```
puppet agent -t
```
✔️ **Result:** Because the certificate is signed, the agent has permission to retrieve the catalog from the primary server.


# Step 3: Analyze the output
Focus on the three lines that look similar to the following text:
```
Info: Loading facts
Info: Caching catalog for agent.puppet.vm
Info: Applying configuration version '1464919481'
```
This output shows one side of the conversation between the agent and primary server:
1. The agent loads the facts (the details of the system that the agent runs on) and sends them to the primary server.
2. The agent receives a new catalog from the primary server and caches a copy of it.

      ✏️ **Note:**   You can configure the agent to fail over to this cached catalog if it can't connect to the primary server.

3. The agent configures the node based on the desired state information in the catalog. After this step, you typically see a list of all the changes that the agent made. In this case, the primary server didn't find any Puppet code to apply to the agent node, so the agent didn't make any changes during this run.

# That’s it?
Those are the high-level agent steps. Next, you'll define a unique setup, or configuration, for the agent node. This includes defining the desired state of the [resources](https://puppet.com/docs/puppet/latest/glossary.html#resource) on the node.