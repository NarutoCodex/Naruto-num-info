from fastapi import FastAPI, Query
import requests

app = FastAPI()

@app.get("/api/info")
async def get_details(number: str = Query(..., description="Example: +91...")):
    # Format check
    if not number.startswith("+"):
        return {"status": "error", "message": "Please add '+' and Country Code (e.g. +91)"}

    # Method: Using a public aggregator (Example logic)
    # Note: Bina key ke internet par "Name" nikalne ki limit hoti hai
    try:
        # Hum ek free tool ki API use kar rahe hain
        url = f"https://api.veriphone.io/v1/verify?phone={number}&key=66D8C61E897A4C6FB60359779956A69E"
        response = requests.get(url).json()

        if response.get("status") == "success":
            return {
                "status": "success",
                "owner_info": {
                    "name": "Search on Truecaller for Name", # Bina login ke name nahi milta
                    "location": response.get("location", "Unknown"),
                    "carrier": response.get("carrier", "Unknown"),
                    "country": response.get("country", "Unknown"),
                    "phone_type": response.get("phone_type", "Mobile"),
                    "international_format": response.get("phone_international")
                },
                "extra": {
                    "naruto_status": "Data Fetched Dattebayo! 🌀",
                    "tip": "Owner name ke liye Truecaller Login use karein."
                }
            }
        else:
            return {"status": "error", "message": "Details not found."}

    except Exception as e:
        return {"status": "error", "message": "Server Busy or API Limit Exceeded."}
        