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
               "MERGE (comp:Competition{name:$c_name}) SET n+= {short_name:$short_name, en_name:$en_name}",
               n_name=obj.nation, c_name=obj.name, short_name=obj.short_name, en_name=obj.en_name)

    def add_club(self, tx, obj):
        tx.run("MERGE (title:Title{id:$title_id})", title_id=obj.id)

    def add_nation_team(self, tx, obj):
        tx.run("MERGE (title:Title{id:$title_id})", title_id=obj.id)

    def add_player(self, tx, obj):
        tx.run("MERGE (title:Title{id:$title_id})", title_id=obj.id)

    def add_coach(self, tx, obj):
        tx.run("MERGE (title:Title{id:$title_id})", title_id=obj.id)

    def add_match(self, tx, obj):
        tx.run("MERGE (title:Title{id:$title_id})", title_id=obj.id)

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

        for q in queryset_iterator(match_qs):
            print('IMPORT MATCH %s' % q.name)
            self.session.write_transaction(self.add_match, q)
