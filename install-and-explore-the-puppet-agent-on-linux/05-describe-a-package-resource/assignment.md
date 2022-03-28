---
slug: describe-a-package-resource
id: 936x4nodyb0p
type: challenge
title: Describe a package resource
teaser: Use the `puppet resource` tool to describe a software package that doesn't
  yet exist on the node.
notes:
- type: text
  contents: |-
    So far, you’ve explored the `file` resource type. However, Puppet manages many types of resources, including:
    - `user`
    - `service`
    - `package`

    Puppet can also manage custom types — for example, types specific to a service or application, such as Apache `vhost` or MySQL `database`.

    In this challenge, you’ll use the agent to describe a software package that doesn't yet exist on the node.
tabs:
- title: Linux
  type: terminal
  hostname: linux
- title: Lab Help Guide
  type: website
  url: https://puppet-kmo.gitbook.io/practice-lab-help/
difficulty: basic
timelimit: 260
---
# Step 1
Run the following command to request a description of the relationship between the node and the Apache HTTP Server software package:

```
puppet resource package httpd
```

✅ **Result:** Because this package doesn't exist on the node, Puppet shows the `ensure => purged` parameter value pair.

The `purged` value is similar to the `absent` value. For a package resource, `purged` indicates that both the package and any configuration files typically installed by the package manager are both absent.

## What do you think?
What parameter could you add to the `puppet resource` command to instruct Puppet to *install* the package instead of just describing it? You’ll find out in the next challenge!

To go to the next challenge, click **Check**.