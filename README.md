# Telegram Gifts Buyer

<img src="https://github.com/user-attachments/assets/a8d750d3-500c-4372-9733-3bbd509643e8" alt="Program Preview" width="100%" />

An automated Telegram userbot that purchases new gifts as they become available in the Telegram store. The bot can
handle both limited and non-limited gifts with flexible configuration options and intelligent prioritization.

> 🌐 [Русская версия документации](README-RU.md)

## 📋 Features

- **Automated Gift Detection**: Continuously monitors for new gifts in the Telegram store
- **Smart Prioritization**: Prioritize gifts with low supply that match your price ranges
- **Range-Based Purchasing**: Buy gifts based on price ranges with supply requirements
- **Multiple Recipients**: Send gifts to one or more users
- **Customizable Quantity**: Send multiple copies of the same gift
- **Notification System**: Get updates on purchases through a designated Telegram channel
- **Advanced Filtering**: Choose to buy only limited or upgradable gifts
- **Multi-language Support**: Available in English and Russian

## 🛠️ Installation

### Setup Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/bohd4nx/Gifts-Buyer.git
   cd Gifts-Buyer
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure the application:
    - Edit the `config.ini` file with your API credentials
    - Set your preferred gift purchasing parameters

## ⚙️ Configuration

Open `config.ini` and configure the following sections:

### Telegram API Settings

```ini
[Telegram]
API_ID = your_api_id              # Get from https://my.telegram.org/apps
API_HASH = your_api_hash          # Get from https://my.telegram.org/apps
PHONE_NUMBER = +1234567890        # Your phone number in international format
CHANNEL_ID = -100123456789        # Channel for notifications (optional, starts with -100)
```

### Bot Behavior

```ini
[Bot]
INTERVAL = 10     # Check interval in seconds (recommended: 5-15)
LANGUAGE = EN     # Interface language (EN or RU)
```

### Gift Preferences

```ini
[Gifts]
# Price ranges with supply limits (format: min_price-max_price: supply_limit)
PRICE_RANGES = 1-1000: 500000, 1001-5000: 100000, 5001-10000: 50000

GIFT_QUANTITY = 1                       # Number of each gift to send
USER_ID = 123456789, username          # Recipients (comma-separated IDs or usernames)

# Purchase filters
PURCHASE_NON_LIMITED_GIFTS = False      # Whether to buy non-limited gifts
PURCHASE_ONLY_UPGRADABLE_GIFTS = False  # Buy only upgradable gifts

# Smart prioritization
PRIORITIZE_LOW_SUPPLY = True            # Prioritize gifts matching ranges with lowest supply first
```

#### Price Range Configuration

The `PRICE_RANGES` parameter allows you to specify multiple price ranges with corresponding supply limits (all ranges
are **inclusive**):

- `1-1000: 500000` - Buy gifts priced 1-1000 stars if supply ≤ 500,000
- `1001-5000: 100000` - Buy gifts priced 1001-5000 stars if supply ≤ 100,000
- `5001-10000: 50000` - Buy gifts priced 5001-10000 stars if supply ≤ 50,000

**Example:** A gift priced at 1000 stars with 500,000 supply will match the first range. A gift with 500,001 supply will
NOT match any range.

#### Smart Prioritization

When `PRIORITIZE_LOW_SUPPLY = True`, the bot will:

1. **First Priority**: Process gifts that match your price ranges, sorted by lowest supply
2. **Second Priority**: Process remaining gifts in discovery order

This ensures you get the rarest gifts that fit your criteria before they sell out!

**Example Scenario:**

- Gift A: 2000⭐, 50,000 supply (matches range, low supply)
- Gift B: 1500⭐, 200,000 supply (matches range, high supply)
- Gift C: 15000⭐, 10,000 supply (doesn't match any range)

**Processing Order:** A → B → C

## 🚀 Usage

Run the bot with:

```bash
python main.py
```

The bot will:

1. Log in to your Telegram account
2. Start monitoring for new gifts
3. Purchase gifts that match your criteria (prioritizing low supply if enabled)
4. Send notifications through your specified channel

## 📊 Monitoring & Notifications

The bot provides detailed notifications including:

- ✅ Successful purchases with recipient information
- ❌ Failed purchases with error explanations
- 📊 Processing summaries (skipped gifts breakdown)
- 💰 Balance notifications for insufficient funds
- 🎯 Range mismatch notifications

### Filter Options

- `PURCHASE_NON_LIMITED_GIFTS = True` - Also buy non-limited gifts
- `PURCHASE_ONLY_UPGRADABLE_GIFTS = True` - Only buy gifts that can be upgraded

## 📝 Notes & Best Practices

- **Balance Management**: Ensure your account has sufficient stars for purchases
- **Error Handling**: The bot automatically handles common errors (insufficient balance, sold out gifts, etc.)
- **24/7 Operation**: For best results, run the bot on a VPS/server for continuous monitoring
- **Rate Limiting**: The bot includes built-in delays to respect Telegram's API limits
- **Priority Strategy**: Use `PRIORITIZE_LOW_SUPPLY = True` for competitive gift hunting

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

<div align="center">
    <h4>Built with ❤️ by <a href="https://t.me/bohd4nx" target="_blank">Bohdan</a></h4>
</div>
