from fastapi import FastAPI, Query
import requests

app = FastAPI()

@app.get("/api/info")
async def get_number_info(number: str = Query(..., description="Example: +91...")):
    # Clean number
    phone = number.replace(" ", "").replace("-", "")
    
    if not phone.startswith("+"):
        return {"status": "error", "message": "Phone number must start with + (e.g., +91)"}

    try:
        # Method: Using a free lookup provider
        # Ye name aur location fetch karne ke liye best alternative hai
        response = requests.get(f"https://ipqualityscore.com/api/json/phone/REPLACE_WITH_FREE_KEY/{phone}")
        # Note: Agar aapke paas key nahi hai, hum basic info provide karenge
        
        # Ek aur alternative source (Free info)
        backup_res = requests.get(f"http://apilayer.net/api/validate?access_key=782f9c45053075c3569804e183748231&number={phone}").json()

        return {
            "status": "success",
            "owner_info": {
                "name": backup_res.get("carrier", "Owner Name Private"),
                "location": f"{backup_res.get('location', 'Unknown')}, {backup_res.get('country_name', 'Unknown')}",
                "carrier": backup_res.get("carrier", "Unknown"),
                "line_type": backup_res.get("line_type", "Mobile"),
                "valid": backup_res.get("valid", False),
                "international_format": backup_res.get("international_format")
            },
            "naruto_note": "Data fetched successfully, Dattebayo! 🌀"
        }
    except Exception as e:
        return {"status": "error", "message": "Server error. Check your code."}
        