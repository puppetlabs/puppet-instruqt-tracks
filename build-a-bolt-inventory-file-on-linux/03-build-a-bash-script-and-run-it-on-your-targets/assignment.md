---
slug: build-a-bash-script-and-run-it-on-your-targets
id: xuxnxfxlf8vj
type: challenge
title: "Build a Bash script and run it on your targets \U0001F4DC"
teaser: Invoke a script with Bolt to complete a multistep NTP configuration.
notes:
- type: text
  contents: |-
    In this challenge, you will build and run an NTP configuration script.

    This script:
     - Synchronizes the system time on all your targets.
     - Appends more NTP servers to the end of the `ntp.conf` files.
     - Starts the NTP service.

    Click **Start** when you’re ready to begin.
tabs:
- title: Bolt
  type: terminal
  hostname: puppet
- title: Editor
  type: code
  hostname: puppet
  path: /root
- title: Lab Help Guide
  type: website
  url: https://puppet-kmo.gitbook.io/instruqt-platform-help/
difficulty: basic
timelimit: 720
---
✏️ **Note:**  This example uses a Bash script, but you can use a script written in any programming language that the targets support.

In this challenge, you'll write an NTP configuration script and run it on your targets. In the same way that you ran a *command* on a group of targets, you'll run a *script* against the same group, replacing the command name with the path to the script:

`bolt script run <filepath.sh> --targets webservers`

# Step 1: Open the script
On the **Editor** tab, open the `/root/configure-ntp.sh` script.

# Step 2: Build the script
Use the comments in the file and your knowledge of NTP configuration to build a script.

✏️ **Note:**  If you get stuck, open `/root/.instruqt/configure-ntp.sh`, copy the code and paste it into your script.

# Step 3: Test the script
Go back to the **Bolt** tab and run the following command:
```
bolt script run /root/configure-ntp.sh --targets webservers
```

If you built the script correctly, you'll see output similar to this:
```
    Started on web1...
    Started on web2...
    Finished on web1:
      14 May 22:32:51 ntpdate[1465]: step time server 17.253.52.253 offset -0.000310 sec
    Finished on web2:
        14 May 22:32:51 ntpdate[1471]: step time server 17.253.52.253 offset -0.000089 sec
    Successful on 2 targets: web1,web2
    Ran on 2 targets in 7.85 sec
```

This output shows the one-time synchronization of the NTP server with the system time on web1 and web2.

If the output doesn’t match the output shown above, go to the **Editor** tab and review the sample solution in the `/root/.instruqt` directory.