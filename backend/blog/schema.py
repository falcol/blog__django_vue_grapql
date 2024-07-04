import graphene
from blog import mutations, queries

schema = graphene.Schema(query=queries.Query, mutation=mutations.Mutation)
