import re

patterns = (
    r'\"',
    r'\'',
    r'\#',
    r'{.*?}',
    r'\%\(.*?\)s',
    r'%\(.*?\)d',
    r'%s',
    r'%d',
)


class Translatable:
    stub_char = "S"

    def __init__(self, msgid, occurrences):
        self.occurrences = occurrences
        self.original_msgid = msgid
        self. preservable = {}
        self.counter = 0
        self.new_msgid = self.omit_preservable_from_msgid()

    def omit_preservable_from_msgid(self):
        new_msgid = self.original_msgid
        for pattern in patterns:
            match_list = re.findall(pattern, new_msgid)
            for match in match_list:
                self.counter += 1
                stub = "{stub_char}{count}".format(
                    stub_char=self.stub_char,
                    count=self.counter
                )
                new_msgid = new_msgid.replace(match, stub)
                self.preservable[stub] = match

        return new_msgid

    def construct_translated_msgid(self, translated_msgid):
        new_translated_msgid = translated_msgid
        for key, val in self.preservable.items():
            new_translated_msgid = new_translated_msgid.replace(key, val.decode().encode('utf-8'))

        return new_translated_msgid
