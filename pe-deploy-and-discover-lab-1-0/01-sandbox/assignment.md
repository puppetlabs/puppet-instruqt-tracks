---
slug: sandbox
id: o7pfcncfzcua
type: challenge
title: Install PE
teaser: Install PE and monitor its services in the console.
notes:
- type: text
  contents: |-
    In this lab, you'll complete an express installation of PE and confirm in the PE console that the installation was successful.

     Click **Start** when you're ready to begin.
tabs:
- title: Primary Server
  type: terminal
  hostname: puppet
- title: PE Console
  type: service
  hostname: puppet
  port: 443
- title: Lab Aid
  type: website
  url: https://puppet-kmo.gitbook.io/lab-aids/-MZKPjwKRKKFuXxxy7ge/pe101/install-the-primary-server
- title: Practice Lab Help
  type: website
  hostname: puppet
  url: https://puppet-kmo.gitbook.io/practice-lab-help/
difficulty: basic
timelimit: 3000
---

1. On the **Primary Server** tab, download the installation tarball: <br><br>💡 **Tip:** Click the code block to copy it, and then right-click and paste it on the command line.<br><br>
    ```
    curl -JLO 'https://pm.puppet.com/cgi-bin/download.cgi?dist=el&rel=7&arch=x86_64&ver=2019.8.6'
    ```

2. Unpack the tarball:<br><br>
    ```
    tar -xf puppet-enterprise-2019.8.6-el-7-x86_64.tar.gz
    ```

3. Run the Puppet Enterprise installer. When prompted, enter ****Y**** to proceed:<br><br>✏️ **Note:** This step might take a few minutes to complete.<br><br>
    ```
    ./puppet-enterprise-2019.8.6-el-7-x86_64/puppet-enterprise-installer
    ```

4. Set the password for the PE console to `puppetlabs`: <br><br>⚠️ **Important:** You will use this password to log into the console after PE is installed.<br><br>
    ```
    puppet infrastructure console_password --password=puppetlabs
    ```

5. Run Puppet <b>**twice**</b> to complete the PE installation:<br><br>⚠️ **Important:** Don't chain the commands.<br><br>✏️ **Note:** Running Puppet twice ensures that all of the post-configuration operations are complete and that PE is running.<br><br>
    ```
    puppet agent -t
    ```

6. Check the status of the Puppet services:<br><br>
    ```
    puppet infrastructure status
    ```

7. ![swtich tabs](https://storage.googleapis.com/instruqt-images/Instruct%20Icons/icon_switch_tabs_white_32.png) Switch to the **PE Console** tab.

8. Log into the console with ID `admin` and password `puppetlabs` (the password you set in Step 4).

9. On the **Status** page, click **Puppet Services status** near the top right. You should see output similar to the following:

    ![Image](https://storage.googleapis.com/instruqt-images/PE-deploy-and-discover/1.0.pe-deploy-and-discover-status.png)

10. Make sure that all the services in the list are running ("Operational").

<br>🎈 **Congratulations!** You installed PE, and its basic configuration is now complete.