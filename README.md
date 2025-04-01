<h1 align="center">Telegram Gifts Auto-Buyer</h1>

<div align="center">
  <img src="https://github.com/user-attachments/assets/b1f6a9f3-2690-41ef-8c7a-c3119f29bab3" alt="Preview" width="600px">
</div>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/github/license/bohd4nx/Gifts-Buyer" alt="License">
  <img src="https://img.shields.io/github/stars/bohd4nx/Gifts-Buyer" alt="Stars">
  <br>
  <a href="https://t.me/bohd4nx">
    <img src="https://img.shields.io/badge/developer-@bohd4nx-blue.svg" alt="Developer">
  </a>
  <a href="https://t.me/GiftsTracker">
    <img src="https://img.shields.io/badge/channel-@GiftsTracker-blue.svg" alt="Channel">
  </a>
</p>

<p align="center">
  <a href="README.md">English</a> |
  <a href="./README-RU.md">Русский</a>
</p>

## 📝 Overview

An advanced Telegram userbot for automated gift sending with dynamic price ranges and more. Supports both
limited and non-limited gifts with configurable sending rules. The bot automatically detects new gifts and processes
them based on your settings.

## ✨ Features

- 🎁 Dynamic gift quantity based on price ranges
- 🔍 Automatic detection of new gifts as they appear
- 📊 Supply limit monitoring
- 🌐 Multi-language support (English, Russian, Ukrainian)
- ⚡️ Smart filtering of gifts based on price and type
- 🔄 Configurable delays and intervals
- 📱 Multiple recipient support
- 🎯 Price-based filtering

## ⚙️ Configuration

### Basic Setup (config.ini)

```ini
[Telegram]
API_ID = your_api_id         # Your Telegram API ID from https://my.telegram.org
API_HASH = your_api_hash     # Your Telegram API Hash from https://my.telegram.org
PHONE_NUMBER = +1234567890   # Your phone number in international format
CHANNEL_ID = -100xxxxxxxxx   # Channel ID for notifications (should start with -100)

[Bot]
INTERVAL = 10                # Interval between checks in seconds (minimum: 10s)
TIMEZONE = Europe/London     # Your timezone for logs and operations
LANGUAGE = EN                # Interface language (EN/RU/UK)

[Gifts]
MIN_GIFT_PRICE = 0           # Minimum price of gifts to consider buying
MAX_GIFT_PRICE = 10000       # Maximum price of gifts to consider buying
GIFT_QUANTITY = 1            # Number of each gift to send
GIFT_DELAY = 5               # Delay between sending gifts in seconds
USER_ID = 123456789, username # Recipients (IDs or usernames without @)
HIDE_SENDER_NAME = True      # Whether to hide the sender's name
PURCHASE_NON_LIMITED_GIFTS = False # Whether to purchase non-limited gifts
PURCHASE_ONLY_UPGRADABLE_GIFTS = False # Whether to purchase only upgradable gifts
```

## 🚀 Installation

1. Clone the repository (or download it as ZIP):

```bash
git clone https://github.com/bohd4nx/Gifts-Buyer.git
cd Gifts-Buyer
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Configure the settings:
    - Open `config.ini`
    - Enter your Telegram API credentials
    - Configure gift price ranges and other preferences
    - Save the file

4. Run the bot:

```bash
python main.py
```

## 🌍 Localization

The bot supports multiple languages:

- 🇺🇸 English
- 🇷🇺 Russian
- 🇺🇦 Ukrainian

To change the language:

- Edit the `LANGUAGE` setting in `config.ini`
- Set to `EN`, `RU`, or `UK`

## 🔧 Troubleshooting

### Common Issues

1. **API connection errors**:
    - Verify your API credentials
    - Check your internet connection
    - Ensure your Telegram account is not restricted

2. **Gift purchasing problems**:
    - Check your price range settings
    - Make sure you have sufficient balance
    - Verify that recipients are valid and reachable

3. **Library errors**:
   ```bash
   pip install -r requirements.txt
   ```

## ⚠️ Disclaimer

This project is for educational purposes only. Use responsibly and at your own risk. The developer is not responsible
for any misuse or consequences resulting from the use of this software.

## 📝 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🌟 Support

If you find this project useful:

- Give it a star ⭐
- Share with others 🔄
- Consider following the developer on Telegram

---

<div align="center">
    <h4>Built with ❤️ by <a href="https://t.me/bohd4nx" target="_blank">Bohdan</a></h4>
</div>
