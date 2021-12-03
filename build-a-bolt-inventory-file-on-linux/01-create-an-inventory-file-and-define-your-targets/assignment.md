---
slug: create-an-inventory-file-and-define-your-targets
id: 69ibjvibsm9i
type: challenge
title: " Create an Inventory File and Define Your Targets \U0001F4C4"
teaser: Group targets by a common operating system or functional role to streamline
  orchestration tasks.
notes:
- type: text
  contents: |-
    In this challenge, you will create a Bolt project, and then populate its inventory file so that you can manage targets by group name. A Bolt project is a directory that contains the project files, configuration files, and data to run a workflow. The project's `inventory.yaml` file is where you define groups of targets and connection information.

    Grouping your targets enables you to run Bolt commands against the group instead of having to reference each target individually.

    ## **Start this track**
    When your environment has finished spinning up, you'll see a green **Start** button at the bottom of the screen (this takes about 1 minute). Click it when you're ready to begin the track.
tabs:
- title: Bolt
  type: terminal
  hostname: puppet
- title: Editor
  type: code
  hostname: puppet
  path: /root
- title: Platform Help
  type: website
  hostname: puppet
  url: https://puppet-kmo.gitbook.io/instruqt-platform-help/
difficulty: basic
timelimit: 720
---
When you create a Bolt project by running the ```bolt project init``` command, Bolt creates an inventory file with placeholder content in the project directory. The project directory also contains configuration files, plans, and tasks.

# Step 1: Create and navigate to your project directory
At the command prompt on the Bolt tab to the left, type the following command (you can also copy it and paste it at the command prompt).

 ```
 mkdir myproject && cd myproject
 ```

# Step 2: Create the Bolt project
Then, run:

 ```
 bolt project init
 ```

✏️ **Note:** For this simple example, you can omit the project name, which would follow `init`. Project names must begin with a lowercase letter and can contain only lowercase letters, numbers, and underscores.

You might create multiple Bolt projects, each with its own purpose, such as managing database servers, patching Windows machines, or completing greenfield deployment tasks.

If multiple projects run against the same inventory, they can share an inventory file so you don't need to maintain your inventory in each project. For details, search for "inventory files" in the [Bolt documentation](https://puppet.com/docs/bolt/latest/bolt.html).

# Step 3: View the inventory.yaml file
On the **Editor** tab, expand **myproject** and open `inventory.yaml`.
<img src="https://storage.googleapis.com/instruqt-images/Build-a-bolt-inventory-file-on-linux/myproject-2.png">
 Notice that the file contains only placeholder content.

# Step 4: Update the inventory file content
The following code defines a group named **webservers**, made up of targets web1 and web2. Copy the code into the inventory file, replacing the placeholder content.

✏️ **Note:**  For this example, Bolt connects to the **webservers** targets over SSH and skips the host key validation.
   - In a self-contained, isolated environment (such as this lab) you can skip checking the host key.
   - In a typical production environment, make sure to have SSH server host key policies for distributing and validating keys during SSH client connections.

    ---
    groups:
      - name: webservers
        targets:
          - web1
          - web2
        config:
          transport: ssh
    config:
      ssh:
        host-key-check: false

# Step 5: Save your changes

Click the disk icon beside the file name (💾) and then click the **Bolt** tab.

# Step 6: Verify that your targets are correct
On the **Bolt** tab, check that the targets are specified correctly. Run the following command to show the list of targets that Bolt commands run against:
```
bolt inventory show --targets all
```

✔️ **Result:** If your inventory file is set up correctly, you'll see the following output, which includes the number of targets in the group and their names:

    Targets
      web1
      web2
    Inventory source
      /root/myproject/inventory.yaml
    Target count
      2 total, 2 from inventory, 0 adhoc
    Additional information
      Use the '--detail' option to view target configuration and data


If your file isn't correct, go back to step 4 and try again.

Click **Check** to continue.
