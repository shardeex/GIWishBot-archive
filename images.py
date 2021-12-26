import os
import textwrap

import github
from PIL import Image, ImageCms, ImageDraw, ImageEnhance, ImageFont

import utils


class Images():
    """

    """
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

    def __init__(self):
        self.repository = github.Github(utils.GITHUB_TOKEN).get_user().get_repo(utils.REPOSITORY_NAME)

        self.assets = \
            list(w[:-4] for w in os.listdir(f'assets/characters')) + \
            list(w[:-4] for w in os.listdir(f'assets/weapons'))

        print(f'Found {len(self.assets)}/{len(utils.characters+utils.weapons)} assets.')

    def _create(self, item, lang) -> None:
        """
        Generates images based on assets.
        """
        image = Image.open('assets/wishes_background.png')
        star = Image.open('assets/star.png').convert(mode='RGBA')
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype('assets/font.ttf', 32)

        item.box = self.image_boxes[item.__class__.__name__.lower()]
        item.size = item.box[2] - item.box[0], item.box[3] - item.box[1]

        assets = []
        
        if item.__class__ == utils.Weapon:
            assets.append((
                Image.open(f'assets/weapon_bg/{item.type}.png').resize((589, 589)),
                self.image_boxes['weapon_bg']))
            assets.append((ImageEnhance.Brightness(
                Image.open(f'assets/weapons/{item.id}.png').resize(item.size)).enhance(0.1),
                self.image_boxes['weapon_shadow']))
            assets.append((
                Image.open(f'assets/weapons/{item.id}.png').resize(item.size),
                self.image_boxes['weapon']))
            assets.append((
                Image.open(f'assets/weapon_icon/{item.type}.png'),
                self.image_boxes['icon']))
        elif item.__class__ == utils.Character:
            assets.append((
                Image.open(f'assets/characters/{item.id}.png').resize(item.size),
                self.image_boxes['character']))
            assets.append((
                Image.open(f'assets/element_icon/{item.element}.png'),
                self.image_boxes['icon']))
        else:
            raise ValueError(item)
        
        # calculate name length (rows)
        name_strings = textwrap.wrap(getattr(item.name, lang), width=15)

        # rarity stars
        for i in range(item.rarity):
            assets.append((star, (
                self.image_boxes['star'][0] + self.delta_star_box[0]*i,
                self.image_boxes['star'][1] + self.delta_star_box[1]*(len(name_strings)),
                self.image_boxes['star'][2] + self.delta_star_box[0]*i,
                self.image_boxes['star'][3] + self.delta_star_box[1]*(len(name_strings)))))
        
        # paste assets using bg as mask
        for asset, asset_box in assets:
            asset_with_bg = image.crop(asset_box)
            asset_with_bg.alpha_composite(asset, (0, 0))
            image.paste(asset_with_bg, asset_box)
        
        # paste item name
        for i in range(len(name_strings)):
            draw.text(
                (self.name_dot[0], self.name_dot[1]+i*32),
                name_strings[i], (255, 255, 255), font,
                stroke_width=1, stroke_fill=(0, 0, 0))

        profile = ImageCms.ImageCmsProfile('assets/AdobeRGB1998.icc')
        path = f'assets/gacha/{lang}/{item.id}.png'
        image.save(path, icc_profile=profile.tobytes())
        return path
    
    def update(self):
        for lang in utils.LANGUAGE_CODES:
            github_gacha_dir = list([x.name[:-4] for x in self.repository.get_contents(f'assets/gacha/{lang}')])
            github_gacha_dir.remove('README.md'[:-4])
            for item in utils.characters+utils.weapons:
                if not item.id in github_gacha_dir:
                    if not item.id in self.assets:
                        print(f'{item.id} not found in assets.')
                    else:
                        image_path = self._create(item, lang)
                        self.repository.create_file(image_path,
                            f'[BOT] create {item.name.en} picture for {lang}',
                            open(image_path, 'rb').read())
            github_gacha_dir = list([x.name[:-4] for x in self.repository.get_contents(f'assets/gacha/{lang}')])
            github_gacha_dir.remove('README.md'[:-4])
            print(f'Total {len(github_gacha_dir)} gacha images for {lang} lang.')
