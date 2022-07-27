from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

def obtain_result(database, keyword, field_names=[]) :

    search_vector = SearchVector(*field_names)
    search_query = SearchQuery(keyword)
    results = database.objects.annotate(
        search=search_vector,
        rank=SearchRank(search_vector, search_query)
    ).filter(search=search_query).order_by('-rank')
    print(results)
    return list(results)