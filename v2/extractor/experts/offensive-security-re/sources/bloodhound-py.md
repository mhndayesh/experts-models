# bloodhound.py (BloodHound.py) — verbatim source

Ingestor/collector for BloodHound, maintained by Dirk-jan Mollema. The collector is split into two branches/packages:
legacy `bloodhound-python` (BloodHound 4.2/4.3) vs `bloodhound-ce-python` (BloodHound Community Edition / CE).
Sources below are verbatim from the GitHub repo (master and bloodhound-ce branches).

---
## SOURCE 1: README.md — master branch (LEGACY, BloodHound 4.2/4.3)
URL: https://raw.githubusercontent.com/dirkjanm/BloodHound.py/master/README.md
```markdown
# BloodHound.py
![Python 3 compatible](https://img.shields.io/badge/python-3.x-blue.svg)
![PyPI version](https://img.shields.io/pypi/v/bloodhound.svg)
![License: MIT](https://img.shields.io/pypi/l/bloodhound.svg)

BloodHound.py is a Python based ingestor for [BloodHound](https://github.com/BloodHoundAD/BloodHound), based on [Impacket](https://github.com/CoreSecurity/impacket/).

The code in this branch is **only compatible with BloodHound 4.2 and 4.3**. For BloodHound CE, check out the [bloodhound-ce branch](https://github.com/dirkjanm/BloodHound.py/tree/bloodhound-ce)

## Installation
There are different install methods for BloodHound Community Edition (CE) and BloodHound legacy. You can only have one of the two tools installed at the same time, unless you use a virtual environment for both tools, or a package manager like pipx that automatically sets these up.

### BloodHound Legacy
The following install methods are available:
* Via pip: `pip install bloodhound`
* Via pipx: `pipx install bloodhound`
* By cloning this repository `git clone https://github.com/dirkjanm/BloodHound.py` and running `pip install .` from the project directory.

The BloodHound.py Legacy installation will add a command line tool `bloodhound-python` to your PATH.

### BloodHound CE
The following install methods are available:
* Via pip: `pip install bloodhound-ce`
* Via pipx: `pipx install bloodhound-ce`
* By cloning this repository `git clone https://github.com/dirkjanm/BloodHound.py`, checking out the CE branch `git checkout bloodhound-ce` and running `pip install .` from the project directory.

The BloodHound.py CE ingestor will add a command line tool `bloodhound-ce-python` to your PATH.

## Usage
To use the ingestor, at a minimum you will need credentials of the domain you're logging in to. Credentials can be specified as username + password, NT hash or AES keys, or a Kerberos TGT in a ccache file.
You will need to specify the `-u` option with a username of this domain (or `username@domain` for a user in a trusted domain). If you have your DNS set up properly and the AD domain is in your DNS search list, then BloodHound.py will automatically detect the domain for you. If not, you have to specify it manually with the `-d` option.

By default BloodHound.py will query LDAP and the individual computers of the domain to enumerate users, computers, groups, trusts, sessions and local admins. 
If you want to restrict collection, specify the `--collectionmethod` parameter, which supports the following options (similar to SharpHound):
- *Default* - Performs group membership collection, domain trust collection, local admin collection, and session collection
- *Group* - Performs group membership collection
- *LocalAdmin* - Performs local admin collection
- *RDP* - Performs Remote Desktop Users collection
- *DCOM* - Performs Distributed COM Users collection
- *Container* - Performs container collection (GPO/Organizational Units/Default containers)
- *PSRemote* - Performs Remote Management (PS Remoting) Users collection
- *DCOnly* - Runs all collection methods that can be queried from the DC only, no connection to member hosts/servers needed. This is equal to Group,Acl,Trusts,ObjectProps,Container
- *Session* - Performs session collection
- *Acl* - Performs ACL collection
- *Trusts* - Performs domain trust enumeration
- *LoggedOn* - Performs privileged Session enumeration (requires local admin on the target)
- *ObjectProps* - Performs Object Properties collection for properties such as LastLogon or PwdLastSet
- *All* - Runs all methods above, except LoggedOn
- *Experimental* - Connects to individual hosts to enumerate services and scheduled tasks that may have stored credentials

