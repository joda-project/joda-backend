from joda.version import get_version

print((
    "Joda Backend version %(version)s"
) % {
    "version": get_version()
})
