# TradingView Widget Integration for Easy Equities

This guide shows you how to integrate [TradingView Widget Card](https://github.com/cataseven/Tradingview-Widget-Card) with your Easy Equities portfolio data.

## Prerequisites

1. **Install TradingView Widget Card via HACS:**
   - Go to HACS → Frontend
   - Search for "TradingView Widget Card"
   - Install and restart Home Assistant

2. **Map Your Holdings to TradingView Symbols:**
   - Check your holdings' `contract_code` and `isin` attributes
   - Find the corresponding TradingView symbol format
   - Common formats:
     - JSE (Johannesburg): `JSE:ABG`
     - NASDAQ: `NASDAQ:AAPL`
     - NYSE: `NYSE:TSLA`
     - LSE (London): `LSE:VOD`

## Finding Your Holdings' TradingView Symbols

1. Go to **Settings** → **Devices & Services** → **Easy Equities**
2. Click on **Entities**
3. Find a holding sensor (e.g., `sensor.easy_equities_holding_EQU_ZA_SYGJP`)
4. Check the `contract_code` and `isin` attributes
5. Search for the symbol on TradingView.com to find the correct format

## Available Widget Types

### 1. Ticker Tape
Scrolling horizontal bar showing live prices of your holdings.

```yaml
type: custom:tradingview-widget-card
widget_type: ticker-tape
pairs:
  - JSE:ABG
  - JSE:AGL
```

### 2. Tickers
Vertical list of holdings with live prices and changes.

```yaml
type: custom:tradingview-widget-card
widget_type: tickers
pairs:
  - JSE:ABG
  - JSE:AGL
```

### 3. Technical Analysis
Candlestick charts with technical indicators for individual holdings.

```yaml
type: custom:tradingview-widget-card
widget_type: technical-analysis
pairs:
  - JSE:ABG
interval: 1D
```

### 4. Single Quote
Detailed view of a single holding with price, change, and volume.

```yaml
type: custom:tradingview-widget-card
widget_type: single-quote
pairs:
  - JSE:ABG
```

### 5. Stock Heatmap
Visual representation of market sectors and performance.

```yaml
type: custom:tradingview-widget-card
widget_type: stock-heatmap
data_source: SPX500
```

### 6. Market Overview
Comprehensive market view with multiple tabs for different asset classes.

```yaml
type: custom:tradingview-widget-card
widget_type: market-overview
tab_config: |-
  Stocks:
   - JSE:ABG
   - JSE:AGL
```

## Example Dashboard

See `tradingview_enhanced.yaml` for a complete example dashboard that combines:
- Portfolio summary from Easy Equities
- Live ticker tape of holdings
- Technical analysis charts
- Market overview
- Stock heatmaps

## Dynamic Symbol Mapping (Advanced)

To automatically map your holdings to TradingView symbols, you can use Jinja2 templates:

```yaml
type: custom:tradingview-widget-card
widget_type: ticker-tape
pairs: >
  {% set holdings = states.sensor | selectattr('entity_id', 'match', 'sensor.*_holding_.*') | list %}
  {% for holding in holdings %}
  - JSE:{{ state_attr(holding.entity_id, 'contract_code') }}
  {% endfor %}
```

**Note:** This requires mapping your `contract_code` to TradingView format, which may need manual configuration.

## Tips

1. **Start Simple:** Begin with the ticker tape or tickers widget
2. **Verify Symbols:** Always verify your symbols work on TradingView.com first
3. **Use Technical Analysis:** Great for monitoring individual holdings
4. **Market Overview:** Perfect for seeing your portfolio in context
5. **Customize Colors:** Match your dashboard theme with `color_theme: dark` or `light`

## Troubleshooting

- **Widgets not showing:** Ensure TradingView Widget Card is installed and Home Assistant is restarted
- **Wrong symbols:** Verify the TradingView symbol format matches your exchange
- **No data:** Some symbols may not be available on TradingView, check on TradingView.com

## Resources

- [TradingView Widget Card GitHub](https://github.com/cataseven/Tradingview-Widget-Card)
- [TradingView Symbol Search](https://www.tradingview.com/symbols/)
- [Easy Equities Integration Documentation](../README.md)
