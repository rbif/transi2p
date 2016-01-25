from distutils.core import setup
# thanks bro: https://stackoverflow.com/a/7525163

# When pip installs anything from packages, py_modules, or ext_modules that
# includes a twistd plugin (which are installed to twisted/plugins/),
# setuptools/distribute writes a Package.egg-info/top_level.txt that includes
# "twisted".  If you later uninstall Package with `pip uninstall Package`,
# pip <1.2 removes all of twisted/ instead of just Package's twistd plugins.
# See https://github.com/pypa/pip/issues/355 (now fixed)
#
# To work around this problem, we monkeypatch
# setuptools.command.egg_info.write_toplevel_names to not write the line
# "twisted".  This fixes the behavior of `pip uninstall Package`.  Note that
# even with this workaround, `pip uninstall Package` still correctly uninstalls
# Package's twistd plugins from twisted/plugins/, since pip also uses
# Package.egg-info/installed-files.txt to determine what to uninstall,
# and the paths to the plugin files are indeed listed in installed-files.txt.
try:
    from setuptools.command import egg_info
    egg_info.write_toplevel_names
except (ImportError, AttributeError):
    pass
else:
    def _top_level_package(name):
        return name.split('.', 1)[0]

    def _hacked_write_toplevel_names(cmd, basename, filename):
        pkgs = dict.fromkeys(
            [_top_level_package(k)
                for k in cmd.distribution.iter_distribution_names()
                if _top_level_package(k) != "twisted"
            ]
        )
        cmd.write_file("top-level names", filename, '\n'.join(pkgs) + '\n')

    egg_info.write_toplevel_names = _hacked_write_toplevel_names

setup(
    name='transi2p',
    version='1.2.2',
    description="Transparent proxy for i2p.",
    url="https://github.com/rbif/transi2p/",
    author="Arnold French",
    author_email="arnold.french1974@yandex.com",
    packages=['transi2p', 'twisted.plugins'],
    install_requires=['txi2p', 'twisted']
)

# Make Twisted regenerate the dropin.cache, if possible.  This is necessary
# because in a site-wide install, dropin.cache cannot be rewritten by
# normal users.
try:
    from twisted.plugin import IPlugin, getPlugins
except ImportError:
    pass
else:
    list(getPlugins(IPlugin))
