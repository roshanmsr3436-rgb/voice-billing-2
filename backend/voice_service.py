import re

def parse_voice_command(text, products_db):
    """
    Parses voice text like "ரெண்டு கிலோ ஆப்பிள்" into product and quantity.
    Returns list of parsed items.
    """
    text = text.lower()
    
    # Very basic numbers mapping (Tamil/Tanglish/English)
    numbers = {
        'ஒரு': 1, 'ஒன்னு': 1, 'oru': 1, 'onnu': 1, 'one': 1, '1': 1,
        'ரெண்டு': 2, 'rendu': 2, 'two': 2, '2': 2,
        'மூணு': 3, 'moonu': 3, 'three': 3, '3': 3,
        'நாலு': 4, 'naalu': 4, 'four': 4, '4': 4,
        'அஞ்சு': 5, 'anju': 5, 'five': 5, '5': 5,
        'ஆறு': 6, 'aaru': 6, 'six': 6, '6': 6,
        'ஏழு': 7, 'ezhu': 7, 'seven': 7, '7': 7,
        'எட்டு': 8, 'ettu': 8, 'eight': 8, '8': 8,
        'ஒன்பது': 9, 'onbadhu': 9, 'nine': 9, '9': 9,
        'பத்து': 10, 'pathu': 10, 'ten': 10, '10': 10,
        'அரை': 0.5, 'arai': 0.5, 'half': 0.5,
        'கால்': 0.25, 'kaal': 0.25, 'quarter': 0.25,
        'முக்கால்': 0.75, 'mukkal': 0.75,
        '500': 0.5, '250': 0.25, '100': 0.1, '200': 0.2
    }
    
    units = {
        'கிலோ': 'kg', 'kilo': 'kg', 'kg': 'kg', 'kilogram': 'kg',
        'கிராம்': 'gram', 'gram': 'gram', 'g': 'gram',
        'லிட்டர்': 'liter', 'liter': 'liter', 'litre': 'liter',
        'பாக்கெட்': 'packet', 'packet': 'packet',
        'பீஸ்': 'piece', 'piece': 'piece'
    }

    # Commands
    if 'bill podu' in text or 'generate bill' in text or 'checkout' in text:
        return {'command': 'checkout'}
    if 'clear cart' in text:
        return {'command': 'clear_cart'}
        
    found_items = []
    
    # Try to find products in the text
    for prod in products_db:
        aliases = [prod['name'].lower()] + prod.get('aliases', [])
        for alias in aliases:
            if alias and alias in text:
                # Find number near the product
                qty = 1 # default
                unit = prod['unit']
                
                # Check for quantities
                words = text.split()
                for i, word in enumerate(words):
                    if word in numbers:
                        val = numbers[word]
                        # check if next word is unit (e.g. 500 gram)
                        if i+1 < len(words) and words[i+1] in units:
                            unit_found = units[words[i+1]]
                            if unit_found == 'gram' and prod['unit'] == 'kg':
                                qty = val if val < 10 else val / 1000.0
                            else:
                                qty = val
                        else:
                            qty = val
                        break
                
                found_items.append({
                    'product_id': prod['id'],
                    'name': prod['name'],
                    'price': prod['price'],
                    'quantity': qty,
                    'unit': prod['unit']
                })
                # Remove matched alias to avoid double matching
                text = text.replace(alias, '')
                break

    return {'items': found_items}
