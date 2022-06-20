---
slug: use-resources-at-the-profile-layer
id: 8uyabtwy0kff
type: challenge
title: Use data types at the profile layer
teaser: Modify the apache profile to introduce data types into class parameters and
  set the Windows and Linux document roots.
notes:
- type: text
  contents: |-
    In this lab, you will:

    - Refactor the apache profile to introduce a `$port` class parameter of data type `Integer`.
    - Add a common setting for all nodes running Apache HTTP Server to use the same docroot via `common.yaml` and Hiera.
    - Deploy your code to production.

    Puppet only manages the resources that you declare. If a resource isn't specified in a Puppet manifest file, Puppet won't manage it.

    Click **Start** when you are ready to begin.
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
- title: Linux Agent 3
  type: terminal
  hostname: nixagent3
- title: Linux Agent 4
  type: terminal
  hostname: nixagent4
- title: Linux Agent 5
  type: terminal
  hostname: nixagent5
- title: Lab Help Guide
  type: website
  url: https://puppet-kmo.gitbook.io/practice-lab-help/
difficulty: basic
timelimit: 2400
---
Create a control repo on the Windows development workstation
========
1. On the **Windows Agent** tab, from the **Start** menu, open **Visual Studio Code**.
2. Enable autosave so that you don't have to remember to save your changes. Click **File** > **Auto Save**.
3. Open the `C:\CODE` directory. Click **File** > **Open Folder**, navigate to the `C:\CODE` directory and click **Select Folder**.

    ✏️ **Note:** If prompted to trust the code in this directory, click **Accept**.<br><br>

4. In Visual Studio Code, open a terminal. Click **Terminal** > **New Terminal**.
5. In the Visual Studio Code terminal window, run the following command:
    ```
    git clone git@gitea:puppet/control-repo.git
    ```


Edit the apache profile
========
1. Check out the **webapp** feature branch:
      ```
      cd control-repo
      git checkout webapp
      ```
2. Refactor the `profile::apache` code to move the site root and set data types. Replace the contents of `site-modules/profile/manifests/apache.pp` with the following code:
    ```
    # site-modules/profile/manifests/apache.pp
    class profile::apache (
      Integer $port,
      Stdlib::Absolutepath $docroot,
    ) {
      $index_html = "${docroot}/index.html"
      $site_content = "Hello world!"
      include apache
      apache::vhost { 'vhost.example.com':
        port    => $port,
        docroot => $docroot,
      }
      file { $docroot:
        ensure => directory,
      }
    }
    ```
3. Add a common setting for all nodes running the Apache HTTP Server to use the same docroot via `common.yaml` and Hiera. Navigate to **control-repo** > **data** > **common.yaml** and add following code to the file:
    ```
    profile::apache::docroot: var/web/cms
    ```
4. Commit and push your code:
    ```
    git add .
    git commit -m "Extend the apache profile"
    git push
    ```

    🔀 Switch to the **PE Console** tab.<br><br>

5. Log into the **PE console** with username `admin` and password `puppetlabs`.

6. Run Puppet, applying the `webapp` feature branch to the **Development** node group:
    1. Navigate to the **Node groups** page.
    2. Expand **All Environments** and click **Development environment**.
    3. Click **Run** > **Puppet**.
    4. For **Environment**, select **Select an environment for nodes to run in**.
    5. From the list, select `webapp` and then click **Run job** in the bottom-right corner.

    ✅ **Result:** The job fails because the filepath `var/web/cms` is not an absolute filepath. Nothing is misconfigured; Puppet just failed to compile a catalog.

    🔀 Switch to the **Windows Agent** tab.<br><br>

7. Find and fix the data in Hiera. Update the content in the `common.yaml` file to the following:
    ```
    profile::apache::docroot: /var/web/cms
    ```
8. Commit and push your code:
    ```
    git add .
    git commit -m "Extend the apache profile"
    git push
    ```
    🔀 Switch to the **PE Console** tab.<br><br>

9. Run Puppet, applying the `webapp` feature branch to the **Development** node group:
    1. Navigate to the **Node groups** page.
    2. Expand **All Environments** and click **Development environment**.
    3. Click **Run** > **Puppet**.
    4. For **Environment**, select **Select an environment for nodes to run in**.
    5. From the list, select `webapp` and then click **Run job** in the bottom-right corner.

    ✅ **Result:** Observe the failure. The apache class failed because the directory was not managed before the vhost.

    🔀 Switch to the **Windows Agent** tab.<br><br>

10. Navigate to `site-modules/profile/manifests/apache.pp` and update your code to the following:
    ```
      # site-modules/profile/manifests/apache.pp
      class profile::apache (
        Integer $port,
        Stdlib::Absolutepath $docroot,
      )
      {
        $index_html = "${docroot}/index.html"
        $site_content = 'Hello world!'
        include apache
        apache::vhost { 'vhost.example.com':
          port    => $port,
          docroot => $docroot,
          # Add a resource relationship, required before the vhost is managed.
          require => File[$index_html],
        }
        # Puppet manages only the resources that are declared. It will not automagically create parent directory of /var/web/cms!
        file { '/var/web':
          ensure => directory,
        }
        file { $docroot:
          ensure => directory,
        }
        file { $index_html:
          ensure  => file,
          content => $site_content,
        }
      }
      ```
10. In the terminal, navigate to `control-repo/site-modules/profile` and run `pdk validate` to check your code.
    ```
    pdk validate
    ```
11. Run `cd ../..` to return to the top-level directory in the control repo.

12. Commit and push your code.
    ```
    git add .
    git commit -m "Extend the apache profile"
    git push
    ```

    🔀 Switch to the **PE Console** tab.<br><br>

13. Run Puppet in your `webapp` environment on your **Development** node group:
    1. Navigate to the **Node groups** page.
    2. Expand **All Environments** and click **Development environment**.
    3. Click **Run** > **Puppet**.
    4. For **Environment**, select **Select an environment for nodes to run in**.
    5. From the list, select `webapp` and then click **Run job** in the bottom-right corner.

    ✅ **Result:** The job runs successfully.

    🔀 Switch to the **Windows Agent** tab.<br><br>

14. Release your changes:
    1. Merge your feature branch to production:
        ```
        git checkout production
        git merge webapp
        git push
        ```
    🔀 Switch to the **PE Console** tab.<br><br>

    2. Run Puppet on all the production nodes:
        1. Navigate to the **Node groups** page.
        2. Expand **All Environments** and click **Production environment**.
        3. Click **Run** > **Puppet** and then click **Run job**.

    ✅ **Result:** The jobs succeed on the production nodes nixagent4 and nixagent5.

---
## 🎈 **Congratulations!**
In this lab, you used file resources in your Apache profile to manage website content before deploying your code to production.