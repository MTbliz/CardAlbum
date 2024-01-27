import os
from typing import Optional

import requests
from bs4 import BeautifulSoup
from bs4 import Tag
from requests.models import Response

from src.card.cardDTO import CardDTO
from src.card.card_repository import CardRepository
from src.common.string_operations import concatenate_words_in_string, capitalize_string, remove_special_characters
from src.models import Card


class CardService:

    def __init__(self) -> None:
        self.card_repository: CardRepository = CardRepository()

    def get_cards(self, field_sort: str, order: str, filters: dict[str, str], page: int, ROWS_PER_PAGE: int):
        return self.card_repository.get_cards(field_sort, order, filters, page, ROWS_PER_PAGE)

    def get_card(self, card_id: int) -> Card:
        return self.card_repository.get_card(card_id)

    def get_card_by_title(self, title: str) -> Card:
        return self.card_repository.get_card_by_title(title)

    def add_card(self, card: Card) -> None:
        return self.card_repository.add_card(card)

    def delete_card(self, card_id: int) -> None:
        return self.card_repository.delete_card(card_id)

    def get_card_data_from_url(self, base_link: str, mtg_set: str, title: str) -> dict[str, any]:
        suffix: str = "#paper"

        mtg_set: str = remove_special_characters(mtg_set)
        mtg_set: str = capitalize_string(mtg_set)
        mtg_set: str = concatenate_words_in_string(mtg_set)

        title: str = remove_special_characters(title)
        title: str = capitalize_string(title)
        title: str = concatenate_words_in_string(title)

        final_link: str = f"{base_link}/{mtg_set}/{title}/{suffix}"
        res: Response = requests.get(final_link)
        result: dict[str, any] = {'status_code': res.status_code,
                                  'body': {}}
        if result['status_code'] == 200:
            soup: BeautifulSoup = BeautifulSoup(res.text, 'html.parser')
            price_card_gatherer: Tag = soup.find(class_='price-card-gatherer')
            gatherer_container: Tag = price_card_gatherer.find(class_='gatherer-container')
            mana_cost_tag: Tag = gatherer_container.find(class_='gatherer-name').find(class_='manacost')
            mana_cost: str = mana_cost_tag.attrs['aria-label'].split('mana cost: ')[1]
            type_tag: Tag = gatherer_container.find(class_='collapse').find(class_='gatherer-type')
            type: str = type_tag.text
            rarity_tag: Tag = gatherer_container \
                .find(class_='collapse') \
                .find(class_='gatherer-type-power') \
                .find(class_='gatherer-rarity')
            rarity: str = rarity_tag.text

            price_card_name_header: Tag = soup.find(class_='price-card-name-header')
            price_tag: Tag = price_card_name_header \
                .find(class_='price-card-current-prices'). \
                find(class_='price-box-price')
            price: str = price_tag.text.replace('$', '').strip()
            img_tag: Tag = price_card_gatherer \
                .find(class_='price-card-image').find(class_='price-card-image-image')
            img_url: str = img_tag.attrs['src']
            img_data: bytes = requests.get(img_url).content

            result['body'] = {
                'mana_cost': self._get_mana_cost_number(mana_cost),
                'color': self._get_card_color(mana_cost),
                'rarity': rarity,
                'type': remove_special_characters(type),
                'price': price,
                'img_data': img_data
            }
        return result

    def _get_mana_cost_number(self, mana_cost: str) -> int:
        colors_with_numbers: list[str] = mana_cost.split(" ")
        mana_cost_number: int = 0
        for color_or_number in colors_with_numbers:
            if color_or_number.isnumeric():
                mana_cost_number += int(color_or_number)
            else:
                mana_cost_number += 1
        return mana_cost_number

    def _get_card_color(self, mana_cost: str) -> str:
        colors_with_numbers: list[str] = mana_cost.split(" ")
        colors: set = set()
        for color_or_number in colors_with_numbers:
            if not color_or_number.isnumeric():
                colors.add(color_or_number)
        if len(colors) > 0:
            return ','.join(colors)
        else:
            return 'colorless'

    def get_set_value_by_name(self, set_name: str) -> str:
        return self.card_repository.get_set_value_by_name(set_name)

    def check_if_card_exist(self, searched_title: str, searched_set: str) -> bool:
        return self.card_repository.check_if_card_exist(searched_title, searched_set)

    def is_card_title_available(self, searched_title: str) -> bool:
        return os.path.exists(f'src/static/img/{searched_title}.jpg')

    def save_card(self, card_title, card_set, card_details):
        if not os.path.exists(f'src/static/img/{card_title}.jpg'):
            with open(f'src/static/img/{card_title}.jpg', 'wb') as f:
                f.write(card_details.get('img_data'))
        card_dto: CardDTO = CardDTO(card_title,
                                    card_details.get('color').split(","),
                                    card_details.get('mana_cost'),
                                    card_details.get('rarity'),
                                    card_set,
                                    card_details.get('type')
                                    )
        card: Card = card_dto.to_card()
        self.add_card(card)

