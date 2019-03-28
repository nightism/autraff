import math

PHI_OF_VISUAL_EFFECT = 0.3
PHI_OF_CONTENT_EFFECT = 1 - PHI_OF_VISUAL_EFFECT


def get_all_clickable_links(driver):
    if driver is None:
        return []

    all_links = driver.find_elements_by_xpath('.//a')
    all_links = list(filter(lambda link: link.text is not None and link.text != "", all_links))

    return all_links


def calculate_link_theme_closeness_in_a_page(page, link):
    score = page.calculate_theme_closeness(link.text)

    return score


def calculate_link_visibility_closeness_in_a_page(page, link):
    page_height = page.height
    # page_width = page.width

    location = link.location
    # x = location['x']
    y = location['y']

    # How far is the x deviated from the middle
    # x_closeness = 1.0 - 0.2 * abs(x - (page_width / 2.0)) / (page_width / 2.0)

    # How far is the y deviated from the top
    # the larger y_closeness, the farther the link
    y_closeness = y / page_height

    actual_closeness = 0.5 - 0.5 * math.sin(math.pi * (y_closeness - 0.5))

    return actual_closeness


def calculate_link_possibility(page, all_links):
    possibility = []

    for index, link in enumerate(all_links):
        visual_effect = PHI_OF_VISUAL_EFFECT * calculate_link_visibility_closeness_in_a_page(page, link)
        theme_closeness = calculate_link_theme_closeness_in_a_page(page, link)
        theme_interest = page.interest_in_theme
        theme_effect = PHI_OF_CONTENT_EFFECT \
                       * (2 * theme_closeness * theme_interest / (theme_closeness ** 2 + theme_interest ** 2))

        effect = (theme_effect + visual_effect)

        if effect > 0.0000000001:
            possibility.append({
                'link': link,
                'possibility': effect
            })

    def take_possibility(link_dict):
        return link_dict['possibility']

    possibility.sort(key=take_possibility, reverse=True)

    return possibility
