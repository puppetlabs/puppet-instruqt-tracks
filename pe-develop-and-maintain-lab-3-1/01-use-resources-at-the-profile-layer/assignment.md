---
slug: use-resources-at-the-profile-layer
id: 8uyabtwy0kff
type: challenge
title: Use Resources at the Profile Layer
teaser: Use resources at the profile layer
notes:
- type: text
  contents: |-
    In this lab you will:

    - Use file resources in your Apache & IIS profile to manage website content
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
  hostname: nixagent1
- title: Git Server
  type: service
  hostname: gitea
  path: /
  port: 3000
difficulty: basic
timelimit: 600
---
# Create a control repo on your Windows development workstation
1. ![switch tabs](https://storage.googleapis.com/instruqt-images/Instruct%20Icons/icon_switch_tabs_white_32.png) Switch to the **Windows Agent** tab.
2. From the **Start** menu, open **Visual Studio Code**.
3. Enable autosave so that you don't have to remember to save your changes. Click **File** > **Auto Save**.
4. Open the `C:\CODE` directory. Click **File** > **Open Folder**, navigate to the `C:\CODE` directory and click **Select Folder**.
5. If prompted to trust the code in this directory, click **Accept**.
6. In VS Code, open a terminal. Click **Terminal** > **New Terminal**.
7. In the VS Code terminal window, run the following command:

        git clone git@gitea:puppet/control-repo.git
---
# Edit apache profile:
1. Check out the **webapp** feature branch:
      ```
      cd control-repo
      git checkout webapp
      ```

2. Refactor your `profile::apache` code to move your site root along with setting data types:

```
# site-modules/profile/manfiests/apache.pp
class profile::apache (
  $port,
) {
  $docroot = '/var/www'
  $index_html = "${docroot}/index.html"
...

becomes...

# site-modules/profile/manfiests/apache.pp
class profile::apache (
  Integer $port,
  Stdlib::Absolutepath $docroot,
) {
  $index_html = "${docroot}/index.html"
  $site_content = "
Hello world!
"
  include apache
  apache::vhost { 'vhost.example.com':
    port    => $port,
    docroot => $docroot,
  }
  file { $docroot:
    ensure => directory,
  }
...
```
2. Run PDK to validate your code, commit, push and deploy.

3. Run puppet in your feature branch env.

4. Why did it fail? The filepath `var/web/cms` is not an absolute filepath - good news is that nothing was misconfigured! Puppet just failed to compile a catalog, find and fix the data in hiera.

```
profile::apache::docroot: var/web/cms
to
profile::apache::docroot: /var/web/cms
```

5. Commit & push - observe the failure - apache class failed because the directory was not managed before the vhost...
```
# site-modules/profile/manfiests/apache.pp
class profile::apache (
  Integer $port,
  Stdlib::Absolutepath $docroot,
  String $site_content,
)
  $index_html = "${docroot}/index.html"
  include apache
  apache::vhost { 'vhost.example.com':
    port    => $port,
    docroot => $docroot,
    require => File[$index_html],  # add a resource relationship,
                                   # required before the vhost is managed.
  }

  # puppet only manages the specific resources that are declared;
  # it will not automagically create parent directory of /var/web/cms!
  file { '/var/web:
    ensure => directory,
  }
  file { $docroot:
    ensure => directory,
  }
  file { $index_html:
    ensure  => file,
    content => $site_content,
  }
}
```
6. Run PDK to validate your code, commit, push and deploy.

7. Run puppet in your feature_branch env - success.

8. For `profile::iis`:

```

# iis profile: site-modules/profile/manifests/iis.pp
class profile::iis (
  $port,
  $site_root,
){
  $site_root    = 'C:\\inetpub\\www'
...

becomes...

# iis profile: site-modules/profile/manifests/iis.pp
class profile::iis (
  Integer $port,
  Stdlib::Absolutepath $site_root,
) {
  $index_html   = "${site_root}\\index.html"
      # Be careful with escapes when interpolating with double quotes
  $site_content = "
Hello world!
"

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
     require         => File[$site_root],  # add a resource relationship,
                                           # required before the site is managed.
   }
   # puppet only manages the specific resources that are declared;
   # it will not automagically create the parent directory of c:\web\ecom!
   file { 'C:\web':
     ensure => directory,
   }
   file { $site_root:
     ensure => directory,
   }
   file { $index_html:
     ensure  => file,
     content => $site_content,
   }
}
```

9. Commit, push, deploy and test. Why did it fail? The filepath `web\ecom` is not an absolute filepath - good news is that nothing was misconfigured! Puppet just failed to compile a catalog, find and fix the data in hiera.

```
profile::iis::site_root: web\ecom
to
profile::iis::site_root: C:\web\ecom
```

10. Run PDK to validate your code, commit, push and deploy.

11. Run puppet in your feature_branch env - success.

12. Release your changes:
    1. Merge (and delete) your feature branch to main
    2. Update your production branch with your merge commit
    3. Deploy your code to the primary server
    4. Run puppet on all nodes in production