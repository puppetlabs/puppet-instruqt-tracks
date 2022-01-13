---
slug: describe-a-file-resource
id: qoptwf0kdkvj
type: challenge
title: "Describe a file resource \U0001F4BB"
teaser: Create an empty file. Then, request a description of it and review the output.
notes:
- type: text
  contents: In the previous challenge, you requested a description of a file that
    doesn't exist. Let’s see what you get for a real file.
tabs:
- title: Linux
  type: terminal
  hostname: linux
- title: Practice Lab Help
  type: website
  url: https://puppet-kmo.gitbook.io/practice-lab-help/
difficulty: basic
timelimit: 400
---
# Step 1
Run the following command to create an empty file in the same path as in the previous challenge:

```
touch /tmp/test
```

✔️ **Result:** The system created an empty file named `test` at `/tmp`.

# Step 2
Run the `puppet resource` command to see how the file is represented in Puppet's resource syntax:

```
puppet resource file /tmp/test
```

✔️ **Result:** The output includes the file owner, when it was created, and when it was last modified.

## The content hash
The content parameter value might not be what you expected for an empty file. When the resource tool interprets a file, it converts the content into an SHA256 hash. Puppet uses this hash to compare the content of the file to what it expects.

To go to the next challenge, click **Check**.