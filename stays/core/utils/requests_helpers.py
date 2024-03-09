from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

# from django.core.cache import cache

# def get_cache_key(model):
#     def _get_cache_key():
#         count = cache.get('publications_count')
#         if count is None:
#             count = model.objects.count()
#             # Cache the count for 6 minutes
#             cache.set('publications_count', count, 60 * 6)
#         return 'home_page_{}'.format(count)
#     return _get_cache_key


class NeverCacheMixin:
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
