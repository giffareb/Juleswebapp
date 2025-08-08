import crc

def generate_payload(phone_number: str, amount: float = 0.0) -> str:
    """
    Generates a PromptPay payload string for QR code generation,
    following the EMVCo Merchant-Presented QR Code standard for Tag 30.
    """
    # Helper to format TLV (Tag-Length-Value)
    def f(id, value):
        return str(id) + str(len(value)).zfill(2) + str(value)

    # Static fields
    payload_format_indicator = f("00", "01")
    point_of_initiation_method = f("01", "11") # "11" for static QR, "12" for dynamic. Using static for simplicity.

    # Merchant Account Information (for PromptPay)
    promptpay_guid = "A000000677010111"
    merchant_guid = f("00", promptpay_guid)

    # Format phone number: country code (66) + phone number without leading zero
    if phone_number.startswith("0"):
        phone_number = "66" + phone_number[1:]

    # Pad with zeros if less than 13 chars, though Thai mobile numbers are standard.
    formatted_phone = phone_number.zfill(13)
    merchant_phone = f("01", formatted_phone)

    merchant_account_info = f("30", merchant_guid + merchant_phone)

    # Transaction details
    transaction_currency = f("53", "764") # 764 for THB
    country_code = f("58", "TH")

    # Amount - This should be part of the payload if provided
    payload_parts = [
        payload_format_indicator,
        point_of_initiation_method,
        merchant_account_info,
        transaction_currency,
    ]

    if amount > 0:
        # Format amount to two decimal places, up to 13 characters total
        formatted_amount = f"{amount:.2f}"
        transaction_amount = f("54", formatted_amount)
        payload_parts.append(transaction_amount)

    payload_parts.append(country_code)

    # Build the initial payload for CRC calculation
    payload_to_crc = "".join(payload_parts) + "6304"

    # Calculate CRC
    crc_value = crc.crc16.ccitt_false(payload_to_crc.encode("ascii"))
    crc_hex = f"{crc_value:04X}"

    # Final payload
    final_payload = payload_to_crc + crc_hex

    return final_payload

# Example usage:
if __name__ == "__main__":
    phone = "0917797477"
    amount = 59.50
    payload = generate_payload(phone, amount)
    print(f"Generated Payload: {payload}")
    # Expected: 00020101021130320016A000000677010111011300669177974775303764540559.505802TH6304XXXX (CRC will vary)

    # Verify CRC
    data_to_check = payload[:-4]
    expected_crc_val = int(payload[-4:], 16)
    calculated_crc_val = crc.crc16.ccitt_false(data_to_check.encode('ascii'))
    print(f"Is CRC correct? {expected_crc_val == calculated_crc_val}")
    print(f"Calculated CRC: {calculated_crc_val:04X}")
