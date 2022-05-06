---
slug: inspect-the-agent-catalog
id: rl9eexqbjtq4
type: challenge
title: Inspect the agent catalog
teaser: See what the Puppet agent manages out of the box.
notes:
- type: text
  contents: |-
    In this lab you will:

    * Run Puppet and explore the Puppet run lifecycle.

    * Inspect the agent catalog — built during the Puppet run — to see what the Puppet agent manages out of the box.

    In this lab, you'll use only the Linux agent (on the Linux Agent tab). Feel free to explore the PE console and primary server command line available on the other tabs. To log into the PE console, use userid `admin` and password `puppetlabs`.

    Click **Start** when you're ready to begin.
tabs:
- title: Linux Agent
  type: terminal
  hostname: nixagent
- title: PE Console
  type: service
  hostname: puppet
  path: /
  port: 443
- title: Primary Server
  type: terminal
  hostname: puppet
- title: Lab Help Guide
  type: website
  url: https://puppet-kmo.gitbook.io/practice-lab-help/
difficulty: basic
timelimit: 1800
---
1. On the Linux agent tab, run Puppet to request the agent's catalog from the primary server:
    ```
    puppet agent -t
    ```
2. Locate the agent's catalog:

    ```
    puppet config print client_datadir
    ```
    ✅ **Result:** The output shows the catalog's location:

       /opt/puppetlabs/puppet/cache/client_data

3. View the catalog's timestamp:

    ```
    ls -l /opt/puppetlabs/puppet/cache/client_data/catalog/nixagent*.json
    ```

4. Verify that the timestamp in the output matches the current system date and time:

    ```
    date
    ```

5. Run the following command to filter the catalog contents for the `Service` resource:

    ```
    jq '.resources[] | select(.type=="Service")' /opt/puppetlabs/puppet/cache/client_data/catalog/*.json
    ```

6. Inspect the catalog contents, and notice that the agent manages the `pxp-agent` service resource:
    ```
    ...
    {
          "type": "Service",
          "title": "pxp-agent",
          "tags": [
            "service",
            "pxp-agent",
            "class",
            "puppet_enterprise::pxp_agent::service",
            "puppet_enterprise",
            "pxp_agent",
            "puppet_enterprise::pxp_agent",
            "puppet_enterprise::profile::agent",
            "profile",
            "agent",
            "node",
            "default"
          ],
          "file": "/opt/puppetlabs/puppet/modules/puppet_enterprise/manifests/pxp_agent/service.pp",
          "line": 4,
          "exported": false,
          "parameters": {
            "ensure": true,
            "enable": true,
            "hasrestart": true
      ...
    ```

<br>🎈 **Congratulations!** You requested a catalog from the primary server, located the catalog on the Linux agent, and verified it was created recently. You then filtered the catalog contents for the `Service` resource type and verified that the agent is managing the `pxp-agent` service resource.

To continue, click **Next**.
