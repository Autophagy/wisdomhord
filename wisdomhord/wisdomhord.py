import os.path
import re

def hladan(file_path):
    return wisdomhord(file_path)

class wisdomhord(object):

    meta = {}
    keys = []
    _key_row = 0
    _column_lengths = {}

    row_regex = '\[ (.*?)\ ]'

    def __new__(self, file_path):
        self = object.__new__(self)

        if os.path.isfile(file_path):
            self.file_path = file_path
            self.open_hord()
            return self
        else:
            raise ValueError("{} does not exist".format(file_path))

    def open_hord(self):
        with open(self.file_path) as hord:
            for line_index, line in enumerate(hord):
                if line[:2] == '//':
                    self._add_to_meta(line[2:])
                if line[0] == '[':
                    self._add_to_keys(line)
                    self._key_row = line_index
                    break

    def _add_to_meta(self, line):
        values = line.split('::', 1)
        self.meta[values[0].strip()] = values[1].strip()

    def _add_to_keys(self, line):
        keys_definition = re.search(self.row_regex, line).group(1)
        for key in keys_definition.split(' | '):
            stripped_key = key.strip().upper()
            self._column_lengths[stripped_key] = len(key)
            self.keys.append(stripped_key)
