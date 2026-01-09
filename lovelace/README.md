# Lovelace Dashboard Examples

This directory contains example Lovelace cards and dashboards for displaying your Easy Equities portfolio in Home Assistant.

## Structure

- **`cards/`** - Individual card examples that can be added to any dashboard
- **`dashboards/`** - Complete dashboard configurations

## Cards

### `portfolio_overview.yaml`
A simple entities card showing key portfolio metrics at a glance.

### `portfolio_summary.yaml`
A vertical stack card with portfolio summary information.

### `holdings_list.yaml`
A card displaying all individual holdings in your portfolio.

## Dashboards

### `portfolio_overview.yaml`
A complete portfolio dashboard with:
- Portfolio value gauges
- Key metrics
- Holdings list

### `master.yaml`
A comprehensive master dashboard with:
- Portfolio overview section
- Holdings details
- Performance analysis
- Charts and statistics

## Installation

### Method 1: Manual Copy
1. Copy the dashboard YAML files to your Home Assistant configuration
2. Import them via the dashboard editor in Home Assistant

### Method 2: Dashboard Import
1. Go to **Settings** → **Dashboards**
2. Click the three dots menu → **Import dashboard**
3. Copy and paste the YAML content from the dashboard files

## Customization

### Entity IDs
The examples use generic entity IDs. You'll need to replace them with your actual sensor entity IDs:

- `sensor.portfolio_value` - Your portfolio value sensor
- `sensor.portfolio_profit_loss` - Your profit/loss sensor
- `sensor.holding_*` - Your individual holding sensors

### Finding Your Entity IDs
1. Go to **Settings** → **Devices & Services**
2. Click on **Easy Equities**
3. Click on **Entities** tab
4. Note the entity IDs for your sensors

### Auto-Entities Card
Some examples use the `auto-entities` card to automatically include all holding sensors. If you don't have this card installed:

1. Install via HACS: Search for "Auto Entities"
2. Or manually add each holding sensor to the entities list

## Requirements

- Home Assistant 2023.1.0 or later
- Easy Equities integration installed and configured
- (Optional) Auto Entities card from HACS for automatic sensor inclusion

## Notes

- All cards use standard Home Assistant cards (no HACS dependencies required, except for auto-entities)
- Entity IDs may vary based on your Home Assistant configuration
- Adjust the entity IDs in the YAML files to match your actual sensor names
- The `master.yaml` dashboard uses Jinja2 templates for dynamic content
