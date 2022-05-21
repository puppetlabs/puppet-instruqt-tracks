---
slug: specify-a-desired-state
id: zkwun505nnze
type: challenge
title: Specify a desired state
teaser: Specify how to keep the agent node in its desired state by adding a node definition
  and resource to the `site.pp` manifest.
notes:
- type: text
  contents: |-
    # Node classification
    When the primary server receives a catalog request from an agent node with a valid certificate, it begins a process called [*node classification*](https://puppet.com/docs/puppet/latest/glossary.html#classify) to determine what Puppet code to compile to generate a catalog for the agent. The primary server gets this information from the `site.pp` manifest.
- type: text
  contents: |-
    ## **The site.pp manifest**
    The `site.pp` manifest is a file on the Puppet server where you can write node definitions and specify your nodes' desired states.

    > **Node**: In the context of Puppet, a *node* is any system or device in your infrastructure.

    > **Node definition**: Defines how the primary server should manage a given system. When an agent contacts the server, the server checks the `site.pp` manifest for node definitions that match the node name. Node definitions enable you to assign specific configurations to specific nodes.

    For this example, working with `site.pp` is the easiest way to see how node classification works. You can also get node classification info in the PE console.

    When you’re ready to begin, click **Start**.
tabs:
- title: Primary Server
  type: terminal
  hostname: puppet
- title: Agent Node
  type: terminal
  hostname: linux-node
- title: Editor
  type: code
  hostname: puppet
  path: /etc/puppetlabs/code/environments/production/manifests/site.pp
- title: Lab Help Guide
  type: website
  url: https://puppet-kmo.gitbook.io/practice-lab-help/
difficulty: basic
timelimit: 450
---
# Step 1: Open the manifest file
Switch to the **Editor** tab and click on the only item in the **FILES** list, your `site.pp` manifest file.

# Step 2: Examine the definition of the agent node
As part of node classification, the server checks the manifest for node definitions, which start with declaring the node name:

node 'linux-node.classroom.puppet.com' {

}


Typically, you would include one or more *[class](https://puppet.com/docs/puppet/latest/glossary.html#class) declarations* inside this `node` block.

# Step 3: Add a resource declaration
Now add a resource declaration, which adds a resource to the catalog and describes that resource's state. Add the following node definition and resource declaration to the node definition section at bottom of the manifest:

✏️ **Customize your code:** In the code block below, replace `Hello Puppet` with your own custom message, which will be displayed on the next Puppet run.

```
node 'linux-node.classroom.puppet.com' {
  notify { 'Hello Puppet!': }
}
```

# Step 4: Save your changes
Click the disk icon: 💾

✅ **Result:** Now when the agent contacts the server, the server uses this node definition (among other things) to compile a catalog for this node.

# Step 5: Trigger an agent run
Now that you have some Puppet code for the server to parse, switch to the **Agent node** tab to the right and trigger a Puppet run:
```
puppet agent -t
```

✏️ **Note:**  In this example, the catalog includes only a `notify` resource type, which instructs the agent to display the message in the code when it applies the catalog on its next run. This code doesn't make any changes to the node.

✅ **Result:** The output from this Puppet run includes the following:

```
Notice: Hello Puppet!
Notice: /Stage[main]/Main/Node[agent.puppet.vm]/Notify[Hello Puppet!]/message: defined 'message' as 'Hello Puppet!'
```

Resource declarations define the desired state of that node. When a Puppet run is triggered, the server parses these declarations, builds the catalog, and sends it back to the agent. If the agent finds any resources that are not in the desired state, the agent makes the necessary changes to bring the resource into the desired state.

You can use multiple resource declarations to perform complex operations such as configuring a load balancer or defining hundreds of firewall rules - the sky's the limit.