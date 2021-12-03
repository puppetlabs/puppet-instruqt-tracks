---
slug: set-up-code-manager-and-deploy-code-to-production
id: zcognslglvff
type: challenge
title: Set up Code Manager and Deploy Code to Production
teaser: Deploy code from your feature branch to the primary server to enable you to
  later test changes on nodes in a separate puppet environment.
notes:
- type: text
  contents: |-
    In this lab you will:
    - Create a dedicated code deployment user you will use to authenticate to deploy code.
    - Configure Code Manager to authenticate and download your control-repo from the git server.
    - Create a feature branch in your control-repo from main to allow you to develop safely without affecting production.
    - Add module in your Puppetfile on your feature branch to test a code deployment
    - Deploy code from your feature branch to the primary server to enable you to later test changes on nodes in a separate puppet environment.
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
- title: Git Server
  type: service
  hostname: gitea
  path: /
  port: 3000
- title: Linux Agent 1
  type: terminal
  hostname: nixagent1
difficulty: basic
timelimit: 3600
---
# Clone the control repo on your Windows development workstation
1. ![switch tabs](https://storage.googleapis.com/instruqt-images/Instruct%20Icons/icon_switch_tabs_white_32.png) Switch to the **Windows Agent** tab.
2. From the **Start** menu, open **Visual Studio Code**.
3. Enable autosave so that you don't have to remember to save your changes. Click **File** > **Auto Save**.
4. Open the `C:\CODE` directory. Click **File** > **Open Folder**, navigate to the `C:\CODE` directory and click **Select Folder**.
5. When prompted, click **Accept** to trust code in this directory.
6. In VS Code, open a terminal. Click **Terminal** > **New Terminal**.
7. In the VS Code terminal window, run the following command:

        git clone git@gitea:puppet/control-repo.git
---
# Configure code manager
1. Make changes to your Puppetfile:

- Checkout your new feature branch `webapp` from `main`.
```
cd control-repo
git checkout webapp
```
- Add the time module by copying and pasting to the end of your Puppetfile. You'll use this module in later labs.
```
mod 'time',
  ;git => 'https://git.local/puppet/puppet-time'
```
- Commit & push your changes to your feature branch `webapp`.
```
git add .
git commit -m "Add time module"
git push
```

2. Create a dedicated code deployment user with password.

3. Set up token-based authentication for code deployment via `puppet-access login` - check that the token has been created in it's default location.

4. Via the PE console, add the parameters to the following keys:

- `puppet_enterprise::profile::master class: code_manager_auto_configure`
- `r10k_remote`
- `r10k_private_key`

5. Run puppet on the primary server to apply the changes and configure code manager.

6. Test the connection to the control repository--the token will be loaded from the default location.` puppet-code deploy --dry-run`.

7. Observe output - success? This means code manager was able to connect and read all the git branches in the control-repo.

8. Check the contents of the puppet codedir `puppet config print codedir` and also compare it with the control-repo in your version control repository - note that the directory environment `feature_1` branch has not been deployed, let's deploy it manually.

9. Initiate a run `puppet-code deploy webapp --wait`

10. Error - puppet code deploy fails - check the syntax in your Puppetfile:
 ```
 mod 'time',
   ;git => 'https://git.local/puppet/puppetlabs-time',
```
11. Check the contents of the codedir - the directory environment `feature_1` did not get deployed.

12. Check the contents of the staging dir - observe the bad code.

13. Replace the semi-colon with a double-colon, commit and push your changes again.

14. Initiate a run `puppet-code deploy webapp --wait`.

15. Check the contents of the puppet codedir and also compare it with the control-repo in your version control repository - note that the directory environment `webapp`  branch has been deployed because it contains your updated module time.