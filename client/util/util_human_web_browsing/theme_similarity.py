from util.util_human_web_browsing.content_smilarity import calculate_content_similarity


def calculate_theme_similarity(cont1, cont2):
    if cont1 is None or cont2 is None:
        return 0
    elif cont1 == "" or cont2 == "":
        return 0

    cont1 = cont1.strip()
    cont2 = cont2.strip()
    return calculate_content_similarity(cont1, cont2)
