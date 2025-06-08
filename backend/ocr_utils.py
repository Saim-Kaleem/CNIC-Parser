import easyocr
import re
import difflib
from datetime import datetime

reader = easyocr.Reader(['en'])

# ---------- Configurable Match Rules ----------
FIELD_RULES = {
    'name': ['name', 'nam'],
    'father_name': ['father name', 'father', 'fathe', 'fath', 'fat'],
    'husband_name': ['husband name', 'husband', 'husb', 'hus'],
    'gender': ['gender', 'gend', 'gen'],
    'country': ['country of stay', 'country', 'stay'],
}

# ---------- Utility Functions ----------
def fuzzy_match(text, keywords, threshold=0.6):
    for keyword in keywords:
        if text.lower().startswith(keyword):
            return True
        if difflib.SequenceMatcher(None, text.lower(), keyword).ratio() > threshold:
            return True
    return False

def find_next_ocr_item(ocr_results, index):
    if index + 1 < len(ocr_results):
        bbox, text, confidence = ocr_results[index + 1]
        return {
            'value': text.strip(),
            'bbox': bbox,
            'confidence': confidence
        }
    return None

def find_after_keyword(ocr_results, keywords, valid_fn):
    for i, (bbox, text, confidence) in enumerate(ocr_results):
        if fuzzy_match(text, keywords):
            for j in range(i + 1, len(ocr_results)):
                next_bbox, next_text, next_confidence = ocr_results[j]
                if valid_fn(next_text.strip()):
                    return {
                        'value': next_text.strip(),
                        'bbox': next_bbox,
                        'confidence': next_confidence
                    }
    return None

def extract_cnic(ocr_results):
    for bbox, text, confidence in ocr_results:
        match = re.search(r'\d{5}-\d{7}-\d', text)
        if match:
            return {
                'value': match.group(),
                'bbox': bbox,
                'confidence': confidence
            }
    return None

def extract_dates(ocr_results):
    date_items = []
    
    # finding all date-like items
    for bbox, text, confidence in ocr_results:
        date_matches = re.findall(r'\d{2}[.,/-]\d{2}[.,/-]\d{4}', text)
        for date_match in date_matches:
            try:
                normalized = date_match.replace(',', '.').replace('/', '.')
                dt = datetime.strptime(normalized, "%d.%m.%Y")
                date_items.append({
                    'datetime': dt,
                    'value': normalized,
                    'bbox': bbox,
                    'confidence': confidence
                })
            except:
                continue
    
    # Sort by datetime
    date_items.sort(key=lambda x: x['datetime'])
    
    result = {
        "date_of_birth": None,
        "date_of_issue": None,
        "date_of_expiry": None
    }
    
    if len(date_items) == 3:
        result["date_of_birth"] = {
            'value': date_items[0]['value'],
            'bbox': date_items[0]['bbox'],
            'confidence': date_items[0]['confidence']
        }
        result["date_of_issue"] = {
            'value': date_items[1]['value'],
            'bbox': date_items[1]['bbox'],
            'confidence': date_items[1]['confidence']
        }
        result["date_of_expiry"] = {
            'value': date_items[2]['value'],
            'bbox': date_items[2]['bbox'],
            'confidence': date_items[2]['confidence']
        }
    
    elif len(date_items) == 2:
        d1, d2 = date_items
        delta = abs((d2['datetime'] - d1['datetime']).days)
        if 3640 <= delta <= 3660:  # ~10 years
            dob = min(date_items, key=lambda x: x['datetime'])
            doi = max(date_items, key=lambda x: x['datetime'])
            
            result["date_of_birth"] = {
                'value': dob['value'],
                'bbox': dob['bbox'],
                'confidence': dob['confidence']
            }
            result["date_of_issue"] = {
                'value': doi['value'],
                'bbox': doi['bbox'],
                'confidence': doi['confidence']
            }
            # calculate expiry (no bbox/confidence as it's calculated)
            expiry_date = doi['datetime'].replace(year=doi['datetime'].year + 10)
            result["date_of_expiry"] = {
                'value': expiry_date.strftime("%d.%m.%Y"),
                'confidence': None
            }
    
    elif len(date_items) == 1:
        dob = date_items[0]
        result["date_of_birth"] = {
            'value': dob['value'],
            'bbox': dob['bbox'],
            'confidence': dob['confidence']
        }
        
        # calculate issue and expiry dates (no bbox/confidence as they're calculated)
        doi_date = dob['datetime'].replace(year=dob['datetime'].year + 18)
        expiry_date = dob['datetime'].replace(year=dob['datetime'].year + 28)
        
        result["date_of_issue"] = {
            'value': doi_date.strftime("%d.%m.%Y"),
            'bbox': None,
            'confidence': None
        }
        result["date_of_expiry"] = {
            'value': expiry_date.strftime("%d.%m.%Y"),
            'bbox': None,
            'confidence': None
        }
    
    return result

