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

## Poetry versions

Three Poetry versions matter, and only one of them is updated by Renovate:

- The Poetry that CI and Docker images install, pinned as `pip install poetry==X`, actions-poetry's `poetry-version: X` or the installer's `POETRY_VERSION=X`.
  `default.json` has a regex manager that bumps these in the CI tooling PR.
- The Poetry that Renovate relocks with, which is the exact version in the `poetry.lock` header.
  Renovate never changes it; it moves only when someone relocks with a different Poetry.
  Renovate's `minimumReleaseAge` is passed to Poetry, and older Poetry versions ignore it, so an old header silently turns that protection off.
- The minimum in each project's `requires-poetry`, which stops an older Poetry rewriting the lock file.
  Nothing updates it automatically: bump it by hand when we need a newer Poetry feature.

## Validating changes

```shell
npx --yes --package renovate -- renovate-config-validator --strict renovate/default.json renovate/library.json
```

This also runs in CI on pull requests that change these files.
