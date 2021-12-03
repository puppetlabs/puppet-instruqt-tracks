---
slug: refactor-profiles-with-parameters
id: w2ebaevntvrz
type: challenge
title: Refactor profiles with parameters
teaser: Refactor profiles with parameters
notes:
- type: text
  contents: |-
    In this lab you will:

    - Configure Hiera via the control-repo
    - Externalize data by moving it out of your profiles to enable reuse of profiles
    - Deploy your code to production
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
- title: Git Server
  type: service
  hostname: gitea
  path: /
  port: 3000
difficulty: basic
timelimit: 600
---
# Identify nodes in the *dc-east* datacenter
1.![switch tabs](https://storage.googleapis.com/instruqt-images/Instruct%20Icons/icon_switch_tabs_white_32.png) Switch to the **PE Console** tab and log in with username `admin` and password `puppetlabs`.
Check the console for nodes with trusted fact pp_datacenter=dc-east - these nodes need their web service port re-configured to 82.

# Develop your profiles to externalize data:
1. ![switch tabs](https://storage.googleapis.com/instruqt-images/Instruct%20Icons/icon_switch_tabs_white_32.png) Switch to the **Windows Agent** tab.
2. From the **Start** menu, open **Visual Studio Code**.
3. Enable autosave so that you don't have to remember to save your changes. Click **File** > **Auto Save**.
4. Open the `C:\CODE` directory. Click **File** > **Open Folder**, navigate to the `C:\CODE` directory and click **Select Folder**.
5. If prompted to trust the code in this directory, click **Accept**.
6. In VS Code, open a terminal. Click **Terminal** > **New Terminal**.
7. In the VS Code terminal window, run the following command:

        git clone git@gitea:puppet/control-repo.git
8. Check out the **webapp** feature branch:
      ```
      cd control-repo
      git checkout webapp
      ```
9. Edit the apache profile:
# site-modules/profile/manfiests/apache.pp
class profile::apache {
    $port    = 80
    $docroot = '/var/www'
    $index_html = "${docroot}/index.html"
    $site_content = "Hello world!"
    include apache
    apache::vhost { 'vhost.example.com':
      port    => $port,
      docroot => $docroot,
  }
  file { $index_html:
    ensure  => file,
    content => $site_content,
    }
}

# becomes...
# site-modules/profile/manfiests/apache.pp
class profile::apache (
    $port,
)
    $docroot = '/var/www'
    $index_html = "${docroot}/index.html"
    $site_content = "Hello world!"
    include apache
    apache::vhost { 'vhost.example.com':
      port    => $port,
      docroot => $docroot,
  }
}

10. Edit the IIS profile:
# iis profile: site-modules/profile/manifests/iis.pp
class profile::iis {
    $site_root = 'c:\\inetpub\\www'
    $iis_features = ['Web-WebServer','Web-Scripting-Tools']

    iis_feature { $iis_features:
      ensure => 'present',
    }

    iis_site { 'ecom':
      ensure          => 'started',
      physicalpath    => $site_root,
      applicationpool => 'DefaultAppPool',
      bindings        => [
          {
            'bindinginformation' => "*:80:",
            'protocol'           => 'http',
          },
        ],
    }
}

becomes...

# iis profile: site-modules/profile/manifests/iis.pp
class profile::iis (
    $port,    # parametarize $port
){
   $site_root    = 'c:\\inetpub\\ecom'
   $iis_features = ['Web-WebServer','Web-Scripting-Tools']

   iis_feature { $iis_features:
     ensure => 'present',
  }

  iis_site { 'ecom':
    ensure          => 'started',
    physicalpath    => $site_root,
    applicationpool => 'DefaultAppPool',
    bindings        => [
      {
        'bindinginformation' => "*:${port}:",   # interpolate $port
        'protocol'           => 'http',
      },
    ],
  }
}

```
11. Run PDK to validate your code, commit, push and deploy.
12. Run puppet on your nodes in dc-east, observe failures:
```
Error: Could not retrieve catalog from remote server: Error 500 on SERVER:
Server Error: Function lookup() did not find a value for the name 'profile::apache::port' on node NODE1.LOCAL
Warning: Not using cache on failed catalog
Error: Could not retrieve catalog; skipping run

Error: Could not retrieve catalog from remote server: Error 500 on SERVER:
Server Error: Function lookup() did not find a value for the name 'profile::iis::port' on node NODE2.LOCAL
Warning: Not using cache on failed catalog
Error: Could not retrieve catalog; skipping run
```
13. <b>Why did it fail to compile?</b> The hiera data does not yet exist and there is no default for the parameter. Remember, a failed catalog is better than a misconfiguration using a default--i.e. an assumption.

14. Add hiera data:

```
# <control-repo>/data/datacenter/dc-west.yaml
profile::apache::port: 82
profile::iis::port: 82

# <control-repo>/data/common.yaml
profile::apache::port: 80
profile::iis::port: 80
```

15. Add the required hiera layer for `pp_datacenter`:

```
# <control-repo>/hiera.yaml
---
version: 5
hierarchy:
    - name: Yaml data
      datadir: data
      data_hash: yaml_data
      paths:
        - "nodes/%{trusted.certname}.yaml"
        - "domain/%{facts.domain}.yaml"
        - "datacenter/%{trusted.extensions.pp_datacenter}.yaml"
        - "common.yaml"
```
16. Run PDK to validate your code, commit, push and deploy.

17. Run puppet on dev nodes in dc-west. Observe successful run. Curl port 82 for a manual acceptance test.

18. Canary release to a single node in production:
    1. Pin a production node to your agent-specified environment
    2. Run puppet in noop mode, specifying your feature branch environment - observe success.
    3. Run puppet in normal mode, specifying your feature branch environment - observe success.
    4. Unpin the node from the agent-specified environment.

19. Release your changes:
    1. Merge (and delete) your feature branch to main.
    2. Update your production branch with your merge commit.
    3. Deploy your code to the primary server.
    4. Run puppet on all nodes in production.