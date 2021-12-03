---
slug: refactor-base-profile-to-use-data-via-hiera-and-class-parameters
id: ajxi4la6m5kq
type: challenge
title: Refactor Base Profile to Use Data Via Hiera and Class Parameters
teaser: In this lab you will refactor your base profile by moving variables to class
  parameters, so that you can re-use the profile in another role without having to
  duplicate code (DRY principle).
notes:
- type: text
  contents: In this lab you will refactor your base profile by moving variables to
    class parameters, so that you can re-use the profile in another role without having
    to duplicate code (DRY principle).
tabs:
- title: Windows Agent
  type: service
  hostname: guac
  path: /#/client/c/winagent?username=instruqt&password=Passw0rd!
  port: 8080
- title: Primary Server
  type: terminal
  hostname: puppet
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
- title: Linux Agent 3
  type: terminal
  hostname: nixagent3
- title: PE Console
  type: service
  hostname: puppet
  path: /
  port: 443
difficulty: basic
timelimit: 600
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

# Create & move a variable in your base profile in a parameter block
1. Check out the **webapp** feature branch:
  ```
  cd control-repo
  git checkout webapp
  ```
2. Edit the profile/manifests/base.pp:
```
# profile/manifests/base.pp
class profile::base {
      $login_message = 'Welcome!'
      class { 'motd':
      message => $login_message,  }
}
```
to:
```
# profile/manifests/base.pp
# profile/manifests/base.pp
class profile::base (
    $loginmessage
){
   class { 'motd':
     message => $loginmessage,
 }
}
```

3. ![switch tabs](https://storage.googleapis.com/instruqt-images/Instruct%20Icons/icon_switch_tabs_white_32.png) Switch to the **PE Console** tab and log in with username `admin` and password `puppetlabs`.

Navigate to the Nodes page and click each node link, then click the Facts tab. For each node, check the value of the fact `domain`- you should have 2 nodes in each of the following domains: `dev.local`, `sec.local`.

4. ![switch tabs](https://storage.googleapis.com/instruqt-images/Instruct%20Icons/icon_switch_tabs_white_32.png) Switch back to the **Windows Agent** tab to continue editing your code.

Externalize the data in hiera for the `sec.local` domain by creadting and editing the data/domain/sec.local.yaml file:
```
# data/domain/sec.local.yaml
profile::base::loginmessage: 'WARNING: This server is monitored by sec ops.'
```

5. Run PDK to validate your code, commit, push and deploy.


6. Run puppet only on your node in the `sec.local` domain, observe the failure and use puppet lookup to troubleshoot - where did hiera look for data?

7. Configure the required domain level hiera data, push your changes, and deploy your code:
```
# <control-repo>/hiera.yaml
---
version: 5
hierarchy:
  - name: Yaml data
    datadir: data
    data_hash: yaml_data
    paths:
      - "nodes/%{trusted.certname}.yaml"
      - "common.yaml"
```
to:
```
# <control-repo>/hiera.yaml
---
version: 5
hierarchy:
    - name: Yaml data
      datadir: data
      data_hash: yaml_data
      paths:
        - "nodes/%{trusted.certname}.yaml"
        - "domain/%{facts.domain}.yaml"
        - "common.yaml"
```

8. Run puppet only on your `sec.local` domain node - observe success.

9. Run puppet on your `dev.local` domain node - observe failure - why did puppet fail lookup?

10. Add the required default data in `common.yaml`, push your changes, and deploy your code:

```
# data/common.yaml
profile::base::loginmessage: 'Welcome!'
```
11. Run PDK to validate your code, commit, push and deploy.

12. Run puppet on your `dev.local` domain node - observe success.