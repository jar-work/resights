class EdgeInformation:
    def __init__(self, share):
        self.lower_ownership = 0
        self.middle_ownership = 0
        self.upper_ownership = 0
        self.__calculate_share_values(share)

    def __calculate_share_values(self, share):
        value = share.replace('%', '')

        if '-' in value:
            start, end = map(float, value.split('-'))
            start /= 100
            end /= 100
            average = (start + end) / 2
            self.lower_ownership = start
            self.middle_ownership = average
            self.upper_ownership = end
            return
        if '<' in value:
            value = float(value.replace('<', ''))
            value /= 100
            self.lower_ownership = 0
            self.middle_ownership = value/2
            self.upper_ownership = value
            return

        value = float(value)/100
        self.lower_ownership = value
        self.middle_ownership = value
        self.upper_ownership = value

    def get_ownership_value(self):
        return EdgeInformation.calculate_ownership_value(self.lower_ownership, self.middle_ownership, self.upper_ownership)

    @staticmethod
    def calculate_ownership_value(lower_ownership, middle_ownership, upper_ownership):
        def format_percentage(value):
            if value <= 10:
                return f"{value:.2f}"
            return f"{value:.0f}"

        # if the three ownership values are equal, return the exact percentage
        if lower_ownership == middle_ownership and middle_ownership == upper_ownership:
            return f"{format_percentage(middle_ownership * 100)}%"

        # if the lower_ownership is zero, return the upper_ownership percentage as <
        if lower_ownership == 0:
            return f"<{format_percentage(upper_ownership * 100)}%"

        # return the range between lower_ownership and upper_ownership
        return f"{format_percentage(lower_ownership * 100)}-{format_percentage(upper_ownership * 100)}%"
