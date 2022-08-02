import semver

NPM_REGISTRY_URL = 'https://registry.npmjs.org'


def build_all_versions_url(name):
    return f'{NPM_REGISTRY_URL}/{name}'


def build_version_url(name, version):
    return f'{NPM_REGISTRY_URL}/{name}/{version}'


def build_tarball_url(name, version):
    return '{}/{}/-/{}'.format(NPM_REGISTRY_URL,
                               name.replace('%2f',
                                            '/'),
                               build_filename(name,
                                              version))


def build_filename(name, version):
    return f'{unscope_name(name)}-{version}.tgz'


def normalize_package(name):
    return name.replace('/', '%2f') if is_scoped(name) else name


def is_scoped(name):
    return name.startswith('@')


def unscope_name(scoped_name):
    return scoped_name.split('%2f')[1] if is_scoped(scoped_name) else scoped_name


def is_uri(version):
    if version is None:
        return False
    if not isinstance(version, (str, )):
        return False
    if version.startswith('http://'):
        return True
    if version.startswith('https://'):
        return True
    return bool(version.startswith('git://'))


def parse_uri(uri):
    if uri.startswith('git:'):
        return uri.replace(
            'git:',
            'http:').replace(
            '.git',
            '/archive/master.zip')
    return uri


def find_lastest_satisfying_version(versions, ver):
    if is_uri(ver):
        return parse_uri(ver)
    return semver.max_satisfying(versions, parse_version(ver), loose=True)


def parse_version(ver):
    return '>0.0.0' if ver == 'latest' else ver


async def copyfileobj(fsrc, fdst, length=16 * 1024):
    while True:
        buf = await fsrc.read(length)
        if not buf:
            break
        await fdst.write(buf)


def multi_pop(queue, count=10):
    items = []
    try:
        items.extend(queue.pop() for _ in range(count))
    except IndexError:
        pass
    return items
