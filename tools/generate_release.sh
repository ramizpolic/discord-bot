#!/bin/bash

############################################################################################
### Build artifacts
make

############################################################################################
### Release
RELEASE_VERSION="1.2.2"
RELEASE_FILE="releases/version-$RELEASE_VERSION.md"

### Secrets
GITHUB_TOKEN=${GITHUB_TOKEN:-}

### Release data
LATEST_TAG=$(git describe --tags --abbrev=0 $RELEASE_VERSION^)
RELEASE_DATA=$(git log $LATEST_TAG..HEAD --no-merges \
            --pretty=format:'* **[`%h`](https://github.com/fhivemind/discord-bot/commit/%H)**  %s')
COMMITTERS=$(git log --format="* [%an](https://github.com/%an)" $LATEST_TAG..HEAD | sort | uniq)
DATE=$(date '+%Y-%m-%d')

### Format release
cat <<EOF > $RELEASE_FILE
# discord-bot v$RELEASE_VERSION ($DATE)

Mass user spam bot for Discord written in Python. For more details, refer to [README.md](README.md).
- [🌐 What's new?](#-whats-new)
- [💭 Usage](#-usage)
- [📖 Requirements](README.md#-requirements)
- [🔍 Documentation](README.md#-documentation)
- [💬 Message format](README.md#-message-format)

---

### :checkered_flag: What's new?
$RELEASE_DATA

### :busts_in_silhouette: Committers:
$COMMITTERS

---

## 💭 Usage
Once you have downloaded the package binaries, to get started, run following:
\`\`\`bash
## Rename
>  mv discord-bot* discord-bot

## Authenticate
>  discord-bot login

## Send messages
>  echo "Hello __USERNAME__, I'm a bot." > FORMAT.md
>  discord-bot notify
\`\`\`

:warning: Please note that using the tool for outside of its indented purpose may lead to your account being banned by Discord, 
as stated in [Discord on Automated user accounts](https://support.discord.com/hc/en-us/articles/115002192352-Automated-user-accounts-self-bots-).
EOF