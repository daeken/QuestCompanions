import battlenet
from battlenet import Connection

connection = Connection()
print "wow_servers = [",
for realm in connection.get_all_realms(battlenet.UNITED_STATES):
    print '%r,' % realm,
print "]",
