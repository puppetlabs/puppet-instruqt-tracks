---
slug: modify-a-file-resource
id: y7jzqqkgnqww
type: challenge
title: Modify a file resource
teaser: Use the `puppet resource` tool to add content to an empty file, and then view
  the file contents.
notes:
- type: text
  contents: Next, you’ll run the **puppet resource** command to add content to the
    empty file.
tabs:
- title: Linux
  type: terminal
  hostname: linux
- title: Lab Help Guide
  type: website
  url: https://puppet-kmo.gitbook.io/practice-lab-help/
difficulty: basic
timelimit: 300
---
Running the `puppet resource` command with a `parameter=value` argument instructs Puppet to modify the resource to match that value.

✏️ **Note:** While this is a great way to test changes in a development environment, running manual commands is not a robust way to specify a node's desired state. In a real installation, you add Puppet code that describes the desired state to classes and modules, known as the *codebase*. Puppet then uses the codebase to manage your infrastructure so that you don't have to manage it manually.

# Step 1
Run the following command:

```
puppet resource file /tmp/test content='Hello Puppet!'
```

✅ **Result** Notice the output as Puppet checks the hash of the existing content against the new content that you provided. When Puppet determines that the hashes don't match, it sets the file content to the value of the `content` parameter.

# Step 2
Show the file content:

```
cat /tmp/test
```
✅ **Result** The system shows the file contents: *Hello Puppet!*


To go to the next challenge, click **Check**.