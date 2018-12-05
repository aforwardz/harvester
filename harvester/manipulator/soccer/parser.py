import os
import re
import json
from datetime import datetime
from lxml.etree import HTML
from bs4 import BeautifulSoup
from soccer import models


def parse(top_path):
    for root, _, files in os.walk(top_path):
        if files:
            paths = root.split('/')
            nation, competition, team = paths[-3], paths[-2], paths[-1]
            print(nation, competition, team)
            competition, _ = models.Competition.objects.get_or_create(
                name=competition,
                nation=nation
            )
            club, nation_team = None, None
            if nation != '国际':
                club, _ = models.Club.objects.get_or_create(
                    name=team,
                    nation=nation
                )
                club.competitions.add(competition)
            else:
                nation_team, _ = models.NationTeam.objects.get_or_create(
                    name=team,
                    nation=nation
                )
                nation_team.competitions.add(competition)
            for file in files:
                with open(os.path.join(root, file), 'r') as f:
                    contents = json.load(f).get('html')
                    tree = HTML(contents)
                    th = tree.xpath('//div[@class="player-info"]//th/text()')
                    td = tree.xpath('//div[@class="player-info"]//td')
                    avatar = tree.xpath('//div[@class="player-info"]/img/@src')
                    if len(avatar) > 0:
                        avatar = avatar[0]
                    else:
                        avatar = ''
                    print(avatar)
                    # print(len(th), len(td))
                    avatar, en_name, field, positions, age, birth, joined, util, nationality, \
                    height, foot, price = None, '', None, None, None, None, None, None, None, None, None, None
                    for t, c in zip(th, td):
                        if '国籍' in t:
                            nationality = c.xpath('img/@alt')[0]
                        content = c.xpath('text()')
                        if len(content) == 0:
                            continue
                        content = content[0].replace('\r', '').replace('\n', '').replace('\t', '').strip()
                        # print(t, content)
                        if '英文名' in t:
                            en_name = content.replace("'", "-") or ''
                        if '场上位置' in t and content != '-':
                            field = content.split('&nbsp')[0]
                            positions = re.findall(r'(\([^\)]+\))', content)
                            positions = positions[0].replace('(', '').replace(')', '').split('、') if positions else []
                        if '年龄' in t and content != '-':
                            age = int(content.split('&nbsp')[0].strip('岁'))
                            birth = re.findall(r'(\([^\)]+\))', content)
                            birth = datetime.strptime(birth[0].replace('(', '').replace(')', ''), '%Y-%m-%d').date() if birth else None
                        if '入队时间' in t and content != '-':
                            joined = datetime.strptime(content, '%Y-%m-%d').date()
                        if '合同到期' in t and content != '-':
                            util = datetime.strptime(content, '%Y-%m-%d').date()
                        if '身高' in t and content != '-':
                            height = int(float(content.strip('m')) * 100)
                        if '惯用脚' in t and content != '-':
                            foot = content
                        if '身价' in t and content != '-':
                            if '万' in content:
                                price = int(content.strip('万'))
                            if '亿' in content:
                                price = int(float(content.strip('亿')) * 10000)

                    print(en_name, field, positions, age, birth, joined, util, nationality, height, foot, price)
                    player, created = models.Player.objects.get_or_create(name=file, en_name=en_name)
                    if created:
                        player.avatar = avatar
                        player.age = age
                        player.birth = birth
                        player.height = height
                        player.field = field or '-'
                        player.positions = positions or []
                        player.foot = foot or '-'
                        player.price = price
                        player.joined = joined
                        player.contract_util = util
                        player.nationality = nationality
                        if club:
                            player.club = club
                        if nation_team:
                            player.nation_team = nation_team
                        player.save()
                    # soup = BeautifulSoup(contents)
                    # print(soup.find(attrs={'class': 'player-info'}))
                # break
            # break
