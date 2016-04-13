<a name="advanceusage"></a>
# Advanced
## Setup of cron and logrotate
You can setup a cron job for the script
`sudo crontab -e`
and type : 

    */5 * * * * /usr/local/bin/ddns-updater-aws >> /var/log/ddnsupdater


I personnaly use logrotate to rotate the created log `vim /etc/logrotate.d/ddnsupdater` and type

    /var/log/ddnsupdater {
    size 1k
    copytruncate
    missingok
    rotate 5
    }


## Config File

The default config files contains a non-working configuration which needs to be filled :
* The settings `ddns_provider_aws/aws_access_key_id` and `ddns_provider_aws/aws_secret_access_key` are used to identify yourself to amazon.
* The setting `ddns_provider_aws/zone_id` and `ddns_provider_aws/record_set_name` are used to identify the record that you which to modify
 
*see ['Specify interface / port for dns query'](#specifyinterface) before using those parameters*
* The setting `ip_provider_opendns/interface_name` is used to specify the port on which the dns query should be made.
* The setting `ip_provider_opendns/interface_name` is used to ensure dns query starts from specified interface.

<a name="specifyinterface"></a>
## Specify interface / port for dns query

Sometime, you need network magic. In my case, I needed to bypass a vpn tunnel to get the ip address. The following parameter can be used to specify the source ip / interface and port of the dns query. 

There are however some additionnal requirements to use this feature. Those were ommited due to netifaces requiring `python-dev` which is not present by default on ubuntu 14.04.

* `sudo apt-get install python-dev # install python header on linux`
* `pip install 'netifaces>=0.10.4,<0.11.0' # install netifaces`