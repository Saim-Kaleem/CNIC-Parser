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
def fuzzy_match(line, keywords, threshold=0.6):
    for keyword in keywords:
        if line.lower().startswith(keyword):
            return True
        if difflib.SequenceMatcher(None, line.lower(), keyword).ratio() > threshold:
            return True
    return False

def find_next_text(lines, index):
    return lines[index + 1].strip() if index + 1 < len(lines) else None

def find_after_keyword(lines, keywords, valid_fn):
    for i, line in enumerate(lines):
        if fuzzy_match(line, keywords):
            for next_line in lines[i+1:]:
                text = next_line.strip()
                if valid_fn(text):
                    return text
    return ''

def extract_cnic(text):
    match = re.search(r'\d{5}-\d{7}-\d', text)
    return match.group() if match else None

def extract_dates(text):
    raw_dates = re.findall(r'\d{2}[.,/-]\d{2}[.,/-]\d{4}', text)
    parsed_dates = []
    for date in raw_dates:
        try:
            normalized = date.replace(',', '.').replace('/', '.')
            dt = datetime.strptime(normalized, "%d.%m.%Y")
            parsed_dates.append((dt, normalized))
        except:
            continue

    if len(parsed_dates) == 3:
        parsed_dates.sort()
        return {
            "date_of_birth": parsed_dates[0][1],
            "date_of_issue": parsed_dates[1][1],
            "date_of_expiry": parsed_dates[2][1]
        }

    # Intelligent guess if < 3 dates
    if len(parsed_dates) == 2:
        d1, d2 = parsed_dates
        delta = abs((d2[0] - d1[0]).days)
        if 3640 <= delta <= 3660:  # ~10 years
            dob = min(d1, d2)
            doi = max(d1, d2)
            return {
                "date_of_birth": dob[1],
                "date_of_issue": doi[1],
                "date_of_expiry": (doi[0].replace(year=doi[0].year + 10)).strftime("%d.%m.%Y")
            }

    if len(parsed_dates) == 1:
        dob = parsed_dates[0]
        doi = dob[0].replace(year=dob[0].year + 20)
        return {
            "date_of_birth": dob[1],
            "date_of_issue": (dob[0].replace(year=dob[0].year + 10)).strftime("%d.%m.%Y"),
            "date_of_expiry": doi.strftime("%d.%m.%Y")
        }

    return {
        "date_of_birth": None,
        "date_of_issue": None,
        "date_of_expiry": None
    }

# ---------- Main Processing ----------
def process_image(image_path):
    lines = reader.readtext(image_path, detail=0)
    lines = [line.strip() for line in lines if line.strip()]
    joined_text = "\n".join(lines)

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
    for i, line in enumerate(lines):
        if fuzzy_match(line, FIELD_RULES['name']):
            result['name'] = find_next_text(lines, i)
            break

    # 2) Father or Husband Name
    for i, line in enumerate(lines):
        if fuzzy_match(line, FIELD_RULES['father_name']):
            result['father_name'] = find_next_text(lines, i)
            # delete husband name key if father name is found
            result.pop('husband_name', None)
            break
        if fuzzy_match(line, FIELD_RULES['husband_name']):
            result['husband_name'] = find_next_text(lines, i)
            # delete father name key if husband name is found
            result.pop('father_name', None)
            break

    # 3) Gender: scan after keyword
    gender = find_after_keyword(lines, FIELD_RULES['gender'], lambda x: x.strip().upper() in ['M', 'F', 'MALE', 'FEMALE'])
    if 'F' in gender.upper() or result.get('husband_name'):
        result['gender'] = 'Female'
    else:
        result['gender'] = 'Male'

    # 4) Country of Stay
    country = find_after_keyword(lines, FIELD_RULES['country'], lambda x: len(x.strip()) > 2)
    if country != '':
        result['country'] = country

    # 5) CNIC Number
    cnic = extract_cnic(joined_text)
    if cnic:
        result['cnic_number'] = cnic

    # 6) Dates
    result.update(extract_dates(joined_text))

    return result

# ---------- Run ----------
if __name__ == "__main__":
    img_path = "EgR6CvyVoAA5HEM.jpg"  # replace as needed
    output = process_image(img_path)
    print("\n📦 Extracted JSON:")
    print(output)
