class FourDigitYearConverter:
    regex = '[0-9]{4}'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return '%04s' % value


class TwoDigitConverter:
    regex = '[0-9]{2}'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return '%02s' % value
