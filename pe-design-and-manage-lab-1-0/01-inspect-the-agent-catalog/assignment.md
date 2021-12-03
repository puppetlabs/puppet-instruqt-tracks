---
slug: inspect-the-agent-catalog
id: rl9eexqbjtq4
type: challenge
title: Inspect the Agent Catalog
teaser: See what the Puppet agent manages out of the box.
notes:
- type: text
  contents: |-
    In this lab you will:

    * Run Puppet and explore the Puppet run lifecycle.

    * Inspect the agent catalog — built during the Puppet run — to see what the Puppet agent manages out of the box.

    In this lab, you'll use only the Linux agent (on the Linux Agent tab). Feel free to explore the PE console and primary server command line available on the other tabs. To log into the PE console, use `userid` admin and password `puppetlabs`.

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
- title: "Bug Zapper \U0001F99F⚡"
  type: website
  hostname: puppet
  url: https://docs.google.com/forms/d/e/1FAIpQLSeW5svhPB8_0R_PJw0RhsKH1ABS31pYMa0mTf3cO8fRGoTA0A/viewform?embedded=true
difficulty: basic
timelimit: 3600
---
1. ![swtich tabs](https://storage.googleapis.com/instruqt-images/Instruct%20Icons/icon_switch_tabs_white_32.png) Switch to the **Linux Agent** tab if needed.
2. Run Puppet to request the agent's catalog from the primary server:

    ```
    puppet agent -t
    ```
3. Locate the agent's catalog:

    ```
    puppet config print client_datadir
    ```
    ✔️ **Result:** The output shows the catalog's location:

       /opt/puppetlabs/puppet/cache/client_data

4. View the catalog's timestamp:

    ```
    ls -l /opt/puppetlabs/puppet/cache/client_data/catalog/nixagent*.json
    ```

5. Verify that the timestamp in the output matches the current system date and time:

    ```
    date
    ```

6. Run the following command to filter the catalog contents for the `Service` resource:

    ```
    cat /opt/puppetlabs/puppet/cache/client_data/catalog/*.json | jq -c '.resources[] | select(.type=="Service")' | jq
    ```

7. Inspect the catalog contents, and notice that the agent manages the `pxp-agent` service resource:
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

---
**Find any bugs or have feedback? Click the **Bug Zapper** tab near the top of the page and let us know!**

To close this lab, click **Next**.
