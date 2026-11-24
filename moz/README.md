# moz

Small helper for managing Mozilla packages in Alpine

## Setup

```console
$ uv tool install .
```

## Usage

### `moz`

Check all versions of Mozilla packages in aports.

### `moz patch`

Generate patches from your current branch in `gecko-dev`,
and apply them automatically to the correct aports package directory.

### `moz readme`

Update versions in `firefox-alpine` README based on latest tags for each product.
