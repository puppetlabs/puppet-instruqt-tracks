---
slug: working-with-the-package-data-collector
id: kcnxqq8o1o5d
type: challenge
title: View and manage packages
teaser: Enable package collection and view the package collection report.
notes:
- type: text
  contents: |-
    ## Scenario

    Your team lead has given you the following list of packages and notes about the roles of the servers that have those packages installed:

    <img src="https://storage.googleapis.com/instruqt-images/PE-deploy-and-discover/lab-3.1-scenario-img.png">

    Click the arrow to the right (**>**) to continue.
- type: text
  contents: |-
    Your team lead wants you to generate reports that show:

    - Which packages are installed on all the nodes in your environment.
    - Which nodes are web servers. From the documentation your team lead gave you, you know that web servers have the **httpd** package installed.

    To complete these tasks, you'll enable package data collection and run Puppet to collect the data. Then, you'll view the package output in the console and generate reports.

    When you know which nodes fulfill which roles, you could also define a **role** fact to group and count servers based on their functional role. You could use this information to collect configuration and performance data about a specific node group (but you won't do that in this lab).

    Click the arrow to the right (**>**) to continue.
- type: text
  contents: |-
    By default, package data collection is disabled, so the Packages page in the PE console doesn't show any data.

    You can choose to collect package data on all your nodes or just a subset. Any node with a recent version of the Puppet agent installed can report package data, including nodes that do not have active configurations defined on the primary server.

    This lab takes about 5 minutes to spin up. When the **Start** button appears, click it to begin.
tabs:
- title: PE Console
  type: service
  hostname: puppet
  path: /
  port: 443
- title: Lab Help Guide
  type: website
  url: https://puppet-kmo.gitbook.io/practice-lab-help/
difficulty: basic
timelimit: 1500
---
Enable package data collection
========
1. Log into the PE console with username `admin` and password `puppetlabs`.

2. From the console sidebar, navigate to the **Node groups** page, expand (click **+**) **PE Infrastructure**, and click the **PE Agent** node group.

3. On the **Classes** tab, notice that the `puppet_enterprise::profile::agent` class has already been added to this node group, along with a couple of class-specific parameters.

4. Enable package data collection.
    1. In the **Parameter name** list for the class, select the `package_inventory_enabled` parameter and set it to `true`.
    2. Click **Add to node group**.
    3. Commit your change by clicking **Commit** near the bottom of the page.<br><br>

5. Run Puppet to apply the change to the nodes in the **PE Agent** node group.
    1. Click **Run > Puppet** near the upper-right corner of the page.
    2. Notice the node details, and leave the options with the default values shown.
    3. Click **Run job** near the bottom of the page.

    ✏️ **Note:** This might take a few moments to complete (monitor the job status near the upper-right corner of the page).

    ✅ **Result:** On this Puppet run, Puppet enables package inventory collection. On subsequent Puppet runs, Puppet collects package data and reports it on the **Packages** page.<br><br>

6. To start collecting and reporting package data, run Puppet a second time.
    1. In the upper right of the **Job details** page, click **Run again > All nodes**.
    2. Click **Run job** to start the second Puppet agent run.
    3. Notice the job status near the upper-right corner of the page.


View and manage package inventory
========
1. From the console sidebar, navigate to the **Packages** page.

2. For this scenario, you're trying to find the app servers, web servers, and load balancers by searching for the packages listed in the table below:
    1. Enter the name or partial name of a package in the **Filter by package name** field and click **Apply**.
    2. In the results list, click the package name, and notice which nodes have the package installed.
    3. Repeat this for all the packages in the table.

    | Package Name        | Server Role   | Server Name |
    |---------------------|---------------|-------------|
    | Java 8              | App server    | ??          |
    | httpd               | Web server    | ??          |
    | nginx               | Load balancer | ??          |


Create a report of all packages installed in your environment
========
1. On the **Packages** page, remove any filters from the previous steps.
2. Right-click **Export Data** and click **Save link as**.
3. Download the CSV file to your local machine and review it.

Create a report that lists the web servers (nodes that have the httpd package installed)
========
1. On the **Packages** page, in the **Filter by package name** field, enter **httpd** and click **Apply**.
2. In the results, click **httpd**.
3. Right-click **Export Data**, and then click **Save link as**.
4. Download the CSV file to your local machine and review it.

---
## 🎈 **Congratulations!**
You enabled package data collection and used the information to discover the roles of the nodes in your environment.
To continue, click **Next**.