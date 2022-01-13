---
slug: verify-your-bolt-installation-linux
id: wvghomls1zpw
type: challenge
title: Verify your Bolt installation ✔️
teaser: Make sure your Bolt installation works as expected.
notes:
- type: text
  contents: |
    Now that you've installed Bolt, make sure it works as expected.

    To begin the next challenge, click **Start**.
tabs:
- title: Bolt
  type: terminal
  hostname: puppet
- title: Practice Lab Help
  type: website
  url: https://puppet-kmo.gitbook.io/instruqt-platform-help/
difficulty: basic
timelimit: 720
---
You can quickly confirm Bolt is installed correctly by running some basic Bolt commands.

First, show the Bolt version by running this command:
```
bolt --version
```

Then, show the Bolt help message:
```
bolt --help
```

To show all the Bolt commands, run **bolt --help** again.

Bolt also shows help for each of its subcommands. For example, to get help for the **script** command, run:
```
bolt script --help
```

✔️ **Result:** If Bolt is installed correctly, you'll see the output on the command line.

To continue, click **Check**.