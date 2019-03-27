def calculate_page_interest(page):
    max_length = page.max_content_length
    page_length = len(page.content)

    original_interest = (page_length * 1.0) / (max_length * 1.0)
    if page.theme_staying_time == 0:
        return original_interest
    else:
        actual_interest = original_interest * (1.0 - page.content_closeness)
        return actual_interest
