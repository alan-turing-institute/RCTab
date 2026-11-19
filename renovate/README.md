# Shared Renovate presets

Default [Renovate](https://docs.renovatebot.com/) configuration for the RCTab repositories.
Changes merged here apply to every repository that extends these presets on its next Renovate run, without a PR in that repository.

## Presets

- `default.json`: the base config for every RCTab repository (weekly schedule, automerge rules, grouping).
- `library.json`: extra rules for libraries without a lock file, such as rctab-models and fastapimsal.
  Use it alongside `default.json`.

## Usage

For an application, add a `renovate.json` like this:

```json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": ["github>alan-turing-institute/rctab//renovate/default"]
}
```

For a library:

```json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": [
    "github>alan-turing-institute/rctab//renovate/default",
    "github>alan-turing-institute/rctab//renovate/library"
  ]
}
```

Anything specific to one repository goes in that repository's `renovate.json` after `extends`.
Its `packageRules` are applied after the presets' rules, so they take precedence.

## Validating changes

```shell
npx --yes --package renovate -- renovate-config-validator --strict renovate/default.json renovate/library.json
```

This also runs in CI on pull requests that change these files.
