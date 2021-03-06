import os


def absdir(directory, base_dir):
    if not directory.startswith('/'):
        directory = os.path.join(base_dir, directory)
    return os.path.normpath(directory)


def dirs(list_dir, base_dir):
    result = []
    for i in list_dir:
        result.append(absdir(i, base_dir))
    return result


def convert_to_djangodb(d, name, base_dir='/tmp'):
    if d.get('database'):
        db = {
            k.upper(): v
            for k, v in d.items()
            if v}
        if db.pop('gis', None):
            db['ENGINE'] = 'django.contrib.gis.db.backends.postgis'
        else:
            db['ENGINE'] = 'django.db.backends.postgresql_psycopg2'
        db['NAME'] = db.pop('DATABASE')
        # Use same db name for test. Use custom config for tests to separate test and dev dbs.
        db['TEST'] = {'NAME': db['NAME']}
    else:
        return {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(base_dir, name + '.sqlite3'),
        }
    return db


def db_to_settings(db_dict, base_dir):
    return {
        n: convert_to_djangodb(v, n, base_dir=base_dir)
        for n, v in db_dict.items()
    }


def convert_to_django_redis(config):
    return {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://{host}:{port}/{db}'.format(**config),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }


def redis_to_settings(redis_dict):
    return {name: convert_to_django_redis(value) for name, value in redis_dict.items()}
