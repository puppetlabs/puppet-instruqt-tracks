---
slug: explore-resource-syntax-by-using-the-puppet-agent
id: zhyswco37bif
type: challenge
title: Explore resource syntax by using the Puppet agent
teaser: Request a description of a resource and review the output.
notes:
- type: text
  contents: |-
    # What is a resource?
    Resources are the single units of a system that you want to manage, such as users, files, services, or packages.

    One of Puppet's core concepts is the *resource abstraction layer*, whereby information about a resource is represented in Puppet code. To view and modify information about resources, run the `puppet resource` command, which becomes available after you install the agent.

    Click **Start** when you’re ready to begin.
tabs:
- title: Linux
  type: terminal
  hostname: linux
- title: Lab Help Guide
  type: website
  url: https://puppet-kmo.gitbook.io/practice-lab-help/
difficulty: basic
timelimit: 200
---
# Step 1
Request a description of a file resource by running the following command:
```
puppet resource file /tmp/test
```
✅ **Result:** The command returns a Puppet code representation of the resource.

## Resource syntax
Let’s break down the output into its basic components:
```
type { 'title':
  parameter => 'value',
}
```
**Type —** Describes what the resource is. In this case, a file.

**Title —** A unique name that Puppet uses internally to identify the resource. In this case, it’s the file path and name, **/tmp/test**.

**Attributes** — A bracketed list of parameter => value pairs that specifies the state of the resource and its relationship to the node. A resource can have many parameter values.

In this example, the agent reports that the file is absent, which means the file does not exist. Yet.

To go to the next challenge, click **Next**.