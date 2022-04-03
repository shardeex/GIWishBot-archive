import os
import sys
import textwrap
from pathlib import Path

from PIL import Image, ImageCms, ImageDraw, ImageEnhance, ImageFont

file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

from app import genshin


image_boxes = {
    'icon': (26, 279, 122, 375),
    'star': (99, 315, 121, 337),
    'character': (-192, -74, 1283, 663),
    'weapon': (372, -39, 700, 617),
    'weapon_bg': (242, -6, 831, 582),
    'weapon_shadow': (374, -27, 702, 630),
}
name_dot = (99, 306)
delta_star_box = (21, 32)

assets = \
    list(w[:-4] for w in os.listdir('wishes_image_generator/characters')) + \
    list(w[:-4] for w in os.listdir('wishes_image_generator/weapons'))
print(f'Found {len(assets)}/{len(genshin.items.values())} assets.')

def create(item: genshin.Character | genshin.Weapon, lang: str) -> None:
    image = Image.open('wishes_image_generator/wishes_background.png')
    star = Image.open('wishes_image_generator/star.png').convert(mode='RGBA')
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('wishes_image_generator/font.ttf', 32)

    box = image_boxes[item.category[:-1]]  # without 's'
    size = box[2] - box[0], box[3] - box[1]

    assets = []
    
    if item.__class__ == genshin.Weapon:
        assets.append((
            Image.open(f'wishes_image_generator/weapon_bg/{item.type}.png').resize((589, 589)),
            image_boxes['weapon_bg']))
        assets.append((ImageEnhance.Brightness(
            Image.open(f'wishes_image_generator/weapons/{item.id}.png').resize(size)).enhance(0.1),
            image_boxes['weapon_shadow']))
        assets.append((
            Image.open(f'wishes_image_generator/weapons/{item.id}.png').resize(size),
            image_boxes['weapon']))
        assets.append((
            Image.open(f'wishes_image_generator/weapon_icon/{item.type}.png'),
            image_boxes['icon']))
    elif item.__class__ == genshin.Character:
        assets.append((
            Image.open(f'wishes_image_generator/characters/{item.id}.png').resize(size),
            image_boxes['character']))
        assets.append((
            Image.open(f'wishes_image_generator/element_icon/{item.vision}.png'),
            image_boxes['icon']))
    else:
        raise ValueError(item)
    
    # calculate name length (rows)
    name_strings = textwrap.wrap(item.name[lang], width=15)

    # rarity stars
    for i in range(item.rarity):
        assets.append((star, (
            image_boxes['star'][0] + delta_star_box[0]*i,
            image_boxes['star'][1] + delta_star_box[1]*(len(name_strings)),
            image_boxes['star'][2] + delta_star_box[0]*i,
            image_boxes['star'][3] + delta_star_box[1]*(len(name_strings)))))
    
    # paste assets using bg as mask
    for asset, asset_box in assets:
        asset_with_bg = image.crop(asset_box)
        asset_with_bg.alpha_composite(asset, (0, 0))
        image.paste(asset_with_bg, asset_box)
    
    # paste item name
    for i in range(len(name_strings)):
        draw.text(
            (name_dot[0], name_dot[1]+i*32),
            name_strings[i], (255, 255, 255), font,
            stroke_width=1, stroke_fill=(0, 0, 0))

    profile = ImageCms.ImageCmsProfile('wishes_image_generator/AdobeRGB1998.icc')
    path = f'assets/images/wishes/{lang}/{item.id}.png'
    image.save(path, icc_profile=profile.tobytes())
    return path

def main():
    for lang in ('en', 'ru'):
        assets_list = list(w[:-4] for w in os.listdir(f'assets/images/wishes/{lang}'))
        for item in genshin.items.values():
            if not item.id in assets_list:
                if not item.id in assets:
                    print(f'{item.id} not found in assets.')
                else:
                    if item.location == 'wish':
                        image_path = create(item, lang)
                        print(f'Created {item.name["en"]} picture for {lang} | {image_path}')

if __name__ == '__main__':
    if input('Are you sure want to generate all images? ') == 'y':
        main()
    else:
        print('Canceled.')
