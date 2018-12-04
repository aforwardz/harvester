# coding: utf-8
from django.core.management.base import BaseCommand
from soccer import models
from utils.neo4j_driver import get_driver
from utils.queryset_iterator import queryset_iterator


class Command(BaseCommand):
    def _start_session(self):
        driver = get_driver()
        self.session = driver.session()

    def add_competition(self, tx, obj):
        tx.run("MERGE (nation:Nation{name:$n_name}) "
               "MERGE (comp:Competition{name:$c_name}) SET comp+= {short_name:$short_name, en_name:$en_name} "
               "MERGE (comp) -[:BELONG_TO]-> (nation)",
               n_name=obj.nation, c_name=obj.name, short_name=obj.short_name, en_name=obj.en_name)

    def add_club(self, tx, obj):
        tx.run("MERGE (nation:Nation{name:$n_name}) "
               "MERGE (club:Club{name:$c_name}) SET club+= "
               "{short_name:$short_name, en_name:$en_name} "
               "MERGE (club) -[:LOCATE_IN]-> (nation) "
               " ".join(["MERGE (comp:Competition{name:%s}) MERGE (club) -[:JOIN_IN]-> (comp)" % c.name
                         for c in obj.competitions]),
               n_name=obj.nation, c_name=obj.name)

    def add_nation_team(self, tx, obj):
        tx.run("MERGE (nation:Nation{name:$n_name}) "
               "MERGE (nt:NationTeam{name:$c_name}) SET nt+= "
               "{short_name:$short_name, en_name:$en_name} "
               "MERGE (nt) -[:TEAM_OF]-> (nation) "
               " ".join(["MERGE (comp:Competition{name:%s}) MERGE (nt) -[:JOIN_IN]-> (comp)" % c.name
                         for c in obj.competitions]),
               n_name=obj.nation, c_name=obj.name)

    def add_player(self, tx, obj):
        cypher = "MERGE (pl:Player{name:%s}) SET pl+={alias:%s, en_name:%s, nick_name:%s, gender:%s, height:%d, " \
                 "birth:%s, age:%d, foot:%s, field:%s, positions:%s, number:%d, price:%d, joined:%s, " \
                 "contract_util:%s} " % (obj.name, str(obj.alias), obj.en_name, obj.nick_name, obj.get_gender_display(),
                                         obj.height, obj.birth.strftime('%Y-%m-%d'), obj.age, obj.foot, obj.field,
                                         str(obj.positions), obj.number, obj.price, obj.joined.strftime('%Y-%m-%d'),
                                         obj.contract_util.strftime('%Y-%m-%d'))
        if obj.nationality:
            cypher += "MERGE (nation:Nation{name:%s}) MERGE (player) -[:BORN_IN]-> (nation) " % obj.nationality
        if obj.club:
            cypher += "MERGE (club:Club{name:%s}) MERGE (player) -[:PLAY_FOR]-> (club) " % obj.club.name
        if obj.nation_team:
            cypher += "MERGE (nt:NationTeam{name:%s}) MERGE (player) -[:PLAY_FOR]-> (nt) " % obj.nation_team.name
        tx.run(cypher)

    def add_coach(self, tx, obj):
        cypher = "MERGE (coach:Coach{name:%s}) SET coach+={alias:%s, en_name:%s, nick_name:%s, gender:%s, height:%d, " \
                 "birth:%s, age:%d} " % (obj.name, str(obj.alias), obj.en_name, obj.nick_name, obj.get_gender_display(),
                                         obj.height, obj.birth.strftime('%Y-%m-%d'), obj.age)
        if obj.nationality:
            cypher += "MERGE (nation:Nation{name:%s}) MERGE (coach) -[:BORN_IN]-> (nation) " % obj.nationality
        if obj.club:
            cypher += "MERGE (club:Club{name:%s}) MERGE (coach) -[:COACH_FOR]-> (club) " % obj.club.name
        if obj.nation_team:
            cypher += "MERGE (nt:NationTeam{name:%s}) MERGE (coach) -[:COACH_FOR]-> (nt) " % obj.nation_team.name
        tx.run(cypher)

    def add_match(self, tx, obj):
        pass

    def handle(self, *args, **options):
        self._start_session()
        competition_qs = models.Competition.objects.all()
        club_qs = models.Club.objects.all()
        nation_team_qs = models.NationTeam.objects.all()
        player_qs = models.Player.objects.all()
        coach_qs = models.Coach.objects.all()
        play_record_qs = models.PlayRecord.objects.all()
        coach_record_qs = models.CoachRecord.objects.all()
        match_qs = models.Match.objects.all()
        performance_qs = models.PlayerPerformance.objects.all()
        compe_data_qs = models.CompetitionData.objects.all()

        for q in queryset_iterator(competition_qs):
            print('IMPORT COMPETITION %s' % q.name)
            self.session.write_transaction(self.add_competition, q)

        for q in queryset_iterator(club_qs):
            print('IMPORT CLUB %s' % q.name)
            self.session.write_transaction(self.add_club, q)

        for q in queryset_iterator(nation_team_qs):
            print('IMPORT NATION TEAM %s' % q.name)
            self.session.write_transaction(self.add_nation_team, q)

        for q in queryset_iterator(player_qs):
            print('IMPORT PLAYER %s' % q.name)
            self.session.write_transaction(self.add_player, q)

        for q in queryset_iterator(coach_qs):
            print('IMPORT COACH %s' % q.name)
            self.session.write_transaction(self.add_coach, q)

