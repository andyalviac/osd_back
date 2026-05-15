from .Provider import provider_query_resolvers, provider_mutation_resolvers

# from .Cycle import cycle_mutation_resolvers, cycle_query_resolvers
# from .Deductions import deductions_query_resolvers, deductions_mutation_resolvers

all_query_resolver = {
    **provider_query_resolvers,
    #   **cycle_query_resolvers,
    #   **deductions_query_resolvers,
}

all_mutation_resolver = {
    **provider_mutation_resolvers,
    #   **cycle_mutation_resolvers,
    #   **deductions_mutation_resolvers,
}
