# Jit - IDE pre-commit hooks


## Jit IDE Extension (VSCode) pre-commit hook
A pre-commit hook to use along with the IDE Extension.

[Getting Started with the pre-commit hook for Jit VSCode IDE Extension users](https://docs.jit.io/docs/jit-ide-extension-for-visual-studio#pre-commit-hook)

### Configuration
You can configure the pre-commit hook by modifying the parameters in the IDE Extension settings.


## Standalone IDE Pre-commit hooks

<details>
    <summary>Click to expand Jit Docker Login Script</summary>
    <br/>


**Copy the following script to a file named `jit-docker-login.sh` and run it in your terminal. This script will log you in to the Jit Docker registry and pull the relevant docker images.**

**Pre-requisites:**
- **jq - https://jqlang.github.io/jq/download/**
```bash
brew install jq
```

-  **Docker up and running**

- **Jit Platform credentials**
    Go to https://platform.jit.io and -> under Settings > Users and Permissions, go to API Tokens, and create a token with an appropriate name and member role. Make sure to copy the values.
    - **Client ID**
    - **Client Secret**

**Script:**
```bash
    #!/bin/bash

    # Endpoint and credentials
    LOGIN_ENDPOINT="https://api.jit.io/authentication/login"
    REGISTRY_ENDPOINT="https://api.jit.io/ide/registry/authenticate"
    # Credentials from Jit Platform
    CLIENT_ID="<YOUR_CLIENT_ID>"
    SECRET="<YOUR_CLIENT_SECRET>"

    # Authenticate and retrieve the access token
    response=$(curl --silent --location "$LOGIN_ENDPOINT" \
                    --header 'Content-Type: application/json' \
                    --data "{
                            \"clientId\": \"$CLIENT_ID\",
                            \"secret\": \"$SECRET\"
                            }")

    # Parse the access token using jq
    accessToken=$(echo "$response" | jq -r '.accessToken')

    # Use the access token to make a POST request to /registry/authenticate
    registry_response=$(curl --silent --location --request POST "$REGISTRY_ENDPOINT" \
                            --header "Authorization: Bearer $accessToken")

    # Extract necessary information for Docker login using jq
    username=$(echo "$registry_response" | jq -r '.username')
    password=$(echo "$registry_response" | jq -r '.password')
    registry_url=$(echo "$registry_response" | jq -r '.registry_url')

    # Perform Docker login
    echo "$password" | docker login --username "$username" --password-stdin "$registry_url"

    # Check if Docker login was successful
    if [ $? -eq 0 ]; then
        echo "Successfully logged in to the Docker registry."
    else
        echo "Docker login failed."
        exit 1
    fi

    # Pull the jit-gitleaks-control image
    docker_image="$registry_url:jit-gitleaks-control"
    docker pull "$docker_image"

    # Check if Docker pull was successful
    if [ $? -eq 0 ]; then
        echo "Successfully pulled the image: $docker_image"
    else
        echo "Failed to pull the image: $docker_image"
    fi
```
</details>

### Secrets Detection
A pre-commit hook to detect secrets in your code. This hook will scan the files you specify for secrets and block the commit if any are found.

### Getting Started
1. **Install `pre-commit`:**
   ```bash
   pip install pre-commit
   ```

2. **Create a `.pre-commit-config.yaml` in your repo:**
   ```yaml
   repos:
    - repo: https://github.com/jitsecurity/ide-pre-commit-hooks
      rev: 0.1.0
      hooks:
        - id: gitleaks
   ```

3. **Install the hook:**
   ```bash
   pre-commit install
   ```

4. **Commit changes:**
   When you commit, the `pre-commit` hook will automatically run.


## Usage
Once the pre-commit hook is installed and configured, it will automatically run whenever you try to commit changes to your repository. If there are findings in the specified file, the commit will be blocked and you will need to address the findings before committing again.
