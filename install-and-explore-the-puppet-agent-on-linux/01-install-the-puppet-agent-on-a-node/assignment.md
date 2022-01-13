---
slug: install-the-puppet-agent-on-a-node
id: kvex76zt0maw
type: challenge
title: "Install the Puppet agent on a node \U0001F4BB"
teaser: Start off by installing the Puppet agent on a fresh node.
notes:
- type: text
  contents: |-
    # What is the Puppet agent?
    Puppet is a suite of tools and services that work together to help you manage and coordinate the systems in your infrastructure.

    One of these tools, the Puppet agent, runs on every system that Puppet manages, acting as a maintenance crew that travels between the system where it's installed (the node) and the primary Puppet server.

    The Puppet agent:
    1. Requests and receives the node's desired state information from the primary server.
    1. Enforces the desired state on the node by checking its current state and making changes as needed.
    1. Sends runtime reports about node changes and status to the primary server.

    ## **Start this track**
    When your environment has finished spinning up, you'll see a green **Start** button at the bottom of the screen. Click it when you're ready to begin the track.
tabs:
- title: Linux
  type: terminal
  hostname: linux
- title: Practice Lab Help
  type: website
  url: https://puppet-kmo.gitbook.io/practice-lab-help/
difficulty: basic
timelimit: 600
---
The best way to learn about Puppet is to try it out for yourself. Start by configuring the Puppet package repository, which by default isn't configured on standard Linux installations. Then, install the Puppet agent.

# Step 1: Configure the Puppet package repository
To configure the Puppet package repository, run the following command:
```
rpm -Uvh https://yum.puppet.com/puppet7-release-el-7.noarch.rpm
```
✔️ **Result:** The `rpm -Uvh` command installs the package that configures the repository. The `-Uvh` flags instruct Puppet to update the system with this package (-U), enable verbose logging (-v), and show a progress bar.

# Step 2: Install the Puppet agent

Install the agent by running this command:
```
yum install -y puppet-agent
```

The `yum` command invokes the Linux package manager, which locates the package in any of the configured package repositories (in this case, puppet-agent) and installs it on the system. The package manager also installs any package dependencies.

The `-y` option suppresses additional installation prompts.


✔️ **Result:** Check the Transaction Summary section in the output. If the agent installed successfully, you'll see “Complete!” at the end of the summary.

✏️ **Note:** For details about other ways to install Puppet, check out the [Puppet installation docs](https://puppet.com/docs/pe/latest/installing.html).

# Step 3: Set the path

Add the `/opt/puppetlabs/bin/` directory to the system path so that you can run the `puppet` command from any directory. Run the following two commands:

```
echo 'export PATH=/opt/puppetlabs/bin:/opt/puppetlabs/puppet/bin:$PATH' >> ~/.bashrc
```
```
source ~/.bashrc
```

✔️ **Result:** You now can invoke Puppet from any directory on the node.

# Step 4: Verify the path

Invoke Puppet without any parameters by running this command:

```
puppet
```

✔️ **Result:** Puppet shows a message (which confirms that the path is set) but takes no action.

To go to the next challenge, click **Check**.