# ---------- Main Processing ----------
def process_image(image_path):
    ocr_results = reader.readtext(image_path, detail=1)
    ocr_results = [(bbox, text.strip(), conf) for bbox, text, conf in ocr_results if text.strip()]

    result = {
        "name": None,
        "father_name": None,
        "husband_name": None,
        "gender": None,
        "country": None,
        "cnic_number": None,
        "date_of_birth": None,
        "date_of_issue": None,
        "date_of_expiry": None
    }

    # 1) Name
    for i, (bbox, text, conf) in enumerate(ocr_results):
        if fuzzy_match(text, FIELD_RULES['name']):
            name_item = find_next_ocr_item(ocr_results, i)
            if name_item:
                result['name'] = name_item
            break

    # 2) Father or Husband Name
    for i, (bbox, text, conf) in enumerate(ocr_results):
        if fuzzy_match(text, FIELD_RULES['father_name']):
            father_item = find_next_ocr_item(ocr_results, i)
            if father_item:
                result['father_name'] = father_item
                # delete husband name key if father name is found
                result.pop('husband_name', None)
            break
        if fuzzy_match(text, FIELD_RULES['husband_name']):
            husband_item = find_next_ocr_item(ocr_results, i)
            if husband_item:
                result['husband_name'] = husband_item
                # delete father name key if husband name is found
                result.pop('father_name', None)
            break

    # 3) Gender: scan after keyword
    gender_item = find_after_keyword(ocr_results, FIELD_RULES['gender'], lambda x: x.strip().upper() in ['M', 'F', 'MALE', 'FEMALE'])
    if gender_item:
        gender_val = gender_item['value'].upper()
        if 'F' in gender_val or result.get('husband_name'):
            gender_item['value'] = 'Female'
        else:
            gender_item['value'] = 'Male'
        result['gender'] = gender_item
    else:
        # infer from husband name presence
        if result.get('husband_name'):
            result['gender'] = {
                'value': 'Female',
                'bbox': None,
                'confidence': None
            }
        else:
            result['gender'] = {
                'value': 'Male',
                'bbox': None,
                'confidence': None
            }

    # 4) Country of Stay
    country_item = find_after_keyword(ocr_results, FIELD_RULES['country'], lambda x: len(x.strip()) > 2)
    if country_item:
        result['country'] = country_item

    # 5) CNIC Number
    cnic_item = extract_cnic(ocr_results)
    if cnic_item:
        result['cnic_number'] = cnic_item

    # 6) Dates
    date_items = extract_dates(ocr_results)
    result.update(date_items)

    return result

def print_formatted_result(result):
    """Print the result in a nicely formatted way"""
    print("\n📦 Extracted Information with OCR Details:")
    print("=" * 60)
    
    for key, value in result.items():
        if value is None:
            print(f"{key.replace('_', ' ').title()}: Not found")
        else:
            print(f"\n{key.replace('_', ' ').title()}:")
            print(f"  Value: {value['value']}")
            print(f"  Confidence: {value['confidence']:.4f}" if value['confidence'] else "  Confidence: N/A (calculated)")
            if value['bbox']:
                # Format bbox coordinates nicely
                coords = value['bbox']
                print(f"  Bounding Box: Top-left({coords[0][0]}, {coords[0][1]}), Bottom-right({coords[2][0]}, {coords[2][1]})")
            else:
                print("  Bounding Box: N/A (calculated)")

def convert_numpy_to_native(obj):
    """Recursively convert numpy types to native Python types."""
    if isinstance(obj, dict):
        return {k: convert_numpy_to_native(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_to_native(v) for v in obj]
    elif hasattr(obj, "item"):  # For numpy.int32, numpy.float64, etc.
        return obj.item()
    else:
        return obj

# ---------- Run ----------
if __name__ == "__main__":
    img_path = "test2.jpg"  # replace as needed
    output = process_image(img_path)
    
    # Print formatted output
    print_formatted_result(output)
    
    # Also print raw JSON for programmatic use
    print("\n" + "="*60)
    print("📝 Raw JSON Output:")
    import json
    print(json.dumps(output, indent=2, default=str))
