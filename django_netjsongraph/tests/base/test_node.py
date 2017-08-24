import six


class TestNodeMixin(object):
    def test_str(self):
        n = self.node_model(addresses='192.168.0.1', label='test node')
        self.assertIsInstance(str(n), str)

    def test_clean_properties(self):
        t = self.topology_model.objects.first()
        n = t._create_node(addresses='192.168.0.1',
                           label='test node',
                           properties=None)
        n.full_clean()
        self.assertEqual(n.properties, {})

    def test_node_address_list_single(self):
        t = self.topology_model.objects.first()
        n = t._create_node(addresses='192.168.0.1',
                           label='test node',
                           properties=None)
        n.full_clean()
        n.save()
        self.assertEqual(n.addresses, '192.168.0.1;')
        self.assertEqual(n.address_list, ['192.168.0.1'])

    def test_node_address_list_semicolon(self):
        t = self.topology_model.objects.first()
        n = t._create_node(label='test node',
                           addresses='192.168.0.1;')
        n.full_clean()
        n.save()
        self.assertEqual(n.addresses, '192.168.0.1;')
        self.assertEqual(n.address_list, ['192.168.0.1'])

    def test_node_address_list_multiple(self):
        t = self.topology_model.objects.first()
        n = t._create_node(label='test node',
                           addresses='192.168.0.1; 10.0.0.1,10.0.0.2;10.0.0.3')
        n.full_clean()
        n.save()
        self.assertEqual(n.addresses, '192.168.0.1; 10.0.0.1; '
                                      '10.0.0.2; 10.0.0.3;')
        self.assertEqual(n.address_list, ['192.168.0.1',
                                          '10.0.0.1',
                                          '10.0.0.2',
                                          '10.0.0.3'])

    def test_node_local_addresses(self):
        t = self.topology_model.objects.first()
        n = t._create_node(label='test node',
                           addresses='192.168.0.1;10.0.0.1;10.0.0.2;')
        self.assertEqual(n.local_addresses, ['10.0.0.1',
                                             '10.0.0.2'])

    def test_node_name(self):
        n = self.node_model(addresses='192.168.0.1,10.0.0.1')
        n._format_addresses()
        self.assertEqual(n.name, '192.168.0.1')
        n.label = 'test node'
        self.assertEqual(n.name, 'test node')

    def test_json(self):
        t = self.topology_model.objects.first()
        n = t._create_node(label='test node',
                           addresses='192.168.0.1;10.0.0.1;',
                           properties='{"gateway": true}')
        self.assertEqual(dict(n.json(dict=True)), {
            'id': '192.168.0.1',
            'label': 'test node',
            'local_addresses': ['10.0.0.1'],
            'properties': {
                'gateway': True,
                'created': n.created,
                'modified': n.modified
            }
        })
        self.assertIsInstance(n.json(), six.string_types)

    def test_get_from_address(self):
        t = self.topology_model.objects.first()
        n = t._create_node(addresses='192.168.0.1,10.0.0.1')
        n.save()
        self.assertIsInstance(self.node_model.get_from_address('192.168.0.1', t), self.node_model)
        self.assertIsInstance(self.node_model.get_from_address('10.0.0.1', t), self.node_model)
        self.assertIsNone(self.node_model.get_from_address('wrong', t))

    def test_count_address(self):
        t = self.topology_model.objects.first()
        t._create_node(addresses='192.168.0.1,10.0.0.1')
        self.assertEqual(self.node_model.count_address('192.168.0.1', t), 1)
        self.assertEqual(self.node_model.count_address('0.0.0.0', t), 0)
