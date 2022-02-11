---
slug: develop-apache-and-iis-profiles
id: pcd8cxyxxxir
type: challenge
title: Develop apache and iis web server profiles
teaser: Gain proficiency in building roles and profiles by using two common web server
  technologies.
notes:
- type: text
  contents: |
    In this lab, you will:

    - Create `apache` and `iis` profile classes that configure web server implementations and add them to role classes.
    - Update these profile classes to use the `apache` module and the `iis` module from Puppet Forge.
         - `apache` module: The default apache class sets up a virtual host on port 80, listening on all interfaces and serving the docroot parameter's default directory of /var/www. This module depends on the `puppetlabs-concat` module.

         - `iis` module: Adds the services to manage IIS sites and application pools.
           This module depends on the `puppetlabs-pwshlib` module.

         - You'll manage these  modules and their dependencies with the Puppetfile.

    - Add the `apache` profile to the `cmsweb` role class, which represents a CMS backend web application server.
    - Add the `iis` profile to the `ecommerce` role class, which represents a front-end ecommerce application server.
    - Run Puppet in no-op mode to simulate a Puppet run across all nodes without actually making changes.
    - After successful testing, run Puppet again to make sweeping changes — in this case, fast provisioning — across your data center at the snap of a finger.

    Click **Start** when you're ready to begin.
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
- title: Lab Help Guide
  type: website
  url: https://puppet-kmo.gitbook.io/practice-lab-help/
difficulty: basic
timelimit: 3000
---
Verify that no websites are currently configured
========
1. On the **Windows Agent** tab, from the **Start** menu, open **Visual Studio Code**.
2. Enable VS Code autosave by clicking **File** > **Auto Save**.

    ✏️ **Note:** This step isn’t required, but by enabling Auto Save, you don't need to remember to save your changes as you work, ensuring your edits won't be lost.<br><br>

3. Open the `C:\CODE` directory. Click **File** > **Open Folder**, navigate to the `C:\CODE` directory and click **Select Folder**.
4. In VS Code, open a terminal. Click **Terminal** > **New Terminal**.
5. From the VS Code terminal, run the `Invoke-WebRequest` command against each node to verify that no websites are already configured:

    Winagent:
    ```
    Invoke-WebRequest -URI http://winagent
    ```
    Nixagent1:
    ```
    Invoke-WebRequest -URI http://nixagent1
    ```

✔️ **Result:** The output will show a failure message for each node: `Unable to connect to the remote server`.
<br><br>
❔  **Why did this happen?** You did not receive a response from either web server because you haven't installed or configured anything yet.

Create your control repo locally on your Windows development workstation
========
1. Clone the control repo. In the VS Code terminal window, run the following command:

    ```
    git clone git@gitea:puppet/control-repo.git
    ```

2. Check out the <b>webapp</b> feature branch:
    ```
    cd control-repo
    git checkout webapp
    ```

Create the Apache and IIS profiles
========
1. Navigate to the `site-modules/profile` directory:
    ```
    cd site-modules/profile
    ```
2. Create the Apache and IIS manifest files by running the following commands:

    ```
    pdk new class profile::apache
    ```
    ```
    pdk new class profile::iis
    ```

💡 **Tip:** When prompted whether or not you consent to anonymous PDK usage information, choose whichever option you prefer.

Update the the Apache and IIS manifest files
========
1. Replace the content in the `apache.pp` file with the following code:
    ```
    # apache profile: site-modules/profile/manifests/apache.pp
    class profile::apache {
      $port    = 80
      $docroot = '/var/www'
      include apache
      apache::vhost { 'vhost.example.com':
        port    => $port,
        docroot => $docroot,
      }
    }
    ```
2. Replace the content in the `iis.pp` file with the following code:

    ```
    # iis profile: site-modules/profile/manifests/iis.pp
    class profile::iis {
      $iis_features = ['Web-WebServer','Web-Scripting-Tools']
      $index_content = "
      <!DOCTYPE html>
      <html>
      <body>

      <h1>Ecommerce Site</h1>

      </body>
      </html>"

      iis_feature { $iis_features:
        ensure => 'present',
      }

      # Delete the default website to prevent a port binding conflict.
      iis_site {'Default Web Site':
        ensure  => absent,
        require => Iis_feature['Web-WebServer'],
      }

      iis_site { 'ecom':
        ensure          => 'started',
        physicalpath    => 'c:\\inetpub\\ecom',
        applicationpool => 'DefaultAppPool',
        require         => [
          File['ecom'],
          Iis_site['Default Web Site']
        ],
      }

      file { 'ecom':
        ensure => 'directory',
        path   => 'c:\\inetpub\\ecom',
      }

      file {'index':
        require => File['ecom'],
        path    => 'c:\\inetpub\\ecom\\index.html',
        content => $index_content
      }
    }
    ```

