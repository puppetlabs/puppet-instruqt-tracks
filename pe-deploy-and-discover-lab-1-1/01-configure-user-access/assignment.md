---
slug: configure-user-access
id: hu8et40y7pvb
type: challenge
title: Configure user access
teaser: Create a user and assign them the default Viewer role.
notes:
- type: text
  contents: |-
    In this lab, you will create a Puppet Enterprise (PE) user and assign them the default Viewer role (which has limited permissions) from the PE console.

    User roles are sets of permissions that you assign to users. In PE, you assign roles to users (or groups of users), rather than assigning specific permissions to individual users.

    Managing access based on roles — or, role-based access — is more efficient than managing user permissions on a per-user basis.

    Click **Start** when you're ready to begin.
tabs:
- title: PE Console
  type: service
  hostname: puppet
  port: 443
  url: https://puppet-8443-INSTRUQT_PARTICIPANT_ID.env.play.instruqt.com
- title: Lab Aid
  type: website
  hostname: puppet
  url: https://puppet-kmo.gitbook.io/lab-aids/-MZKPjwKRKKFuXxxy7ge/pe101/configure-user-access
difficulty: basic
timelimit: 3600
---
1. On the **PE Console** tab, log in with username `admin` and password `puppetlabs`.<br><br>✏️ **Note:** If the console doesn't load correctly, refresh your browser window.

2. From the console sidebar, click **Access Control**.

3. Add the user. In the **Full name** field, enter the user's name using standard capitalization and spacing.<br><br>✏️ **Note:** Not sure what name to use? Feel free to use your own!

4. Add the user's login info. In the **Login** field, enter a username, for example, `firstname.lastname`. Use a naming convention that easily maps to the user's actual name. Then, click **Add local user**.<br><br>✔️ **Result:** The name is added to the list.

5. Open the **User details** page by clicking the username.

6. Generate a password for the user. In the top-right corner of the page, click **Generate password reset**, copy the link, and then click **Close**.

7. Paste the link into a new web browser tab. Then, enter a new password and click **Reset password**.<br><br>✏️ **Note:** Choose a memorable password — you'll use it to log in on the final step.

8. Close the browser tab and go back to the **PE Console** tab within the lab. In the sidebar, click **Access Control**, and then click the **User roles** tab.

9. Assign the Viewer role to the new user. In the list of roles, click **Viewers**. On the **Member users** tab, select the new user from the **User name** list, and then click **Add user**.

10. Commit your changes — see the button in the bottom-right corner of the page.

11. To verify the settings, log in as the new user: In the console sidebar, click **Log out**, and then log in again with the username and password that you set in steps 4 and 7. From here you can explore your user settings.

<br>🎈 **Congratulations!** Using the PE console, you created a user and assigned them the Viewer role, which has limited permissions in PE.

<br>To close this lab, click **Next**.