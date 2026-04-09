from fastapi import FastAPI, Query
import phonenumbers
from phonenumbers import geocoder, carrier, timezone

app = FastAPI()

@app.get("/api/number")
async def get_number_info(phone: str = Query(..., description="Phone number with country code, e.g., +91...")):
    try:
        # Parse the number
        parsed_number = phonenumbers.parse(phone)
        
        # Validating number
        is_valid = phonenumbers.is_valid_number(parsed_number)
        
        if not is_valid:
            return {"status": "error", "message": "Invalid phone number format"}

        # Fetching Information
        location = geocoder.description_for_number(parsed_number, "en")
        service_provider = carrier.name_for_number(parsed_number, "en")
        time_zones = timezone.time_zones_for_number(parsed_number)

        return {
            "status": "success",
            "number": phone,
            "info": {
                "valid": is_valid,
                "location": location or "Unknown",
                "carrier": service_provider or "Unknown",
                "timezone": time_zones,
                "country_code": parsed_number.country_code,
                "national_number": parsed_number.national_number,
                "international_format": phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            },
            "note": "For 'Name' lookup, integrate a Truecaller/Numverify API key."
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
        