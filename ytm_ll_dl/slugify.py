import unicodedata
import re

def slugify(value, allow_unicode=True):
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')

    value = re.sub(r'~', '-', value)
    value = re.sub(r'/', '-', value)
    value = re.sub(r'\'', '', value)
    value = re.sub(r'\"', '', value)
    value = re.sub(r'`', '', value)

    return value