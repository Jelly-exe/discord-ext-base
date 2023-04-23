import re

from setuptools import setup

with open('discord/ext/base/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('version is not set')

if version.endswith(('a', 'b', 'rc')):
    # append version identifier based on commit count
    try:
        import subprocess
        p = subprocess.Popen(['git', 'rev-list', '--count', 'HEAD'],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if out:
            version += out.decode('utf-8').strip()

        p = subprocess.Popen(['git', 'rev-parse', '--short', 'HEAD'],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if out:
            version += '+g' + out.decode('utf-8').strip()

    except Exception:
        pass

setup(name='discord-ext-base',
      author='Jelly-exe',
      url='https://github.com/Jelly-exe/discord-ext-base',
      version=version,
      packages=['discord.ext.base'],
      license='MIT',
      description='An extension module to provide a base bot class for discord.py',
      install_requires=['discord.py>=2.2.2'],
      python_requires='>=3.11.0'
)