---
slug: refactor-profiles-with-parameters
id: w2ebaevntvrz
type: challenge
title: Refactor the apache web server profile
teaser: Extend the apache profile by using a class parameter to abstract port information.
  Then, deploy your code to production.
notes:
- type: text
  contents: |-
    In this lab you will:

    - Run a PQL query to get the list of nodes in the dc-west data center.
    - Extend the apache profile by using a class parameter to abstract port information.
    - Test your changes by running Puppet against a specific node group.
    - Test your changes incrementally in a canary release. Within the subset of nodes in the canary release, you'll run Puppet in no-op mode and run it again normally.
    - Deploy code to the production environment.

    Click **Start** when you are ready to begin.
tabs:
- title: PE Console
  type: service
  hostname: puppet
  path: /
  port: 443
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
timelimit: 1500
---
Identify nodes in the dc-west data center
========
1. Log into the **PE console** with username `admin` and password `puppetlabs`.
2. Retrieve the list of nodes with the trusted fact `pp_datacenter=dc-west`:
    1. Navigate to the **Nodes** page.
    2. From the **Filter by** list, choose **PQL Query**.
    3. From the **Common queries** list, choose **Nodes with a specific fact and fact value**.
    4. Copy the following code into the query box and click **Submit query** to get the list of nodes:
    ```
    inventory[certname] { trusted.extensions.pp_datacenter = "dc-west" }
    ```
✅ **Result:** Observe which nodes are returned by the query. These nodes need their web service port configured to 8080.

Develop profiles to externalize node data
========
🔀 Switch to the **Windows Agent** tab.

1. On the **Windows Agent** tab, from the **Start** menu, open **Visual Studio Code**.
2. Enable autosave so that you don't have to remember to save your changes. Click **File** > **Auto Save**.
3. Open the `C:\CODE` directory. Click **File** > **Open Folder**, navigate to the `C:\CODE` directory, and click **Select Folder**.

    ✏️ **Note:** If prompted to trust the code in this directory, click **Accept**.<br><br>

4. Open a new terminal. Click **Terminal** > **New Terminal**.
5. In the VS Code terminal window, run the following command:
    ```
    git clone git@gitea:puppet/control-repo.git
    ```
6. Check out the `webapp` feature branch to inspect some preconfigured Hiera data:
    ```
    cd control-repo
    git checkout webapp
    ```

7. Navigate to **control-repo** > **site-modules** > **profile** > **manifests** > **apache.pp** and replace the existing code with the following code to extend the apache profile. Note the `$port` variable:

    ```
    # site-modules/profile/manifests/apache.pp
    class profile::apache (
        $port,
    )
    {
        $docroot = '/var/www'
        $index_html = "${docroot}/index.html"
        $site_content = 'Hello world!'
        include apache
        apache::vhost { 'vhost.example.com':
          port    => $port,
          docroot => $docroot,
      }
    }
    ```
8. In the terminal window, navigate to `site-modules/profile` and check your code by running `pdk validate` in the terminal window.

9. Run `cd ../..` to return to the top-level directory in the control repo.

10. Commit, push, and deploy your code:
    ```
    git add .
    git commit -m "Extend the apache profile"
    git push
    ```

Run Puppet against the Development node group
========
🔀 Switch to the **PE Console** tab.

1. <a name="runpuppet">Run Puppet on your development node group:</a>
    1. Navigate to the **Node Groups** page.
    2. Expand **All Environments** and click **Development environment**.
    3. Click **Run** > **Puppet**.
    4. Under **Environment**, select **Select an environment for nodes to run in:**.
    5. From the list, select `webapp` and then click **Run job** in the bottom-right corner.
    ✅ **Result:** The job fails on all nixagent nodes.<br><br>

2. Click the report link for one of the nodes, and on the **Log** tab, find an error message similar to the following:
    ```
    Could not retrieve catalog from remote server:
    Error 500 on SERVER: Server Error: Evaluation Error:
    Error while evaluating a Function Call, Class[Profile::Apache]:
    expects a value for parameter 'port'
    ```
    ✅ **Result:** The catalog didn't compile because the Hiera data does not yet exist and there is no default value for the parameter.

Edit the Hiera data
========
🔀 Switch to the **Windows Agent** tab.


1. Add Hiera data for both `dc-west.yaml` and `common.yaml` configurations. Create the `data/datacenter/` directory and relevant files:
    1. Navigate to **control-repo** > **data**.
    2. Right-click the `data` directory and then click **New Folder**. Name the new folder `datacenter`.
    3. Right-click the `datacenter` directory and then click **New File**. Name the new file `dc-west.yaml` and paste in the following contents. Note the `port` value:
        ```
        # <control-repo>/data/datacenter/dc-west.yaml
        ---
        profile::apache::port: 8080
        ```
    4. Open `common.yaml` and append the following code to the end of the file:
        ```
        # <control-repo>/data/common.yaml
        profile::apache::port: 80
        ```

