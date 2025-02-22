# Manifold Markets Trading Bot

![GitHub last commit](https://img.shields.io/github/last-commit/ugine-bor/Manifold_Trading_Bot)

A Python-based trading bot that interacts with the [Manifold Markets](https://manifold.markets/) API to automate market predictions. This project includes a basic (and intentionally simplistic) trading strategy for demonstration purposes.

## Features

- **API Interaction**: Wrapper methods for Manifold Markets API endpoints, including:
  - Market data retrieval (by ID, slug, filters)
  - User information lookup
  - Group and league data
  - Bet placement and historical bet analysis
- **Basic Trading Strategy**: 
  - Monitors recently created binary markets closing soon
  - Places opposing bets when significant trading activity is detected
  - Includes simple volume-based decision logic
- **Caching System**: Basic bet caching to avoid duplicate actions
- **Console Logging**: Optional verbose logging for debugging and monitoring

## Installation

1. Clone repository:
   ```bash
   git clone https://github.com/yourusername/manifold-bot.git
   cd manifold-bot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create `.env` file:
   ```env
   API_KEY=your_manifold_api_key_here
   ```

## Configuration

1. Obtain your API key from [Manifold Markets](https://manifold.markets/) (Settings -> API Key)
2. Add key to `.env` file as shown above

## Usage

Run the bot:
```bash
python main.py
```

The bot will:
1. Continuously monitor newest binary markets closing this month
2. Track recent bets on these markets
3. Place opposing limit orders when:
   - Significant trading volume (≥10% of market volume) appears on one side
   - New bets are detected since last check

## Strategy Overview

The included demonstration strategy implements basic contrarian logic:

```python
1. Fetch 10 newest binary markets closing soon
2. Check last 5 bets on each market
3. If new bets detected:
   a. Calculate total YES and NO bet amounts
   b. If YES bets ≥ 10% market volume:
      - Place NO bet at 5% below current probability
   c. If NO bets ≥ 10% market volume:
      - Place YES bet at 5% above current probability
4. Repeat every second
```

**Note**: This is intentionally simplistic for demonstration. Consider it a starting point rather than a profitable strategy.

## API Methods

The `Bot` class implements several API endpoints:

| Method | Description |
|--------|-------------|
| `get_markets()` | Retrieve market list with filters |
| `get_market_by_id()` | Get full market details |
| `post_bet()` | Place limit/market orders |
| `get_bets()` | Historical bet data |
| `get_users()` | User lookup |
| `get_groups()` | Group information |

See code comments for full method details and parameters.

## Disclaimer

This project is for educational purposes only. The included strategy is not financial advice. Use at your own risk.