Multiple collectionmethods should be separated by a comma, for example: `-c Group,LocalAdmin`

You can override some of the automatic detection options, such as the hostname of the primary Domain Controller if you want to use a different Domain Controller with `-dc`, or specify your own Global Catalog with `-gc`.

## Limitations
BloodHound.py currently has the following limitations:
- Supports most, but not all BloodHound (SharpHound) features. Currently GPO local groups are not supported, all other collection methods are implemented.

## Docker usage
1. Build container  
```docker build -t bloodhound .```  
2. Run container  
```docker run -v ${PWD}:/bloodhound-data -it bloodhound```  
After that you can run `bloodhound-python` inside the container, all data will be stored in the path from where you start the container.

## Credits
BloodHound.py was originally written by Dirk-jan Mollema, Edwin van Vliet and Matthijs Gielen from [Fox-IT (NCC Group)](https://fox-it.com/). BloodHound.py is currently maintained by Dirk-jan Mollema from [Outsider Security](https://outsidersecurity.nl). The implementation and data model is based on the original tool from [SpecterOps](https://specterops.io). Many thanks to everyone who contributed by testing, submitting issues and pull requests over the years.
```

---
## SOURCE 2: README.md — bloodhound-ce branch (BloodHound CE)
URL: https://raw.githubusercontent.com/dirkjanm/BloodHound.py/bloodhound-ce/README.md
```markdown
# BloodHound.py
![Python 3 compatible](https://img.shields.io/badge/python-3.x-blue.svg)
![PyPI version](https://img.shields.io/pypi/v/bloodhound.svg)
![License: MIT](https://img.shields.io/pypi/l/bloodhound.svg)

BloodHound.py is a Python based ingestor for [BloodHound](https://github.com/BloodHoundAD/BloodHound), based on [Impacket](https://github.com/CoreSecurity/impacket/).

The code in this branch is **only compatible with BloodHound CE**. 

## Installation
There are different install methods for BloodHound Community Edition (CE) and BloodHound legacy. You can only have one of the two tools installed at the same time, unless you use a virtual environment for both tools, or a package manager like pipx that automatically sets these up.

### BloodHound Legacy
The following install methods are available:
* Via pip: `pip install bloodhound`
* Via pipx: `pipx install bloodhound`
* By cloning this repository `git clone https://github.com/dirkjanm/BloodHound.py` and running `pip install .` from the project directory.

The BloodHound.py Legacy installation will add a command line tool `bloodhound-python` to your PATH.

### BloodHound CE
The following install methods are available:
* Via pip: `pip install bloodhound-ce`
* Via pipx: `pipx install bloodhound-ce`
* By cloning this repository `git clone https://github.com/dirkjanm/BloodHound.py`, checking out the CE branch `git checkout bloodhound-ce` and running `pip install .` from the project directory.

The BloodHound.py CE ingestor will add a command line tool `bloodhound-ce-python` to your PATH.

## Usage
To use the ingestor, at a minimum you will need credentials of the domain you're logging in to. Credentials can be specified as username + password, NT hash or AES keys, or a Kerberos TGT in a ccache file.
You will need to specify the `-u` option with a username of this domain (or `username@domain` for a user in a trusted domain). If you have your DNS set up properly and the AD domain is in your DNS search list, then BloodHound.py will automatically detect the domain for you. If not, you have to specify it manually with the `-d` option.

By default BloodHound.py will query LDAP and the individual computers of the domain to enumerate users, computers, groups, trusts, sessions and local admins. 
If you want to restrict collection, specify the `--collectionmethod` parameter, which supports the following options (similar to SharpHound):
- *Default* - Performs group membership collection, domain trust collection, local admin collection, and session collection
- *Group* - Performs group membership collection
- *LocalAdmin* - Performs local admin collection
- *RDP* - Performs Remote Desktop Users collection
- *DCOM* - Performs Distributed COM Users collection
- *Container* - Performs container collection (GPO/Organizational Units/Default containers)
- *PSRemote* - Performs Remote Management (PS Remoting) Users collection
- *DCOnly* - Runs all collection methods that can be queried from the DC only, no connection to member hosts/servers needed. This is equal to Group,Acl,Trusts,ObjectProps,Container
- *Session* - Performs session collection
- *Acl* - Performs ACL collection
- *Trusts* - Performs domain trust enumeration
- *LoggedOn* - Performs privileged Session enumeration (requires local admin on the target)
- *ObjectProps* - Performs Object Properties collection for properties such as LastLogon or PwdLastSet
- *All* - Runs all methods above, except LoggedOn
- *Experimental* - Connects to individual hosts to enumerate services and scheduled tasks that may have stored credentials

Multiple collectionmethods should be separated by a comma, for example: `-c Group,LocalAdmin`

You can override some of the automatic detection options, such as the hostname of the primary Domain Controller if you want to use a different Domain Controller with `-dc`, or specify your own Global Catalog with `-gc`.

## Limitations
BloodHound.py currently has the following limitations:
- Supports most, but not all BloodHound (SharpHound) features. Currently GPO local groups are not supported, all other collection methods are implemented.

## Docker usage
1. Build container  
```docker build -t bloodhound .```  
2. Run container  
```docker run -v ${PWD}:/bloodhound-data -it bloodhound```  
After that you can run `bloodhound-python` inside the container, all data will be stored in the path from where you start the container.

## Credits
BloodHound.py was originally written by Dirk-jan Mollema, Edwin van Vliet and Matthijs Gielen from [Fox-IT (NCC Group)](https://fox-it.com/). BloodHound.py is currently maintained by Dirk-jan Mollema from [Outsider Security](https://outsidersecurity.nl). The implementation and data model is based on the original tool from [SpecterOps](https://specterops.io). Many thanks to everyone who contributed by testing, submitting issues and pull requests over the years.
```

---
## SOURCE 3: setup.py — master (LEGACY) — defines package name, version, and console command
URL: https://raw.githubusercontent.com/dirkjanm/BloodHound.py/master/setup.py
```python
from setuptools import setup

setup(name='bloodhound',
      version='1.9.0',
      description='Python based ingestor for BloodHound',
      author='Dirk-jan Mollema, Edwin van Vliet, Matthijs Gielen',
      author_email='dirkjan@dirkjanm.io, edwin.vanvliet@fox-it.com, matthijs.gielen@fox-it.com',
      maintainer='Dirk-jan Mollema',
      maintainer_email='dirkjan@dirkjanm.io',
      url='https://github.com/dirkjanm/bloodhound.py',
      packages=['bloodhound',
                'bloodhound.ad',
                'bloodhound.lib',
                'bloodhound.enumeration'],
      license='MIT',
      install_requires=['dnspython', 'impacket>=0.9.17', 'ldap3>=2.5,!=2.5.2,!=2.5.0,!=2.6', 'pyasn1>=0.4', 'pycryptodome'],
      classifiers=[
        'Intended Audience :: Information Technology',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
      ],
      entry_points= {
        'console_scripts': ['bloodhound-python=bloodhound:main']
      }
      )
```

## SOURCE 4: setup.py — bloodhound-ce (CE) — defines package name, version, and console command
URL: https://raw.githubusercontent.com/dirkjanm/BloodHound.py/bloodhound-ce/setup.py
```python
from setuptools import setup

setup(name='bloodhound-ce',
      version='1.9.0',
      description='Python based ingestor for BloodHound Community Edition',
      author='Dirk-jan Mollema, Edwin van Vliet, Matthijs Gielen',
      author_email='dirkjan@dirkjanm.io, edwin.vanvliet@fox-it.com, matthijs.gielen@fox-it.com',
      maintainer='Dirk-jan Mollema',
      maintainer_email='dirkjan@dirkjanm.io',
      url='https://github.com/dirkjanm/bloodhound.py',
      packages=['bloodhound',
                'bloodhound.ad',
                'bloodhound.lib',
                'bloodhound.enumeration'],
      license='MIT',
      install_requires=['dnspython', 'impacket>=0.9.17', 'ldap3>=2.5,!=2.5.2,!=2.5.0,!=2.6', 'pyasn1>=0.4', 'pycryptodome'],
      classifiers=[
        'Intended Audience :: Information Technology',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
      ],
      entry_points= {
        'console_scripts': ['bloodhound-ce-python=bloodhound:main']
      }
      )
```

---
## SOURCE 5: bloodhound/__init__.py — CLI argument parser (bloodhound-ce branch)
URL: https://raw.githubusercontent.com/dirkjanm/BloodHound.py/bloodhound-ce/bloodhound/__init__.py
NOTE: The argument parser is byte-for-byte identical between the master (LEGACY) and bloodhound-ce branches EXCEPT for two lines (the parser description and the startup log line), shown separately in SOURCE 7. All flags/options below apply to BOTH bloodhound-python and bloodhound-ce-python.
```python
    parser = argparse.ArgumentParser(add_help=True, description='Python based ingestor for BloodHound Community Edition\nFor help or reporting issues, visit https://github.com/dirkjanm/BloodHound.py', formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-c',
                        '--collectionmethod',
                        action='store',
                        default='Default',
                        help='Which information to collect. Supported: Group, LocalAdmin, Session, '
                             'Trusts, Default (all previous), DCOnly (no computer connections), DCOM, RDP,'
                             'PSRemote, LoggedOn, Container, ObjectProps, ACL, All (all except LoggedOn). '
                             'You can specify more than one by separating them with a comma. (default: Default)')
    parser.add_argument('-d',
                        '--domain',
                        action='store',
                        default='',
                        help='Domain to query.')
    parser.add_argument('-v',
                        action='store_true',
                        help='Enable verbose output')
    helptext = 'Specify one or more authentication options. \n' \
               'By default Kerberos authentication is used and NTLM is used as fallback. \n' \
               'Kerberos tickets are automatically requested if a password or hashes are specified.'
    auopts = parser.add_argument_group('authentication options', description=helptext)
    auopts.add_argument('-u',
                        '--username',
                        action='store',
                        help='Username. Format: username[@domain]; If the domain is unspecified, the current domain is used.')
    auopts.add_argument('-p',
                        '--password',
                        action='store',
                        help='Password')
    auopts.add_argument('-k',
                        '--kerberos',
                        action='store_true',
                        help='Use kerberos ccache file')
    auopts.add_argument('--hashes',
                        action='store',
                        help='LM:NLTM hashes')
    auopts.add_argument('-no-pass', action="store_true", help='don\'t ask for password (useful for -k)')
    auopts.add_argument('-aesKey',
                        action="store",
                        metavar="hex key",
                        help='AES key to use for Kerberos Authentication (128 or 256 bits)')
    auopts.add_argument('--auth-method',
                        choices=('auto','ntlm','kerberos'),
                        default='auto',
                        action='store',
                        help='Authentication methods. Force Kerberos or NTLM only or use auto for Kerberos with NTLM fallback')
    coopts = parser.add_argument_group('collection options')
    coopts.add_argument('-ns',
                        '--nameserver',
                        action='store',
                        help='Alternative name server to use for queries')
    coopts.add_argument('--dns-tcp',
                        action='store_true',
                        help='Use TCP instead of UDP for DNS queries')
    coopts.add_argument('--dns-timeout',
                        action='store',
                        type=int,
                        default=3,
                        help='DNS query timeout in seconds (default: 3)')
    coopts.add_argument('-dc',
                        '--domain-controller',
                        metavar='HOST',
                        action='store',
                        help='Override which DC to query (hostname)')
    coopts.add_argument('-gc',
                        '--global-catalog',
                        metavar='HOST',
                        action='store',
                        help='Override which GC to query (hostname)')
    coopts.add_argument('-w',
                        '--workers',
                        action='store',
                        type=int,
                        default=10,
                        help='Number of workers for computer enumeration (default: 10)')
    coopts.add_argument('--exclude-dcs',
                        action='store_true',
                        help='Skip DCs during computer enumeration')
    coopts.add_argument('--disable-pooling',
                        action='store_true',
                        help='Don\'t use subprocesses for ACL parsing (only for debugging purposes)')
    coopts.add_argument('--disable-autogc',
                        action='store_true',
                        help='Don\'t automatically select a Global Catalog (use only if it gives errors)')
    coopts.add_argument('--zip',
                        action='store_true',
                        help='Compress the JSON output files into a zip archive')
    coopts.add_argument('--computerfile',
                        action='store',
                        help='File containing computer FQDNs to use as allowlist for any computer based methods')
    coopts.add_argument('--cachefile',
                        action='store',
                        help='Cache file (experimental)')
    coopts.add_argument('--ldap-channel-binding',
                        action='store_true',
                        help='Use LDAP Channel Binding (will force ldaps protocol to be used)')
    coopts.add_argument('--use-ldaps',
                        action='store_true',
                        help='Use LDAP over TLS on port 636 by default')
    coopts.add_argument('-op',
                        '--outputprefix',
                        metavar='PREFIX_NAME',
                        action='store',
                        help='String to prepend to output file names')

    args = parser.parse_args()
    logging.info('BloodHound.py for BloodHound Community Edition')

    if args.v is True:
```

---
## SOURCE 6: bloodhound/enumeration/outputworker.py — output JSON meta version
This is the BloodHound/SharpHound JSON data-model version written into the "meta" block of every output file.

### master (LEGACY) outputworker.py — writes "version":5
URL: https://raw.githubusercontent.com/dirkjanm/BloodHound.py/master/bloodhound/enumeration/outputworker.py
```python
79:                computers_out.write('],"meta":{"methods":0,"type":"computers","count":%d, "version":5}}' % current_num_computers)
90:        computers_out.write('],"meta":{"methods":0,"type":"computers","count":%d, "version":5}}' % current_num_computers)
139:                membership_out.write('],"meta":{"methods":0,"type":"%s","count":%d, "version":5}}' % (enumtype, current_num_members))
149:        membership_out.write('],"meta":{"methods":0,"type":"%s","count":%d, "version":5}}' % (enumtype, current_num_members))
```

### bloodhound-ce (CE) outputworker.py — writes "version":6
URL: https://raw.githubusercontent.com/dirkjanm/BloodHound.py/bloodhound-ce/bloodhound/enumeration/outputworker.py
```python
79:                computers_out.write('],"meta":{"methods":0,"type":"computers","count":%d, "version":6}}' % current_num_computers)
90:        computers_out.write('],"meta":{"methods":0,"type":"computers","count":%d, "version":6}}' % current_num_computers)
139:                membership_out.write('],"meta":{"methods":0,"type":"%s","count":%d, "version":6}}' % (enumtype, current_num_members))
149:        membership_out.write('],"meta":{"methods":0,"type":"%s","count":%d, "version":6}}' % (enumtype, current_num_members))
```

---
## SOURCE 7: The ONLY code differences between the master (LEGACY) and bloodhound-ce branches of bloodhound/__init__.py
Verbatim unified diff (master = <, bloodhound-ce = >):
```diff
166c166
<     parser = argparse.ArgumentParser(add_help=True, description='Python based ingestor for BloodHound LEGACY\nFor help or reporting issues, visit https://github.com/dirkjanm/BloodHound.py', formatter_class=argparse.RawDescriptionHelpFormatter)
---
>     parser = argparse.ArgumentParser(add_help=True, description='Python based ingestor for BloodHound Community Edition\nFor help or reporting issues, visit https://github.com/dirkjanm/BloodHound.py', formatter_class=argparse.RawDescriptionHelpFormatter)
273c273
<     logging.info('BloodHound.py for BloodHound LEGACY (BloodHound 4.2 and 4.3)')
---
>     logging.info('BloodHound.py for BloodHound Community Edition')
```

Interpretation (verbatim strings): the LEGACY build self-identifies at startup as "BloodHound.py for BloodHound LEGACY (BloodHound 4.2 and 4.3)"; the CE build self-identifies as "BloodHound.py for BloodHound Community Edition".
