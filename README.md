# Smoke Lab (**Bot**)

![Bot](https://img.shields.io/badge/Bot-Smoke_Lab-brightgreen)
![Status](https://img.shields.io/badge/Status-Complete-yellow)
![Self Development](https://img.shields.io/badge/Project-Self_Development-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

The Smoke Lab Bot is a comprehensive Telegram bot built to enhance user experience with various features. It includes language change, a user-friendly inline keyboard menu, user profile management, promocode creation, order checking, and status updates. Additionally, an admin panel provides control over stock management, order tracking, promocode administration, user statistics, and administrative privileges.

## Table of Contents

-  [Folder Structure](#folder-structure)
-  [Usage](#usage)
-  [Media](#media)
-  [Contributing](#contributing)
-  [Dependencies](#dependencies)

## Folder Structure

-  **bot:** Folder containing the bot's source code and logic.
-  **run.py:** Python script for running the bot.
-  **requirements.txt:** File specifying the required Python packages and their versions.

## Usage

1. Clone the repository:

```bash
git clone https://github.com/HEAD0223/smoke-lab-bot.git
cd smoke-lab-bot
```

2. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install required dependencies:

```bash
pip install --upgrade -r requirements.txt
```

4. Run the bot:

```bash
python run.py
```

## Media

### Mobile

#### User

![mobile_Smoke-Lab_user](./preview/mobile_Smoke-Lab_user.gif)
<img src="./preview/mobile_smoke-lab-bot_admin_1.jpg" style="width:50%">
<img src="./preview/mobile_smoke-lab-bot_admin_1.jpg" style="width:50%">

**Main Page, languages, about us:**
![mobile_smoke-lab-bot_user_1](./preview/mobile_smoke-lab-bot_user_1.jpg)
![mobile_smoke-lab-bot_user_2](./preview/mobile_smoke-lab-bot_user_2.jpg)
![mobile_smoke-lab-bot_user_3](./preview/mobile_smoke-lab-bot_user_3.jpg)
![mobile_smoke-lab-bot_user_4](./preview/mobile_smoke-lab-bot_user_4.jpg)

**Profile, promocodes, current order:**
![mobile_smoke-lab-bot_user_5](./preview/mobile_smoke-lab-bot_user_5.jpg)
![mobile_smoke-lab-bot_user_6](./preview/mobile_smoke-lab-bot_user_6.jpg)
![mobile_smoke-lab-bot_user_7](./preview/mobile_smoke-lab-bot_user_7.jpg)

#### Admin Panel

![mobile_Smoke-Lab_admin](./preview/mobile_Smoke-Lab_admin.gif)
![mobile_smoke-lab-bot_admin_1](./preview/mobile_smoke-lab-bot_admin_1.jpg)

**Stock management, Orders management, finished promocodes:**
![mobile_smoke-lab-bot_admin_2](./preview/mobile_smoke-lab-bot_admin_2.jpg)
![mobile_smoke-lab-bot_admin_3](./preview/mobile_smoke-lab-bot_admin_3.jpg)
![mobile_smoke-lab-bot_admin_4](./preview/mobile_smoke-lab-bot_admin_4.jpg)

**Statistics and user editing, Admin privileges management:**
![mobile_smoke-lab-bot_admin_5](./preview/mobile_smoke-lab-bot_admin_5.jpg)
![mobile_smoke-lab-bot_admin_6](./preview/mobile_smoke-lab-bot_admin_6.jpg)

### PC

#### User

![pc_Smoke-Lab_user](./preview/pc_Smoke-Lab_user.gif)

**Main Page, languages, about us:**
![pc_smoke-lab-bot_user_1](./preview/pc_smoke-lab-bot_user_1.png)
![pc_smoke-lab-bot_user_2](./preview/pc_smoke-lab-bot_user_2.png)
![pc_smoke-lab-bot_user_3](./preview/pc_smoke-lab-bot_user_3.png)
![pc_smoke-lab-bot_user_4](./preview/pc_smoke-lab-bot_user_4.png)

**Profile, promocodes, current order:**
![pc_smoke-lab-bot_user_5](./preview/pc_smoke-lab-bot_user_5.png)
![pc_smoke-lab-bot_user_6](./preview/pc_smoke-lab-bot_user_6.png)
![pc_smoke-lab-bot_user_7](./preview/pc_smoke-lab-bot_user_7.png)

#### Admin Panel

![pc_Smoke-Lab_admin](./preview/pc_Smoke-Lab_admin.gif)
![pc_smoke-lab-bot_admin_1](./preview/pc_smoke-lab-bot_admin_1.png)

**Stock management, Orders management, finished promocodes:**
![pc_smoke-lab-bot_admin_2](./preview/pc_smoke-lab-bot_admin_2.png)
![pc_smoke-lab-bot_admin_3](./preview/pc_smoke-lab-bot_admin_3.png)
![pc_smoke-lab-bot_admin_4](./preview/pc_smoke-lab-bot_admin_4.png)

**Statistics and user editing, Admin privileges management:**
![pc_smoke-lab-bot_admin_5](./preview/pc_smoke-lab-bot_admin_5.png)
![pc_smoke-lab-bot_admin_6](./preview/pc_smoke-lab-bot_admin_6.png)

## Contributing

If you would like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request.

## Dependencies

-  **aiogram:** Telegram bot library for Python.
-  **aiohttp:** Asynchronous HTTP client/server framework for Python.
-  **aiosignal:** Signal handling library for asyncio.
-  **async-timeout:** Timeout context manager for asyncio.
-  **asyncio:** Asynchronous I/O framework.
-  **attrs:** Python classes without boilerplate.
-  **Babel:** Internationalization framework for Python.
-  **certifi:** Certificates for Python.
-  **charset-normalizer:** Charset normalization library.
-  **dnspython:** DNS toolkit for Python.
-  **frozenlist:** Immutable list data type.
-  **idna:** Internationalized Domain Names in Applications (IDNA) library.
-  **magic-filter:** Asynchronous DNS-based content filtering library.
-  **multidict:** Multidimensional dictionaries for Python.
-  **pandas:** Data manipulation and analysis library.
-  **pymongo:** MongoDB driver for Python.
-  **python-dotenv:** Loads environment variables from a .env file.
-  **pytz:** Time zone library for Python.
-  **yarl:** Yet another URL library for Python.

Make sure to include these dependencies in your virtual environment using `pip install -r requirements.txt`.
