---
slug: run-a-command-on-your-targets
id: aumjsw3ompmd
type: challenge
title: ' Run a Command on Your Targets ✔️'
teaser: Run the `ntpdate` command to synchronize the system time on the targets defined
  in the **webservers** group.
notes:
- type: text
  contents: |-
    In this challenge, you'll run the `ntpdate` command to synchronize the system time of the targets in the **webservers** group that you defined in the `inventory.yaml` file.

    Assigning targets to groups and running commands against the group enables you to:
    - Eliminate hard-coded target names from commands and scripts.
    - Easily move targets among groups as system needs change.
    - Ensure that commands run against the correct targets.

    Click **Start** when you’re ready to begin.
tabs:
- title: Bolt
  type: terminal
  hostname: puppet
- title: Platform Help
  type: website
  hostname: puppet
  url: https://puppet-kmo.gitbook.io/instruqt-platform-help/
difficulty: basic
timelimit: 720
---
To run a Bolt command against multiple targets *without* an inventory file, you need a comma-separated list of targets to run the command against, which looks like this:
`bolt command run <command> --targets web1,web2`

But because you defined the webservers group in `inventory.yaml` in the previous challenge, you can simplify the command by specifying the group name:
`bolt command run <command> --targets webservers`

# Step 1: Run the `ntpdate` command
Run the following `ntpdate` command to synchronize the system time on the targets defined in the **webservers** group:

```
bolt command run 'ntpdate -b time.apple.com' --targets webservers
```

Notice that the time was adjusted on the targets (your run date and time will differ):
```
    Started on web2…
    Started on web1…
    Finished on web2:
      14 May 16:32:35 ntpdate[1605]: adjust time server 50.205.57.38 offset -0.000023 sec
    Finished on web1:
        14 May 16:32:35 ntpdate[1599]: adjust time server 45.87.76.3 offset 0.000690 sec
    Successful on 2 targets: web1,web2
    Ran on 2 targets in 7.55 sec
```

To recap, running commands against defined groups instead of against individual targets enables you to:
 - Eliminate hard-coded target names from commands and scripts.
 - Easily move targets among groups as system needs change.
 - Ensure the correct commands run against the correct targets.

 Click **Check** to continue.


