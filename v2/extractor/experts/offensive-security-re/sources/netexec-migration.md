# NetExec (nxc) — Source corpus for FactBank extraction

NetExec is the maintained fork of CrackMapExec. Binary/command renamed `cme` -> `nxc` (also `NetExec`/`netexec`); db tool `cmedb` -> `nxcdb`; home folder `~/.cme` -> `~/.nxc`; config `cme.conf` -> `nxc.conf`; env var `CME_PATH` -> `NXC_PATH`; pip/pipx package `crackmapexec` -> `netexec`. The two sections below are (1) verbatim wiki pages and (2) verbatim GitHub release notes.



============================================================
# PART 1 — WIKI PAGES (verbatim)
============================================================



<<< WIKI: Welcome / README >>>
# Welcome

## NetExec

NetExec (a.k.a nxc) is a network service exploitation tool that helps automate assessing the security of *large* networks.

<figure><img src="/files/pqVKzRGwUvMfsYQcCxws" alt=""><figcaption></figcaption></figure>

<table data-view="cards"><thead><tr><th></th><th></th><th></th><th></th></tr></thead><tbody><tr><td><i class="fa-discord">:discord:</i></td><td><strong>Discord Community</strong></td><td>Join our Discord community to post questions, get help, and share resources</td><td><a href="https://discord.gg/pjwUTQzg8R" class="button secondary">Join Discord</a></td></tr><tr><td><i class="fa-github-alt">:github-alt:</i></td><td><strong>Github</strong></td><td>NetExec is 100% open source and built by developers just like you.</td><td><a href="https://github.com/Pennyw0rth/NetExec" class="button secondary">Submit a PR</a></td></tr><tr><td><i class="fa-flask-vial">:flask-vial:</i></td><td><strong>NetExec Lab</strong></td><td>Deploy and launch a lab focused on Windows Active Directory exploitation</td><td><a href="https://github.com/Pennyw0rth/NetExec-Lab" class="button secondary">Launch a lab</a></td></tr></tbody></table>



<<< WIKI: News: v1.0.0 Release >>>
# v1.0.0 Release!

## The Release of Version 1.0.0!

Hello everyone!\
Today will be our first release of NetExec version 1.0.0 🎉\
If you are reading this you have already found your way to the GitBook wiki, good to see you!\
Here we will give you a rundown of all the new features of NetExec as we release new versions.\
We will also provide documentation of all the existing modules and features to give you an idea of what NetExec is capable of!

<figure><img src="/files/ANB6WF30jCRw55T4qM07" alt=""><figcaption></figcaption></figure>

