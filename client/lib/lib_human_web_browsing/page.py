class Page:
    max_content_length = 0

    def __init__(self, title, content, height, util_wrapper):
        self.title = title
        self.content = content
        self.height = height

        # calculate the interest in current theme
        self.interest_in_theme = util_wrapper.get_theme_interest_level()

        # calculate the content closeness with previous page
        self.content_closeness = util_wrapper.calculate_content_similarity(self.content)

        # record the max length of web page
        if Page.max_content_length < len(self.content):
            Page.max_content_length = len(self.content)

        # calculate the page interest
        self.interest_in_page = util_wrapper.calculate_interest_in_page(self)

        # calculate staying time for current page
        # among all content in a page, around 10% of them will be really useful information
        self.staying_time = int(util_wrapper.calculate_staying_time(self.interest_in_page,
                                                                    self.interest_in_theme,
                                                                    self.max_content_length))
