# Easy Equities Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub release](https://img.shields.io/github/release/henzard/ha_easy_equities.svg)](https://github.com/henzard/ha_easy_equities/releases)
[![License](https://img.shields.io/github/license/henzard/ha_easy_equities.svg)](LICENSE)

A Home Assistant integration to monitor your Easy Equities and Satrix portfolio directly from your dashboard.

## Features

- 📊 **Portfolio Overview**: Monitor your total portfolio value, purchase value, and profit/loss
- 📈 **Individual Holdings**: Track each holding with current value, purchase value, shares, and more
- 🔄 **Auto Updates**: Automatically updates every 5 minutes (configurable)
- 🔐 **Secure**: Credentials stored securely in Home Assistant
- 🎯 **Multiple Accounts**: Support for multiple Easy Equities accounts
- 🏢 **Satrix Support**: Works with both Easy Equities and Satrix accounts

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Go to Integrations
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL: `https://github.com/henzard/ha_easy_equities`
6. Select category: "Integration"
7. Click "Add"
8. Search for "Easy Equities" and install it
9. Restart Home Assistant

### Manual Installation

1. Download the latest release from [GitHub Releases](https://github.com/henzard/ha_easy_equities/releases)
2. Extract the `easy_equities` folder to `custom_components/` in your Home Assistant configuration directory
3. Restart Home Assistant

## Configuration

1. Go to **Settings** → **Devices & Services**
2. Click **Add Integration**
3. Search for **Easy Equities**
4. Enter your Easy Equities username and password
5. Select your account (if you have multiple accounts)
6. Click **Submit**

## Sensors

The integration creates the following sensors:

### Portfolio Sensors

- **Portfolio Value**: Total current value of your portfolio
- **Portfolio Purchase Value**: Total amount invested
- **Portfolio Profit/Loss**: Total profit or loss in ZAR
- **Portfolio Profit/Loss %**: Total profit or loss percentage
- **Portfolio Holdings Count**: Number of holdings in your portfolio

### Individual Holding Sensors

For each holding in your portfolio, a sensor is created with:
- Current value
- Purchase value
- Current price
- Number of shares
- Contract code
- ISIN code

## Dashboard Example

You can create a dashboard card to display your portfolio:

```yaml
type: entities
title: Easy Equities Portfolio
entities:
  - entity: sensor.portfolio_value
    name: Total Value
  - entity: sensor.portfolio_profit_loss
    name: Profit/Loss
  - entity: sensor.portfolio_profit_loss_percent
    name: Profit/Loss %
  - entity: sensor.portfolio_holdings_count
    name: Holdings
```

## Options

You can configure the update interval in the integration options:

1. Go to **Settings** → **Devices & Services**
2. Click on **Easy Equities**
3. Click **Options**
4. Adjust the **Scan Interval** (in seconds, default: 300)

## Requirements

- Home Assistant 2023.1.0 or later
- Python 3.9 or later
- Easy Equities or Satrix account

## Troubleshooting

### Authentication Errors

If you see authentication errors:
1. Verify your username and password are correct
2. Check if your account is locked or requires 2FA
3. Try removing and re-adding the integration

### No Data

If sensors show "unknown" or no data:
1. Check the Home Assistant logs for errors
2. Verify your account has holdings
3. Try reloading the integration

### Update Issues

If data is not updating:
1. Check the scan interval in options
2. Verify your internet connection
3. Check Home Assistant logs for API errors

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This is an unofficial integration and is not affiliated with Easy Equities or Satrix. Use at your own risk. The developers are not responsible for any financial decisions made based on this integration.

## Credits

- Built using [easy-equities-client](https://github.com/deanmalan/easy-equities-client) by [@deanmalan](https://github.com/deanmalan)
- Inspired by the Home Assistant community

## Support

For issues, feature requests, or questions:
- Open an issue on [GitHub](https://github.com/henzard/ha_easy_equities/issues)
- Check the [documentation](https://github.com/henzard/ha_easy_equities)