2. Navigate to `control-repo/hiera.yaml` and add the required Hiera layer for `pp_datacenter` by updating the file with the following content. Note the new `datacenter` path beneath the `department` path:
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
            - "department/%{trusted.extensions.pp_department}.yaml"
            - "datacenter/%{trusted.extensions.pp_datacenter}.yaml"
            - "common.yaml"
    ```
3. Commit, push, and deploy the code:
    ```
    git add .
    git commit -m "Add Apache configuration YAML"
    git push
    ```

    🔀 Switch to the **PE Console** tab.<br><br>


4. Run Puppet on the **Development environment** node group again (if you need a refresher, [refer back to step 1](#runpuppet) in this section).

    ✅ **Result:** Notice that the run is successful.

    🔀 Switch to the **Windows Agent** tab.<br><br>


5. Test the port updates by running a web request on each node:

    dc-west:
    ```
    Invoke-WebRequest -URI http://nixagent1:8080
    ```
    dc-east
    ```
    Invoke-WebRequest -URI http://nixagent3:80
    ```

    🔀 Switch to the **PE Console** tab.<br><br>


6. Create a one-time run exception group as a child of the **Production** group:
    1. Navigate to the **Node Groups** page.
    2. Click **Add group**.
    3. Set the new group attributes as follows. Make sure that you select the **Environment group** checkbox.
          | Parent Name            | Group Name                              | Environment     |
          |------------------------|-----------------------------------------|-----------------|
          | Production environment | Production Agent-Specified One-Time Run | agent-specified |

    4. Enter a description.
    6. Click **Add**.

Pin a node and perform a canary release of the `webapp` branch to a Production node
========
1. Pin a production node to the agent-specified environment. Your choices are nixagent4 or nixagent5:
    1. Navigate to the **Node Groups** page.
    2. Expand **All Environments**, expand **Production environment**, and click **Production Agent-Specified One-Time Run**.
    3. In the **Certname** field, click **node name** and select either **nixagent4** or **nixagent5**.
    4. Click **Pin node** and then commit your changes (click **Commit 1 change** in the bottom-right corner).<br><br>

2. Run Puppet in no-op mode, specifying the feature branch environment:
    1. Click **Run** > **Puppet**.
    2. Choose **Select an environment for nodes to run in:** and then choose **webapp** from the list.
    3. Select the **No-op** checkbox and then click **Run job**.
    ✅ **Result:** Notice that the run was successful.<br><br>

3. Run Puppet in normal mode, specifying the feature branch environment:
   1. Click **Run** > **Puppet**.
   2. Choose **Select an environment for nodes to run in:** and then choose **webapp** from the list. This time, **do not** select the **No-op** checkbox.
    ✅ **Result:** Notice that the run was successful.<br><br>

4. Unpin the node from the agent-specified environment:
    1. Navigate to the **Node Groups** page.
    2. Expand **All Environments**, and then expand **Production environment** and click **Production Agent-Specified One-Time Run**.
    3. Click **Unpin** (located at the right of page) and then click **Commit 1 change**.

    🔀 Switch to the **Windows Agent** tab.<br><br>

5. Release your changes:
    1. Merge the `webapp` branch to the production branch.
        ```
        git checkout production
        git merge webapp
        git push
        ```

    🔀 Switch to the **PE Console** tab.<br><br>

6. Run Puppet on all the production nodes.

    1. Navigate to the **Node Groups** page.
    2. Expand **All Environments** and then click **Production environment**.
    3. Click **Run** > **Puppet**.
    4. For **Environment**, select the radio button for **Select an environment for nodes to run in:**.
    5. From the list, select **Production** and then click **Run job**.<br><br>

7. Both production nodes (nixagent4 and nixagent5) should return with a successful run. Run the following commands from a Powershell session on the Winagent to verify they ran successfully:

    **dc-east**:
    ```
    Invoke-WebRequest -URI http://nixagent4:80
    ```
    **dc-west**:
    ```
    Invoke-WebRequest -URI http://nixagent5:8080
    ```

    ✅ **Result:** Nixagent4 and Nixagent5 ran successfully.

---
## 🎈 **Congratulations!**
In this lab, you ran a PQL query to get the list of nodes in the **dc-west** data center. Next, you extended the apache profile by using a class parameter to abstract port information. You tested your changes by running Puppet against a specific node group. You then tested your changes incrementally in a canary release. Finally, within the subset of nodes in the canary release, you ran Puppet in no-op mode and then ran it again normally.

<style type="text/css" rel="stylesheet">
ol { margin-left: 20px; }
</style>
