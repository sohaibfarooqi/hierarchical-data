from flask.views import MethodView

class RouteHanlder:
    """
    Defines all routing rules
    """
    def __init__(self, blueprint):
        self.blueprint = blueprint

    def route(self, url, pk_name='pk', pk_type='int'):
        def decorator(resource):
            # URL rule defining default_value for key: pk
            self.blueprint.add_url_rule(url,
                                        defaults={pk_name: None},
                                        view_func=resource,
                                        methods=['GET'])
            # example url for this rule http://abc.com/root/,http://abc.com/child/ 
            self.blueprint.add_url_rule('{}/'.format(url),
                                        view_func=resource,
                                        methods=['GET'])
            #example url rule http://abc.com/child/2, http://abc.com/getsubtree/2
            self.blueprint.add_url_rule('{}/<{}:{}>/'.format(url, pk_type, pk_name),
                                        view_func=resource,
                                        methods=['GET'])
            
            return resource
        return decorator


class Resource(MethodView):
    pass
