from .base.link import AbstractLink
from .base.node import AbstractNode
from .base.topology import AbstractTopology


class Topology(AbstractTopology):
    class Meta(AbstractTopology.Meta):
        abstract = False


class Node(AbstractNode):
    pass


class Link(AbstractLink):
    pass
