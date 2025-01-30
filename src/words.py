from dataclasses import dataclass
import unicodedata
import re

@dataclass
class Word:
    value: str

    def __post_init__(self):
        self.value = self.value.strip().lower()
        
        self.value = unicodedata.normalize('NFKD', self.value) \
            .encode('ASCII', 'ignore') \
            .decode('ASCII')
        
        self.value = re.sub(r'\s+', ' ', self.value)
