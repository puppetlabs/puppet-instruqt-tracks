---
slug: agent-specified-node-groups-for-testing
id: byvczbgv7ity
type: challenge
title: Agent-Specified Node Groups for Testing
teaser: In this lab you will configure PE so you can implement environment-based testing
  using a one-time run exception environment group.
tabs:
- title: Windows Agent
  type: service
  hostname: guac
  path: /#/client/c/winagent?username=instruqt&password=Passw0rd!
  port: 8080
- title: PE Console
  type: service
  hostname: puppet
  path: /
  port: 443
- title: Primary Server
  type: terminal
  hostname: puppet
- title: Linux Agent 3
  type: terminal
  hostname: nixagent3
- title: Linux Agent 1
  type: terminal
  hostname: nixagent1
- title: Linux Agent 2
  type: terminal
  hostname: nixagent2
- title: Git Server
  type: service
  hostname: gitea
  path: /
  port: 3000
difficulty: basic
timelimit: 3600
---
# Create a control repo on your Windows development workstation
1. ![switch tabs](https://storage.googleapis.com/instruqt-images/Instruct%20Icons/icon_switch_tabs_white_32.png) Switch to the **Windows Agent** tab.
2. From the **Start** menu, open **Visual Studio Code**.
3. Enable autosave so that you don't have to remember to save your changes. Click **File** > **Auto Save**.
4. Open the `C:\CODE` directory. Click **File** > **Open Folder**, navigate to the `C:\CODE` directory and click **Select Folder**.
5. If prompted to trust the code in this directory, click **Accept**.
6. In VS Code, open a terminal. Click **Terminal** > **New Terminal**.
7. In the VS Code terminal window, run the following command:

        git clone git@gitea:puppet/control-repo.git
---
# Add a debug message to all nodes via site.pp
```
# control-repo/manifests/site.pp
node default {
    include "${trusted['extensions']['pp_role']}"
    notify { 'it worked! This is experimental code on your feature branch!': }
    }
 ```
2. Check the one-time run exception group within the development environment, verify the settings:
- Name — Canary one-time run exception
- Parent — Development environment
- Environment — agent-specified
- Environment group — checked

3. Add an agent-specified environment node group for production to enable canary release--you will use this later:
- Name — Canary one-time run exception
- Parent — Production environment
- Environment — agent-specified
- Environment group — checked

4. Login to your nodes--check that they have the pp_environment trusted fact set to "development". Notice that one of your nodes does not have this trusted fact set, so you'll need to manually pin that node to the development environment node group.

5. Pin the node to the parent development environment node group.

6. Run puppet agent -t --environment <ENVNAME>, where <ENVNAME> is the name of the Puppet environment that contains your test code (your feature branch).

7. <FAIL> Why did the run fail? The code has not yet been deployed - log on to the primary to inspect the codedir to confirm this.

8. Deploy your feature branch - log on to the primary server to confirm that your feature branch environment has been deployed.

9. Run puppet agent -t --environment <ENVNAME>, where <ENVNAME> is the name of the Puppet environment that contains your test code (your feature branch).


If you're using Code Manager and a Git workflow, <ENVNAME> is the name of your Git development or feature branch.


During this Puppet run, the agent sets the agent_specified_environment value to <ENVNAME>. The Canary one-time run exception group matches the node and permits it to use the requested environment.