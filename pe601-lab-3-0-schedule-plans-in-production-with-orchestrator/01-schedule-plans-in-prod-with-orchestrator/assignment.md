---
slug: schedule-plans-in-prod-with-orchestrator
id: sf7hpmojacjx
type: challenge
title: Schedule plans to run in production with Puppet orchestrator
notes:
- type: text
  contents: |-
    In this lab, you will:
    - Use the PE console to:
        - Run Puppet Query Language (PQL) to identify development nodes.
        - Test a Puppet plan against development nodes.
    - Verify that backup directories have been created.
    - Create a service account to secure running the backup plan in production.
    - Use PQL and an access token to schedule a plan run for production with the Orchestrator API.
    - Verify that backup directories were created on the production node.
tabs:
- title: PE Console
  type: service
  hostname: puppet
  port: 443
- title: Windows Agent 1
  type: service
  hostname: guac2
  path: /#/client/c/winagent1?username=instruqt&password=Passw0rd!
  port: 8080
- title: Linux Agent 1
  type: terminal
  hostname: nixagent1
- title: Linux Agent 2
  type: terminal
  hostname: nixagent2
- title: Primary Server
  type: terminal
  hostname: puppet
- title: Windows Workstation
  type: service
  hostname: guac
  path: /#/client/c/workstation?username=instruqt&password=Passw0rd!
  port: 8080
- title: Git Server
  type: service
  hostname: gitea
  path: /
  port: 3000
- title: Bug Zapper
  type: website
  url: https://docs.google.com/forms/d/e/1FAIpQLSdNqjFgi9Acryyoz6swH7oKx2EaC6cbD57bg2LCYb9K1TMjzw/viewform?embedded=true
- title: Lab Help
  type: website
  url: https://puppet-kmo.gitbook.io/instruqt-platform-help/
difficulty: basic
timelimit: 2700
---
Use PQL to identify development nodes from the console
========
1. On the **PE Console** tab, log in with the username `admin` and password `puppetlabs`.
2. Navigate to the **Nodes** page.
3. In the **Filter by** list, choose **PQL query** and then select **Nodes assigned to a specific environment (example: production)**.
4. Update the query text to the following:
    ```
    nodes[certname] { catalog_environment = "development" }
    ```
5. Run the query by clicking **Submit query**.
6. Copy the node name results to a local text editor. You'll use these in the next section.

Use the console to test a Puppet plan against development nodes
========

1. Navigate to the **Plans** page.
2. Click **Run a plan** (top-right corner of the page).
3. Click into the **Code environment** field and choose **development**.
4. Click into the **Plan** field, scroll down and choose **nginx::backup_all_logs**.
5. In the **Plan parameters** section, for the **targets = Value** field, paste the agent node names you copied earlier, using a comma separator between node names.
6. Click **Run job**.
✔️ **Result:** The page automatically refreshes to show that the plan completes successfully.

Verify the backup directories have been created on the development nodes
========

🔀 Switch to the **Windows Agent 1** tab.<br><br>
✏️ **Note:** If you've been disconnected, click **Reconnect** to connect to the Windows agent.<br><br>
1. In the system tray, click the **Windows Explorer** icon.
1. Navigate to **This PC** > **Local Disk (C:)** > **backups**.
2. Double-click the date-stamped directory and notice that the NGINX log files (`access.log`, `error.log`) have been backed up.

🔀 Switch to the **Linux Agent 2** tab.<br><br>
1. Run the following command to change directories into the backups directory:
    ```
    cd /var/backup
    ```
2. Run `ls` to show the date-stamped backup directory.
3. Change directories into the date-stamped directory and observe the NGINX log files that have been backed up (replace the directory name between the `<>`):
    ```
    cd <DATE-STAMPED DIRECTORY>
    ```
4. Run `ls` to show the backup files contained in the directory (`access.log`, `error.log`).

Create a service account to secure running the backup plan in production
========
🔀 Switch to the **PE Console** tab.<br><br>

2. Click navigate to **Access Control**.
3. Create a new role. On the **User roles** tab, in the **name** field, enter the following:
    ```
    plan_automation_service
    ```
