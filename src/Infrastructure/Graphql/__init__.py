from ariadne import gql
from ariadne import QueryType, MutationType
from ariadne import make_executable_schema
from pathlib import Path
from ..Graphql.Resolvers import all_mutation_resolver, all_query_resolver


def load_schemas():
    schema_dir = Path(__file__).parent / "Schemas"
    schemas = [schema.read_text() for schema in schema_dir.rglob("*.graphql")]
    return gql("\n".join(schemas))


type_defs = load_schemas()


query = QueryType()
mutation = MutationType()

for field, resolver in all_mutation_resolver.items():
    mutation.set_field(field, resolver)

for field, resolver in all_query_resolver.items():
    query.set_field(field, resolver)

# Executable Schema
schema = make_executable_schema(type_defs, query, mutation)
