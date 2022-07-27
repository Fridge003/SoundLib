from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from App.models import Recording, User, Composer

def obtain_result(database, keyword, search_vector) :

    search_query = SearchQuery(keyword)
    results = database.objects.annotate(
        search=search_vector,
        rank=SearchRank(search_vector, search_query)
    ).filter(search=search_query).order_by('-rank')
    return list(results)

def default_search(keyword) :

    RecordingSearchVector = \
        SearchVector('Name', weight='A')+\
        SearchVector('Composer__Name', weight='B')+\
        SearchVector('UploadUserName', weight='C')+\
        SearchVector('UploadUser__username', weight='C')
    
    UserSearchVector = \
        SearchVector('username', weight='A')+\
        SearchVector('Introduction', weight='D')
    
    ComposerSearchVector = \
        SearchVector('Name', weight='A')+\
        SearchVector('Introduction', weight='D')

    RecordingSearchResults = obtain_result(Recording, keyword, RecordingSearchVector)
    UserSearchResults = obtain_result(User, keyword, UserSearchVector)
    ComposerSearchResults = obtain_result(Composer, keyword, ComposerSearchVector)

    return RecordingSearchResults + UserSearchResults + ComposerSearchResults