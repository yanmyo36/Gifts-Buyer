<h2 align="center">Telegram Gifts Auto-Buyer</h2>

<div align="center">
  <img src="https://github.com/user-attachments/assets/2c4540b7-4e39-4306-945f-389271123ecc" alt="Preview" width="600px">
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

An advanced Telegram userbot for automated gift sending with dynamic price ranges and supply management. Supports both
limited and non-limited gifts with configurable sending rules.

## ✨ Features

- 🎁 Dynamic gift quantity based on price ranges
- 📊 Supply limit monitoring
- 🌐 Multi-language support (EN/RU/UK)
- ⚡️ Automatic gift detection
- 🔄 Configurable delays and intervals
- 📱 Multiple recipient support
- 🎯 Price-based filtering

## ⚙️ Configuration

### Basic Setup (config.ini)

```ini
[Telegram]
API_ID = your_api_id  # Your Telegram API ID
API_HASH = your_api_hash  # Your Telegram API Hash
CHANNEL_ID = your_channel_id  # The ID of the channel to monitor

[Bot]
INTERVAL = 10  # Interval between checks in seconds
TIMEZONE = Europe/Moscow  # Timezone for scheduling
LANGUAGE = EN  # Language for bot messages (EN/RU/UK)

[Gifts]
MAX_GIFT_PRICE = 10000  # Maximum price of gifts to consider
GIFT_DELAY = 5  # Delay between sending gifts in seconds
USER_ID = user1_id, username  # User IDs or usernames to send gifts to
HIDE_SENDER_NAME = True  # Whether to hide the sender's name
PURCHASE_NON_LIMITED_GIFTS = False  # Whether to purchase non-limited gifts
```

### Price Range Configuration

The bot uses a sophisticated price range system to determine gift quantities:

```ini
[Ranges]
0,999,10000 = 1      # Price 0-999, supply limit 10000, send 1 gift
1000,1999,100 = 2    # Price 1000-1999, supply limit 100, send 2 gifts
2000,2999,1000 = 3   # Price 2000-2999, supply limit 1000, send 3 gifts
```

Format: `min_price,max_price,supply_limit = quantity`

## 🚀 Installation

1. Clone repository: (or just download it)

```bash
git clone https://github.com/bohd4nx/Gifts-Buyerr.git
cd Gifts-Buyer
```

2. Install requirements:

```bash
pip install -r requirements.txt
```

3. Configure settings:
    - Open `config.ini`
    - Edit with your details
    - Set up price ranges

4. Run:

```bash
python main.py
```

## 🌍 Localization

Currently supports:

- 🇺🇸 English
- 🇷🇺 Russian
- 🇺🇦 Ukrainian

Add new language:

1. Create `locales/your_lang.py`
2. Add to `LANG_CODES` in `config.py`
3. Set `LANGUAGE = YOUR_LANG` in config.ini

## 🔧 Troubleshooting

### Common Issues

1. `AttributeError: 'Client' object has no attribute 'get_star_gifts'`
   ```bash
   pip uninstall pyrogram
   pip install pyrofork
   ```

2. Supply limit errors:
    - Check your [Ranges] configuration
    - Verify supply limits are appropriate

3. Connection errors:
    - Increase INTERVAL (minimum 10 seconds)
    - Check internet connection
    - Verify API credentials

## ⚠️ Disclaimer

For educational purposes only. Use responsibly and at your own risk.

## 📝 License

This project is MIT licensed. See LICENSE for more information.

## 🌟 Support

If you find this project useful:

- Give it a star ⭐
- Share with others 🔄
- Consider contributing 🛠️

---

<div align="center">
    <h4>Built with ❤️ by <a href="https://t.me/bohd4nx" target="_blank">Bohdan</a></h4>
</div>
