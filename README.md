<h1>discord-bot</h1>

Mass user spam bot for Discord written in Python. Refer below for installation and example usages. 
It **strongly advised** to read the whole document before running any commands.     

:warning: Please note that using the tool for outside of its indented purpose may lead to your account being banned by Discord, as stated in [Discord on Automated user accounts](https://support.discord.com/hc/en-us/articles/115002192352-Automated-user-accounts-self-bots-).


**Contents**
- [📖 Requirements](#-requirements)
- [💭 Usage](#-usage)
  - [Source](#source)
  - [Binaries](#binaries)
  - [Building procedures](#building-procedures)
- [🔍 Documentation](#-documentation)
- [💬 Message format](#-message-format)

## 📖 Requirements
There are several requirements needed to successfully configure and use the tool.
* **Authentication token** - Discord user authentication token. Follow this [guide](https://bit.ly/31Vcno0) on how to obtain the token.

## 💭 Usage
There are two ways to install & use this package, either via binaries or via source code.
* **[Source](Source)** - Use native Python source code to extend and customize the tool. Advised for advanced configuration and development.
* **[Binaries](Binaries)** - Use OS-native binaries to interact with the tool. Best to use if you only want to consume the library.

### Source
Use this step if you would like to extend and contribute. You will have to install required packages in order to properly run 
and customize the code.

**Requirements**
* Python >= `3.6.9`

Launch your OS-native development environment and start hacking:
```bash
### Install
$ git clone https://github.com/fhivemind/discord-bot
$ cd discord-bot
$ python -m pip install -r requirements.txt

### Verify
$ python cli.py info

🎯 Environment information

   Version: v1.0.0
   Author: Ramiz Polic (fhivemind)

```

### Binaries
You can find all the binaries under **[release](https://github.com/fhivemind/discord-bot/releases)** page. Download the necessary files to start hacking.

Launch your OS native shell in the same folder where the binary is located and verify the installation:
```bash
$ cli info

🎯 Environment information

   Version: v1.0.0
   Author: Ramiz Polic (fhivemind)

```

### Building procedures
You can build the library by simply running `make`. This will generate OS-specific binaries under `./dist` folder.

## 🔍 Documentation
Short list about available CLI commands and their usages is available under [docs](docs) folder.

## 💬 Message format
The format of the private messages that will be sent to users is defined by **[MESSAGE.md](MESSAGE.md)**. 
To add your custom message, update this file. 

All attributes formatted as `__ATTR__` will be replaced by their respective definition value.     
Currently supported attributes include:

Format | Value
---|---
`__USERNAME__`| User mention, e.g. @fhivemind

---

* **Auhor:** Ramiz Polic (fhivemind)
* **Version:** v1.0.0
