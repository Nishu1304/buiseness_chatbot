from apps.common.constants import MAIN_MENU_TEXT

def get_welcome_message(client):
    return MAIN_MENU_TEXT.format(business_name=client.name)
