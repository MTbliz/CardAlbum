from src.card.card_repository import CardRepository
import requests
from bs4 import BeautifulSoup
from src.common.string_operations import concatenate_words_in_string, capitalize_string, remove_special_characters


class CardService:

    def __init__(self):
        self.card_repository = CardRepository()

    def get_cards(self, field_sort, order, filters, page, ROWS_PER_PAGE):
        return self.card_repository.get_cards(field_sort, order, filters, page, ROWS_PER_PAGE)

    def get_card(self, card_id):
        return self.card_repository.get_card(card_id)

    def add_card(self, card):
        return self.card_repository.add_card(card)

    def delete_card(self, card_id):
        return self.card_repository.delete_card(card_id)

    def get_card_details_from_url(self, base_link, mtg_set, title):
        suffix = "#paper"

        mtg_set = remove_special_characters(mtg_set)
        mtg_set = capitalize_string(mtg_set)
        mtg_set = concatenate_words_in_string(mtg_set)

        title = remove_special_characters(title)
        title = capitalize_string(title)
        title = concatenate_words_in_string(title)

        final_link = f"{base_link}/{mtg_set}/{title}/{suffix}"
        res = requests.get(final_link)
        result = {'status_code': res.status_code,
                  'body': {}}
        if result['status_code'] == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            price_card_gatherer = soup.find(class_='price-card-gatherer')
            gatherer_container = price_card_gatherer.find(class_='gatherer-container')
            mana_cost_tag = gatherer_container.find(class_='gatherer-name').find(class_='manacost')
            mana_cost = mana_cost_tag.attrs['aria-label'].split('mana cost: ')[1]
            type_tag = gatherer_container.find(class_='collapse').find(class_='gatherer-type')
            type = type_tag.text
            rarity_tag = gatherer_container \
                .find(class_='collapse') \
                .find(class_='gatherer-type-power') \
                .find(class_='gatherer-rarity')
            rarity = rarity_tag.text

            price_card_name_header = soup.find(class_='price-card-name-header')
            price_tag = price_card_name_header \
                .find(class_='price-card-current-prices'). \
                find(class_='price-box-price')
            price = price_tag.text.replace('$', '').strip()
            img_tag = price_card_gatherer \
                .find(class_='price-card-image').find(class_='price-card-image-image')
            img_url = img_tag.attrs['src']
            img_data = requests.get(img_url).content

            result['body'] = {
                'mana_cost': self._get_mana_cost_number(mana_cost),
                'color': self._get_card_color(mana_cost),
                'rarity': rarity,
                'type': remove_special_characters(type),
                'price': price,
                'img_data': img_data
            }
        return result

    def _get_mana_cost_number(self, mana_cost: str):
        colors_with_numbers = mana_cost.split(" ")
        mana_cost_number = 0
        for color_or_number in colors_with_numbers:
            if color_or_number.isnumeric():
                mana_cost_number += int(color_or_number)
            else:
                mana_cost_number += 1
        return  mana_cost_number

    def _get_card_color(self, mana_cost: str):
        colors_with_numbers = mana_cost.split(" ")
        colors = set()
        for color_or_number in colors_with_numbers:
            if not color_or_number.isnumeric():
                colors.add(color_or_number)
        if len(colors) > 0:
            return ','.join(colors)
        else:
            return 'colorless'



    def get_set_value_by_name(self, set_name):
        return self.card_repository.get_set_value_by_name(set_name)
