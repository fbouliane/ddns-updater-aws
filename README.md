# DDNS updater for AWS
This script keeps a domain name pointing *server.yourdomain.com* to your ip address using Amazon's route53 api. It can be useful something like a home server or a raspberry pi, or anything that could execute python. 

*This script could be a replacement for no-ip, dyn or duck dns services if executed often.*

## How it works

0. A dns query is made to get your external ip address.
0. A rest api call is made to update your domain to point on your ip address.


*The Amazon route53 API provides an api to change the A record on a domain (on which ip the domain points to). This script uses this api and push it the ip address it discovered on a subdomain.*

## Why

I have a server at home that i use on a weekly basis and I wand it to be always accessible on internet using my own domain name. My ISP Provider charges for fixed ip address and my ip changes often. I was using [will warren bash script](https://willwarren.com/2014/07/03/roll-dynamic-dns-service-using-amazon-route53/), but I wanted to have something more reliable.
Also I wanted to have logs that showed what the script did, and when error happened.
Those are the reason why I invested time to create this project.

## Setup

Please follow [these instruction](https://willwarren.com/2014/07/03/roll-dynamic-dns-service-using-amazon-route53/#step-2-set-up-your-hosted-zone-on-route53:bef5789d633e223574fb4cc7b8ade916)
from step 2-4 to setup your amazon server. The recovered values should be added to your ddns_aws_updater.ini


## Usage

0. Copy and edit the `ddns_updater_aws/ddns_updater_aws.default.ini` to `ddns_updater_aws/ddns_updater_aws.ini`
0. Install the requirements `python setup.py install`
0. Execute the software (*python style* `python -m ddns_updater_aws`, *bash style* `ddns_updater_aws/__main__.py`)

*The script only updates once the IP, it's intended usage is to launch the script at an interval by something like a cron job.*

## Tests
only tested on ubuntu 12.04, should work on other platforms however.

`tox -r`

## Contributions
Opening a pull-request or an issue is encouraged !
