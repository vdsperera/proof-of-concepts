import re
import json

def parse_edi_835(raw_edi: str):
    """
    Parses a raw EDI 835 string and extracts key healthcare payment information.
    """
    # 1. Clean up the raw string (ensure consistent segment terminator)
    raw_edi = raw_edi.replace('\n', '').strip()
    segments = raw_edi.split('~')
    
    extraction_results = {
        "patient_name": "Not Found",
        "total_payment": "0.00",
        "denial_reasons": []
    }

    # 2. Define Regex Patterns
    # Patient Name: NM1*QC*1*LAST*FIRST*...
    # Group 1: Last Name, Group 2: First Name
    patient_pattern = re.compile(r"NM1\*QC\*1\*([^*]+)\*([^*]+)")
    
    # Total Payment: CLP*ClaimID*Status*TotalCharge*TotalPayment*...
    # Group 1: Total Payment (Element 4)
    payment_pattern = re.compile(r"CLP\*[^*]+\*[^*]+\*[^*]+\*([^*]+)")
    
    # Denial Reason: CAS*GroupCode*ReasonCode*Amount
    # Group 1: Reason Code
    denial_pattern = re.compile(r"CAS\*[^*]+\*([^*]+)")

    # 3. Process Segments
    for segment in segments:
        segment = segment.strip()
        if not segment:
            continue

        # Extract Patient Name
        if segment.startswith("NM1*QC"):
            match = patient_pattern.search(segment)
            if match:
                extraction_results["patient_name"] = f"{match.group(2)} {match.group(1)}"

        # Extract Total Payment
        elif segment.startswith("CLP"):
            match = payment_pattern.search(segment)
            if match:
                extraction_results["total_payment"] = match.group(1)

        # Extract Denial/Adjustment Reasons
        elif segment.startswith("CAS"):
            match = denial_pattern.search(segment)
            if match:
                extraction_results["denial_reasons"].append(match.group(1))

    return extraction_results

if __name__ == "__main__":
    # Mock EDI 835 Raw Message
    mock_edi_835 = (
        "ISA*00*          *00*          *ZZ*SENDERID       *ZZ*RECEIVERID     *210101*1200*^*00501*000000001*0*P*:~"
        "NM1*QC*1*DOE*JOHN*M***MI*123456789~"
        "CLP*CLAIM123*1*150.00*112.50**MC*0123456789~"
        "CAS*PR*1*37.50~"
        "CAS*CO*45*10.00~"
        "NM1*QC*1*SMITH*JANE*A***MI*987654321~"
        "CLP*CLAIM456*1*200.00*0.00**MC*987654321~"
        "CAS*OA*18*200.00~"
    )

    print("--- Raw EDI 835 Message ---")
    print(mock_edi_835)
    print("\n--- Parsed JSON Output ---")
    
    # For a multi-claim file, we might want to loop via CLP segments, 
    # but for this POC we'll process it and return the last/aggregated data
    # or improve the parser to return a list of claims.
    
    # Let's improve the parser to handle multiple claims (multiple CLP segments)
    
    def parse_multiple_claims(raw_edi):
        raw_edi = raw_edi.replace('\n', '').strip()
        segments = raw_edi.split('~')
        
        claims = []
        current_claim = None
        current_patient = "Unknown"

        for segment in segments:
            segment = segment.strip()
            if not segment: continue

            if segment.startswith("NM1*QC"):
                match = re.search(r"NM1\*QC\*1\*([^*]+)\*([^*]+)", segment)
                if match:
                    current_patient = f"{match.group(2)} {match.group(1)}"

            if segment.startswith("CLP"):
                if current_claim:
                    claims.append(current_claim)
                
                match = re.search(r"CLP\*[^*]+\*[^*]+\*[^*]+\*([^*]+)", segment)
                payment = match.group(1) if match else "0.00"
                
                current_claim = {
                    "patient_name": current_patient,
                    "total_payment": payment,
                    "denial_reasons": []
                }

            if segment.startswith("CAS") and current_claim:
                match = re.search(r"CAS\*[^*]+\*([^*]+)", segment)
                if match:
                    current_claim["denial_reasons"].append(match.group(1))
        
        if current_claim:
            claims.append(current_claim)
            
        return claims

    results = parse_multiple_claims(mock_edi_835)
    print(json.dumps(results, indent=4))