Add the Apache and IIS profiles to the role files
========

1. Open the **cmsweb.pp** file at `control-repo/site-modules/role/manifests/cmsweb.pp` and add the following line:
    ```
    include profile::apache
    ```
2. Open the **ecommerce.pp** file at `control-repo/site-modules/role/manifests/ecommerce.pp` and add the following line:
    ```
    include profile::iis
    ```
3. Navigate to the control repo:
    ```
    cd C:\CODE\control-repo
    ```

    💡 **Tip:** Remember to run `git status` frequently to check on the status of your files.<br><br>

4. Commit and push your code to your feature branch:
    ```
    git add .
    git commit -m "Change profiles for role features"
    git push -u origin webapp
    ```

In the PE console, run Puppet in no-op mode and inspect the reports
========
🔀 Switch to the **PE Console** tab.
1. Log into PE with username `admin` and password `puppetlabs`.
2. In the console, run Puppet in no-op mode against your environment branch: <a name="run-in-noop">
    1. Navigate to the **Node groups** page; then, expand the **All Environments** group (click the plus sign (**+**) beside the group name) and click **Development environment**.
    2. Click the **Classes** tab, and then click **Refresh** (on the right-hand side of the page) to reload the classes you just pushed.
    3. On the **Matching nodes** tab, ensure all your nodes are listed for this group:
        - nixagent1
        - nixagent2
        - winagent
    4. In the upper-right corner, click **Run > Puppet**.
    5. You will be redirected to the **Run Puppet** page. Select the following options:
        - **Environment**: Click **Select an environment for nodes to run in:** and choose **webapp** from the list.
        - **Schedule**: Accept the default settings.
        - **Run options**: Select **No-op**.
    6. In the lower-right corner, click **Run Job** to run Puppet on all the nodes shown. You will be redirected to the **Job details** page.
3. After the jobs have completed, click the **Report** link shown to the right of each failed node.
4. On the **Log** tab in each report, notice the error message in the output:
   - nixagent1: `Could not find class ::apache`
   - winagent: `Unknown resource type: 'iis_feature' `

    🔀 Switch to the **Windows Agent** tab.<br><br>

5. Fix the missing module dependency by adding the Apache module to the Puppetfile (`control-repo/Puppetfile`):
    ```
    # Puppetfile
    mod 'puppetlabs-apache', '7.0.0' # Fixes nixagent1 module dependency
    mod 'puppetlabs-iis', '8.0.3'    # Fixes winagent module dependency
    ```
6. Commit and push your code to your feature branch:
    ```
    git add .
    git commit -m "Add Puppet Forge module dependencies"
    git push
    ```

    🔀 Switch to the **PE Console** tab.<br><br>

7. Run Puppet in no-op mode against your environment branch again.

    💡 **Tip:** Need a refresher for this step? Refer to [Step 3](#run-in-noop) above.<br><br>

8. For each failed node, click the link in the **Report** column. On the **Log** tab in the report, notice the error message in the output:
    - nixagent1: `Unknown resource type: 'concat' `
    - winagent: `no such file to load -- ruby-pwsh`

    🔀 Switch to the **Windows Agent** tab.<br><br>

9. Fix the missing module dependency by adding the `concat` module to the Puppetfile (`control-repo/Puppetfile`):
    ```
    # Puppetfile
    mod 'puppetlabs-concat', '7.1.1'   # Fixes nixagent1 module dependency
    mod 'puppetlabs-pwshlib', '0.10.0' # Fixes winagent module dependency
    ```
10. Commit and push your code to your feature branch:
    ```
    git add .
    git commit -m "Change puppetfile to fix dependencies"
    git push
    ```
    🔀 Switch to the **PE Console** tab.<br><br>

11. Run Puppet again in no-op mode. Notice that the run is successful.

12. Run Puppet **without noop mode selected**. Notice that the run is successful.

    🔀 Switch to the **Windows Agent** tab.<br><br>

14. From the VS Code terminal, run `Invoke-WebRequest` to verify that a new website has been created on each of your nodes:

Winagent:
    ```
    Invoke-WebRequest -URI http://winagent
    ```

Nixagent1:
    ```
    Invoke-WebRequest -URI http://nixagent1
    ```

  💡 **Tip:** Alternatively, you can minimize VS Code, open the Microsoft Edge browser and navigate to each web address.

---
## 🎈 **Congratulations!**
You created and updated the Apache and IIS manifest files and added the profiles to the roles. You then ran Puppet in no-op mode in the PE console and inspected the error messages in the reports. You then fixed the module dependencies, which resulted in creating a website on each of your nodes.

To continue, click **Next**.
