import re

def fix_encoding_artifacts(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Common UTF-8 artifacts when read/written incorrectly under cp1252
    replacements = {
        'â‚¹': '₹',      # Rupee
        'â˜…': '★',      # Star
        'â€”': '—',      # Em dash
        'â†’': '→',      # Right arrow
        'Â·': '·',       # Middle dot
    }

    for artifact, correct in replacements.items():
        content = content.replace(artifact, correct)

    # Ensure all money is displayed in Rupees (if there's a standalone $)
    content = content.replace('$', '₹')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

fix_encoding_artifacts('ScoreShield.html')
