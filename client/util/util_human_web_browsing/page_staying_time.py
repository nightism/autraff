import random


def calculate_page_staying_time(page_interest, theme_interest, max_content_length):
    # On average people's reading speed is between 200 to 300 words per minutes
    scanning_speed = random.randint(200, 301)

    # We will convert the time from minutes to seconds
    scan_whole_content = (max_content_length * 1.0) / (scanning_speed * 1.0) * 60.0
    actual_scanning_time = scan_whole_content * page_interest * theme_interest

    return int(actual_scanning_time)
