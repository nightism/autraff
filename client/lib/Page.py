from util.util_human_web_browsing.sentence_smilarity import sentence_similarity


class Page:
    def __init__(self, title, content):
        self.title = title
        self.content = content

    def calculate_theme_closeness(self, another_title):
        result = sentence_similarity(self.title, another_title)
        return result

    def calculate_content_closeness(self, another_content):
        # TODO
        result = sentence_similarity(self.content, another_content)
        return result


