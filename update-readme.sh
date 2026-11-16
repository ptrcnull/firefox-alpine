#!/bin/sh

set -euo pipefail

tags="$(curl -s -A "git/2.48.0" https://github.com/ptrcnull/firefox-alpine.git/info/refs\?service=git-upload-pack | grep -a refs/tags/aports)"

get_latest() {
    echo "$tags" |\
        grep -v base |\
        grep "$1" |\
        tail -n1 |\
        cut -d/ -f3- |\
        sed -E 's/esr-([0-9]{3}.[0-9])/esr-\1.0/' |\
        cut -d- -f3- |\
        sed -E 's/([0-9]{3})([ab])([0-9])/\1.0\2\3/;s/^([0-9]{3})$/\1.0/'
}

esr="$(get_latest esr)"
stable="$(get_latest stable)"
thunderbird="$(get_latest thunderbird)"
aurora="$(get_latest aurora)"
nightly="$(get_latest nightly)"

sed -E -i "19 s/[0-9ab.]{3,}/$esr/" README.md
sed -E -i "20 s/[0-9ab.]{3,}/$stable/" README.md
sed -E -i "21 s/[0-9ab.]{3,}/$thunderbird/" README.md
sed -E -i "22 s/[0-9ab.]{3,}/$aurora/" README.md
sed -E -i "23 s/[0-9ab.]{3,}/$nightly/" README.md
