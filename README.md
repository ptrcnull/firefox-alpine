Hi! This repo is a fork that allows for easier maintenance of patches for Alpine Linux.

<table>
	<tr>
		<td width="18%"><img width="100%" src="/assets/svg/firefox-logo-esr.svg"></td>
		<td width="18%"><img width="100%" src="/assets/svg/firefox-logo.svg"></td>
		<td width="23%" align="center"><img width="75%" src="/assets/svg/thunderbird-logo.svg"></td>
		<td width="18%"><img width="100%" src="/assets/svg/firefox-logo-aurora.svg"></td>
		<td width="18%"><img width="100%" src="/assets/svg/firefox-logo-nightly.svg"></td>
	</tr>
	<tr>
		<td align="center"><h3>ESR</h3></td>
		<td align="center"><h3>Release</h3></td>
		<td align="center"><h3>Thunderbird</h3></td>
		<td align="center"><h3>Aurora</h3></td>
		<td align="center"><h3>Nightly</h3></td>
	</tr>
	<tr>
        <td align="center"><b>153.7.0</b></td>
       	<td align="center"><b>160.0.1</b></td>
       	<td align="center"><b>160.0</b></td>
       	<td align="center"><b>161.0b5</b></td>
       	<td align="center"><b>163.0a1</b></td>
   	</tr>
    <tr>
		<td><a href="https://github.com/ptrcnull/firefox-alpine/tree/aports-esr"><code>aports-esr</code></a></td>
		<td><a href="https://github.com/ptrcnull/firefox-alpine/tree/aports-stable"><code>aports-stable</code></a></td>
		<td><a href="https://github.com/ptrcnull/firefox-alpine/tree/aports-thunderbird"><code>aports-thunderbird</code></a></td>
		<td><a href="https://github.com/ptrcnull/firefox-alpine/tree/aports-aurora"><code>aports-aurora</code></a></td>
		<td><a href="https://github.com/ptrcnull/firefox-alpine/tree/aports-nightly"><code>aports-nightly</code></a></td>
	</tr>
    <tr>
		<td><a href="https://pkgs.alpinelinux.org/package/edge/community/x86_64/firefox-esr">pkgs.a.o</a></td>
		<td><a href="https://pkgs.alpinelinux.org/package/edge/community/x86_64/firefox">pkgs.a.o</a></td>
		<td><a href="https://pkgs.alpinelinux.org/package/edge/community/x86_64/thunderbird">pkgs.a.o</a></td>
		<td><a href="https://pkgs.alpinelinux.org/package/edge/testing/x86_64/firefox-developer-edition">pkgs.a.o</a></td>
		<td><a href="https://gitlab.alpinelinux.org/ptrcnull/aports/-/tree/ffnightly/testing/firefox-nightly">gitlab.a.o</a></td>
	</tr>
   	<tr>
        <td><a href="https://github.com/ptrcnull/firefox-alpine/releases?q=esr">Releases</a></td>
        <td><a href="https://github.com/ptrcnull/firefox-alpine/releases?q=firefox">Releases</a></td>
        <td><a href="https://github.com/ptrcnull/firefox-alpine/releases?q=thunderbird">Releases</a></td>
        <td><a href="https://github.com/ptrcnull/firefox-alpine/releases?q=aurora">Releases</a></td>
        <td><a href="https://github.com/ptrcnull/firefox-alpine/releases?q=nightly">Releases</a></td>
    </tr>
</table>

Tags are created whenever the package builds successfully for all architectures supported in Alpine.

Thunderbird needs the `comm/` submodule from [ptrcnull/thunderbird-desktop](https://github.com/ptrcnull/thunderbird-desktop).

Nightlies are released as often as I can be bothered, APK files will be attached to releases.

### Local setup

Put this into `.git/config` before fetching tags to avoid a mess of irrelevant tags:

```
[remote "origin"]
	url = https://github.com/mozilla-firefox/firefox/
	fetch = +refs/heads/*:refs/remotes/origin/*
	fetch = ^refs/tags/B2G*
	fetch = ^refs/tags/FENNEC*
	fetch = ^refs/tags/FIREFOX-ANDROID*
	fetch = ^refs/tags/GECKO*
	fetch = ^refs/tags/MOZILLA*
	fetch = ^refs/tags/PRE*
	fetch = ^refs/tags/RELEASE_BASE*
	fetch = ^refs/tags/SEAMONKEY*
	fetch = ^refs/tags/THUNDERBIRD*
	fetch = ^refs/tags/UPDATE*
	fetch = ^refs/tags/bsmedberg*
	fetch = ^refs/tags/chromium*
```

*Original README follows:*

<hr>

![Firefox Browser](./docs/readme/readme-banner.svg)

[Firefox](https://firefox.com/) is a fast, reliable and private web browser from the non-profit [Mozilla organization](https://mozilla.org/).

### Contributing

To learn how to contribute to Firefox read the [Firefox Contributors' Quick Reference document](https://firefox-source-docs.mozilla.org/contributing/contribution_quickref.html).

We use [bugzilla.mozilla.org](https://bugzilla.mozilla.org/) as our issue tracker, please file bugs there.

### Resources

* [Firefox Source Docs](https://firefox-source-docs.mozilla.org/) is our primary documentation repository
* Nightly development builds can be downloaded from [Firefox Nightly page](https://www.mozilla.org/firefox/channel/desktop/#nightly)

If you have a question about developing Firefox, and can't find the solution
on [Firefox Source Docs](https://firefox-source-docs.mozilla.org/), you can try asking your question on Matrix at
chat.mozilla.org in the [Introduction channel](https://chat.mozilla.org/#/room/#introduction:mozilla.org).
