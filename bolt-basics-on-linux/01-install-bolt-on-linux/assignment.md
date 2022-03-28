---
slug: install-bolt-on-linux
id: eqmodrpl9ij4
type: challenge
title: Install Bolt
teaser: Install Bolt in minutes and start using it right away.
notes:
- type: text
  contents: |-
    # What is Bolt?
    Bolt is an open source automation tool that automates manual infrastructure maintenance tasks, including both ad hoc tasks and tasks that are part of a bigger workflow.

    Use Bolt to:
    - Patch and update systems
    - Troubleshoot servers
    - Deploy applications
    - Stop and restart services

    ## **Start this track**
    When your environment has finished spinning up, you'll see a green **Start** button at the bottom of the screen (this should take about 1 minute). Click it when you're ready to begin the track.
tabs:
- title: Bolt
  type: terminal
  hostname: puppet
- title: Lab Help Guide
  type: website
  url: https://puppet-kmo.gitbook.io/instruqt-platform-help/
difficulty: basic
timelimit: 360
---
# Install Bolt
The best way to learn about Bolt is to try it out for yourself. Start by configuring the Bolt yum repository, also known as the Puppet package repository — by default, this isn't configured on standard Linux installations. Then, install Bolt.

# Step 1: Configure the Puppet package repository
To configure the Puppet package repository, run the following command:
```
rpm -Uvh https://yum.puppet.com/puppet-tools-release-el-7.noarch.rpm
```
The `rpm -Uvh` command installs the package that configures the Bolt yum repository. The `-Uvh` flags tell Bolt to update the system with this package (-U), enable verbose logging (-v), and show a progress bar.

# Step 2: Install Bolt

Now, install Bolt by running this command:
```
yum install -y puppet-bolt-3.7.1
```

The `yum` command invokes the Linux package manager, which locates the package in any of the configured package repositories (in this case, puppet-bolt-3.7.1) and installs it on the system. The package manager also installs any package dependencies.

The `-y` option suppresses additional installation prompts.

Notice that a specific version (3.7.1) of Bolt is installed by running this command. The commands in the rest of this track work with this Bolt version. To install the latest version of Bolt, just omit the version number:
yum install -y puppet-bolt

✏️ **Note:**
There are many ways to install Bolt. For details, check out the [Bolt installation docs](https://puppet.com/docs/bolt/latest/bolt_installing.html).

✅ **Result:** Notice the Transaction Summary section in the output. If Bolt installed successfully, you'll see “Complete!” at the end of the summary.

To go to the next challenge, click **Check**.
