import subprocess

from setuptools import find_packages, setup


def get_version():
    process = subprocess.Popen(["git", "describe", "--always", "--tags"], stdout=subprocess.PIPE, stderr=None)
    last_tag = process.communicate()[0].decode('ascii').strip()
    if '-g' in last_tag:
        return last_tag.split('-g')[0].replace('-', '.')
    else:
        return last_tag


with open('requirements.txt', encoding='utf-8') as f:
    install_reqs = f.read().splitlines()

setup(
    name='devdeck_toggl',
    version=get_version(),
    description="Toggl controls for DevDeck.",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Nicolas Dumazet',
    url='https://github.com/nicdumz/devdeck-toggl',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_reqs
)
