import os
import json
# from soccer import models


def parse(top_path):
    for root, _, files in os.walk(top_path):
        print(root, files)
        if files:
            paths = root.split('/')
            nation, competition, team = paths[-3], paths[-2], paths[-1]
            print(nation, competition, team)
            # _, competition = models.Competition.objects.get_or_create(
            #     name=competition,
            #     nation=nation
            # )
            # _, team = models.Team.objects.get_or_create(
            #     name=team,
            #     nation=nation
            # )
            # team.competitions.add(competition)
            for file in files:
                with open(os.path.join(root, file), 'r') as f:
                    content = json.load(f)
                    print(content.get('url'))

if __name__ == '__main__':
    parse('/Users/ycw/PycharmProjects/harvester/harvester/collector/pages/tzuqiu')