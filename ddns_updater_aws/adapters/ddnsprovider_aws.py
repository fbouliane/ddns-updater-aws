import logging

import route53
from . import UpdateDnsFailed

logger = logging.getLogger(__name__)


def update_dns(ip, config):
    found = False
    for record_set in _get_record_sets(config['zone_id'], config):
        if record_set.name == config['record_set_name']:
            record_set.records = [str(ip)]
            record_set.save()
            found = True
            break
    if not found:
        raise UpdateDnsFailed("Recordset not found")


def _get_record_sets(zone_id, config):
    conn = route53.connect(
        aws_access_key_id=config['aws_access_key_id'],
        aws_secret_access_key=config['aws_secret_access_key']
    )
    try:
        zone = conn.get_hosted_zone_by_id(zone_id)
    except TypeError as type_error:
        logger.exception(type_error)
        raise UpdateDnsFailed("Unable to connect to route53")
    return zone.record_sets


