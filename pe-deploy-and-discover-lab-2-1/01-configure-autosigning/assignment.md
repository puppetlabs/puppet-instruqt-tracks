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
- title: Lab Help Guide
  type: website
  url: https://puppet-kmo.gitbook.io/practice-lab-help/
difficulty: basic
timelimit: 1500
---
1. On the **Primary Server** tab, navigate to:
	```
	cd /etc/puppetlabs/puppet
	```

2. Create and edit the `autosign.rb` script:

	```
	vim autosign.rb
	```

3. Copy the code below into the file.

    💡 **Tip:** To do this, type `:set paste`, press **Enter**, and then press `i`. Click the code below to copy it, and paste it from the clipboard. Then, save and exit by pressing `ESC` and typing `:wq`.

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
	💡 To learn more about autosigning certificate requests, visit [Puppet Docs](https://puppet.com/docs/puppet/6/ssl_autosign.html).<br><br>
4. Make the script executable and set the owner/group to `pe-puppet:pe-puppet`.

    💡 **Tip:** To save time, click the code below to copy it, and then paste it on the command line:
	```
	chmod 700 /etc/puppetlabs/puppet/autosign.rb
	```
	then:
	```
	chown pe-puppet:pe-puppet /etc/puppetlabs/puppet/autosign.rb
	```

5. Create and edit the pre-shared key (PSK) file:

	```
	vim psk
	```
6. Copy the following pre-shared key into the file.

    💡 **Tip:** To do this, type `:set paste`, press **Enter**, and then press `i`. Click the code below to copy it, and paste it from the clipboard. Then, save and exit by pressing `ESC` and typing `:wq`.

	```
	PASSWORD_FOR_AUTOSIGNER_SCRIPT
	```

7.  Lock down the key file permissions and set the owner/group to `pe-puppet:pe-puppet`.

	```
	chmod 600 /etc/puppetlabs/puppet/psk
	```
	then:
	```
	chown pe-puppet:pe-puppet /etc/puppetlabs/puppet/psk
	```

8. Configure the primary server to enable autosigning with `autosign.rb` by running:

	```
	puppet config set autosign /etc/puppetlabs/puppet/autosign.rb --section server
	```

9. Restart the primary server:

	```
	service pe-puppetserver restart
	```

    🔀 Switch to the **Linux Agent** tab.<br><br>


11. Install the Puppet agent by using the installation script with the `custom_attributes:challengePassword` parameter:

	```
	uri='https://puppet:8140/packages/current/install.bash'
	```
	then:
	```
	curl --insecure "$uri" | bash -s custom_attributes:challengePassword=PASSWORD_FOR_AUTOSIGNER_SCRIPT
	```

    🔀 Switch back to the **PE Console** tab when the agent installation is complete.<br><br>


1. Log in with username `admin` and password `puppetlabs`.


2. From the console sidebar, navigate to the **Nodes** page and confirm that the `nixagent` node is shown in the node list, which means that the agent's certificate was signed automatically and the node is now managed by PE.


3. Click the `nixagent` node, and on the **Facts** tab, explore the facts about the machine, such as OS version, number of CPUs, and so on.


---
## 🎈 **Congratulations!**
You installed the Puppet agent with autosigning enabled.

<br>To continue, click **Next**.