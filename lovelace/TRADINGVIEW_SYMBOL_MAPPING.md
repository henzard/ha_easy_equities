# TradingView Symbol Mapping Guide

This guide helps you map Easy Equities contract codes to TradingView symbols for use in the TradingView Widget Card.

## Contract Code Format

Easy Equities uses the following contract code format:
- `EQU.{EXCHANGE}.{SYMBOL}`
- Examples:
  - `EQU.ZA.BVT` → South African exchange, Bidvest Limited
  - `EQU.US.TSLA` → US exchange, Tesla Inc
  - `EQU.AU.MND` → Australian exchange, Monadelphous Group
  - `EQU.DE.BMW` → German exchange, BMW

## Symbol Mapping Rules

### South African Stocks (EQU.ZA.*)
- Remove `EQU.ZA.` prefix
- Add `.JSE` suffix for JSE-listed stocks
- Example: `EQU.ZA.BVT` → `BVT.JSE`

### US Stocks (EQU.US.*)
- Remove `EQU.US.` prefix
- Use symbol directly
- Example: `EQU.US.TSLA` → `TSLA`

### Australian Stocks (EQU.AU.*)
- Remove `EQU.AU.` prefix
- Add `.ASX` suffix
- Example: `EQU.AU.MND` → `MND.ASX`

### European Stocks
- **German (EQU.DE.*)**: Remove `EQU.DE.` prefix, add `.XETR` or `.XETRA` suffix
  - Example: `EQU.DE.BMW` → `BMW.XETR`
- **Netherlands (EQU.NL.*)**: Remove `EQU.NL.` prefix, add `.AMS` suffix
  - Example: `EQU.NL.SHELL` → `SHELL.AMS`

## Automated Mapping Function

You can use this Home Assistant template to automatically convert contract codes:

```yaml
{% set contract_code = state_attr('sensor.easy_equities_holding_equ_za_bvt', 'contract_code') %}
{% if contract_code.startswith('EQU.ZA.') %}
  {{ contract_code.replace('EQU.ZA.', '') }}.JSE
{% elif contract_code.startswith('EQU.US.') %}
  {{ contract_code.replace('EQU.US.', '') }}
{% elif contract_code.startswith('EQU.AU.') %}
  {{ contract_code.replace('EQU.AU.', '') }}.ASX
{% elif contract_code.startswith('EQU.DE.') %}
  {{ contract_code.replace('EQU.DE.', '') }}.XETR
{% elif contract_code.startswith('EQU.NL.') %}
  {{ contract_code.replace('EQU.NL.', '') }}.AMS
{% else %}
  {{ contract_code }}
{% endif %}
```

## Common Symbols Reference

### South African (JSE)
- `EQU.ZA.BVT` → `BVT.JSE` (Bidvest)
- `EQU.ZA.SHP` → `SHP.JSE` (Shoprite)
- `EQU.ZA.VOD` → `VOD.JSE` (Vodacom)
- `EQU.ZA.NPN` → `NPN.JSE` (Naspers)
- `EQU.ZA.SBK` → `SBK.JSE` (Standard Bank)

### US Stocks
- `EQU.US.TSLA` → `TSLA` (Tesla)
- `EQU.US.AAPL` → `AAPL` (Apple)
- `EQU.US.MSFT` → `MSFT` (Microsoft)
- `EQU.US.NVDA` → `NVDA` (Nvidia)
- `EQU.US.AMD` → `AMD` (AMD)

### Australian (ASX)
- `EQU.AU.MND` → `MND.ASX` (Monadelphous)
- `EQU.AU.FMG` → `FMG.ASX` (Fortescue)
- `EQU.AU.WES` → `WES.ASX` (Wesfarmers)

### European
- `EQU.DE.BMW` → `BMW.XETR` (BMW)
- `EQU.DE.SIE` → `SIE.XETR` (Siemens)
- `EQU.NL.SHELL` → `SHELL.AMS` (Shell)

## Notes

- Some symbols may need manual verification on TradingView
- ETF symbols may require different mapping
- International ADRs may use different symbols
- Always verify the symbol exists on TradingView before using in widgets
