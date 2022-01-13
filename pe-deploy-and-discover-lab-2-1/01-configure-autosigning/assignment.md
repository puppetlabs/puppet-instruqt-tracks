---
slug: configure-autosigning
id: jfhy7qsxgss1
type: challenge
title: Configure autosigning
teaser: Install the Puppet agent with autosigning enabled.
notes:
- type: text
  contents: |-
    In this lab, you will:

    * Configure the primary server to enable policy-based autosigning, enabling new nodes to be automatically added and managed by the primary server.

    In this example, the policy includes a simple check for a password. More complex policies might include an external database lookup or requiring other information to be passed in with the certificate request.

    * Run the agent installation script and automatically sign the agent's certificate by providing a challenge password.

    Click **Start** when you're ready to begin.
tabs:
- title: Primary Server
  type: terminal
  hostname: puppet
- title: Linux Agent
  type: terminal
  hostname: nixagent
- title: PE Console
  type: service
  hostname: puppet
  port: 443
- title: Lab Aid
  type: website
  hostname: nixagent
  url: https://puppet-kmo.gitbook.io/lab-aids/-MZKPjwKRKKFuXxxy7ge/pe101/configure-agent-certificate-autosigning
- title: Practice Lab Help
  type: website
  hostname: nixagent
  url: https://puppet-kmo.gitbook.io/practice-lab-help/
difficulty: basic
timelimit: 3000
---
1. On the **Primary Server** tab, navigate to:<br><br>
	```
	cd /etc/puppetlabs/puppet
	```

2. Create and edit the `autosign.rb` script:<br><br>

	```
	vim autosign.rb
	```

3. Copy the code below into the file.<br><br>💡 **Tip:** To do this, type `:set paste`, press **Enter**, and then press `i`. Click the code below to copy it, and paste it from the clipboard. Then, save and exit by pressing `ESC` and typing `:wq`.<br><br>

	```
	#!/opt/puppetlabs/puppet/bin/ruby
	#
	# A note on logging:
	#   This script's stderr and stdout are only shown at the DEBUG level
	#   of the server's logs. This means you won't see the error messages
	#   in puppetserver.log by default. All you'll see is the exit code.
	#
	#   https://docs.puppet.com/puppet/latest/ssl_autosign.html#policy-executable-api
	#
	# Exit Codes:
	#   0 - A matching challengePassword was found.
	#   1 - No challengePassword was found.
	#   2 - The wrong challengePassword was found.
	#
	require 'puppet/ssl'

	csr = Puppet::SSL::CertificateRequest.from_s(STDIN.read)
	psk = File.read('/etc/puppetlabs/puppet/psk').chomp.strip

	if pass = csr.custom_attributes.find do |attribute|
	     ['challengePassword', '1.2.840.113549.1.9.7'].include? attribute['oid']
	   end
	else
	  puts 'No challengePassword found. Rejecting certificate request.'
	  exit 1
	end

	if pass['value'] == psk
	  exit 0
	else
	  puts "challengePassword does not match: #{pass['value']}"
	  exit 2
	end
	```

4. Make the script executable and set the owner/group to `pe-puppet:pe-puppet`. <br><br>💡 **Tip:** To save time, click the code below to copy it, and then paste it on the command line:<br><br>
	```
	chmod 700 /etc/puppetlabs/puppet/autosign.rb
	```
	then:
	```
	chown pe-puppet:pe-puppet /etc/puppetlabs/puppet/autosign.rb
	```

5. Create and edit the pre-shared key (PSK) file:<br><br>
	```
	vim psk
	```

6. Copy the following pre-shared key into the file.<br><br>💡 **Tip:** To do this, type `:set paste`, press **Enter**, and then press `i`. Click the code below to copy it, and paste it from the clipboard. Then, save and exit by pressing `ESC` and typing `:wq`.<br><br>

	```
	PASSWORD_FOR_AUTOSIGNER_SCRIPT
	```

7. ![switch tabs](https://storage.googleapis.com/instruqt-images/Instruct%20Icons/icon_switch_tabs_white_32.png)Switch to the **Primary Server** tab and lock down the key file permissions and set the owner/group to `pe-puppet:pe-puppet`.<br><br>

	```
	chmod 600 /etc/puppetlabs/puppet/psk
	```
	then:
	```
	chown pe-puppet:pe-puppet /etc/puppetlabs/puppet/psk
	```

8. Configure the primary server to enable autosigning with `autosign.rb` by running:<br><br>

	```
	puppet config set autosign /etc/puppetlabs/puppet/autosign.rb --section server
	```

9. Restart the primary server:<br><br>

	```
	service pe-puppetserver restart
	```

10. ![swtich tabs](https://storage.googleapis.com/instruqt-images/Instruct%20Icons/icon_switch_tabs_white_32.png) Switch to the **Linux Agent** tab.

11. Install the Puppet agent by using the installation script with the `custom_attributes:challengePassword` parameter:<br><br>

	```
	uri='https://puppet:8140/packages/current/install.bash'
	```
	then:
	```
	curl --insecure "$uri" | bash -s custom_attributes:challengePassword=PASSWORD_FOR_AUTOSIGNER_SCRIPT
	```

12. ![swtich tabs](https://storage.googleapis.com/instruqt-images/Instruct%20Icons/icon_switch_tabs_white_32.png) Switch back to the **PE Console** tab when the agent installation is complete.

1. Log in with username `admin` and password `puppetlabs`.

1. From the console sidebar, navigate to the **Nodes** page and confirm that the `nixagent` node is shown in the node list, which means that the agent's certificate was signed automatically and the node is now managed by PE.

1. Click the `nixagent` node, and on the **Facts** tab, explore the facts about the machine, such as OS version, number of CPUs, and so on.

<br>🎈 **Congratulations!**  You installed the Puppet agent with autosigning enabled.

<br>To continue, click **Next**.