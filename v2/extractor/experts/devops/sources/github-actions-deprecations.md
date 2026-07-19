# GitHub Actions — deprecated workflow commands and runner changes

The `set-output` workflow command (`echo "::set-output name=x::value"`) is deprecated; write to the `GITHUB_OUTPUT` environment file instead (`echo "x=value" >> "$GITHUB_OUTPUT"`).
The `save-state` workflow command (`echo "::save-state name=x::value"`) is deprecated; write to the `GITHUB_STATE` environment file instead.
The `set-env` workflow command (`echo "::set-env name=x::value"`) is deprecated; write to the `GITHUB_ENV` environment file instead.
The `add-path` workflow command (`echo "::add-path::/path"`) is deprecated; write to the `GITHUB_PATH` environment file instead.
