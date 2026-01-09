---
description: "Easy Equities integration specific rules and guidelines"
alwaysApply: true
---

# Easy Equities Integration Specific Rules

## Integration Domain
- Domain: `easy_equities`
- Integration folder: `custom_components/easy_equities/`
- Display name: "Easy Equities"

## Dependencies
- **easy-equities-client** - Python client library for Easy Equities API
- Minimum version: `easy-equities-client>=0.1.0`
- Always check for latest version compatibility

## Supported Platforms
- Easy Equities (default)
- Satrix (via configuration option)

## Data Sources
- Portfolio holdings
- Account valuations
- Transaction history
- Historical prices (via instruments API)

## Security Considerations
- Never log user credentials
- Store credentials securely in Home Assistant config entries
- Handle authentication errors gracefully
- Support re-authentication flow

## Update Intervals
- Default: 300 seconds (5 minutes)
- Configurable via options flow
- Minimum: 60 seconds
- Maximum: 3600 seconds (1 hour)

## Sensor Naming
- Portfolio sensors: `sensor.portfolio_*`
- Holding sensors: `sensor.holding_*`
- Use descriptive names with proper units

## Error Handling
- Handle API rate limits gracefully
- Retry logic for transient failures
- Clear error messages for authentication failures
- Log API errors for debugging

## Testing
- Test with both Easy Equities and Satrix accounts
- Verify multi-account support
- Test error scenarios (invalid credentials, network failures)
- Validate data parsing and calculations
