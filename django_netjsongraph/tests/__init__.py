class CreateGraphObjectsMixin(object):
    def _create_topology(self, **kwargs):
        options = dict(label='TestNetwork',
                       parser='netdiff.OlsrParser',
                       strategy='fetch',
                       url='http://127.0.0.1:9090',
                       protocol='OLSR',
                       version='0.8',
                       metric='ETX',
                       created='2017-07-10T20:02:52.483Z',
                       modified='2015-07-14T20:02:52.483Z')
        options.update(kwargs)
        t = self.topology_model(**options)
        t.full_clean()
        t.save()
        return t

    def _create_node(self, **kwargs):
        options = dict(label='TestNode',
                       addresses='192.168.0.1;',
                       created='2017-07-10T20:02:52.483Z',
                       modified='2017-07-14T20:02:52.483Z',
                       properties={})
        options.update(kwargs)
        n = self.node_model(**options)
        n.full_clean()
        n.save()
        return n

    def _create_link(self, **kwargs):
        options = dict(cost='1',
                       cost_text='one',
                       properties={})
        options.update(kwargs)
        l = self.link_model(**options)
        l.full_clean()
        l.save()
        return l
