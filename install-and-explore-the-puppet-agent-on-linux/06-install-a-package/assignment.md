---
slug: install-a-package
id: 4vclrt84vclu
type: challenge
title: "Install a package \U0001F469‍\U0001F4BB"
teaser: Use the Puppet agent to install a package and learn about package providers.
notes:
- type: text
  contents: |-
    # Question
    What parameter would you add to the `puppet resource` command from the previous challenge to instruct Puppet to install the package instead of just describing it?

    # Answer
    Adding the `ensure=present` parameter to the command will install the package.
tabs:
- title: Linux
  type: terminal
  hostname: linux
- title: Practice Lab Help
  type: website
  url: https://puppet-kmo.gitbook.io/practice-lab-help/
difficulty: basic
timelimit: 600
---

# Step 1
Run the following command to have Puppet install the Apache HTTP Server software package:

```
puppet resource package httpd ensure=present
```

✔️ **Result:** Puppet installs the package, and the value of the `ensure` parameter now shows the version that's installed.

## How did Puppet know I specified a real package name?
Puppet uses a default package provider such as `yum` or `apt`, depending on your OS. This package provider gets, installs, and manages packages by connecting to official Red Hat, Ubuntu, and third-party software repositories.

# Step 2
Notice what happens when you run the command again with a bogus package:

```
puppet resource package bogus-package ensure=present
```

✔️ **Result:** Puppet shows an error indicating that it couldn't find the bogus package.

## Can I specify which package provider installs a package?
Yes. Simply add the `provider` parameter to the command.

# Step 3
Run the following command:
```
puppet resource package bogus-package ensure=present provider=gem
```

**NOTE:** This command may take several minutes to complete while the entire RubyGems repository is searched for the bogus package name.

✔️ **Result:** As expected, Puppet still can't install the bogus package, however, this time the error message comes from the `gem` package provider, not `yum`.

## Can I specify which package version to install?
Yes. Simply specify the version in the `ensure` parameter. If you don't specify a version, Puppet installs the latest available.

The value `present` means *install the latest version*, but other values are interpreted as a specific version. If the package provider can't find the requested version, you'll see an error in the output.

# Step 4
Run the following command to install an older version of the `colors` gem package:
```
puppet resource package colors ensure=0.0.6 provider=gem
```
## Result
Puppet installs the version that you specify.

# One final note
Remember that in this training you are using these command-line tools manually. In an automated production environment, Puppet configures nodes based on the Puppet codebase on the primary Puppet server.

So, for example, if you always want a specific package version to come from a specific provider, you must specify those parameters as part of the command in a script.

To go to the next challenge, click **Check**.