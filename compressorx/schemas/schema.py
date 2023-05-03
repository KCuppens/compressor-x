from graphene import ObjectType, Schema

from apps.action.schemas.schema import Mutation as ActionMutation
from apps.blog.schemas.schema import Query as BlogQuery
from apps.compress.schemas.schema import Mutation as CompressMutation
from apps.config_file.schemas.schema import Mutation as ConfigFileMutation
from apps.contact.schemas.schema import Mutation as ContactMutation
from apps.cookies.schemas.schema import Query as CookieQuery
from apps.faq.schemas.schema import Query as FaqQuery
from apps.initial_files.schemas.schema import Mutation as InitialFileMutation
from apps.locales.schemas.schema import Query as LocaleQuery
from apps.pages.schemas.schema import Query as PageQuery
from apps.users.schemas.schema import Mutation as UserMutation
from apps.users.schemas.schema import Query as UserQuery


class Query(
    BlogQuery,
    CookieQuery,
    UserQuery,
    FaqQuery,
    LocaleQuery,
    PageQuery,
    ObjectType,
):
    pass


class Mutation(
    ConfigFileMutation,
    CompressMutation,
    InitialFileMutation,
    ActionMutation,
    ContactMutation,
    UserMutation,
    ObjectType,
):
    pass


schema = Schema(query=Query, mutation=Mutation)
