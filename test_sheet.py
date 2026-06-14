import asyncio
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import Settings
from app.services.google_sheet_service import GoogleSheetService

async def test_sheet_read():
    try:
        settings = Settings()
        sheet_service = GoogleSheetService(settings)
        
        print("Testing Google Sheets connection...")
        rows = await sheet_service.fetch_pending_rows()
        print(f"✅ Successfully read {len(rows)} pending rows")
        for row in rows:
            print(f"  Row {row['row_number']}: {row['input_one']} | {row['input_two']} | Status: {row['status']}")
        
        print("\nTesting sheet update...")
        await sheet_service.update_row(2, "Test Content from API", "Completed")
        print("✅ Successfully updated row 2 (column D and E)")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_sheet_read())
