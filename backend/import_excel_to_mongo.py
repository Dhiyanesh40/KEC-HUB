import pandas as pd
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def import_excel_to_mongo():
    """Import data from Excel file to MongoDB"""
    
    # Get MongoDB connection string from environment
    mongo_uri = os.getenv('MONGODB_URI')
    if not mongo_uri:
        print("Error: MONGODB_URI not found in environment variables")
        return
    
    # Read Excel file
    excel_path = 'E:/KEC-HUB/KEC_Students_Email_List.xlsx'
    print(f"Reading Excel file: {excel_path}")
    
    try:
        # Read all sheets from Excel
        excel_file = pd.ExcelFile(excel_path)
        print(f"Found {len(excel_file.sheet_names)} sheet(s): {excel_file.sheet_names}")
        
        # Connect to MongoDB
        client = AsyncIOMotorClient(mongo_uri)
        db = client.kec_hub  # Database name
        
        # Process each sheet
        for sheet_name in excel_file.sheet_names:
            print(f"\nProcessing sheet: {sheet_name}")
            df = pd.read_excel(excel_path, sheet_name=sheet_name, header=0)
            
            # Clean column names - convert all to strings and strip whitespace
            df.columns = [str(col).strip() for col in df.columns]
            
            # Display sheet info
            print(f"  Rows: {len(df)}, Columns: {len(df.columns)}")
            print(f"  Columns: {list(df.columns)}")
            
            # Show first few rows
            print(f"\n  First few rows:")
            print(df.head().to_string(index=False))
            
            # Convert DataFrame to list of dictionaries
            # Replace NaN values with None for MongoDB
            data = df.where(pd.notna(df), None).to_dict('records')
            
            if not data:
                print(f"  No data in sheet {sheet_name}, skipping...")
                continue
            
            # Use sheet name as collection name (sanitize it)
            collection_name = sheet_name.lower().replace(' ', '_').replace('-', '_')
            collection = db[collection_name]
            
            # Ask user for confirmation
            print(f"\n  Ready to insert {len(data)} records into collection '{collection_name}'")
            print(f"  Sample data (first record):")
            for key, value in list(data[0].items())[:5]:  # Show first 5 fields
                print(f"    {key}: {value}")
            
            # Insert data
            result = await collection.insert_many(data)
            print(f"  ✓ Inserted {len(result.inserted_ids)} documents into '{collection_name}'")
        
        print("\n✓ Import completed successfully!")
        
        # Close connection
        client.close()
        
    except FileNotFoundError:
        print(f"Error: Excel file not found at {excel_path}")
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(import_excel_to_mongo())
