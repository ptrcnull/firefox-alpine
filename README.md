Hi! This repo is a fork that allows for easier maintenance of patches for Alpine Linux.

| Package | Branch name | Releases |
| ------- | ----------- | -------- |
| `community/firefox`                 | [`aports-stable`][1]      | [Releases][1t] |
| `community/firefox-esr`             | [`aports-esr`][2]         | [Releases][2t] |
| `community/thunderbird`             | [`aports-thunderbird`][3] | [Releases][3t] |
| `testing/firefox-developer-edition` | [`aports-aurora`][4]      | [Releases][4t] |
| `testing/firefox-nightly`           | [`aports-nightly`][5]     | [Releases][5t] |

Tags are created whenever the package builds successfully for all architectures supported in Alpine.

Thunderbird needs the `comm/` submodule from [ptrcnull/thunderbird-desktop](https://github.com/ptrcnull/thunderbird-desktop).

Nightlies are released as often as I can be bothered, APK files will be attached to releases.

[1]: https://github.com/ptrcnull/firefox-alpine/tree/aports-stable
[2]: https://github.com/ptrcnull/firefox-alpine/tree/aports-esr
[3]: https://github.com/ptrcnull/firefox-alpine/tree/aports-thunderbird
[4]: https://github.com/ptrcnull/firefox-alpine/tree/aports-aurora
[5]: https://github.com/ptrcnull/firefox-alpine/tree/aports-nightly

<!-- GitHub does not allow searching tags 😔 -->

[1t]: https://github.com/ptrcnull/firefox-alpine/releases?q=firefox
[2t]: https://github.com/ptrcnull/firefox-alpine/releases?q=esr
[3t]: https://github.com/ptrcnull/firefox-alpine/releases?q=thunderbird
[4t]: https://github.com/ptrcnull/firefox-alpine/releases?q=aurora
[5t]: https://github.com/ptrcnull/firefox-alpine/releases?q=nightly

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
