import graphene
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required
from graphql_relay import from_global_id

from .models import Player, Team


class PlayerNode(DjangoObjectType):
    class Meta:
        model = Player
        # 要修正、height、weight、salary
        filter_fields = {
            "name": ["exact", "icontains"],
            "born": ["exact", "gte", "lte"],
            "height": ["exact", "gte", "lte"],
            "weight": ["exact", "gte", "lte"],
            "salary": ["exact", "gte", "lte"],
            "team__team_name": ["icontains"],
        }
        interfaces = (relay.Node,)


class TeamNode(DjangoObjectType):
    class Meta:
        model = Team
        filter_fields = {
            "players": ["exact"],
            "team_name": ["icontains"],
        }
        interfaces = (relay.Node,)


class PlayerCreateMutation(relay.ClientIDMutation):
    class Input:
        name = graphene.String(required=True)
        born = graphene.Date(required=True)
        height = graphene.Int(required=True)
        weight = graphene.Int(required=True)
        salary = graphene.Int(required=True)
        uniform_number = graphene.Int(required=True)
        team = graphene.ID(required=True)

    player = graphene.Field(PlayerNode)

    @login_required
    def mutate_and_get_payload(root, info, **input):
        player = Player(
            name=input.get("name"),
            born=input.get("born"),
            height=input.get("height"),
            weight=input.get("weight"),
            salary=input.get("salary"),
            uniform_number=input.get("uniform_number"),
            team=from_global_id(input.get("team"))[1],
        )
        player.save()

        return PlayerCreateMutation(player=player)


class PlayerUpdateMutation(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
        name = graphene.String(required=True)
        born = graphene.Date(required=True)
        height = graphene.Int(required=True)
        weight = graphene.Int(required=True)
        salary = graphene.Int(required=True)
        uniform_number = graphene.Int(required=True)
        team = graphene.ID(required=True)

    player = graphene.Field(PlayerNode)

    @login_required
    def mutate_and_get_payload(root, info, **input):
        player = Player(id=from_global_id(input.get))[1]
        player.name = input.get("name")
        player.born = input.get("born")
        player.height = input.get("height")
        player.weight = input.get("weight")
        player.salary = input.get("salary")
        player.uniform_number = input.get("uniform_number")
        player.team = from_global_id(input.get("team"))[1]

        player.save()

        return PlayerUpdateMutation(player=player)


class PlayerDeleteMutation(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)

    player = graphene.Field(PlayerNode)

    @login_required
    def mutate_and_get_payload(root, info, **input):
        player = Player(
            id=from_global_id(input.get("id"))[1]
        )
        player.delete()

        return PlayerDeleteMutation(player=None)


class Mutation(graphene.ObjectType):
    create_player = PlayerCreateMutation.Field()
    update_player = PlayerUpdateMutation.Field()
    delete_player = PlayerDeleteMutation.Field()


class Query(graphene.ObjectType):
    player = graphene.Field(PlayerNode, id=graphene.NonNull(graphene.ID))
    all_players = DjangoFilterConnectionField(PlayerNode)
    all_teams = DjangoFilterConnectionField(TeamNode)

    def resolve_player(self, info, **kwargs):
        id = kwargs.get("id")
        if id is not None:
            return Player.objects.get(id=from_global_id(id)[1])

    def resolve_all_players(self, info, **kwargs):
        return Player.objects.all()

    def resolve_all_teams(self, info, **kwargs):
        return Team.objects.all()
