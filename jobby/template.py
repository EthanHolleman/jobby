from pathlib import Path
import re
from jobby import TEMPLATES_PATH

# args are just going to be tuples


class Template():
    sbatch_regex = re.compile(r'#SBATCH (.*)')
    field_regex = re.compile(r'(\S*)[=\s]{{(\S*)}}')

    def __init__(self, path):
        self.path = Path(path)
    
    def copy_jobby(self):
        jobby_path = TEMPLATES_PATH.with_name(self.path.name)
        with open(str(jobby_path), 'w') as handle:
            handle.write(self.text)
        
    @property
    def text(self):
        with open(str(self.path)) as handle:
            return handle.read()

    @property
    def sbatch_args(self):
        collected_args = []
        sbatch_args = Template.sbatch_regex.findall(self.text)
        for match in sbatch_args:
            match = match.split('#')[0]  # remove comments
            collected_args.append(
                tuple(match.split('='))
            )
        return collected_args
    
    @property
    def fields(self):
        matches = Template.field_regex.finditer(self.text)
        return matches
    
    def fill(self, filled_fields, keyword_dict={}):
        filled_text = self.text
        for arg, value in filled_fields:
            field_re = re.compile(f'({arg})[=\s]{{(\S*)}}')
            match = field_re.search(filled_text)
            if match:
                s, e = match.span(2)
                filled_text = filled_text[:s-1] + value + filled_text[e+1:]
        
        filled_text = self._process_keywords(filled_text, keyword_dict)

        return filled_text

    def _process_keywords(self, text, keyword_dict):
        temp_text = text 
        for keyword, replace_str in keyword_dict.items():
            keyword_regex = re.compile(f'{keyword}')
            temp_text = keyword_regex.sub(str(replace_str), temp_text)
        return temp_text











