---
slug: run-bolt-commands-on-remote-targets
id: xpxk4boeqvir
type: challenge
title: "Run Bolt Commands on Remote Targets \U0001F469‍\U0001F4BB"
teaser: Run your first Bolt commands on remote targets.
notes:
- type: text
  contents: |-
    Bolt runs commands on remote target nodes and orchestrates ad hoc tasks across your server infrastructure.

    In this challenge, you will run Bolt commands to check, start, and verify the Network Time Protocol (NTP) service on two target nodes.

    When you’re ready to continue, click **Start**.
tabs:
- title: Bolt
  type: terminal
  hostname: puppet
- title: Target 1
  type: terminal
  hostname: target1
- title: Target 2
  type: terminal
  hostname: target2
- title: Platform Help
  type: website
  hostname: puppet
  url: https://puppet-kmo.gitbook.io/instruqt-platform-help/
difficulty: basic
timelimit: 720
---
Now that you've verified your Bolt installation, it's time to get some hands-on practice with Bolt by managing the Network Time Protocol (NTP) service on two target nodes.

**What is a target?**
A target is anything that Bolt can connect to, such as servers (nodes), Docker containers, and network devices.

**What is NTP?**
NTP is a service that synchronizes servers' clocks. It’s important to configure this service to start automatically on servers that you add to your infrastructure. Accurate timekeeping ensures proper secure communications between remote clients and networked servers that host databases, web servers, and other applications.

In this challenge, you will check the status of the NTP service on two remote target nodes. Then, you will remotely log into each target node to start the service. Finally, you will confirm that the NTP service has been started on both target nodes.

# Step 1: Check the NTP service status
Check the status of the NTP service on two remote target nodes: target1 and target2. Hint: The ‘fail’ message that you'll see is expected because you haven't started the service yet - you'll do that in step 2.

Run the following command:
```
bolt command run '/bin/systemctl status ntpd.service' --no-host-key-check --targets target1,target2
```

This Bolt command logs in remotely to the target nodes and returns their NTP service status.

The`--no-host-key-check` portion of the command is optional and is included here to:
- Suppress a warning that would be shown if the target has never been remotely accessed before.
- Eliminate the need for you to confirm the SSH fingerprint of the remote machine.

✔️ **Result:**
The ‘fail’ messages indicate that each target is inactive, which is expected at this point. Continue to step 2.


# Step 2: Start the NTP service
The NTP service does not start by default. Run the following command to remotely log in again and start the service on the target nodes:
```
bolt command run '/bin/systemctl start ntpd.service' --no-host-key-check --targets target1,target2
```

✔️ **Result:** Notice the “Successful on 2 targets: target1, target2” message. This means that you started the NTP service on both target nodes. Nice job.

# Step 3: Confirm that the NTP service is running
Run the command from step 1 again to confirm that the NTP service has been started on both targets.

✔️ **Result:** Now that you have started the NTP service on the targets, notice the detailed information and the message “Successful on 2 targets: target1, target2”.

You can now add the targets to an existing infrastructure with additional configuration for their specific purposes.

To continue, click **Check**.