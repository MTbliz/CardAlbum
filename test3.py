from bs4 import BeautifulSoup
import requests
from src.card.card_service import CardService
from src.models import UserCard, Album
from src import db
from run import app



def get_card_details_from_url(base_link, mtg_set, title):
    suffix = "#paper"

    final_link = f"{base_link}/{mtg_set}/{title}/{suffix}"

    res = requests.get(final_link)
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

    result = {
        'mana_cost': mana_cost,
        'rarity': rarity,
        'type': type,
        'price': price,
        'img_data': img_data
    }
    return result


if __name__ == '__main__':
    base_link = 'https://www.mtggoldfish.com/price'
    mtg_set = "Wilds of Eldraine"
    title = "Agatha's Soul Cauldron"

    #card_service = CardService()
    #result = card_service.get_card_details_from_url(base_link, mtg_set, title)
    #print(result)


    with app.app_context():
        new_album = Album()
        new_album.title = "TestAlbum"

        user_cards = UserCard.query.all()

        new_album.user_cards = user_cards


        db.session.add(new_album)
        db.session.commit()
