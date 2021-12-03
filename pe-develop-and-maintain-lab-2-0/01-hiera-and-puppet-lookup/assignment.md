---
slug: hiera-and-puppet-lookup
id: pjzdkzqxxmfh
type: challenge
title: Hiera and Puppet Lookup
teaser: In this lab you will use the puppet lookup command on your primary server
  to discover how hiera looks for data based on your hiera.yaml configuration and
  your node facts.
tabs:
- title: Primary Server
  type: terminal
  hostname: puppet
- title: Windows Agent
  type: service
  hostname: guac
  path: /#/client/c/winagent?username=instruqt&password=Passw0rd!
  port: 8080
- title: Linux Agent 1
  type: terminal
  hostname: nixagent1
- title: Linux Agent 2
  type: terminal
  hostname: nixagent2
- title: Linux Agent 3
  type: terminal
  hostname: nixagent3
- title: Git Server
  type: service
  hostname: gitea
  path: /
  port: 3000
difficulty: basic
timelimit: 600
---
1. Check each your node's certnames by logging in to each node and running:
`puppet config print certname   # you will need this in the next step`.

2. Logon to your primary server and run puppet lookup to lookup data for each node:
```
puppet lookup profile::base::login_message --explain --node <node certname>puppet lookup profile::base::ntp_servers --explain --node <node certname>
```
3. Check the `hiera.yaml` file in your control-repo to verify the hierarchies against the puppet lookup command output.

4. What were the facts that affected the lookup? Login to each node and check the facts that are used in the hierarchy of the `hiera.yaml` configuration file.

5. Are all facts present on both nodes? Why did Hiera retrieve data from `common.yaml` for Node B?