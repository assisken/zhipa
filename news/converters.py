class FourDigitYearConverter:
    regex = r"[0-9]{4}"

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return "%04s" % value


class TwoDigitConverter:
    regex = r"[0-9]{2}"

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return "%02s" % value


class ActivateCodeConverter:
    regex = r"[-:\w]+"

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value
