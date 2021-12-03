---
slug: sign-a-certificate
id: dty1ff36osqi
type: challenge
title: "Sign an Agent Node's Certificate \U0001F4BB"
teaser: Sign a certificate on an unsigned agent node so that the primary Puppet server
  can validate the node before authorizing communication.
notes:
- type: text
  contents: |-
    # How the primary Puppet server and agents communicate
    The primary Puppet server and Puppet agents communicate over an SSL connection. Before the primary server can communicate with an agent, it verifies that the agent node’s certificate is signed.

    The primary server accepts catalog compilation requests only from agent nodes with signed certificates.

    ## **Start this track**
    When your environment has finished spinning up (this takes about 1 minute), you'll see a green **Start** button at the bottom of the screen. Click it when you're ready to begin the track.
tabs:
- title: Primary Server
  type: terminal
  hostname: puppet
- title: Agent Node
  type: terminal
  hostname: linux-node
- title: Platform Help
  type: website
  hostname: puppet
  url: https://puppet-kmo.gitbook.io/instruqt-platform-help/
difficulty: basic
timelimit: 600
---
# Step 1: Switch to the agent node
Switch to the **Agent node** tab to the right so that you can run tasks from the agent node's command line.

# Step 2: Trigger a Puppet run
Run the following command to trigger a Puppet run on the agent node, whose certificate is not yet signed.
```
puppet agent -t
```
✔️ **Result:** As expected, the Puppet run fails. The agent attempts to contact the primary server, but the primary server rejects the request. No problem — you just have to sign the agent node's certificate.

# A note on autosigning
As your infrastructure grows, you’ll likely use the Puppet Enterprise (PE) graphical console to manage certificates or enable autosigning so that you can sign many certificates at a time. In this practice lab, or in a demo environment, signing certificates manually from the command line is sufficient for signing a few certificates at a time.

# Step 3: On the primary server, list the unsigned certificates
Switch back to the **Primary Server** tab and use the `puppetserver ca` tool to list unsigned certificates:
```
puppetserver ca list
```
Note the name of the unsigned node: `linux-node.classroom.puppet.com`

# Step 4: Sign the certificate
Run the following command, which includes the node name:
```
puppetserver ca sign --certname linux-node.classroom.puppet.com
```

✔️ **Result:** The Puppet agent on `linux-node.classroom.puppet.com` is now authorized to request the catalog from the primary server.

# Step 5: On the agent node, trigger another run
Switch back to the **Agent node** tab and run the following command again:
```
puppet agent -t
```
✔️ **Result:** The agent completes a successful run.

## **What’s with all that text?**

Most of the text scrolling by is from a process called `pluginsync`. During `pluginsync`, any extensions installed on the server (such as custom facts, resource types, or providers) are copied to the agent *before* the Puppet run. This ensures that the agent has the tools it needs to apply the catalog.

In the next challenge, you'll examine the output to understand what happens during a Puppet run.