4. Click **Add Role**.
5. Click the **plan_automation_service** link that now appears in the list.
6. Click the **Permissions** tab.
7. Add the following permissions to the role, clicking the **Add** button after each selection:
    - Plans > Run Plans > nginx::backup_all_logs
    - Job Orchestrator > Start, stop, and view jobs<br><br>
8. Click **Commit 2 changes**.
9. Return to the **Access Control** page.
10. Add a new user account:

    Full name:
    ```
    plan_automation_service_account
    ```
    Login:
    ```
    plan_automation_service_account
    ```
11. Click **Add local user**.
12. Click the **User roles** tab, then click the **plan_automation_service** link.
12. From the list, choose **plan_automation_service_account** and then click **Add user**.
13. Click **Commit 1 change** to add the new service account to the **plan_automation_service** role..
14. Click the **plan_automation_service_account** link and then click **Generate password reset**.
15. Copy the link into a new browser tab, enter the password **puppetlabs**, and click **Reset password**.
16. Close the browser tab and then click the **Close** link in the PE console.

Use PQL and an access token to schedule a plan run for production with the orchestrator API
========

🔀 Switch to the **Primary Server** tab.<br><br>

1. Create an access token for your service account user credentials by running the command below. Enter the password **puppetlabs** when prompted:
    ```
    puppet access login plan_automation_service_account -t /root/.puppetlabs/token.plan-svc-acct
    ```
3. Create a variable to hold the authentication header needed to make the API call by running the following command in the terminal and then copying and pasting your token value where specified:
    ```
    header="X-Authentication: $(cat /root/.puppetlabs/token.plan-svc-acct)"
    ```
4. Use PQL to find all of the non-PE server nodes in the production environment:
    ```
    puppet query 'nodes[certname] { catalog_environment = "production" and certname !~ "puppet." }'
    ```
5. Using a PQL query and the `jq` utility, create a variable to hold the list of production nodes:
    ```
    node_list=$(puppet query 'nodes[certname] { catalog_environment = "production" and certname !~ "puppet." }' | jq 'map(.certname)  | join(",")')
    ```
6. Create a date variable with a timestamp of two minutes from now:
    ```
    run_date=$(date -d '2 minutes' +"%Y-%m-%dT%H:%M:%S%z")
    ```
7. Run the following command to schedule your plan run using curl and the variables you created:
    ```
    curl -X POST -k -H "$header" https://localhost:8143/orchestrator/v1/command/schedule_plan \
    --data-binary @- << EOF
    {
    "environment": "production",
    "plan": "nginx::backup_all_logs",
      "params": {
        "targets": $node_list
      },
      "scheduled_time": "$run_date"
    }
    EOF
    ```

🔀 Switch to the **PE Console** tab.<br><br>
1. Navigate to the **Plans** page.
9. Click **Scheduled Plans** to view your scheduled plan.
✔️ **Result:** In two minutes the scheduled plan runs and disappears from the scheduled plans list.

Verify the backup directories have been created on the production node
========

🔀 Switch to the **Linux Agent 1** tab.<br><br>

1. Run the following command to change directories into the backups directory:
    ```
    cd /var/backup
    ```
2. Run `ls` to show the date-stamped backup directory.
3. Change directories into the date-stamped directory and observe the NGINX log files that have been backed up (replace the directory name between the `<>`):
    ```
    cd <DATE-STAMPED DIRECTORY>
    ```
5. Run `ls` to show the backup files (`access.log`, `error.log`) contained in the directory.



---
🎈 **Congratulations!** In this lab, you tested your Puppet plan to backup NGINX log files on nodes in the development environment. Then, you configured role-based access control (RBAC) for a service account user with permissions to run the plan on production agent nodes. Finally, you configured a scheduled job using the `schedule_plan` API endpoint to run the backup logs plan on your production Linux node and verified that it completed successfully.

---
**Find any bugs or have feedback? Click the **Bug Zapper** tab near the top of the page and let us know!**

When you're ready to close the lab, click **Next**.