If you still have questions, feel free to join our [Discord server](https://discord.gg/pjwUTQzg8R) for help or to suggest new ideas and feature requests 📣\
This release is mainly aimed at stability, to provide a solid baseline from which to work. Some minor and major bugs have been fixed, see below for details.

Version 1.1.0 is already in the works, with great new modules in the works as well as new features such as zblurx's delegation technique coming soon to NetExec 🚀\
Stay tuned!

Credit where credit is due: This tool is based on CrackMapExec and was originally created by bytebleeder and maintained by mpgn over the years, shout out to them! With the retirement of mpgn, we ([@zblurx](https://twitter.com/_zblurx), [@Marshall](https://twitter.com/MJHallenbeck) and [@NeffIsBack](https://twitter.com/al3x_n3ff)) decided to maintain the tool NetExec, formerly known as CrackMapExec, as a completely free open source tool.



<<< WIKI: News: v1.1.0 nxc4u >>>
# v1.1.0 - nxc4u

{% embed url="<https://youtu.be/DB79HuYbemw>" fullWidth="false" %}

A new release of NetExec has been released!

In this blog post we will give an overview of what is new in the current release and what we have been working on over the last few weeks. Native binaries for Linux, Windows and MacOS are available on GitHub. The latter has not been tested though, so please report any problems you encounter with any of these binaries.

Over the past month we have had a huge amount of pull requests and issues opened and resolved. We really want to thank you all for the great participation in NetExec. Not only pull requests, but also people filing issues are really valuable. Pointing out what bugs still exist and what features could make nxc even better is really important!

<figure><img src="/files/9rIVM1nYUrZkYixMCqTR" alt=""><figcaption></figcaption></figure>

There were a lot of really cool PRs so lets dive in:

### Ever heard of Kerberos Delegation?

A new core feature has been added that automates the Kerberos extensions S4U2Self and S4U2Proxy by [@zblurx](https://twitter.com/_zblurx). It allows you to abuse Kerberos Constrained Delegation with protocol transition and Resource-based Constrained Delegation automatically in NetExec.

<figure><img src="/files/dqNVbBTyES97JJEKoX7O" alt=""><figcaption></figcaption></figure>

It is also possible to use only S4U2Self in order to impersonate any account on a domain joined computer for which you know the credentials:

<figure><img src="/files/jPv9CYbAt8wePMgNi0b4" alt=""><figcaption></figcaption></figure>

### Execute Tasks on behalf of logged-on Users with Scheduled Tasks

Hunt for users logged on to systems where they shouldn't be 🏹 Executing commands with user sessions is now easier than ever, thanks to the new "schtask\_as" module by [@Defte\_](https://twitter.com/Defte_). This allows you to impersonate logged-on users using the Windows task scheduling mechanism.

<figure><img src="/files/n98zZG8Am5SNQOByeRCT" alt=""><figcaption></figcaption></figure>

### Refactoring and bug fixes

A huge refactoring has been done behind the scenes, mainly by [@MJHallenbeck](https://twitter.com/MJHallenbeck). A number of bugs have been fixed, log messages have been added, and the overall code quality has been greatly improved. The CLI will now check for linting to ensure good code quality in the future :rocket:

A number of other bugs has been fixed, check out the GitHub release page for those!

### BloodHound now supports computer accounts

The BloodHound extension now also marks computer accounts as owned if you compromise the corresponding host, thanks to [@NeffIsBack](https://twitter.com/al3x_n3ff). This comes in handy if you gain local admin privileges through lateral movement or delegation.

<figure><img src="/files/B3rQ9tqbFf3SHw9PRrY7" alt=""><figcaption></figcaption></figure>

### FTP Enhancement

Many great improvements have been contributed by [@RomanRII](https://twitter.com/riiroman). The FTP protocol can now list files in any directory. Also, you can now download and upload files with FTP using the `--get` and `--put` command respectively!

<figure><img src="/files/nFE3WjjbdfZn1urIqMCf" alt=""><figcaption></figcaption></figure>

### Module sorting

Previously, it was difficult to see which modules you could use if you were not already a local or domain administrator. Now modules are sorted by the privileges required for execution so you can get a better idea of which modules are available for further privilege escalation and lateral movement.

<figure><img src="/files/0epQfEQMkO5nKl8tnKVW" alt=""><figcaption></figcaption></figure>

### WinRM improvements

The stability of the WinRM protocol has been greatly improved by [@Xiaoli](https://twitter.com/Memory_before). It is now more light-weight, has better exception handling and better command execution.

### ASCII-Art

We now have a cool spider in our CLI, crawling through the network... :spider::sunglasses:\
Made by [@bongobongostan](https://twitter.com/bongobongostan).

<figure><img src="/files/3bmQsrspejDGiPST9JGp" alt=""><figcaption></figcaption></figure>

### The GitBook wiki is now open source!

At the time of publishing this GitBook will be synced to GitHub. This means anybody can contribute to this GitBook via a Pull Request on GitHub! There is a lot left to do, for example we desperately need a contributors guide, but none of the dev team had time for it.\
You will find the repository of the wiki here: <https://github.com/Pennyw0rth/NetExec-Wiki>

*Notes by* \[[Alex](mailto:undefined)]\(<https://x.com/al3x\\_n3ff>)



<<< WIKI: News: v1.2.0 >>>
# v1.2.0 - ItsAlwaysDNS

Hello everyone!

It has been quite a while since the last release. We now have so many great features that a new release was long overdue. But first of all, a big thank you to all the contributors and people who have contributed ideas, submitted issues and participated on the [Discord server](https://discord.gg/pjwUTQzg8R). So let us dive into the long list of amazing new modules and features and start with our first big announcement.

<figure><img src="/files/qH02OhIEiiasVyYIBxwp" alt=""><figcaption><p>Woop woop</p></figcaption></figure>

## NetExec is available on Kali:rocket:

The biggest news first, thanks to the great help of [@arszilla ](https://x.com/arszilla)this release is also available on kali. After about 3 months of package updates on the Kali side everything is ready for the launch. So now you can just install the latest release with apt:

<figure><img src="/files/LOg8MoDSYnRuox913Cek" alt=""><figcaption><p>Installing NetExec with apt</p></figcaption></figure>

## It's Always DNS ...

... and that's why we now have fully integrated DNS options, thanks to [@XiaoliChan](https://x.com/Memory_before)! You can specify a DNS server with `--dns-server` or force TCP to be used for DNS with `--dns-tcp`. This also allows you to force IPv6 with `-6` and set a DNS timeout with `--dns-timeout`.

![Specifying a dns server](https://github.com/Pennyw0rth/NetExec-Wiki/assets/50464194/42925ec8-c693-48ae-9c02-bb4ef27a1b0a)

## It's Credential Looting Time💰

Ever heard of SCCM? You can now dump all SCCM credentials stored by the DPAPI with the new flag `--sccm`. Also there are a ton of new modules that loot various software which can store credentials like MobaXterm, mRemoteNG, some vnc server software and Google Refresh Tokens, thanks to [@zblurx](https://x.com/_zblurx)!

<figure><img src="https://github.com/Pennyw0rth/NetExec-Wiki/assets/50464194/5301e0f8-39cf-4716-894f-75e8bd197f40" alt=""><figcaption><p>Looting SCCM</p></figcaption></figure>

<figure><img src="https://github.com/Pennyw0rth/NetExec-Wiki/assets/50464194/be55049d-45cf-4b52-be81-502c2b6e0013" alt=""><figcaption><p>Looting MobaXterm</p></figcaption></figure>

<div data-full-width="false"><figure><img src="https://github.com/Pennyw0rth/NetExec-Wiki/assets/50464194/3b919e10-6b67-414e-af11-000645e33d4e" alt=""><figcaption><p>Looting mRemoteNG</p></figcaption></figure></div>

<figure><img src="https://github.com/Pennyw0rth/NetExec-Wiki/assets/50464194/ced41d32-e8ba-4463-af77-d2ce0d9801e8" alt=""><figcaption><p>Looting VNC</p></figcaption></figure>

## Looting PuTTY

Also credentials and RSA private keys stored in PuTTY can be looted thanks to an addition by [@NeffIsBack](https://x.com/al3x_n3ff).

<figure><img src="https://github.com/Pennyw0rth/NetExec-Wiki/assets/50464194/0dd0c207-b244-4244-8668-f7587602453b" alt=""><figcaption><p>Looting RSA private keys and proxy credentials stored by PuTTY</p></figcaption></figure>

## Extract obsolete operating systems from LDAP

With the new LDAP module `-M obsolete` you can query for obsolete operating systems in LDAP! Made by [@Shad0wC0ntr0ller](https://x.com/Shad0wCntr0ller).

![image](https://github.com/Pennyw0rth/NetExec-Wiki/assets/50464194/5eb296e6-3ab4-4932-b7d3-69b88f7a2b7b)

## New LDAP flag for retrieving active Users on the Domain

The new LDAP Flag `--active-users` serves the same purpose as `--users`, but filters out deactivated accounts. Made by [@termanix](https://github.com/termanix).

![image](https://github.com/Pennyw0rth/NetExec-Wiki/assets/50464194/14e39eec-4342-404f-86ae-014c74d6de2d)

## New SMB Module Printerbug

The well-known coercion technique using Printerbug can now be exploited with NetExec, abusing MS-RPRN! Made by [@lodos2005](https://github.com/lodos2005).

<div data-full-width="false"><img src="https://github.com/Pennyw0rth/NetExec-Wiki/assets/50464194/94a83b39-5bec-4934-931b-e33353dc4529" alt="Coercing authentications using NetExec and the new Printerbug module"></div>

![Relaying the incoming connection](https://github.com/Pennyw0rth/NetExec-Wiki/assets/50464194/bd0f18e7-3a94-421b-b763-1fc7445e7c60)

{% embed url="<https://www.thehacker.recipes/ad/movement/mitm-and-coerced-authentications/ms-rprn>" %}

## Hunt for the ADCS using SMB

A new SMB module is now available, that enumerates DCERPC endpoints for certsrv.exe, indicating that the server is a CA. It also enumerates whether the CA is vulnerable against ESC8. Made by [@0xjbb](https://github.com/0xjbb).

![Hunting for ADCS using SMB DCERPC](https://github.com/Pennyw0rth/NetExec-Wiki/assets/50464194/babcd4a5-c96d-4705-b164-d205e0f1b685)

## New LDAP Module Enumerate userPassword and unixUserPassword Attribute

There is software that will populate the LDAP attributes `userPassword` and `unixUserPassword` potentially with credentials in plaintext. The new LDAP modules `-M get-userPasswsord` and `-M get-unixUserPassword` will query all users for these attributes. Made by [@Syzik](https://x.com/SyzikSecu).

![image](https://github.com/Pennyw0rth/NetExec-Wiki/assets/50464194/a01986e8-62ee-496f-ae92-6cfc168a1f31)

## New Winlogon Autologon Module

Windows allows to configure user that will automatically log on to a machine on startup. With the new SMB module by [@swisskyrepo](https://x.com/pentest_swissky) you can now retrieve the content of the keys **DefaultDomainName, DefaultPassword, DefaultUserName, AutoAdminLogon** stored in the registry `HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon`, which are used for that logon process.

![Retrieve autologon credentials from the registry](https://github.com/Pennyw0rth/NetExec-Wiki/assets/50464194/dcaf5906-db93-409a-9937-dbf82ca728b6)

{% embed url="<https://learn.microsoft.com/en-us/troubleshoot/windows-server/user-profiles-and-logon/turn-on-automatic-logon>" %}

## Raw LDAP queries

There is now a new LDAP flag `--query "(Object)" "Filter"` with the standard ldapsearch syntax to be able to quickly look up attributes in LDAP. Made by [@NeffIsBack](https://x.com/al3x_n3ff).

![image](https://github.com/Pennyw0rth/NetExec-Wiki/assets/50464194/145e0573-bf1e-4e18-971b-3f098506c8e3)

## Updated LDAP and SMB User enumeration

SMB/LDAP `--users` and LDAP `--active-users` flags now allow filtering for specific users! Thanks to [@Marshall-Hallenbeck](https://x.com/MJHallenbeck).

<div data-full-width="false"><img src="https://github.com/Pennyw0rth/NetExec-Wiki/assets/50464194/f191bd1f-af45-4cdc-bd84-e82b74bff502" alt=""> <img src="https://github.com/Pennyw0rth/NetExec-Wiki/assets/50464194/e2c4e3eb-ec14-42a7-a895-2df852d2cfe1" alt=""></div>

![](https://github.com/Pennyw0rth/NetExec-Wiki/assets/50464194/28d9208f-b7be-4f06-9505-d1b76e6b4201)

## Updated PSO Module

[@sebrink](https://x.com/_sandw1ch) updated the pso module which retrieves all fine-grained password policies in the domain, giving the module a fresh new look and fixing a critical bug, where a policy wasn't displayed if it was attached to multiple obejcts.

![The new pso module](https://github.com/Pennyw0rth/NetExec-Wiki/assets/50464194/899e73df-e4b0-4db6-9de1-2527bff470d2)

## Authentication throttling

The old `--jitter` option got reworked to enable throttling of authentications. Super useful if you want to be a bit more stealthy or bypass lock out mechanisms. Made by [@NeffIsBack](https://x.com/al3x_n3ff).

## Tab-completion

Thanks to [@Adamkadaban](https://x.com/Adamkadaban) NetExec now supports tab-completion if installed with pipx! Check out the Installation page for the setup.

<figure><img src="/files/XhVG3rzqt32ZpXwzE6Ya" alt=""><figcaption><p>Tab-completion with NetExec</p></figcaption></figure>

## Rework of the Powershell command execution

A major overhaul of the powershell functionality within NetExec has taken place, fixing most bugs and improving overall usability and stability. Obfuscation and Amsi bypasses have also been set to non-default, as they were often flagged even by AVs. A nice side effect is that the `ps32` downgrade now bypasses Windows Defender😄\
Made by [@Marshall-Hallenbeck](https://x.com/MJHallenbeck).

<figure><img src="/files/k5FFX5NgwDxbAZMRYRhA" alt=""><figcaption><p>Bypassing Windows Defender with --force-ps32</p></figcaption></figure>

## Outro

If you want to read about all changes in detail or download the latest standalone binaries check out the github page:

{% embed url="<https://github.com/Pennyw0rth/NetExec/releases/tag/v1.2.0>" %}

*Notes by* \[[Alex](mailto:undefined)]\(<https://x.com/al3x\\_n3ff>)



<<< WIKI: News: v1.3.0 >>>
# v1.3.0 - NeedForSpeed

Hello everyone!

Recently, a lot of incredible Pull Requests have been submitted. Over 22 PRs in 2 weeks! This community activity is incredible, so be prepared for a lot of upcoming features, even if not all of them are included in this release.

Therefore, a big thank you to all the contributors in the past months. Of course, also a big thank you to people who have been submitting issues on github and our [Discord Server](https://discord.gg/pjwUTQzg8R). This is very important to improve the stability and to ensure everything is working as expected.

## NeedForSpeed - NFS

After quite some time, a new protocol has been added: NFS! This provides the ability to detect NFS servers, enumerate shares recursively. You can also download and upload files with the commands `--get-file` and `--put-file` respectively. Big thanks to [@termanix](https://github.com/termanix) for implementing this protocol, with the help of [@Marshall-Hallenbeck](https://x.com/MJHallenbeck) and [@NeffIsBack](https://x.com/al3x_n3ff).

![](https://github.com/user-attachments/assets/214662be-b873-42b1-b515-9f73c28828c3)

![](https://github.com/user-attachments/assets/861765a4-8b45-4390-b7bc-62182e2c1286)

## SCCM LDAP Reconnaissance

There has been a lot of recent research into Microsoft's System Center Configuration Manager (SCCM), also known as Microsoft Endpoint Configuration Manager (MECM). Therefore, [@NeffIsBack](https://x.com/al3x_n3ff) developed a module to detect an SCCM environment in Active directory via LDAP! This will find SCCM Site-Servers, SCCM Sites, SCCM Management Points and Users, Computers or Groups related to SCCM.

![](https://github.com/user-attachments/assets/8e9f3f14-0f98-453d-8db7-4abe5dc5b7da)

## coerce\_plus Module

The new coerce\_plus module combines all 5 coercion methods (PetitPotam, DFSCoerce, MSEven, ShadowCoerce and PrinterBug). You can now check all these vulnerabilities with a single module, rather than one by one! If you want to coerce authentications with one of these techniques, just set a LISTENER ip. Made by [@lodos2005](https://github.com/lodos2005).

![](https://github.com/user-attachments/assets/fcc9d81f-15a1-4d44-8b3a-f9c534973153)

## Identify Pre-Created Computer Accounts

Pre-WIndows 2000 computer accounts are valuable targets during engagements, as by default the password is set to the computer name. [@Shad0wC0ntr0ller](https://x.com/Shad0wCntr0ller) developed a module to identify these accounts and save a ccache for accounts, where the password was not changed. If you want to learn more, check out this great article at TrustedSec: <https://trustedsec.com/blog/diving-into-pre-created-computer-accounts>

![](https://github.com/user-attachments/assets/f2423fdb-d649-4fbf-baac-23eac596b4b7)

## Hunting for passwords in PowerShell Histories

The Powershell History can be a goldmine for credentials. If admins forget to clear their history and passwords are typed in the console, they can be easily extracted. Thanks to [@357384n](https://github.com/357384n) we have a new module, which will check the history of all users on the target for keywords that might get you plaintext credentials.

![](https://github.com/user-attachments/assets/5cdc6d16-341b-41d4-9e7d-9b78a363af44)

## Detection for the Guest Session

Unsure about the anonymous authentication? NetExec now has a new flag to detect, if the guest session is active! Thanks to [@Marshall-Hallenbeck](https://x.com/MJHallenbeck) for nice idea.

![](https://github.com/user-attachments/assets/6d3f7b15-8c0e-432d-8318-bf2d94ef9b83)

## Retrieving networks and subnets via new SMB Interfaces flag

The new SMB flag `--interfaces` will enumerate all interfaces on the target. Very useful to find subnets and servers for pivoting! Made by [@Sant0rryu](https://github.com/Sant0rryu).

![](https://github.com/user-attachments/assets/ceb885df-50e7-410f-971b-01ff107f5f81)

## Enumerating BitLocker

The new BitLocker module `-M bitlocker` is checking the BitLocker status on all drives. Also this module is available in both WMI and SMB! Made by [@termanix](https://github.com/termanix).

![](https://github.com/user-attachments/assets/ec6ac04d-5172-4201-aa41-497f8e0bb47e)

## Find Security Questions

This SMB module will dump security questions and answers for all users on the machine. Made by [Adamkabadan](https://github.com/Adamkadaban).

![](https://github.com/user-attachments/assets/9a28219d-b17a-4432-99a7-e4d7fe7862d0)

## Enumerate Hyper-V Hosts

Hyper-V saves the Hostname of the hypervisor in the registry. With this module you can query that information from any target VMs. Made by [@joaovarelask](https://x.com/joaovarelas)

![](https://github.com/user-attachments/assets/14a12c1d-12a6-4c3b-a6b0-995a16b6f155)

## Checks Regarding Defender AV via WCC Module

The WCC module got some new checks regarding Windows Defender settings. E.g. you can check if Defender has exclusions set for specific paths or file extensions. Made by [@jubeaz](https://github.com/jubeaz).

![](https://github.com/user-attachments/assets/e469059e-3113-4e7d-87c8-47160f3214c7)

## Smbghost Scanning Module

With the new SMB module `-M smbghost`, you can check for prerequisits that have to be enabled for the SMBGhost vulnerability. Made by [@r4anan](https://x.com/r4vanan).

![](https://github.com/user-attachments/assets/8f17c451-76ed-40dd-bc06-2f26b5277126)

## Outro

If you want to read about all changes in detail or download the latest standalone binaries check out the github page:

{% embed url="<https://github.com/Pennyw0rth/NetExec/releases/tag/v1.3.0>" %}

*Notes by* \[[Alex](mailto:undefined)]\(<https://x.com/al3x\\_n3ff)_and>\_ [*@termanix*](https://github.com/termanix)



<<< WIKI: News: v1.4.0 >>>
# v1.4.0 - SmoothOperator

Hello everyone!

It has been almost half a year since the last release and **a lot** of new features have been added since then. Besides the most dominant protocol, SMB, other protocols like NFS, LDAP, and MSSQL have seen some love with new modules and improvements.

Thank you to everyone who contributed over the past months, and of course, a big thank you to everyone who has been reporting issues on GitHub and helping to troubleshoot or taking part in discussions on Discord. If you want to join our Discord, follow the [link](https://discord.gg/pjwUTQzg8R).

In case you didn't know, this wiki is open source too and you can contribute to it. If you would like to add missing content or improve existing content, please feel free to do so. Any help is much appreciated! You can find the wiki's source code on GitHub [here](https://github.com/Pennyw0rth/NetExec-Wiki).

## Backup Operator to Domain Admin

As the name suggest, the new module `-M backup_operator` can leverage the Backup Operator privileges to dump the SAM / SECURITY of the DC. This ultimately leads to a full compromise of the domain with the dump of the NTDS.dit. Huge thanks to [@mpgn](https://x.com/mpgn_x64) for this module.

![Backup Operator to full domain compromise](https://github.com/user-attachments/assets/bce85c5a-ffb1-4b17-9d02-acd76b4d51cd)

## Certificate Authentication

NetExec now also supports certificate authentication, thanks to the integration of [@dirkjanm](https://x.com/_dirkjan)'s [PKINITtools](https://github.com/dirkjanm/PKINITtools) authentication mechanisms into NetExec, by [@mpgn](https://x.com/mpgn_x64).

```bash
--pfx-cert/--pfx-base64 with --pfx-pass for PFX certificates
--pem-cert with --pem-key for PEM certificates
```

![Certificate authentication using a pfx certificate](https://github.com/user-attachments/assets/c758b9bc-a587-4ced-84ec-453af69ae90c)

![Certificate authentication using a crt and key certificate](https://github.com/user-attachments/assets/90558bd8-3f81-428e-afb3-97719e7aa231)

## NFS Escape to Root File System

Recent research has shown that the default NFS configuration on Linux systems is often insecure.\
In short: The NFS server does not check if a requested file is inside the exported directory.\
This means that if a user has access to the NFS share, they can access any file on the system. In combination with write access, this can lead to a full compromise of the system.

The details of the attack can be found on our wiki page [here](/nfs-protocol/escape-to-root-file-system.md) or on the great blog post by the guys from [HvS Consulting](https://www.hvs-consulting.de/en/blog/nfs-security-identifying-and-exploiting-misconfigurations).

An implementation of the attack is now available in NetExec, indicating the vulnerability by a new flag in the host banner. The implementation was done by [@NeffIsBack](https://x.com/al3x_n3ff).

**Note**: **With this update, the semantics of the file download and upload flags have been changed. Don't forget to check at the new** [**flag usage**](/nfs-protocol/download-and-upload-files.md)**.**

![Example how to own a Debian host with read/write privileges and no\_root\_squash enabled (the latter is not necessarily needed)](https://github.com/user-attachments/assets/2c2a0f98-3493-42bb-bc26-234836b722f1)

## Dumping SAM and LSA

One of NetExec's most prominent features is dumping the local account database (SAM) and the SECURITY registry hive (LSA secrets). Previously, Impacket achieved this by writing the SAM and SECURITY hives to a temporary file on disk, which was then deleted. However, this has now changed, as [@laxaa](https://github.com/laxaa) has implemented a method that retrieves the data directly from the registry hives via the remote registry service, which he has contributed to Impacket. Thanks to [@mpgn](https://x.com/mpgn_x64)'s integration, this method is now the default in NetExec and should offer much greater stealth. However, if you need to use the old method for some reason, you can still switch back with `--sam/--lsa secdump`.

## Timeroasting the Domain

The Timeroast attack has been added as a module to NetExec. This attack allows an attacker on the network to request a hashed & salted version of **any** computer account NT hash in the domain **without** the need for authentication. If you would like to know more about the attack, check out [this article](https://cybersecurity.bureauveritas.com/uploads/whitepapers/Secura-WP-Timeroasting-v3.pdf) from [@SecuraBV](https://x.com/SecuraBV). Module by [@Disgame\_](https://x.com/Disgame_).

<figure><img src="/files/lS6ViPEnIfdWXh11kGZQ" alt=""><figcaption><p>Timeroast attack to retrieve hashed and salted computer NT hashes</p></figcaption></figure>

## QWINSTA

While the `--loggedon-users` flag is very useful if you don't have administrative privileges yet, if you do have control over the host it can be very useful to know **where** users are connecting from. Thanks to [@Defte](https://x.com/Defte_), NetExec uses the native `qwinsta` protocol implementation from Impacket to enumerate RDP sessions on the target, providing information such as the connecting IP address and session state.

<figure><img src="/files/fVGWalAjnvRSCGFMKkVa" alt=""><figcaption><p>Using qwinsta to enumerate active RDP sessions on the host</p></figcaption></figure>

## Tasklist

One of the best ways to trigger an EDR is to run the command `-x 'tasklist /v /fo csv | findstr /i "lsass"'`. However, listing tasks can be very useful for finding out what PID `lsass.exe` has or for checking which services are running with which privileges. Thanks to [@Defte](https://x.com/Defte_), NetExec now has a native implementation of the `tasklist` command that uses a native Windows protocol to query this information, which makes it less likely for EDRs to detect.

<figure><img src="/files/pSLxZcZagCmghOlRCWG2" alt=""><figcaption><p>Query the tasklist over a native Windows protocol</p></figcaption></figure>

## SMB Share Listing Option

You can now list SMB shares directories with new `--dir` SMB flag! Created by [@y0no](https://github.com/y0no).

![Take a look into shares with the new --dir flag](https://github.com/user-attachments/assets/8ef5d270-0b86-4cf8-acee-f4ae370e59e7)

## NFS Share Listing Option

The NFS protocol has a build in share listing option as well. Without specifying a share it will try to use the [escape-to-root-fs](/nfs-protocol/escape-to-root-file-system.md) and list the root of the file system. Made by [@NeffIsBack](https://x.com/al3x_n3ff).

<figure><img src="/files/tVlGYXUFmfOt5Eyu9zcD" alt=""><figcaption><p>Listing directories with NFS and if possible the root file system</p></figcaption></figure>

## WAM Module

On the hunt for Entry ID or M365 access tokens? The new `wam` module by [@zblurx](https://x.com/_zblurx) dumps you these tokens from the local Token Broker Cache. You can find a great article by [@xpn](https://x.com/_xpn_) [here](https://blog.xpnsec.com/wam-bam/) if you want to learn more.

## Enumerate Delegation Configurations in the Domain

It is now easier to enumerate miss configured delegation privileges, thanks to the integration by [@termanix](https://github.com/termanix) of impackets findDelegation.py tool. With the new LDAP flag `--find-delegation` any delegation can be found in the domain, including information about the user/computer object and the delegation details.

![Enumerate delegation configurations in the domain](https://github.com/user-attachments/assets/be853996-137e-4ff2-b46a-0956a208e86d)

## LDAPS Channel Binding now Supported

The new integration of LDAP Channel Binding is now available in Impacket, which means hardened environments are not a problem anymore. The LDAP protocol automatically picks up the required security options and will work out of the box without user interaction. Thanks to [@NeffIsBack](https://x.com/al3x_n3ff) who took care of the Pull Request in Impacket.

![Native LDAP Channel Binding support](https://github.com/user-attachments/assets/3dcb9ff0-e0b6-4df5-b643-3bd662182915)

## RID Brute Force on MSSQL

You probably know the `--rid-brute` feature of the [SMB protocol](/smb-protocol/enumeration/enumerate-users-by-bruteforcing-rid.md), but do you also know that this is possible with the [MSSQL protocol](/mssql-protocol/enumerate-users-by-bruteforcing-rid.md) as well? Well, now you can do it with NetExec, thanks to the work of [@Adamkadaban](https://x.com/Adamkadaban)!

![Enumerate Domain Users and Groups with MSSQL](https://github.com/user-attachments/assets/6ee1749b-650c-420b-aa5c-76009847035f)

## Coercing with MSSQL

Coercing connections with SMB is a well-known technique that can be achieved by using the `coerce_plus` module in NetExec. However, it is now also possible to coerce connections using MSSQL and the new `mssql_coerce` module by [@lodos](https://x.com/lodos2005)!

![Coercing SMB authentications with the MSSQL protocol](https://github.com/user-attachments/assets/272c2b13-53a2-436c-afdc-1a82152ced82)

## Shadow RDP Module

The new shadowrdp module allows you to enable or disable [Shadow RDP](https://learn.microsoft.com/en-us/troubleshoot/windows-server/remote/shadow-terminal-server-session), which can be used to eavesdrop on a specific RDP session. Module by [@Dfte](https://x.com/Defte_).

![Enable or disable shadow RDP on the target host](https://github.com/user-attachments/assets/0cf2a863-baf5-4df5-9113-99ae029abc38)

## Notepad++ Module

Finding credentials in text files never happens, right? Right??

Well, even typing in sensible content into unsaved notepad++ documents can be dangerous, as they still leave traces on the system. With the new `notepad++` module by [@Dfte](https://x.com/Defte_) you can automatically dump this information :rocket:

![Dumping unsaved notepad++ documents](https://github.com/user-attachments/assets/462b4dc3-1d7e-4fca-9292-04e4e4c39156)

## New Modules on MSSQL

[@deathflamingo](https://github.com/deathflamingo) added **six** new modules for the MSSQL protocol! That includes a few enumeration modules, as well as modules to perform actions on linked servers:

* `enum_impersonate`: List users that can be impersonated (similar to the mssql\_priv module)
* `enum_logins`: Enumerate active MSSQL logins
* `enum_links`: Enumerate linked MSSQL servers
* `exec_on_link`: Execute SQL queries on a linked server
* `link_enable_cmdshell`: Enable/Disable the cmd shell on a linked server
* `link_xpcmd`: Execute shell commands on the linked server

<figure><img src="/files/HCfuHc2hCRKqVy2a9yEx" alt=""><figcaption><p>A bunch of new modules for the MSSQL protocol</p></figcaption></figure>

## Enumerate Recently Accessed Files

By default, Windows creates LNK files for recently accessed objects and stores them in the `AppData\Roaming\Microsoft\Windows\Recent` directory. This module retrieves and parses these LNK files in order to extract the source files, which can be useful during internal assessments for retrieving recently modified and potentially juicy files. Module by [@Defte](https://x.com/Defte_).

<figure><img src="/files/hq5UE6bEpU4pkwByUMkQ" alt=""><figcaption><p>Enumerate recently accessed files</p></figcaption></figure>

## Snipping Tool Module

Admins, think twice before taking screenshots of sensitive data! With the new `snipped` module you can automatically dump all screenshots done by the Windows Snipping Tool. Module by [@Yeeb1](https://x.com/Yeeb_).

<figure><img src="/files/HlZk0gF4FecZa8G91CFT" alt=""><figcaption><p>Automatically download all screenshots from the target host</p></figcaption></figure>

## Uploading and Downloading files with SSH

The SSH protocol now also has `--get-file` and `--put-file` flags, to enable the easy upload and download of files with an authenticated session. Made by [@jdholtz](https://github.com/jdholtz).

<figure><img src="/files/TAQB3XwPzvRX0idUi998" alt=""><figcaption><p>Upload and Download files via SSH</p></figcaption></figure>

## Remote UAC

This module enables you to disable, or more realistically re-enable, the remote UAC. This might be useful after manual exploitation, for example, to restore the system's original security (never leave a system more vulnerable than when you found it!). Module by [@Defte](https://x.com/Defte_).

<figure><img src="/files/NzFEo1JqyzzOrbQfldNG" alt=""><figcaption><p>Enabling the remote UAC of the target system</p></figcaption></figure>

## Detect drop-the-MIC

The [drop-the-MIC attack](https://www.thehacker.recipes/ad/movement/ntlm/relay#mic-message-integrity-code) is known for quite some time, but still really powerful if you find an outdated host. Relaying SMB traffic to LDAP? No Problem!

With the new module `remove-mic` made by [@XiaoliChan](https://x.com/Memory_before) you can easily check if the target is vulnerable to CVE-2019-1040, aka drop the MIC :fire:

![Check for CVE-2019-1040 aka drop-the-MIC](https://github.com/user-attachments/assets/e34cacc8-6601-4039-ba8d-b9739fe7fa3a)

## DPAPI Hash

Interested in dumping DPAPI hashes? This module, `dpapi_hash`, extracts DPAPI 'hashes' based on the user's protected master key, which can then be brute-forced with Hashcat (modes 15310 or 15900). Module by [@nikaiw](https://github.com/nikaiw).

![Dump the DPAPI hashes of users' master keys](https://github.com/user-attachments/assets/af676b4a-aadc-40f5-b8d5-cf1521d35281)

## Automatically Generate Hosts File

NetExec now creates host files for machines enumerated over SMB with `--generate-hosts-file <filename>`, making it easier to add/remove the `/etc/hosts` in CTFs and in real life. Made by [@mpgn](https://x.com/mpgn_x64).

![Generate the /etc/hosts file with hosts discovered over SMB](https://github.com/user-attachments/assets/ffe68e1f-ea15-4ecc-86b3-abc059064691)

## Automatically Generate KRB5 File

The new SMB flag `--generate-krb5-file <filename>` generates a valid `krb5.conf` file, similar to `--generate-hosts-file`, to enable Kerberos authentication with other tools. Made by [@mpgn](https://x.com/mpgn_x64).

![Generate a kerberos config file with the SMB](https://github.com/user-attachments/assets/e0655094-72fd-42d0-b9b9-8bceef049a8c)

## Outro

If you want to read about all changes in detail or download the latest standalone binaries check out the GitHub release page:

{% embed url="<https://github.com/Pennyw0rth/NetExec/releases/tag/v1.4.0>" %}

*Notes by* \[[Alex](mailto:undefined)]\(<https://x.com/al3x\\_n3ff)_and>\_ [*@termanix*](https://github.com/termanix)*, copyedit by* [Marshall Hallenbeck](mailto:undefined)



<<< WIKI: Installation for Unix >>>
# Installation for Unix

## Installing NetExec with pipx :saxophone:

{% hint style="info" %}
We do recommend to install rust before to make sure everything will work properly

```
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

Also, on some distributions, python headers may not be installed with python but are needed for [arc4 dependency](https://pypi.org/project/arc4/) build. To [install them](https://stackoverflow.com/questions/21530577/fatal-error-python-h-no-such-file-or-directory#answer-21530768) if you encounter `arc4.c:2:10: fatal error: Python.h: No such file or directory` error.
{% endhint %}

Using [pipx](https://github.com/pypa/pipx) to install NetExec is recommended. This allows you to use NetExec and the nxcdb system-wide.

```bash
sudo apt install pipx git
pipx ensurepath
pipx install git+https://github.com/Pennyw0rth/NetExec
```

Open a new shell and you are ready to go:

```bash
NetExec
nxcdb
```

Updating via pipx:

```bash
pipx upgrade netexec        # Will update if there is a new version
pipx reinstall netexec      # Force download the latest commits from github
```

#### Failed building wheel for aardwolf

If pip fails to build aardwolf you need to [install rust](https://www.rust-lang.org/tools/install). Don't forget to reload your shell so rust is added to your PATH!

## Installation for Kali :dragon\_face:

```bash
apt update
apt install netexec
```

## Installation for BlackArch :dagger:

```bash
pacman -Syu netexec
```

## Installation for ParrotSec 🦜

```bash
apt update
apt install netexec
```

## Availability on other Unix distributions :penguin:

[![Packaging status](https://repology.org/badge/vertical-allrepos/netexec.svg)](https://repology.org/project/netexec/versions)

## Installation for development using UV

Install uv (and rust)

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
apt install pipx git
pipx ensurepath
pipx install uv
```

Now that UV is set up, we can download the NetExec repository and install its dependencies:

```bash
git clone https://github.com/Pennyw0rth/NetExec
cd NetExec
uv tool install .
uv run netexec
```

## Installation for development using Poetry :postal\_horn:

{% hint style="warning" %}
We do not recommend to install poetry via APT on kali
{% endhint %}

You're going to need to install [Poetry](https://python-poetry.org/docs/#installation) which is what nxc uses to manage dependencies. To install poetry you should use [pipx](https://github.com/pypa/pipx), because our dynamic-versioning plugin will likely crash otherwise.

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
apt install pipx git
pipx ensurepath
pipx install poetry
poetry self add "poetry-dynamic-versioning[plugin]"
poetry dynamic-versioning enable
```

Now that poetry is set, up and we can download the NetExec repository and install its dependencies:

```bash
git clone https://github.com/Pennyw0rth/NetExec
cd NetExec
poetry install
poetry run NetExec
```

## Binaries

We recommend installing via pipx/pip, but if you want to use a pre-compiled binary, go to the [Releases](https://github.com/Pennyw0rth/NetExec/releases) and download the appropriate binary.



<<< WIKI: Installation for Windows >>>
# Installation for Windows

## Using Python and pipx

{% hint style="success" %}
If Python is available it is recommended to install NetExec with pipx
{% endhint %}

{% hint style="warning" %}
For Windows, git and Rust are required for installation. If you can't install either of these, see below for a standalone executable.
{% endhint %}

Set up git, Rust and C++:\
<https://git-scm.com/download/win>\
<https://www.rust-lang.org/tools/install>\
<https://visualstudio.microsoft.com/de/visual-cpp-build-tools/>

Install pipx and NetExec directly from the repository:

```bash
pip install pipx
python -m pipx ensurepath
python -m pipx install git+https://github.com/Pennyw0rth/NetExec
```

Restart your command line and you should be able to execute NetExec:

```bash
NetExec
```

## Using NetExec Binary

1. Download the latest Windows binary on the [release ](https://github.com/Pennyw0rth/NetExec/releases)page (netexec-windows-latest)
2. Unzip the folder
3. Run the binary from the command line

## From Python ZippApp

{% hint style="warning" %}
Not all functionalities have been tested
{% endhint %}

1. You can also use the [standalone](https://www.python.org/downloads/windows/) version of Python, then add the path of the folder containing the python.exe file to the **PATH** env variable of your user.
2. Download the ZippApp for your specific OS & Python version [here](https://github.com/Pennyw0rth/NetExec/actions/runs/6374124950)
3. Then just run the binary `python.exe .\nxc`

{% embed url="<https://www.python.org/downloads/windows/>" %}

If you got this error

```bash
FileNotFoundError: [Errno 2] No such file or directory: 'C:\Users\Admin.shiv\nxc_51b7721208fc3d0af7e301aa9a56e1da0a38e9ec5bc08bfe8cc9ba14853ac5d1.tmp\site-packages\nxc\data\powersploit\CodeExecution\Invoke-ReflectivePEInjection_Resources\DemoDLL_RemoteProcess\DemoDLL_RemoteProcess\DemoDLL_RemoteProcess.vcxproj.filters
```

Add the following registry key:

```bash
REG ADD "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\FileSystem" /v LongPathsEnabled /t REG_DWORD /d 1 /f
```



<<< WIKI: Post Installation Setup / Tab Completion / Homefolder >>>
# Post Installation Setup

## Setting up Tab Completion

Currently, we use [argcomplete](https://github.com/kislyuk/argcomplete) to automatically do tab completion through argparse.

Once you've installed nxc globally, do the following:

{% hint style="info" %}
Installing with pipx is recommended for global availability
{% endhint %}

```bash
sudo apt install python3-argcomplete

# For Bash
register-python-argcomplete nxc >> ~/.bashrc

# For Zsh
register-python-argcomplete nxc >> ~/.zshrc
```

Open a new shell and you are ready to go:

```bash
NetExec
netexec
nxc
```

## Configuring NetExec's Homefolder

NetExec will create a folder to which the `nxc.conf` configuration file and all other data created/extracted during day-to-day use are written. The default folder that will be created is `~/.nxc`. If you would like to change the destination folder set the environment variable `NXC_PATH` to the target folder.



<<< WIKI: Selecting & Using a Protocol >>>
# Selecting & Using a Protocol

## Available Protocols

```bash
smb
ssh
ldap
ftp
wmi
winrm
rdp
vnc
mssql
nfs
```

Note that not all protocols support the same functionality, be sure to check each protocol's options

## Using Protocol Options

To view a protocols options, run: `nxc <protocol> --help`

Then use those options: `nxc <protocol> <protocol options>`

## Viewing Available Protocols

Running `nxc --help` will list general options and protocols that are available (Notice the 'protocols' section below):

```bash
#~ nxc --help
usage: nxc [-h] [-t THREADS] [--timeout TIMEOUT] [--jitter INTERVAL] [--no-progress] [--verbose] [--debug] [--version] {smb,ssh,ldap,ftp,wmi,winrm,rdp,vnc,mssql} ...

    <-- Banner -->   

options:
  -h, --help            show this help message and exit
  -t THREADS            set how many concurrent threads to use (default: 100)
  --timeout TIMEOUT     max timeout in seconds of each thread (default: None)
  --jitter INTERVAL     sets a random delay between each connection (default: None)
  --no-progress         Not displaying progress bar during scan
  --verbose             enable verbose output
  --debug               enable debug level information
  --version             Display nxc version

protocols:
  available protocols

  {smb,ssh,ldap,ftp,wmi,winrm,rdp,vnc,mssql,nfs}
    smb                 own stuff using SMB
    ssh                 own stuff using SSH
    ldap                own stuff using LDAP
    ftp                 own stuff using FTP
    wmi                 own stuff using WMI
    winrm               own stuff using WINRM
    rdp                 own stuff using RDP
    vnc                 own stuff using VNC
    mssql               own stuff using MSSQL
    nfs                 own stuff using NFS
```



<<< WIKI: Using Credentials >>>
# Using Credentials

## Using Credentials

Every protocol supports using credentials in one form or another. For details on using credentials with a specific protocol, see the appropriate wiki section.

Generally speaking, to use credentials, you can run the following commands:

```bash
nxc <protocol> <target(s)> -u username -p password
```

{% hint style="success" %}
Code execution results in a (**Pwn3d!**) added after the login confirmation. With the SMB protocol, your compromised users are most likely in the (local) administrators group.
{% endhint %}

| Protocol | See Pwn3d! in output                                   |
| -------- | ------------------------------------------------------ |
| FTP      | No check                                               |
| SSH      | root (otherwise specific message) :white\_check\_mark: |
| WINRM    | Code execution at least :space\_invader:               |
| LDAP     | Path to domain admin :crown:                           |
| SMB      | Most likely (local) admin :white\_check\_mark:         |
| RDP      | Code execution at least :space\_invader:               |
| VNC      | Code execution at least :space\_invader:               |
| WMI      | Most likely local admin :white\_check\_mark:           |

{% hint style="info" %}
When using usernames or passwords that contain special symbols (especially exclaimation points!), wrap them in single quotes to make sure your shell interprets them as a string.
{% endhint %}

Example:

```bash
nxc <protocol> <target(s)> -u username -p 'October2022!'
```

{% hint style="info" %}
Due to a [bug](https://bugs.python.org/issue9334) in Python's argument parsing library, credentials beginning with a dash (`-`) will throw an `expected at least one argument` error message. To get around this, specify the credentials by using the 'long' argument format (note the `=` sign):
{% endhint %}

```bash
nxc <protocol> <target(s)> -u='-username' -p='-October2022'
```

## Using a Credential Set From the Database

By specifying a credential ID (or multiple credential IDs) with the `-id` flag, nxc will automatically pull that credential from the back-end database and use it to authenticate (saves a lot of typing):

```bash
nxc <protocol> <target(s)> -id <cred ID(s)>
```

## Multi-Domain Environment

You can use nxc with mulitple domain environment

```bash
nxc <protocol> <target(s)> -u FILE -p password
```

Where **FILE** is a file with usernames in this format

```bash
DOMAIN1\user
DOMAIN2\user
```

## Brute Forcing & Password Spraying

All protocols support brute-forcing and password spraying. For details on brute-forcing/password spraying with a specific protocol, see the appropriate wiki section.

By specifying a file or multiple values nxc will automatically brute-force logins for all targets using the specified protocol:

Examples:

```bash
nxc <protocol> <target(s)> -u username1 -p password1 password2
```

```bash
nxc <protocol> <target(s)> -u username1 username2 -p password1
```

```bash
nxc <protocol> <target(s)> -u ~/file_containing_usernames -p ~/file_containing_passwords
```

```bash
nxc <protocol> <target(s)> -u ~/file_containing_usernames -H ~/file_containing_ntlm_hashes
```

## Password Spraying Without Bruteforce

Can be useful for protocols like WinRM and MSSQL. This option avoids bruteforcing when you use files (-u file -p file).

```bash
nxc <protocol> <target(s)> -u ~/file_containing_usernames -H ~/file_containing_ntlm_hashes --no-bruteforce
```

```bash
nxc <protocol> <target(s)> -u ~/file_containing_usernames -p ~/file_containing_passwords --no-bruteforce
```

```bash
user1 -> pass1
user2 -> pass2
```

{% hint style="info" %}
By default nxc will exit after a successful login is found. Using the --continue-on-success flag will continue spraying even after a valid password is found. Useful for spraying a single password against a large user list. The --continue-on-success flag is incompatible with command execution.
{% endhint %}

```bash
nxc <protocol> <target(s)> -u ~/file_containing_usernames -H ~/file_containing_ntlm_hashes --no-bruteforce --continue-on-success
```

### Throttling Authentication Requests

{% hint style="warning" %}
Authentication throttling works on a per-host basis! Keep this in mind if you are spraying credentials against multiple hosts.
{% endhint %}

If there is a need to throttle authentications during brute forcing, you can use the jitter functionality. The length of the timeout (in seconds) between requests is randomly selected from an interval unless otherwise specified. If you want to hardcode the timeout, set the upper and lower bounds of the interval to the same value. The syntax is as follows:

```bash
nxc <protocol> <target> --jitter 3 -u ~/file_containing_usernames -p ~/file_containing_passwords
nxc <protocol> <target> --jitter 2-5 -u ~/file_containing_usernames -p ~/file_containing_passwords
nxc <protocol> <target> --jitter 4-4 -u ~/file_containing_usernames -p ~/file_containing_passwords
```



<<< WIKI: Using Modules >>>
# Using Modules

## Using Modules

### Viewing Available Modules for a Protocol

Run `nxc <protocol> -L` to view available modules for the specified protocol.

For example to view all modules for the SMB protocol:

```bash
nxc smb -L
```

### Using a Module

Run `nxc <protocol> <target(s)> -M <module name>`.

For example to run the SMB Mimikatz module:

```bash
nxc smb <target(s)> -u Administrator -p 'October2022' -M lsassy
```

### Viewing Module Options

Run `nxc <protocol> -M <module name> --options` to view a modules supported options, e.g:

```bash
nxc smb -M lsassy --options
```

### Using Module Options

Module options are specified with the `-o` flag. All options are specified in the form of KEY=value (msfvenom style)

Example:

```bash
nxc <protocol> <target(s)> -u Administrator -p 'P@ssw0rd' -M lsassy -o COMMAND=xxxxxxxxug'
```

### 🆕 Running Multiple Modules

Simply define all the modules you want, each proceeded by a `-M` option flag:

```bash
nxc <protocol> <target(s)> -u Administrator -p 'P@ssw0rd' -M spooler -M iis -M lsassy -M winscp
```



<<< WIKI: Database General Usage >>>
# Database General Usage

## Database General Usage

nxc automatically stores all used/dumped credentials (along with other information) in its database which is setup on first run.

Each protocol has its own database which makes things much more sane and allows for some awesome possibilities. Additionally, there are workspaces (like Metasploit), to separate different engagements/pentests.

For details and usage of a specific protocol's database see the appropriate wiki section.

All workspaces and their relative databases are stored in `~/.nxc/workspaces`

## Interacting with the Database

nxc ships with a secondary command line script `nxcdb` which abstracts interacting with the back-end database. Typing the command `nxcdb` will drop you into a command shell:

```bash
#~ nxcdb
nxcdb (default) >
```

## Listing Help

At anytime, just type "help" for a list of commands:

```bash
nxcdb (default)(smb) > help

Documented commands (type help <topic>):
========================================
clear_database  creds  dpapi  exit  export  groups  help  hosts  shares  wcc

Undocumented commands:
======================
back  import
```

## Workspaces

The default workspace name is called 'default' (as represented within the prompt), once a workspace is selected everything that you do in nxc will be stored in that workspace.

To create a workspace:

```bash
nxcdb (default) > workspace create test
[*] Creating workspace 'test'
<-- CUT -->
nxcdb (test) >
```

To switch workspace:

```bash
nxcdb (test) > workspace default
nxcdb (default) >
```

To list workspaces:

```bash
nxcdb (test) > workspace list
[*] Enumerating Workspaces
default
==> test
```

## Accessing a Protocol's Database

To access a protocol's database simply run `proto <protocol>`, for example:

```bash
nxcdb (test) > proto smb
nxcdb (test)(smb) >
```

As you can see by the prompt, we are now in the workspace called 'test' and using the SMB protocol's database. Every protocol database has its own set of commands, you can run `help` to view available commands.

Please refer to the appropriate wiki section for details and usage of a specific protocol's database.

To switch protocol database:

```bash
nxcdb (test)(smb) > back
nxcdb (test) > proto http
nxcdb (test)(http) >
```

## :new: Exporting From the Database

You can export information from the database in a few different ways

```bash
nxcdb (test)(smb) > export shares detailed file.csv
```

For all of the up to date options, type `help export`

```bash
nxcdb (default)(smb) > help export

export [creds|hosts|local_admins|shares|signing|keys] [simple|detailed|*] [filename]
Exports information to a specified file

* hosts has an additional third option from simple and detailed: signing - this simply writes a list of ips of
hosts where signing is enabled
* keys' third option is either "all" or an id of a key to export
    export keys [all|id] [filename]
```



<<< WIKI: Target Formats >>>
# Target Formats

## Target Formats

Every protocol supports targets by CIDR notation(s), IP address(s), IP range(s), hostname(s), a file containing a list of targets or combination of all of the latter:

```bash
nxc <protocol> poudlard.wizard
```

```bash
nxc <protocol> 192.168.1.0 192.168.0.2
```

```bash
nxc <protocol> 192.168.1.0/24
```

```bash
nxc <protocol> 192.168.1.0-28 10.0.0.1-67
```

```bash
nxc <protocol> ~/targets.txt
```



<<< WIKI: Audit Mode >>>
# Audit Mode

Audit Mode is a configuration-based feature in NetExec that redacts credentials from console output.

In the config file located at `~/.nxc/nxc.conf` add the character of your choice on the line `audit_mode`

If you don't want the audit mode, just leave it blank!



<<< WIKI: DNS Options >>>
# DNS options

There are several options that can be set to configure the DNS server that is used.\
Besides forcing NetExec to use ipv6 there is an option to set the dns server manually, set a dns timeout or to configure using tcp for dns resolution:

```bash
nxc <protocol> <target(s)> -u username -p password --dns-server <dns-server ip>
nxc <protocol> <target(s)> -u username -p password --dns-timeout <seconds>
nxc <protocol> <target(s)> -u username -p password --dns-tcp    # Use TCP for DNS
nxc <protocol> <target(s)> -u username -p password -6           # Enforce ipv6

```



============================================================
# PART 2 — GITHUB RELEASE NOTES (verbatim, Pennyw0rth/NetExec)
============================================================



===== RELEASE v1.5.1 (v1.5.1) =====

# **Notice**

This release is a unique patch version for a security vulnerability in the `spider_plus` module. All users should upgrade to this version ASAP by installing from GitHub via pipx. We are working on releasing this version to Kali natively. A huge thank you to @RaynLight on reporting this professionally and responsibly - we love our community!



## What's Changed

* **Fix for arbitrary file write via spider_plus module** by @Marshall-Hallenbeck in https://github.com/Pennyw0rth/NetExec/pull/1121

* Fix binaries by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/1050

* Rename windows binary by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/1051

* Allow changing password for locked pre2k accounts by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/1056

* Fix Not Listing All User on Groups by @termanix in https://github.com/Pennyw0rth/NetExec/pull/1055

* Fix ls arg in nfs by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/1057

* [ShadowCopy] Add `list-snapshots` function for SMB & WMI by @XiaoliChan in https://github.com/Pennyw0rth/NetExec/pull/1053

* Fixes #1068 - FTP module --ls flag now displays hidden files (dotfiles) by @strikoder in https://github.com/Pennyw0rth/NetExec/pull/1069

* Add database fix commands for Windows by @Signum21 in https://github.com/Pennyw0rth/NetExec/pull/1070

* Fix inconsistent LDAP attribute name in module get-userPassword.py by @Barneee in https://github.com/Pennyw0rth/NetExec/pull/1090

* Properly handle shell metacharacters in command output for wmi by @Adamkadaban in https://github.com/Pennyw0rth/NetExec/pull/1094

* Minor RDP enhancement by @Mauriceter in https://github.com/Pennyw0rth/NetExec/pull/1066

* Refactor is_host_dc call based on file generation flags by @mpgn in https://github.com/Pennyw0rth/NetExec/pull/1097

* Fix NFS get_file and put_file auth during path traversal by @0xdf223 in https://github.com/Pennyw0rth/NetExec/pull/1103

* Add issue template config and PR template check workflow by @Marshall-Hallenbeck in https://github.com/Pennyw0rth/NetExec/pull/1105

* Add AI policy by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/1109

* fix(snipped): properly parse and set output file for saved screenshots by @Marshall-Hallenbeck in https://github.com/Pennyw0rth/NetExec/pull/1122



## New Contributors

* @strikoder made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/1069

* @Signum21 made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/1070

* @Barneee made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/1090

* @0xdf223 made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/1103



**Full Changelog**: https://github.com/Pennyw0rth/NetExec/compare/v1.5.0...v1.5.1


===== RELEASE v1.5.0 (v1.5.0) =====

## What's Changed

* Add missing Pillow package to binary workflow by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/644

* Update nfs.py by @bandrel in https://github.com/Pennyw0rth/NetExec/pull/645

* fix: Refactor output file path construction in SMB protocol by @moscowchill in https://github.com/Pennyw0rth/NetExec/pull/650

* Added more AV Signatures by @n00py in https://github.com/Pennyw0rth/NetExec/pull/660

* Update database.py by @nikaiw in https://github.com/Pennyw0rth/NetExec/pull/658

* Fix bunch of stuff from ippsec and 0xdf writeup for vintage box  by @mpgn in https://github.com/Pennyw0rth/NetExec/pull/663

* Fix pfx output path on windows by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/665

* Fix authentication with an empty domain by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/667

* Update pylnk3 to remove debug print by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/669

* Upgrade the schtask_as module so that we can upload binaries and execute them  by @Dfte in https://github.com/Pennyw0rth/NetExec/pull/668

  * You can now customize the command and binary that is executed, so you can provide your custom executables with its flags

* New change-password module. by @KriyosArcane in https://github.com/Pennyw0rth/NetExec/pull/512

  * `STATUS_PASSWORD_MUST_CHANGE` locking you out is a thing of the past, just reset the password

* Fix domain trust with kerberos in ldap by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/677

* remove old server code unused by @mpgn in https://github.com/Pennyw0rth/NetExec/pull/662

* Add a check if the database scheme contains the unique attribute by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/681

* Disable signing in LDAP temporarily by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/682

* Automatically preserve state of "advanced options" on the target by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/686

  * MSSQL execution will automatically backup and restore the "advanced options", as well as the "xp_cmdshell" options to preserve the original settings of the target server

* Add option to  --spider and add recyclebin.py module by @Dfte in https://github.com/Pennyw0rth/NetExec/pull/463

  * The admin finally deleted the password.txt on the desktop? Well, if the recyclebin wasn't emptied you are in luck...

* new module: mssql > enable_cmdshell by @crosscutsaw in https://github.com/Pennyw0rth/NetExec/pull/557

* fix(ntlm): include server hostname in Workstation field of Authentication by @cyberG33k02 in https://github.com/Pennyw0rth/NetExec/pull/694

* Fix winrm database logic by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/696

* eventlog_creds Module  by @lodos2005 in https://github.com/Pennyw0rth/NetExec/pull/452

  * If process creation auditing is enabled, there can be hidden gems (credentials) in the event log. This new modules will find them for you.

* Updated whoami and find-computer modules by @Cyb3rC3lt in https://github.com/Pennyw0rth/NetExec/pull/695

* Update PULL_REQUEST_TEMPLATE.md by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/699

* Fix ldap simple auth with base object by @mpgn in https://github.com/Pennyw0rth/NetExec/pull/670

* update ntdsutil.py to behave like --ntds by @crosscutsaw in https://github.com/Pennyw0rth/NetExec/pull/691

* Add Badsuccessor module by @mpgn in https://github.com/Pennyw0rth/NetExec/pull/702

  * Checking for BadSuccessor made easy!

* Fix logging port and also update the port when switching to LDAPS by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/703

* Switch LDAP source to fixed version by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/704

* Check for win server 2025 instead of DFL 2025 by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/705

* Improve eventlog_creds by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/706

* Fix hostname info if no ntlm and not resolution by @mpgn in https://github.com/Pennyw0rth/NetExec/pull/671

* Make nxc compatible with bloodhound-ce zip by @mpgn in https://github.com/Pennyw0rth/NetExec/pull/664

  * BloodHound Community Edition is taking over and now we also support its collector. If you want to swap to the legacy collector, change the config setting.

* Update Ruff and Fix Linting by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/629

* Switch impacket branch to Pennyw0rth fork by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/707

* Fix spec file by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/710

* REopen Update --dc-list Now check trusted domains DCs by @termanix in https://github.com/Pennyw0rth/NetExec/pull/666

  * Integration of domain trust into the `--dc-list` flag

* Ldap checker removal by @zblurx in https://github.com/Pennyw0rth/NetExec/pull/709

  * Built-in checks for LDAP signing and channelBinding requirements in the host banner!

* Add base_dn option to subnet module by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/714

* Update kerberoast command output to be idiomatic by @t94j0 in https://github.com/Pennyw0rth/NetExec/pull/711

* Enable asreproast with anonymous ldap logins by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/712

* Fix querying when non searchResultEntries are returned by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/717

* Move version log after file logger is attached by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/722

* Add error handling if we can't mount share with --ls by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/724

* new module: smb > presence by @crosscutsaw in https://github.com/Pennyw0rth/NetExec/pull/561

  * Admins are breaking the tier infrastructur? Now you have a module to check for such artifacts

* Fixing --generate-hosts-file smb option by @Mojo8898 in https://github.com/Pennyw0rth/NetExec/pull/725

* Refactoring nxc path and adding support for XDG Base Directory - addressing issue #558 by @d4ytox in https://github.com/Pennyw0rth/NetExec/pull/649

* Add new SMB module to extract GPO deployed privilege assignments by @Yeeb1 in https://github.com/Pennyw0rth/NetExec/pull/493

* Add efsr_spray module by @rtpt-romankarwacik in https://github.com/Pennyw0rth/NetExec/pull/718

* Fix dns resolution when finding 2025 dc by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/737

* New module: AWS Credentials Finder by @dev-fortress in https://github.com/Pennyw0rth/NetExec/pull/455

* Skip cbt check if port explicitly set to 389 by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/741

* New SMB Module Notepad by @termanix in https://github.com/Pennyw0rth/NetExec/pull/608

  * This module extracts the contents of unsaved notepad files, similar to the notepad++ module

* Fix function to check if hosts is a dc or not by @mpgn in https://github.com/Pennyw0rth/NetExec/pull/739

* Fix conn reset error on windows if dc doesnt have tls cert by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/743

* Fixed minor typo in issue template by @Reelix in https://github.com/Pennyw0rth/NetExec/pull/747

* Fix #744 by @zblurx in https://github.com/Pennyw0rth/NetExec/pull/745

* Add Kerberoasting support with no-preauth user by @azoxlpf in https://github.com/Pennyw0rth/NetExec/pull/719

  * You can now kerberoast even **without** valid credentials. How? Use an account which does not require pre-authentication.

* Fix two minor bugs by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/750

* Update mssql enum login by @mpgn in https://github.com/Pennyw0rth/NetExec/pull/755

* Update flag to better understand by @mpgn in https://github.com/Pennyw0rth/NetExec/pull/756

* Fix enum_links module privilege requirement by @zblurx in https://github.com/Pennyw0rth/NetExec/pull/760

* fix hashcat/John format for TGS-REP by @azoxlpf in https://github.com/Pennyw0rth/NetExec/pull/765

* Update wcc.py by @v3gahax in https://github.com/Pennyw0rth/NetExec/pull/766

* Fix winrm's ps_execute() to return output by @tiagomanunes in https://github.com/Pennyw0rth/NetExec/pull/767

* Only display success message if accounts found by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/772

* fix: color SMB STATUS_NOLOGON_WORKSTATION_TRUST_ACCOUNT as magenta by @azoxlpf in https://github.com/Pennyw0rth/NetExec/pull/773

* Image size improvements and pinned Netexec version by @kaisersource in https://github.com/Pennyw0rth/NetExec/pull/735

* State that using a BINARY for schtask_as is optional by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/775

* Update bitlocker.py - Corrected BitLocker EncryptionMethods by @Powett in https://github.com/Pennyw0rth/NetExec/pull/774

* Add module to find the entra-id sync server by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/763

  * You want to pivot into entra id? Find the server with the new `entry-id` module and dump its sync credentials with the msol module.

* Patch --qwinsta --tasklist stack trace by @Dfte in https://github.com/Pennyw0rth/NetExec/pull/777

* Add the taskkill option by @Dfte in https://github.com/Pennyw0rth/NetExec/pull/779

  * Your  payload hangs? Just kill the process from remote.

* Add process filtering in --tasklist by @Dfte in https://github.com/Pennyw0rth/NetExec/pull/782

* setRemoteName to avoid Kerberos SPN resolution error in rid_brute by @azoxlpf in https://github.com/Pennyw0rth/NetExec/pull/784

* Patches the --filter-shares so that it correctly finds READ,WRITE perm by @Dfte in https://github.com/Pennyw0rth/NetExec/pull/787

* Allows --qwinsta to filter for a specific user by @Dfte in https://github.com/Pennyw0rth/NetExec/pull/783

* Add get-info-users module by @sepauli in https://github.com/Pennyw0rth/NetExec/pull/769

  * Passwords can be found everywhere in LDAP, for example in the "info" attribute of a user. This new modules will query these fields for you.

* fix(ldap): support get-sid and admin flag when using --use-kcache by @azoxlpf in https://github.com/Pennyw0rth/NetExec/pull/789

* [WCC] Improve NBTNS check and add LLMNR check by @fpreynaud in https://github.com/Pennyw0rth/NetExec/pull/701

* add huge disclaimer to issue template by @Marshall-Hallenbeck in https://github.com/Pennyw0rth/NetExec/pull/795

* new module: ldap > dump-computers by @crosscutsaw in https://github.com/Pennyw0rth/NetExec/pull/556

* docs: add deprecation change type and clarify e2e tests checklist by @Marshall-Hallenbeck in https://github.com/Pennyw0rth/NetExec/pull/794

* Add entra id sync credentials extractor by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/764

* deprecation: remove the horrible opsec flag by @mpgn in https://github.com/Pennyw0rth/NetExec/pull/788

* Refactor get-network and fix encoding by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/803

* Switch pso module to core feature by @mpgn in https://github.com/Pennyw0rth/NetExec/pull/798

* Removing the horrible multiple hosts option by @mpgn in https://github.com/Pennyw0rth/NetExec/pull/804

* Fix veeam script if there is no salt reg key by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/808

* Slinky set lnk target by @Geetub in https://github.com/Pennyw0rth/NetExec/pull/800

* Add ldap parsing to daclread by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/811

* Fix NFS Network Value by @termanix in https://github.com/Pennyw0rth/NetExec/pull/813

* Fix command execution in wmi by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/812

* Update LDAP find-computer Module by @termanix in https://github.com/Pennyw0rth/NetExec/pull/805

* Add raw-ntds-copy module by @0xb11a1 in https://github.com/Pennyw0rth/NetExec/pull/468

  * AV blocks access to the SAM/SECURITY/SYSTEM registry hives? This module will mount the disk and parse its raw content to extract the sam, lsa, and NTDS secrets! Also available for the WMI and WINRM protocol!

* Refactor WMI protocol execution by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/820

* Add WMI to ntds_dump_raw module by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/821

* Add TARGET option to ntds-dump-raw to dump LSA/SAM hashes by @0xb11a1 in https://github.com/Pennyw0rth/NetExec/pull/828

* docs(contributors): add termanix and dfte to awesome contributors by @Marshall-Hallenbeck in https://github.com/Pennyw0rth/NetExec/pull/835

* Refactor smb spider by @haytechy in https://github.com/Pennyw0rth/NetExec/pull/729

* Add null-auth info to host banner by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/836

  * The server allows authentication without credentials? This is now automatically displayed in the host banner

* Improve daclread: also allow passing a file for TARGET_DN, and refactor by @tiagomanunes in https://github.com/Pennyw0rth/NetExec/pull/832

* Rework atexec and -M schtask_as to rely on a single TSCH_EXEC class by @Dfte in https://github.com/Pennyw0rth/NetExec/pull/818

* Add 'Warning' rule to linting by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/838

* Fixed typo in smb.py by @x-ticker in https://github.com/Pennyw0rth/NetExec/pull/841

* Fix dpapi by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/844

* Revert "Merge pull request #729 from haytechy/refactor_SMBSpider" by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/845

* Add --reg-sessions option to SMB protocol by @MaxToffy in https://github.com/Pennyw0rth/NetExec/pull/824

  * Until now session enumeration required admin privileges on the host. The new `--reg-sessions` option enumerates them with normal user privileges!

* Added `DUMP_TICKETS` flag to lsassy module by @gatariee in https://github.com/Pennyw0rth/NetExec/pull/833

* Add --database option to MSSQL protocol by @A3-N in https://github.com/Pennyw0rth/NetExec/pull/847

  * Built-in options for database enumerations for the MSSQL protocol

* Fixing the bug report issue template, currently not present on github by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/850

* remove ntds warning as it is solved now by @mpgn in https://github.com/Pennyw0rth/NetExec/pull/853

* Fix typo by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/855

* [SMB] Added new smb module to enumerate active network interfaces over SMB by @fulc2um in https://github.com/Pennyw0rth/NetExec/pull/846

* Update schtask_as.py to help bypass detection by @Kahvi-0 in https://github.com/Pennyw0rth/NetExec/pull/721

* Add ability to execute commands via RDP by @Adamkadaban in https://github.com/Pennyw0rth/NetExec/pull/676

  * You can now execute commands using the RDP protocol!

* Added the lockscreendoors module by @E1A in https://github.com/Pennyw0rth/NetExec/pull/837

* Update Masky module to 0.2.1 (fix warning message) by @Z4kSec in https://github.com/Pennyw0rth/NetExec/pull/858

* add guest check on recon by @mpgn in https://github.com/Pennyw0rth/NetExec/pull/856

  * Automatic checks if the guest account is enabled, if the config flag is configured in `~/.nxc/nxc.conf`

* Update gpp_password.py by @P4cm4n90 in https://github.com/Pennyw0rth/NetExec/pull/867

* fix(ldap): return False for general OS errors by @Marshall-Hallenbeck in https://github.com/Pennyw0rth/NetExec/pull/876

* Show success messages when krb conf is saved. by @adityatelange in https://github.com/Pennyw0rth/NetExec/pull/863

* Fix aardwolf logging by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/898

* Fix stacktrace with anon auth and using gmsa by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/899

* Refactor to use internal ldap search function to prevent stack traces by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/900

* fix(printnightmare): do not exit thread on failure to bind so other modules can run by @Marshall-Hallenbeck in https://github.com/Pennyw0rth/NetExec/pull/884

* fix(dc_list): disable automatic configuration of DNS so we can point it to the target by @Marshall-Hallenbeck in https://github.com/Pennyw0rth/NetExec/pull/875

* Fix 879 by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/901

* Unnecessary file by @lodos2005 in https://github.com/Pennyw0rth/NetExec/pull/904

* Fix poetry run pytest & adding tests to ntds-dump-raw module by @0xb11a1 in https://github.com/Pennyw0rth/NetExec/pull/830

* display group description for --groups by @Marshall-Hallenbeck in https://github.com/Pennyw0rth/NetExec/pull/885

* Remove efsr_spray module, superceded by simply using EPM map on the EFS interface by @rtpt-romankarwacik in https://github.com/Pennyw0rth/NetExec/pull/866

* Add module categories by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/859

  * The number of modules keep growing and growing. We introduce module categories to help keeping it organized.

* Add ldap pass-pol option #868 by @mpgn in https://github.com/Pennyw0rth/NetExec/pull/877

* Updated schtasks_as.py to control if output will be provided by @SGMG11 in https://github.com/Pennyw0rth/NetExec/pull/907

* New module: SCCM enumeration on DP and PSS with winreg by @Mauriceter in https://github.com/Pennyw0rth/NetExec/pull/586

* [New Module] CVE 2025 33073 by @Mauriceter in https://github.com/Pennyw0rth/NetExec/pull/905

  * New module to check if the NTLM reflection attack has been patched!

* Fix MAQ module crash by @azoxlpf in https://github.com/Pennyw0rth/NetExec/pull/909

* Enforce that category is one of the enums by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/916

* fix(enum_ca): properly return false if theres an error with fetchList by @Marshall-Hallenbeck in https://github.com/Pennyw0rth/NetExec/pull/887

* fix(webdav): handle transport errors and prevent session crash by @azoxlpf in https://github.com/Pennyw0rth/NetExec/pull/914

* catch BrokenPipe and transport errors to prevent session crash by @azoxlpf in https://github.com/Pennyw0rth/NetExec/pull/918

* Resolve hostname to IP in dc_list when no --dns-server is given by @azoxlpf in https://github.com/Pennyw0rth/NetExec/pull/911

* Allow kerberoasting on specific users by @Marshall-Hallenbeck in https://github.com/Pennyw0rth/NetExec/pull/912

* Minor bug fixes by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/920

* Stop logging NXDOMAIN multiple times in DNS resolution by @azoxlpf in https://github.com/Pennyw0rth/NetExec/pull/851

* Allow kerbroast computers by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/919

* Fix missing , by @Dfte in https://github.com/Pennyw0rth/NetExec/pull/929

* Add certificate request options to schtask_as by @Dfte in https://github.com/Pennyw0rth/NetExec/pull/908

  * Instead of executing commands in the context of another user you can just request a certificate in their context. This allows you to directly impersonate them on any machine.

* enum_av module: add checkpoint indicators by @joaovarelas in https://github.com/Pennyw0rth/NetExec/pull/932

* [NTLM reflection] Fix false assumption over smb signing by @Dfte in https://github.com/Pennyw0rth/NetExec/pull/935

* Add dedent for easier reading by @Dfte in https://github.com/Pennyw0rth/NetExec/pull/937

* Striped by @Dfte in https://github.com/Pennyw0rth/NetExec/pull/938

* Use SMBv1 in enum_host_info to get Windows version from smbv1 by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/946

* Add certipy module with 'find' implementation by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/857

  * ADCS is still a major attack vector for threat actors. This module integrates the certipy "find" command to give an easy overview over the existing certificate templates and (mis-)configurations.

* Readd removed code by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/951

* Catch dns resolver issue when domain can't be resolved by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/952

* Add stderr printing to winrm execution by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/957

* Fix winrm output for powershell by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/961

* Query the samaccountname instead of queryint the name and appending the dollar sign by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/969

* feat(schtask_as): improve ADCS certificate handling and PFX retrieval by @azoxlpf in https://github.com/Pennyw0rth/NetExec/pull/962

* Update dump-computers.py by @crosscutsaw in https://github.com/Pennyw0rth/NetExec/pull/941

* Refactor filename templating by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/970

* Fix Procdump by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/975

* Changed print() statements to new print-only logging method by @danwroy in https://github.com/Pennyw0rth/NetExec/pull/925

* Fix nxcdb signing export by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/977

* Fix RDP execution without output by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/983

* fix: Correct typos in WINRM argparse by @augustus-7613 in https://github.com/Pennyw0rth/NetExec/pull/988

* enum_av module: add FortiClient and FortiEDR indicators by @Janrdrz in https://github.com/Pennyw0rth/NetExec/pull/990

* Fix dir listing on NFS by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/991

* Database rework by @zblurx in https://github.com/Pennyw0rth/NetExec/pull/727

* Add LDAP signing and LDAPS channel binding info to db by @stfnw in https://github.com/Pennyw0rth/NetExec/pull/982

* Fix encoding issue and use proper LDAP attr parsing in SCCM module by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/994

* Polish #895 and fix numerous bugs by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/995

* Add raisechild module  by @azoxlpf in https://github.com/Pennyw0rth/NetExec/pull/792

  * Automatic cross-forest privilege escalation!

* Fix Kerberos authentication handling in certipy-find by @azoxlpf in https://github.com/Pennyw0rth/NetExec/pull/981

* Switch impacket back to fortra by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/998

* Add error checking to mssql_exec by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/997

* Make --debug and --verbose mutually exclusive by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/1000

* added support for `--generate-st` and `--delegate-spn` flags by @gatariee in https://github.com/Pennyw0rth/NetExec/pull/825

* New module : drop-library-ms by @XedSama in https://github.com/Pennyw0rth/NetExec/pull/657

  * This module implements yet another technique to force Windows into sending credentials to you

* Remove useless option group subtitles by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/1004

* feat(db): modified the change-password module to modify the password in DB by @lap1nou in https://github.com/Pennyw0rth/NetExec/pull/1005

* enum_av module: add Kaseya EDR Agent indicator by @Janrdrz in https://github.com/Pennyw0rth/NetExec/pull/1009

* Fix import to fix sqlalchemy deprecation warning by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/1010

* feat(db): adding add-computer credential by @lap1nou in https://github.com/Pennyw0rth/NetExec/pull/1008

* Update firefox.py for new AES-256-CBC encryption (fix dpapi error) by @hilarex in https://github.com/Pennyw0rth/NetExec/pull/968

* Add MSSQL LSA and SAM dump by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/1003

  * Do you have Admin privs on an MSSQL server? Then you can now dump SAM and LSA secrets conveniently with the new `--sam`/`--lsa` flags

* Fix sam/lsa dump if user is not local admin by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/1011

* fix: MSSQL db fix by @lap1nou in https://github.com/Pennyw0rth/NetExec/pull/1012

* Fix bug when using delegation by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/1014

* Fix issues with transferring large or non-UTF-8 data over NFS by @lebr0nli in https://github.com/Pennyw0rth/NetExec/pull/1017

* Add credential manager dump feature to winrm protocol by @tiagomanunes in https://github.com/Pennyw0rth/NetExec/pull/768

  * You can now dump (some) dpapi secrets via WinRM!

* Remove duplicate module by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/1022

* Fix/mssql xpcmdshell permission check by @azoxlpf in https://github.com/Pennyw0rth/NetExec/pull/960

* Fix NetBIOS resolution in raisechild by @azoxlpf in https://github.com/Pennyw0rth/NetExec/pull/1025

* --no-admin-check flag for smb to disable the "admin check" with SC_MANAGER_ALL_ACCESS which is done by default by @4zuk4m in https://github.com/Pennyw0rth/NetExec/pull/1026

* enum_av : add WithSecure Elements detector by @Testeur-2-stylos in https://github.com/Pennyw0rth/NetExec/pull/1020

* Update impacket by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/1027

* Insert FQDN instead of NETBIOS name into winrm db by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/1028

* BUG Fix: VNC, better handling of RFB 3.3 by @Mauriceter in https://github.com/Pennyw0rth/NetExec/pull/943

* Fix accidental creation of empty workspace by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/1033

* Add --history option for NTDS by @KriyosArcane in https://github.com/Pennyw0rth/NetExec/pull/759

  * You can now also dump AES Kerberos keys and the password history of users from the Domain Controller.

* [MSSQL] Add EncryptionReq flag to MSSQL proto by @Dfte in https://github.com/Pennyw0rth/NetExec/pull/939

  * Encryption requirements will now be displayed automatically in the host banner

* added support for LDAP simple auth by @c4pit0ch3f in https://github.com/Pennyw0rth/NetExec/pull/648

* Added share exclusion functionality by @MickeyDB in https://github.com/Pennyw0rth/NetExec/pull/680

* Add AES key support for golden ticket forging by @azoxlpf in https://github.com/Pennyw0rth/NetExec/pull/1034

* enum_av module: add Malwarebytes EDR Agent indicator by @Janrdrz in https://github.com/Pennyw0rth/NetExec/pull/1040

* New module `dns-nonsecure` by @MaxToffy in https://github.com/Pennyw0rth/NetExec/pull/1038

  * This module will automatically discover DNS zones where you can add records without any authentication!

* Small logging adjustment by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/1046

* NXCDB RDP hosts by @Dfte in https://github.com/Pennyw0rth/NetExec/pull/1039

* Release version 1.5.0 - Yippie-Ki-Yay by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/1048



## New Contributors

* @bandrel made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/645

* @moscowchill made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/650

* @KriyosArcane made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/512

* @crosscutsaw made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/557

* @cyberG33k02 made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/694

* @Cyb3rC3lt made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/695

* @t94j0 made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/711

* @Mojo8898 made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/725

* @d4ytox made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/649

* @dev-fortress made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/455

* @Reelix made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/747

* @azoxlpf made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/719

* @v3gahax made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/766

* @tiagomanunes made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/767

* @kaisersource made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/735

* @Powett made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/774

* @Geetub made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/800

* @0xb11a1 made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/468

* @x-ticker made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/841

* @gatariee made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/833

* @A3-N made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/847

* @fulc2um made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/846

* @E1A made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/837

* @Z4kSec made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/858

* @P4cm4n90 made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/867

* @adityatelange made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/863

* @SGMG11 made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/907

* @Mauriceter made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/586

* @danwroy made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/925

* @augustus-7613 made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/988

* @Janrdrz made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/990

* @stfnw made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/982

* @XedSama made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/657

* @hilarex made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/968

* @lebr0nli made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/1017

* @4zuk4m made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/1026

* @c4pit0ch3f made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/648

* @MickeyDB made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/680



**Full Changelog**: https://github.com/Pennyw0rth/NetExec/compare/v1.4.0...v1.5.0


===== RELEASE v1.4.0 (v1.4.0) =====

## What's Changed

* Fix runasppl.py by @Hackndo in https://github.com/Pennyw0rth/NetExec/pull/458

* Fixed issue with --options flag by @haytechy in https://github.com/Pennyw0rth/NetExec/pull/466

* Fix a bytes-like object is required, not str` in `nxc/protocols/smb.py` by @Chocapikk in https://github.com/Pennyw0rth/NetExec/pull/470

* Drop support for Python 3.8 and 3.9 by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/460

* Code and stability improvements   by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/473

* fix(nfs): check if status is 13 and print out permission denied for share by @Marshall-Hallenbeck in https://github.com/Pennyw0rth/NetExec/pull/474

* [SMB] Add --dir option by @y0no in https://github.com/Pennyw0rth/NetExec/pull/462

  * You can now list the content of any SMB share by specifying `--dir` and an optionally Path or `--share`

* Mssql automatic backup&restore for optionis by @0xQRx and @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/405

* Fix nmap XML parser when looking for ftp service by @j-mie in https://github.com/Pennyw0rth/NetExec/pull/486

* Add option to generate hosts file for smb proto to first blood more quickly on htb by @mpgn in https://github.com/Pennyw0rth/NetExec/pull/482

  * With the new option `--generate-hosts-file <path>` you can auto generate the `/etc/hosts` file for e.g. AD labs

* schtask_as - Delete task when there is an error by @Kahvi-0 in https://github.com/Pennyw0rth/NetExec/pull/481

* Fix veeam output by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/487

* New LDAP Flag Find Delegation by @termanix in https://github.com/Pennyw0rth/NetExec/pull/381

  * The new ldap flag `--find-delegation` enumerates all configured delegations in the domain

* Bugfix : exec-method specified in module file is not used by @snowpeacock in https://github.com/Pennyw0rth/NetExec/pull/438

* add an option to ioxidresolver to get only IP values different than targets by @nikaiw in https://github.com/Pennyw0rth/NetExec/pull/380

* Allow for empty domains by @TheToddLuci0 in https://github.com/Pennyw0rth/NetExec/pull/488

* Update impacket so ldaps channel binding is supported by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/495

  * Hardened environments shouldn't be a problem anymore, the LDAP protocol should now work in all situations

* Speed improvements and bug fixes by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/498

* Timeroast module by @Disgame in https://github.com/Pennyw0rth/NetExec/pull/311

  * Will retrieve all computer passwords in a windows-ntp-hash format from an unauthenticated perspective

* Bugfix: file extension filter of spiderplus was misleading/broken by @Joytide in https://github.com/Pennyw0rth/NetExec/pull/499

* Fix RDP '--nla-screenshot' option by @lap1nou in https://github.com/Pennyw0rth/NetExec/pull/502

* Fix TARGET_DN object query by @MaxToffy in https://github.com/Pennyw0rth/NetExec/pull/500

* Add baseDN flag to ldap by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/503

* Add rid-brute flag to mssql protocol by @Adamkadaban in https://github.com/Pennyw0rth/NetExec/pull/492

  * New `--rid-brute` flag for the mssql protocol, which enumerates users in the domain

* Add mssql_coerce Module by @lodos2005 in https://github.com/Pennyw0rth/NetExec/pull/456

  * Coercing is now possible with the mssql protocol as well

* Upgrade dploot to 3.0.3 by @zblurx in https://github.com/Pennyw0rth/NetExec/pull/491

  * `--dpapi` now also loots Firefox cookies

  * New `wam` module which dumps Entra and M365 access tokens from Token Broker Cache

  * Updated of the dploot package

* [SMB] Powershell history module rework by @Dfte in https://github.com/Pennyw0rth/NetExec/pull/449

* Add the shadow RDP module by @Dfte in https://github.com/Pennyw0rth/NetExec/pull/465

  * Checks if Shadow RDP is enabled which can be used to eavesdrop on a particular RDP session and even interact with it

* [SMB] Rework the runasppl module by @Dfte in https://github.com/Pennyw0rth/NetExec/pull/451

* [SMB] Add the Notepad++ module by @Dfte in https://github.com/Pennyw0rth/NetExec/pull/444

  * This new module dumps unsaved and thus backed up notepad files from Appdata\Roaming\Notepad++\Backup

* Added new modules for mssql - namely enum_impersonate, enum_logins, enum_links, exec_on_link, link_enable_xp, link_xpcmd by @deathflamingo in https://github.com/Pennyw0rth/NetExec/pull/415

  * The module `enum_impersonate` displays all users with impersonation privileges

  * The module `enum_logins` active login sessions

  * The module `enum_links` displays all linked MSSQL Servers 

  * The module `exec_on_link` let's you execute commands on linked servers

  * The module `link_xpcmd ` let's you enable or disable the `xp_cmdshell` on a linked servers

* fix ruff by @mpgn in https://github.com/Pennyw0rth/NetExec/pull/506

* Update pyproject.toml to add missing dependency for wam module by @Mortimus in https://github.com/Pennyw0rth/NetExec/pull/509

* fix trust relation for smb by @mpgn in https://github.com/Pennyw0rth/NetExec/pull/510

* Remove smb from ldap proto by @mpgn in https://github.com/Pennyw0rth/NetExec/pull/508

  * No more SMB in the LDAP protocol, just plain LDAP ðŸŽ‰

* fix trust relation for ldap by @mpgn in https://github.com/Pennyw0rth/NetExec/pull/511

* Add new SMB module to download Screenshots created by Snipping Tool by @Yeeb1 in https://github.com/Pennyw0rth/NetExec/pull/368

  * Automatically download all Screenshots from the target with the new `snippet` module, maybe you find some creds in it?

* Change error to fail message by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/515

* Add a query for the linked server config if we are local admin by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/516

* Rename ldapConnection to the new ldap_connection var #508 #4767762 - Fix Modules by @lodos2005 in https://github.com/Pennyw0rth/NetExec/pull/520

* Fix #514 by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/522

* [SMB] Allow force to disable SMBv1 by @XiaoliChan in https://github.com/Pennyw0rth/NetExec/pull/523

* [Module] Add remove mic check by @XiaoliChan in https://github.com/Pennyw0rth/NetExec/pull/521

  * The new module `remove-mic` checks for the CVE-2019-1040, also known as "Drop the Mic"

* Fix user-desc.py by @lap1nou in https://github.com/Pennyw0rth/NetExec/pull/526

* Show error messages when rdp fails by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/528

* [PrintNightmare] Add more exception catch in module by @XiaoliChan in https://github.com/Pennyw0rth/NetExec/pull/529

* Improve LDAP dc-list flag by @termanix in https://github.com/Pennyw0rth/NetExec/pull/476

* ssh: allow for putting and getting files by @jdholtz in https://github.com/Pennyw0rth/NetExec/pull/524

  * Uploading/Downloading files via ssh is now possible with `--put-file`/`--get-file` respectively

* coerce_plus: Support DCERPC for PrinterBug by @rtpt-romankarwacik in https://github.com/Pennyw0rth/NetExec/pull/505

* push bloodhound to 1.8 by @mpgn in https://github.com/Pennyw0rth/NetExec/pull/532

* fix connection issue with socks ldap by @mpgn in https://github.com/Pennyw0rth/NetExec/pull/530

* Refactor ssh by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/531

* add certificate authentication aka pass-the-cert by @mpgn in https://github.com/Pennyw0rth/NetExec/pull/533

  * Certificate authentication in NetExec ðŸŽ‰ 

  * Use `--pfx-cert`/`--pfx-base64` with `--pfx-pass` for PFX certificates

  * Use `--pem-cert` with `--pem-key` for PEM certificates

* Update license file and lint py version by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/535

* switch default conn from smbv1 to smbv3 by @mpgn in https://github.com/Pennyw0rth/NetExec/pull/534

* fix pfx auth on non dc by @mpgn in https://github.com/Pennyw0rth/NetExec/pull/536

* Fix spec file by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/538

* update dploot to 3.1.0 by @zblurx in https://github.com/Pennyw0rth/NetExec/pull/539

* Add dpapi hash module based on the work of @fist0urs by @nikaiw in https://github.com/Pennyw0rth/NetExec/pull/379

  * Dump the users hashed passwords from dpapi

* fix ruff by @mpgn in https://github.com/Pennyw0rth/NetExec/pull/545

* Add option generate-krb5-file for krb5 configuration by @mpgn in https://github.com/Pennyw0rth/NetExec/pull/544

* Swap cert-pem to pem-cert to match pfx syntax by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/546

* Fix: privileged groups SID not found error by @Joytide in https://github.com/Pennyw0rth/NetExec/pull/547

* Ruff fixed LDAP protocol  by @termanix in https://github.com/Pennyw0rth/NetExec/pull/553

* Fix lsass Dump Files Deleting Process When Dump Fail by @termanix in https://github.com/Pennyw0rth/NetExec/pull/542

* Updated exe files while putting for evasion by @termanix in https://github.com/Pennyw0rth/NetExec/pull/541

* [smb] Always delete service when using smbexec by @jdholtz in https://github.com/Pennyw0rth/NetExec/pull/552

* Add Backup operators module by @mpgn in https://github.com/Pennyw0rth/NetExec/pull/537

  * Automate the privilege escalation from the `Backup Operators` group to the Domain Admins including an NTDS.dit dump ðŸš€ 

* Update users and active-users against anonymous ldap authentication by @termanix in https://github.com/Pennyw0rth/NetExec/pull/441

* Fix hardcoded option by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/560

* Fix #564 by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/565

* Exception handling for spider_plus  by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/569

* [smb] Always delete output file by @jdholtz in https://github.com/Pennyw0rth/NetExec/pull/568

* Bugfixes for py3.13 by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/571

  * Added official support for Python 3.13

* LDAP checker fix when checking without creds by @zblurx in https://github.com/Pennyw0rth/NetExec/pull/573

* Refactored powershell_history module to fix case sensitivity by @Mercury0 in https://github.com/Pennyw0rth/NetExec/pull/575

* Fix ASCII Art by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/576

* Rename ambigous function by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/577

* [SMB] Add the --qwinsta and --tasklist options by @Dfte in https://github.com/Pennyw0rth/NetExec/pull/445

  * The new flag `--qwinsta` enumerates sessions on the target including much useful information like IPv4 of the connected users

  * The new flag `--tasklist` enumerates all processes on the target

  * Both flags use native windows protocols, so no command execution which could be catched by AV!

* Linting by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/580

* NFS escape to root fs by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/583

  * New technique which allows to automatically escape to the root file filesystem `/` on many linux hosts

  * E.g. the default NFS export settings on debian allows to fully compromise the system by overwriting the `/etc/passwd`

* Small bug fixes for NFS by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/584

* Add support for latest Veeam version and add description to cred output by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/570

* Improve reliability of ldap-checker module by @Mercury0 in https://github.com/Pennyw0rth/NetExec/pull/587

* Fix NFS issues when share is not listable by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/588

* Create remote-uac.py by @Dfte in https://github.com/Pennyw0rth/NetExec/pull/464

  * Enable/Disable the remote UAC on the target with the new module `remote-uac`

* Catch ldap error if host is not reachable by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/591

* Fix Poetry 2.1+ compatibility in `pyproject.toml` by @n3rada in https://github.com/Pennyw0rth/NetExec/pull/574

* Remove pywerview dependency by @mpgn in https://github.com/Pennyw0rth/NetExec/pull/579

* Use host IP for DNS resolution in asreproast function if kdcHost not specified by @Mercury0 in https://github.com/Pennyw0rth/NetExec/pull/594

* Revert #411 due to connection issues (#479) by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/601

* Add regsecretdump technique by @mpgn in https://github.com/Pennyw0rth/NetExec/pull/599

  * Introducing `regsecretsdump` which dump `--lsa` and `--sam` just with registry queries, without writing to disk

  * At the moment this appears to be much stealthier than the normal secretsdump technique https://github.com/fortra/impacket/pull/1898#issuecomment-2686073924

  * The old method can still be used by specifying it in the commands themselves if you want to switch back, e.g. `--lsa secdump`

* Several smaller bug fixes by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/597

* fix 0x_df issue with hosts file by @mpgn in https://github.com/Pennyw0rth/NetExec/pull/603

* Add information if ntlm disabled by @mpgn in https://github.com/Pennyw0rth/NetExec/pull/604

* Silently handle connection timed out during LDAP scan by @jdholtz in https://github.com/Pennyw0rth/NetExec/pull/606

* fix: check if an IP is being searched for when calling get_hosts by @Marshall-Hallenbeck in https://github.com/Pennyw0rth/NetExec/pull/590

* Modified the password used in pre2k.py for machine names longer than the max of 14 chars by @shikatano in https://github.com/Pennyw0rth/NetExec/pull/611

* Added credential and host DB for LDAP protocol by @lap1nou in https://github.com/Pennyw0rth/NetExec/pull/527

  * Full LDAP support in the `nxcdb`!

* Update smb.py to test smbv1 connection before writing in nxcdb by @Testeur-2-stylos in https://github.com/Pennyw0rth/NetExec/pull/615

* Add Error handling for loading users into registry by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/619

* Fix spec file by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/620

* Export Users to a File by @haytechy in https://github.com/Pennyw0rth/NetExec/pull/602

  * If you would like to export the queried users from the SMB/LDAP flag `--users`, just use the new flag `--users-export <out-path>`

* Improve WinSCP module by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/622

* remove pywerview from spec by @noraj in https://github.com/Pennyw0rth/NetExec/pull/626

* [SMB]: Prevent infinite loops handling an unknown error retrieving command output by @jdholtz in https://github.com/Pennyw0rth/NetExec/pull/625

* [SMB] Add the recent_files module by @Dfte in https://github.com/Pennyw0rth/NetExec/pull/450

  * The new `recent_files` module displays all files recently used by users on the system.

* Fix left handside indent from exec output by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/628

* Remove firefox module in favour of --dpapi which includes firefox by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/630

* Fix the baseDN for admin_check for custom baseDN by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/634

* SMB DPAPI Now Store Results, Issue  #632 by @termanix in https://github.com/Pennyw0rth/NetExec/pull/633

* Fix Kerberos Login While Using --use-kcache by @termanix in https://github.com/Pennyw0rth/NetExec/pull/636

* Fix ldap hash auth with signing enforced by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/637

* Fix encoding issue in get-desc-user by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/639

* Catch rpc error nca_s_op_rng_error when method is not implemented by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/638

* Update ldap.py for parse_result_attributes  by @termanix and @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/471

  * Refactor of many functions in LDAP including encoding improvements

* Add read principal to GMSA by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/640

  * `--gmsa` now also shows the user that has read permissions on the GMSA passwords

* completions: no not complete options without entering `-` first by @exploide in https://github.com/Pennyw0rth/NetExec/pull/641

* Add sid parsing directly to the ldap attribute parser by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/642

* Add CODENAME for release v1.4.0 by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/643



## New Contributors

* @Hackndo made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/458

* @haytechy made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/466

* @Chocapikk made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/470

* @y0no made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/462

* @0xQRx made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/405

* @j-mie made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/486

* @snowpeacock made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/438

* @TheToddLuci0 made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/488

* @Disgame made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/311

* @Joytide made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/499

* @lap1nou made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/502

* @MaxToffy made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/500

* @deathflamingo made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/415

* @Mortimus made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/509

* @Yeeb1 made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/368

* @jdholtz made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/524

* @rtpt-romankarwacik made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/505

* @Mercury0 made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/575

* @n3rada made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/574

* @shikatano made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/611

* @Testeur-2-stylos made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/615

* @noraj made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/626



**Full Changelog**: https://github.com/Pennyw0rth/NetExec/compare/v1.3.0...v1.4.0


===== RELEASE v1.3.0 (v1.3.0) =====

## What's Changed

* fix extract_password in the keepass module by @sepauli in https://github.com/Pennyw0rth/NetExec/pull/279

* [NXCDB] Add support for CTRL-D by @fpreynaud in https://github.com/Pennyw0rth/NetExec/pull/334

* Add output if a successful authentication is via Guest privileges by @Marshall-Hallenbeck in https://github.com/Pennyw0rth/NetExec/pull/333

  * New label for the guest account so this is quickly identified

* add testing hash file to e2e_commands.txt by @Marshall-Hallenbeck in https://github.com/Pennyw0rth/NetExec/pull/336

* Improve OS detection by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/340

* Adding some logger when users have been dumped by @Anhydrite in https://github.com/Pennyw0rth/NetExec/pull/343

* Added domain name for --users with samr by @Anhydrite in https://github.com/Pennyw0rth/NetExec/pull/345

* Add EnumAV Detection for Cortex XDR by @n00py in https://github.com/Pennyw0rth/NetExec/pull/344

* fix: little typo in help args by @aelmosalamy in https://github.com/Pennyw0rth/NetExec/pull/354

* Update pso.py by @bfnserra in https://github.com/Pennyw0rth/NetExec/pull/355

* Adding module to retrieve network interfaces info by @Sant0rryu in https://github.com/Pennyw0rth/NetExec/pull/293

* New SMB/WMI Module BitLocker by @termanix in https://github.com/Pennyw0rth/NetExec/pull/286

* Fix #332 - Add exception handling to prevent crashes against linux hosts by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/356

* Bug Fix While Using Bloodhound with --use-kcache Issue #363 by @termanix in https://github.com/Pennyw0rth/NetExec/pull/364

* Small Bug Fix on Listing SMB Shares with Kerberos Auth by @termanix in https://github.com/Pennyw0rth/NetExec/pull/357

* Fix mmcexec method thanks to @ippsec AND a lot of other small things by @mpgn in https://github.com/Pennyw0rth/NetExec/pull/361

* Remove message that could be too annoying by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/365

* Update enum_av Added Trellix EDR by @termanix in https://github.com/Pennyw0rth/NetExec/pull/371

* Fixed nla detection and error format string by @Kamuno in https://github.com/Pennyw0rth/NetExec/pull/372

* Fix ruff linting by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/375

* Add try&except block for DCERPCExceptions to fix #373 by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/376

* add new security-questions module by @Adamkadaban in https://github.com/Pennyw0rth/NetExec/pull/295

  * This queries the security questions for all local users, potentially containing passwords

* Update dploot to 2.7.4 in pyproject.toml by @zblurx in https://github.com/Pennyw0rth/NetExec/pull/384

* Update handlekatz.py pypykatz import by @3ldidi94 in https://github.com/Pennyw0rth/NetExec/pull/389

* Stop NetBiosTimeout and error producing large stack traces by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/387

* Fix check admin false positive on certain target (e.g Netapp) by @nikaiw in https://github.com/Pennyw0rth/NetExec/pull/378

* Fix admin check in mssql_priv by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/390

* Fix: module spider_plus with filtered folders by @glefait in https://github.com/Pennyw0rth/NetExec/pull/391

* Adding SCCM LDAP Reconnaissance to NetExec by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/386

  - Enumerate SCCM Site-Servers

  - Enumerate SCCM Sites

  - Enumerate SCCM Management Points and associate them with their respective SCCM Site

  - Enumerate all Users that might be related to the SCCM environment

  - Enumerate all Computers that might be related to the SCCM environment

  - Enumerate all Groups that might be related to the SCCM environment (also possible with recursive search)

* Fix spider_plus bug where len was applied to the count not an array by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/392

* Add module to lookup hostname of Hyper-V host - 'hyperv-host.py' by @joaovarelas in https://github.com/Pennyw0rth/NetExec/pull/374

* Add Unix availability to README.md by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/399

* ldap-checker.py false positive fixed by @cauan in https://github.com/Pennyw0rth/NetExec/pull/408

* ldap-checker.py Catch connection errors by @cauan in https://github.com/Pennyw0rth/NetExec/pull/409

* Updated github workflows by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/394

* Identify Pre-Created Computer Accounts by @Shad0wC0ntr0ller in https://github.com/Pennyw0rth/NetExec/pull/328

  * Identify Pre-Created Computer Accounts and save a ccache for each account if vulnerable. Based on the research of https://trustedsec.com/blog/diving-into-pre-created-computer-accounts

* Fix issues with kerberos and non NTLM domains by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/393

* Module wcc added some defender checks by @jubeaz in https://github.com/Pennyw0rth/NetExec/pull/306

* schtask_as Improvement - Options for custom task, file, and location. by @Kahvi-0 in https://github.com/Pennyw0rth/NetExec/pull/342

* Smbghost scanning module by @r4vanan in https://github.com/Pennyw0rth/NetExec/pull/407

* Make --version switch universal so help2man will work properly by @jsherwood0 in https://github.com/Pennyw0rth/NetExec/pull/417

* Encode delegate/impersonate user name string as utf8 unicode, not latin1 by @a-urth in https://github.com/Pennyw0rth/NetExec/pull/418

* Small cosmetic fix for ldap when using --no-smb by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/423

* Fix maq module if MAQ not set by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/422

* Add new SMB module to get the PowerShell history on all the users by @357384n in https://github.com/Pennyw0rth/NetExec/pull/341

* Fix file logging for display messages by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/406

* New Protocol NFS by @termanix in https://github.com/Pennyw0rth/NetExec/pull/366

  * Detect NFS Server

  * Enumerate Shares and their privileges

  * Recursive file enumeration with uid detection

  * Up- and Download Files

* Fix a bug with the databases when a new protocol is added by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/433

* Add file write check on smb by @tiyeuse in https://github.com/Pennyw0rth/NetExec/pull/404

* Fix pwned label when brute forcing with guest account enabled by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/434

* Improve test suite by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/435

* Increase plaintext&hash login speeds by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/411

* Add coerce_plus Module by @lodos2005 in https://github.com/Pennyw0rth/NetExec/pull/300

  * Combines the most popular coercion techniques into one module. Available techniques are:

  * DFSCoerce

  * PetitPotam

  * PrinterBug

  * ShadowCoerce

  * MSEven

* refactoring to fix InterfaceError of DB by @dazzgt in https://github.com/Pennyw0rth/NetExec/pull/400

* Small fixes for coerce_plus by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/442

* Updated the  --get-file method to get large files from NFS shares by @ledrypotato in https://github.com/Pennyw0rth/NetExec/pull/440

* Fix module loading for ssh, vnc and ftp by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/447

* Fix windows and encoding stuff by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/446

* Release v1.3.0 by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/448



## New Contributors

* @Anhydrite made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/343

* @n00py made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/344

* @aelmosalamy made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/354

* @bfnserra made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/355

* @Sant0rryu made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/293

* @Kamuno made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/372

* @3ldidi94 made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/389

* @glefait made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/391

* @joaovarelas made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/374

* @cauan made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/408

* @jubeaz made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/306

* @r4vanan made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/407

* @jsherwood0 made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/417

* @a-urth made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/418

* @357384n made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/341

* @tiyeuse made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/404

* @dazzgt made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/400

* @ledrypotato made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/440



**Full Changelog**: https://github.com/Pennyw0rth/NetExec/compare/v1.2.0...v1.3.0


===== RELEASE v1.2.0 (v1.2.0) =====

## What's Changed

* tests: improve output of e2e tests for errors  by @Marshall-Hallenbeck in https://github.com/Pennyw0rth/NetExec/pull/120

* Ms17 010 error handling by @Marshall-Hallenbeck in https://github.com/Pennyw0rth/NetExec/pull/121

* fix(smb errors): getErrorString only returns one item, not a tuple by @Marshall-Hallenbeck in https://github.com/Pennyw0rth/NetExec/pull/119

* Add New Ldap Flag `--active-users` by @termanix in https://github.com/Pennyw0rth/NetExec/pull/128

  * Serves the same purpose as `--users`, but filters out deactivated accounts

* Fix bug in WCC module by @fpreynaud in https://github.com/Pennyw0rth/NetExec/pull/137

* Fix array index by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/140

* [winrm] better output by @XiaoliChan in https://github.com/Pennyw0rth/NetExec/pull/114

* Fix: iis module cmd exec quotes by @0xlazY in https://github.com/Pennyw0rth/NetExec/pull/146

* Modules enumeration ldap  by @Syzik in https://github.com/Pennyw0rth/NetExec/pull/133

  * Added two modules for querying the attributes `userPassword` and `unixUserPassword`

  * These attributes are sometimes filled with cleartext passwords by 3rd party applications, also see https://swisskyrepo.github.io/InternalAllTheThings/active-directory/pwd-comments/

* Restructure how laps login works to fix login issues by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/141

* Remove domain DN from ldap query, fixes #144 by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/150

* Fixing binaries for RDP and WINRM by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/130

* Removing deprecâ€¦ by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/132

* add argcomplete bash/zsh completion by @Adamkadaban in https://github.com/Pennyw0rth/NetExec/pull/148

  * When installed with pipx, netexec now supports autocomplete when pressing tab. See the [wiki](https://www.netexec.wiki/getting-started/installation/setting-up-tab-completion) for the setup.

* Fixing module name check with windows backspace path by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/155

* Fix some issues in deps by @thiagokokada in https://github.com/Pennyw0rth/NetExec/pull/162

* Fix issue #134 with tempfile on windows by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/135

* Surpress any errors when using rdp and broken python version by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/139

* Fix usernames with empty spaces in ntds dump by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/153

* Hotfix: Allow broader version for argcomplete to fix macos installations by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/167

* [WCC] Make check names more explicit by @fpreynaud in https://github.com/Pennyw0rth/NetExec/pull/169

* nxcdb: refactor shared database/workspace setup code & allow for creation/setting of workspaces outside of nxcdb interactive console by @Marshall-Hallenbeck in https://github.com/Pennyw0rth/NetExec/pull/123

  * Add command `--get-workspace`/`-gw`

  * Add command `--create-workspace`/`-cw`

  * Add command `--set-workspace`/`-sw`

* Allow a single word as audit mode "character" by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/179

* Write without delete will now be displayed as write access by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/183

* Remove unnecessary remote ops check by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/185

* Add error handling for protocol level by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/176

* Update ntlmv1.py by @Dfte in https://github.com/Pennyw0rth/NetExec/pull/173

* Update impacket dependency to pull latest changes by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/187

* Fix audit_mode in ldap by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/186

* [Module] Enum ADCS Certificate Authority without creds. by @0xjbb in https://github.com/Pennyw0rth/NetExec/pull/160

* [winrm] say goodbye to SMB by @XiaoliChan in https://github.com/Pennyw0rth/NetExec/pull/172

  * No longer need SMB to gather NTLM info

* Update README.md by @Marshall-Hallenbeck in https://github.com/Pennyw0rth/NetExec/pull/193

* [lib] Improve ntlm_parser.py by @XiaoliChan in https://github.com/Pennyw0rth/NetExec/pull/191

* [MSSQL] Improvement by @XiaoliChan in https://github.com/Pennyw0rth/NetExec/pull/136

  * No more SMB needed (also remove --no-smb)

  * Fix no-output option in command execution

  * Improve the logic in mssqlexec.py

  * Add --mssql-timeout

  * Fix --use-kcache

* Update connection.py to force login by @mpgn in https://github.com/Pennyw0rth/NetExec/pull/190

* Remove pyreadline as it causes errors in nxcdb by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/171

* Update neo4j python driver by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/202

* Fix string escaping issues for Kali package, fix some logging, and allow for lsa and sam WinRM dumping by @Marshall-Hallenbeck in https://github.com/Pennyw0rth/NetExec/pull/204

* Extract obsolete operating systems from LDAP by @Shad0wC0ntr0ller in https://github.com/Pennyw0rth/NetExec/pull/41

* fix(wcc.py): properly escape for #200 by @Marshall-Hallenbeck in https://github.com/Pennyw0rth/NetExec/pull/206

* Create get_fgpp.py by @sebrink in https://github.com/Pennyw0rth/NetExec/pull/65

* [Module] printerbug by @lodos2005 in https://github.com/Pennyw0rth/NetExec/pull/163

* Revert #190 to enable null-auth without explicit specification by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/208

* Adding the fileNamePrefix which was introduced in bloodhound so filesâ€¦ by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/212

* Stop Netexec from adding null auth user to bloodhound by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/213

* Fix SMB users lookup and return last password set date by @Marshall-Hallenbeck in https://github.com/Pennyw0rth/NetExec/pull/214

* Fix: module names 8-10 chars being cut off by @Marshall-Hallenbeck in https://github.com/Pennyw0rth/NetExec/pull/220

* Update LDAP users lookup to match SMB by @Marshall-Hallenbeck in https://github.com/Pennyw0rth/NetExec/pull/215

* BloodHound & hash_spider fixes by @Marshall-Hallenbeck in https://github.com/Pennyw0rth/NetExec/pull/226

* [ldap-checker] Module fix by @zblurx in https://github.com/Pennyw0rth/NetExec/pull/216

* Fixing antivirus enumeration by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/218

  * add new AVs to enumerate

* Update LDAP active users lookup to match SMB by @termanix in https://github.com/Pennyw0rth/NetExec/pull/224

* Several LDAP improvements by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/152

* Module 'get-desc-users' Update - Marshall's #201 Issue Bug Fix by @termanix in https://github.com/Pennyw0rth/NetExec/pull/228

* Make loggedon-users unique to reduce spam and fix alignment by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/222

* Several ldap bug fixes by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/227

* Logging fixes (double logging & function caller obfuscation) by @Marshall-Hallenbeck in https://github.com/Pennyw0rth/NetExec/pull/229

* Logging in DEBUG mode: change normal output from DEBUG to INFO by @Marshall-Hallenbeck in https://github.com/Pennyw0rth/NetExec/pull/231

* rename MAQ.py to maq.py by @Marshall-Hallenbeck in https://github.com/Pennyw0rth/NetExec/pull/238

* Fix testing and linting by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/230

* Small QOL changes by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/240

* Winlogon Autologon module by @swisskyrepo in https://github.com/Pennyw0rth/NetExec/pull/236

* fix --users for LDAP proto by @zblurx in https://github.com/Pennyw0rth/NetExec/pull/235

* Neff qol the second by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/242

* Remove oscrypto and swap back to fortra/impacket by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/234

* --kerberoast Improvement by @Kahvi-0 in https://github.com/Pennyw0rth/NetExec/pull/126

* Add git commit to version command by @Marshall-Hallenbeck in https://github.com/Pennyw0rth/NetExec/pull/239

* Fix tmp PATH on windows for msol and scuffy by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/244

* Add missing packages to spec file, fixing ldap and pso module by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/247

* Add verbosity to dpapi, so the user knows if no secrets were found by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/246

* bugfixes: add-computer & nanodump modules by @Marshall-Hallenbeck in https://github.com/Pennyw0rth/NetExec/pull/237

* fixed one grammar error repeated in several files by @scottymiller9 in https://github.com/Pennyw0rth/NetExec/pull/251

* Fix ssh authentication with encrypted ssh file by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/254

* Update Slinky module by @Marshall-Hallenbeck in https://github.com/Pennyw0rth/NetExec/pull/255

* Fix "Too many open files" by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/257

* Fix computers enum by @zblurx in https://github.com/Pennyw0rth/NetExec/pull/259

* Update lsassy.py by @mpgn in https://github.com/Pennyw0rth/NetExec/pull/262

* Ldap active users bug fix by @termanix in https://github.com/Pennyw0rth/NetExec/pull/248

* ldap-checker: fix for Python 3.12 compatibility by @exploide in https://github.com/Pennyw0rth/NetExec/pull/270

* Fix ssh auth message by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/272

* fix mssql_priv by @sepauli in https://github.com/Pennyw0rth/NetExec/pull/277

* Fixing #263 by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/271

* Fix bug where modules would be the same object across protocols by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/250

* Updating dependencies by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/269

* Add feature request template by @Marshall-Hallenbeck in https://github.com/Pennyw0rth/NetExec/pull/283

* Fix #284 by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/285

* Reduce third party debug logging by @Marshall-Hallenbeck in https://github.com/Pennyw0rth/NetExec/pull/290

* Feat: Allow for running specific e2e tests by line number by @Marshall-Hallenbeck in https://github.com/Pennyw0rth/NetExec/pull/297

  * helpful for devs who just want to tests _some_ e2e test commands

* #281 - Multi-file put/get for smb by @wumb0 in https://github.com/Pennyw0rth/NetExec/pull/282

  * Can now multi put/get files in one command

* Change jitter option to throttle authentications by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/291

  * Changed the old jitter function to randomly insert sleeps before authenticating

* Create Pull Request Template by @Marshall-Hallenbeck in https://github.com/Pennyw0rth/NetExec/pull/299

* fix issue #252 by @mpgn in https://github.com/Pennyw0rth/NetExec/pull/304

* Update e2e_commands.txt by @termanix in https://github.com/Pennyw0rth/NetExec/pull/298

* Revert a9bd576392af8ec5ee284446bc99ffd24b9b696a by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/305

* Update test.yml to include pipx install by @mpgn in https://github.com/Pennyw0rth/NetExec/pull/265

* Add PuTTY module and fix WinSCP by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/249

  * A new module to query for saved private keys in PuTTY

  * Add detection for saved proxy credentials in PuTTY

  * Bug fixes and improvements for WinSCP cred dumping

* Fix: hash_spider Lsassy Parser syntax by @Marshall-Hallenbeck in https://github.com/Pennyw0rth/NetExec/pull/308

  * `hash_spider` should be working again

* fix: move PR template to the correct location by @Marshall-Hallenbeck in https://github.com/Pennyw0rth/NetExec/pull/310

* Fix for tests referencing files, password/username variable, and a couple KERBEROS space issues by @Marshall-Hallenbeck in https://github.com/Pennyw0rth/NetExec/pull/314

* Handle paramiko error when bruteforcing by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/313

  * Fixes where paramiko fails to read the ssh banner when brute forcing credentials

* fix(tests): add spaces & fix one file reference by @Marshall-Hallenbeck in https://github.com/Pennyw0rth/NetExec/pull/318

* [DNS] Add DNS args by @XiaoliChan in https://github.com/Pennyw0rth/NetExec/pull/196

  * Allow using force IPv6 with -6

  * Allow specify DNS server with --dns-server

  * Allow using tcp DNS query with --dns-tcp

  * Set DNS query timeout with --dns-timeout

  * Auto resolve DC IP and set it as kdcHost, which means you can play with kerberos stuff without set /etc/hosts files

* Refactor/fix/update PowerShell and related features by @Marshall-Hallenbeck in https://github.com/Pennyw0rth/NetExec/pull/296

  * Tons of Powershell fixes for both SMB and MSSQL

  * `met_inject` module should work again!

  * 32-bit Powershell usage also helps running against defender

  * turn off obfuscation by default for powershell, since defender picks it up easily

  * turn off amsi-bypass by default, since it was an incredibly old signatured bypass (users can still pass in their own)

  * some test enhancements for us developers

* Fix: WCC Module - do not create log file on every file load by @Marshall-Hallenbeck in https://github.com/Pennyw0rth/NetExec/pull/307

* Improving execution speed and misc command execution improvements by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/317

* Add ldap query option by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/309

  * Can now perform raw LDAP queries with NetExec!

* Refactor argparse options by @Marshall-Hallenbeck in https://github.com/Pennyw0rth/NetExec/pull/321

  * Now you can append `--debug` and other global options to the end of commands 

* Added --dns-tcp,--dns-timeout and --dns-server parameters to the ldap protocol when using --bloodhound by @Fabrizzio53 in https://github.com/Pennyw0rth/NetExec/pull/325

* Passwords dump update by @zblurx in https://github.com/Pennyw0rth/NetExec/pull/225

  * Can now dump Google Refresh Token, SCCM, VNC, mRemoteNG, and mobaxterm creds!

* Improve testing suite by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/315

* Windows Fixes for v1.2 by @Marshall-Hallenbeck in https://github.com/Pennyw0rth/NetExec/pull/326

* ItsAlwaysDNS by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/327



## New Contributors

* @termanix made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/128

* @fpreynaud made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/137

* @0xlazY made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/146

* @Syzik made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/133

* @Adamkadaban made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/148

* @thiagokokada made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/162

* @0xjbb made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/160

* @Shad0wC0ntr0ller made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/41

* @sebrink made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/65

* @lodos2005 made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/163

* @swisskyrepo made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/236

* @Kahvi-0 made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/126

* @scottymiller9 made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/251

* @exploide made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/270

* @sepauli made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/277

* @wumb0 made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/282

* @Fabrizzio53 made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/325



**Full Changelog**: https://github.com/Pennyw0rth/NetExec/compare/v1.1.0...v1.2.0


===== RELEASE v1.1.0 (v1.1.0) =====

## What's Changed

* Fix #48 tries to falsly add creds to bloodhound using --laps by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/49

* Bump urllib3 from 2.0.4 to 2.0.6 by @dependabot in https://github.com/Pennyw0rth/NetExec/pull/53

* Update enum_av.py by @bongobongoland in https://github.com/Pennyw0rth/NetExec/pull/58

* Create schtask.py by @Dfte in https://github.com/Pennyw0rth/NetExec/pull/54

  - Add the schtask module that can be used to impersonate loggedon users and run commands on their behalf.

* Add ascii art to cli by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/57

  - courtesy of @bongobongoland!

* [nanodump] fix error with temporary path by @XiaoliChan in https://github.com/Pennyw0rth/NetExec/pull/67

* Update dependencies (including impacket fork) for v1.1.0 by @Marshall-Hallenbeck in https://github.com/Pennyw0rth/NetExec/pull/30

* Bump urllib3 from 2.0.6 to 2.0.7 by @dependabot in https://github.com/Pennyw0rth/NetExec/pull/77

* mpgn is back ðŸŽ‰  by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/80

* Update README.md by @mishrasamiksha in https://github.com/Pennyw0rth/NetExec/pull/83

* Enhancing the FTP protocol by @RomanRII in https://github.com/Pennyw0rth/NetExec/pull/40

  - Modified the --ls flag to allow for listing the current directory and sub-directories. Default now lists .. If an argument is provided, it will list the provided sub-directory

  - Added the --get flag to download a file on the server. If the file exists and is successfully downloaded, it will be written to the users cwd with the remote file's filename.

  - Added the --put flag to upload files onto the server.

  - Modified nxc/protocols/ftp/proto_args.py to reflect the added features

  - Modified the --ls flag to allow for a default directory listing (.) or use a provided directory

  - Added the --get and --put flags

  - Modified [nxc/protocols/ftp.py#L83](https://github.com/Pennyw0rth/NetExec/blob/main/nxc/protocols/ftp.py#L83) to comply with [RFC 1635](https://www.rfc-editor.org/rfc/rfc1635.html)

* Add module sorting by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/74

* [ssh] improvement by @XiaoliChan in https://github.com/Pennyw0rth/NetExec/pull/25

  - [ssh.py]: less create ssh connect, keep doing set credential via paramiko transport

  - [ssh.py]: rewrite enum_host_info function

  - [ssh.py]: fix hanging, old one will never exit

  - [ssh.py]: fix private key with passphrase

  - [ssh.py]: add sudo check for linux user

  - [ssh.py]: windows privileges check

  - [ssh.py]: improve command execute and format command execute result

  - [ssh.py]: paramiko always discovery private keys in ~/.ssh/, that will make paramiko exception, disable it.

* fix(dependencies): add bloodhound to netexec.spec, fixes #79 by @Marshall-Hallenbeck in https://github.com/Pennyw0rth/NetExec/pull/87

* Downgrade termcolor to prevent atty check which disables colors by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/86

* Cleanup & Lint Code by @Marshall-Hallenbeck in https://github.com/Pennyw0rth/NetExec/pull/35

  - Add Ruff configuration (version pinned due to discrepancies on GitHub runner versioning)

  - Create linter workflow to run Ruff on push & pull request

  - Remove encoding specification from files (unnecessary in Py3)

  - Update strings to be more descriptive, remove typos, and be properly capitalized

  - Change additionally remaining .format() and % old string interpolation to f-string usage (partially FLY)

  - Fix blank Except statements and unnecessary parenthesis in Excepts (partially RSE)

  - Update exception handling for some circumstances where another except was thrown, causing unnecessary output

  - Remove unused imports

  - Fix poorly and non-pythonic variable/function/class names

  - Fix additional single/double quote usage (Q)

  - Add docstrings to some functions and fix docstrings for others

  - Fix usages of mutable function defaults (see B006, mutable-argument-default in Ruff)

  - Properly inform user if file they specified doesn't exist for several modules

  - Fix usages of comprehension and list/dict initialization via Ruff (C4)

  - Remove unnecessary str-concat (ISC)

  - Fix unnecessary pass statements and unnecessary creation of additional variables before return (PIE)

  - Fix some pytest style (PT)

  - Fix return statements returning None (unnecessary) (RET)

  - Add --poetry option for e2e tests, so all commands are prepended with poetry run

  - Fix ftp class name (got changed to "Ftp" by accident)

  - Simplify lots of code (SIM)

  - Fix tests using a password file to properly reference said file (was missing data/)

  - Remove commented out code (ERA)

  - Import and call sys.exit() instead of just exit() (PL)

  - Fix some try except outside loops (PERF203); additional ones are ignored for now

  - Implement list and dict comprehension where possible and preferred (PERF401)

  - Fix some spaces before inline comments (E261)

  - Modernize some code via Refurb (FURB)

  - Fix bug in add-computer module where improper access was being requested, causing an exception

  - Fix bug in add-computer module where module was not exiting if the computer already exists

  - Add in e2e tests for several missing modules 

* Add python version and OS info to debug output by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/89

* Update README.md - one grammatical error. by @ayushrakesh in https://github.com/Pennyw0rth/NetExec/pull/94

* Fix import error on windows by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/98

* fix typos in python files of directory `nxc/modules` by @shresthasurav in https://github.com/Pennyw0rth/NetExec/pull/97

* Implement s4u abuse by @zblurx in https://github.com/Pennyw0rth/NetExec/pull/50

  - This option will do a full S4U abuse (S4U2Self + S4U2Proxy) in an automated way, allowing to use all postex functionalities of NXC ðŸ”¥

* [connection.py] Improvement by @XiaoliChan in https://github.com/Pennyw0rth/NetExec/pull/63

  - connection.py: Add missing self.port in connection.py, in order to use connection.port when writing module.

  - connection.py and protocol: Redirect self.args.port to self.port

  - connection.py: improve ipv6 support, now add is_ipv6 is_link_local_ipv6 variables

  - connection.py: rewrite gethost_addinfo function, don't need try to detect ipv6 anymore, just use AF_UNSPEC instead AF_INET6, AF_INET

  - connection.py: IPv4 preferred when target is dual stack

* Improve bloodhound connector with Netbios domain name by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/88

* Set computer accounts as owned in bloodhound if local admin privs by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/90

* [winrm] Improvement by @XiaoliChan in https://github.com/Pennyw0rth/NetExec/pull/72

* Fix: update MS17-010 for Python3 properly; add debug logging by @Marshall-Hallenbeck in https://github.com/Pennyw0rth/NetExec/pull/108

* [winrm] disable logger & add miss port args by @XiaoliChan in https://github.com/Pennyw0rth/NetExec/pull/107

* Fix Kerberoasting for #104 by @Marshall-Hallenbeck in https://github.com/Pennyw0rth/NetExec/pull/111

* Improve module texts by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/109

* [ssh] fix #112 by @XiaoliChan in https://github.com/Pennyw0rth/NetExec/pull/113

* disable use of ssh_agent  by @nikaiw in https://github.com/Pennyw0rth/NetExec/pull/106

* Adding error handling for unexpected powershell output, see issue #93 by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/115

* Netexec v1.1.0 by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/116



## New Contributors

* @bongobongoland made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/58

* @Dfte made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/54

* @RomanRII made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/40

* @nikaiw made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/106



**Full Changelog**: https://github.com/Pennyw0rth/NetExec/compare/v1.0.0...v1.1.0


===== RELEASE v1.0.0 (v1.0.0) =====

## v1.0.0 Release



This release is mainly aimed at stability, to provide a solid baseline from which to work. Some minor and major bugs have been fixed, see below for details. 

Version 1.1.0 is already in the works, with great new modules in the works as well as new features such as zblurx's delegation technique coming soon to NetExec.

Stay tuned! 



Note: as always, the best way to install NetExec is by cloning the repo and running `pipx install .`, but we have provided binaries for Windows (!!!) and Ubuntu below!



## What's Changed

* Update README by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/1

* Fix for allowing to test multiple users with one password by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/2

* Update README.md for NetExec rename by @Marshall-Hallenbeck in https://github.com/Pennyw0rth/NetExec/pull/11

* Add CODEOWNERS by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/13

* Fix CLI by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/16

* Make some text more precise by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/7

* [winrm] less ugly if condition by @XiaoliChan in https://github.com/Pennyw0rth/NetExec/pull/9

* [wmi] bug fix in 'check_admin' function by @XiaoliChan in https://github.com/Pennyw0rth/NetExec/pull/4

* Update LICENSE for NetExec by @Marshall-Hallenbeck in https://github.com/Pennyw0rth/NetExec/pull/12

* NetExec Rename by @Marshall-Hallenbeck in https://github.com/Pennyw0rth/NetExec/pull/19

* fix webdav module exception handler by @professor-hillman in https://github.com/Pennyw0rth/NetExec/pull/29

* Windows Build for NetExec by @Marshall-Hallenbeck in https://github.com/Pennyw0rth/NetExec/pull/26

* Update Github Build Actions for Releases by @Marshall-Hallenbeck in https://github.com/Pennyw0rth/NetExec/pull/27

* Fix encoding errors by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/32

* Fix #42, --dc-list crashes on ldap with logging enabled by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/43

* Add README text by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/24

* Create CODE_OF_CONDUCT.md by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/44

* Create CONTRIBUTING.md by @NeffIsBack in https://github.com/Pennyw0rth/NetExec/pull/45

* Finalize Native Builds by @Marshall-Hallenbeck in https://github.com/Pennyw0rth/NetExec/pull/52



## New Contributors

* @professor-hillman made their first contribution in https://github.com/Pennyw0rth/NetExec/pull/29



**Full Changelog**: https://github.com/Pennyw0rth/NetExec/commits/v1.0.0