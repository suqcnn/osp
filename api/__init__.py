from rest_framework.routers import SimpleRouter


class SlashOptionRouter(SimpleRouter):
    """
    url后缀
    """
    def __init__(self, *args, **kwargs):
        super(SlashOptionRouter, self).__init__(*args, **kwargs)
        self.trailing_slash = '/?'
