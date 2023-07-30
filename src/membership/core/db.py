from functools import lru_cache

from cassandra.cluster import Cluster
from cassandra.cqlengine import connection
from cassandra.auth import PlainTextAuthProvider


from membership.core.config import settings


cloud_config= {
  'secure_connect_bundle': settings.CASSANDRA_DB_ENCRYPTED_BUNDLE
}

@lru_cache(maxsize=1)
def get_cdb():
    """
    Get session for cassandra database.
    """
    auth_provider = PlainTextAuthProvider(settings.CASSANDRA_DB_CLIENT_ID, settings.CASSANDRA_DB_CLIENT_SECRET)
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    session = cluster.connect()
    connection.register_connection(str(session), session=session)
    connection.set_default_connection(str(session))

    return session
