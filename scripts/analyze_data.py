#!/usr/bin/env python3
"""Script to analyze Easy Equities data structure."""
import asyncio
import json
import os
import sys
from pathlib import Path

# Fix Windows encoding issues
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Add parent directory to path to import the integration
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from easy_equities_client.clients import EasyEquitiesClient, SatrixClient

# Load environment variables
load_dotenv()


async def analyze_data():
    """Fetch and analyze Easy Equities data structure."""
    username = os.getenv("EASYEQUITIES_USERNAME") or os.getenv("EASY_EQUITIES_USERNAME")
    password = os.getenv("EASYEQUITIES_PASSWORD") or os.getenv("EASY_EQUITIES_PASSWORD")
    is_satrix = os.getenv("EASYEQUITIES_IS_SATRIX", os.getenv("EASY_EQUITIES_IS_SATRIX", "false")).lower() == "true"
    account_id = os.getenv("EASYEQUITIES_ACCOUNT_ID", os.getenv("EASY_EQUITIES_ACCOUNT_ID", ""))

    if not username or not password:
        print("ERROR: EASYEQUITIES_USERNAME and EASYEQUITIES_PASSWORD must be set in .env file")
        print("Copy .env.example to .env and fill in your credentials")
        sys.exit(1)

    print("=" * 80)
    print("Easy Equities Data Analysis")
    print("=" * 80)
    print(f"Username: {username}")
    print(f"Platform: {'Satrix' if is_satrix else 'Easy Equities'}")
    print(f"Account ID: {account_id if account_id else 'All accounts'}")
    print("=" * 80)
    print()

    try:
        # Initialize client
        if is_satrix:
            client = SatrixClient()
        else:
            client = EasyEquitiesClient()

        print("Step 1: Logging in...")
        client.login(username, password)
        print("[OK] Login successful")
        print()

        # Get accounts
        print("Step 2: Fetching accounts...")
        accounts = client.accounts.list()
        print(f"[OK] Found {len(accounts)} account(s)")
        print()

        for idx, account in enumerate(accounts, 1):
            print(f"Account {idx}:")
            print(f"  ID: {account.id}")
            print(f"  Name: {account.name}")
            print(f"  Trading Currency ID: {account.trading_currency_id}")
            print()

        # Determine which accounts to analyze
        accounts_to_analyze = []
        if account_id:
            account = next((acc for acc in accounts if acc.id == account_id), None)
            if account:
                accounts_to_analyze = [account]
            else:
                print(f"ERROR: Account ID {account_id} not found")
                sys.exit(1)
        else:
            accounts_to_analyze = accounts

        all_data = {}

        for account in accounts_to_analyze:
            print("=" * 80)
            print(f"Analyzing Account: {account.name} ({account.id})")
            print("=" * 80)
            print()

            account_data = {
                "account": {
                    "id": account.id,
                    "name": account.name,
                    "trading_currency_id": account.trading_currency_id,
                }
            }

            # Fetch holdings
            print("Step 3: Fetching holdings...")
            holdings = client.accounts.holdings(account.id, True)
            print(f"[OK] Found {len(holdings)} holding(s)")
            print()

            if holdings:
                print("Sample Holding Structure:")
                sample_holding = holdings[0]
                print(json.dumps(sample_holding, indent=2, default=str, ensure_ascii=False))
                print()

                print("Holdings Analysis:")
                print("-" * 80)
                currencies_found = set()
                contract_codes = []
                for holding in holdings:
                    # Analyze currency
                    purchase_value = holding.get("purchase_value", "")
                    current_value = holding.get("current_value", "")
                    
                    # Extract currency symbols
                    for val in [purchase_value, current_value]:
                        if isinstance(val, str):
                            if val.startswith("R") or "ZAR" in val.upper():
                                currencies_found.add("ZAR")
                            elif val.startswith("$") or "USD" in val.upper():
                                currencies_found.add("USD")
                            elif "€" in val or "EUR" in val.upper():
                                currencies_found.add("EUR")
                            elif "£" in val or "GBP" in val.upper():
                                currencies_found.add("GBP")
                    
                    contract_code = holding.get("contract_code", "")
                    if contract_code:
                        contract_codes.append(contract_code)
                    
                    print(f"  - {holding.get('name', 'Unknown')}")
                    print(f"    Contract Code: {contract_code}")
                    print(f"    ISIN: {holding.get('isin', 'N/A')}")
                    print(f"    Purchase Value: {purchase_value}")
                    print(f"    Current Value: {current_value}")
                    print(f"    Current Price: {holding.get('current_price', 'N/A')}")
                    print(f"    Shares: {holding.get('shares', 'N/A')}")
                    print()

                print(f"Currencies found in holdings: {', '.join(sorted(currencies_found)) if currencies_found else 'None detected'}")
                print(f"Contract codes found: {', '.join(contract_codes[:10])}{'...' if len(contract_codes) > 10 else ''}")
                print()

            account_data["holdings"] = holdings

            # Fetch valuations
            print("Step 4: Fetching valuations...")
            valuations = client.accounts.valuations(account.id)
            print(f"[OK] Found {len(valuations)} valuation(s)")
            if valuations and isinstance(valuations, (list, dict)):
                if isinstance(valuations, list) and len(valuations) > 0:
                    print("Sample Valuation Structure:")
                    print(json.dumps(valuations[0], indent=2, default=str, ensure_ascii=False))
                elif isinstance(valuations, dict):
                    print("Valuations Structure:")
                    print(json.dumps(valuations, indent=2, default=str, ensure_ascii=False))
                print()
            account_data["valuations"] = valuations

            # Fetch transactions
            print("Step 5: Fetching transactions...")
            transactions = client.accounts.transactions(account.id)
            print(f"[OK] Found {len(transactions)} transaction(s)")
            if transactions:
                print("Sample Transaction Structure:")
                print(json.dumps(transactions[0] if transactions else {}, indent=2, default=str))
                print()
            account_data["transactions"] = transactions[:10]  # Limit for analysis

            all_data[account.id] = account_data

        # Save full data to file for analysis
        output_file = Path(__file__).parent.parent / "data_analysis_output.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(all_data, f, indent=2, default=str)
        print("=" * 80)
        print(f"Full data saved to: {output_file}")
        print("=" * 80)

        # Summary
        print()
        print("=" * 80)
        print("DATA STRUCTURE SUMMARY")
        print("=" * 80)
        print(f"Total Accounts Analyzed: {len(all_data)}")
        total_holdings = sum(len(data["holdings"]) for data in all_data.values())
        print(f"Total Holdings: {total_holdings}")
        print()
        print("Key Findings:")
        print("- Check data_analysis_output.json for complete data structure")
        print("- Verify currency formats in holdings")
        print("- Check contract_code format for TradingView symbol mapping")
        print("- Review ISIN codes for symbol lookup")
        print("=" * 80)

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(analyze_data())
