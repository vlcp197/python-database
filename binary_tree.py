import pickle
from logical import LogicalBase, ValueRef


class BinaryNode:

    @classmethod

    def from_node(cls, node, **kwargs):

        length = node.length

        if 'left_ref' in kwargs:

            length += kwargs['left_ref'].length - node.left_ref.length

        if 'right_ref' in kwargs:

            length += kwargs['right_ref'].length - node.right_ref.length


        return cls(

            left_ref=kwargs.get('left_ref', node.left_ref),

            key=kwargs.get('key', node.key),

            value_ref=kwargs.get('value_ref', node.value_ref),

            right_ref=kwargs.get('right_ref', node.right_ref),

            length=length
        )


    def __init__(self, left_ref, key, value_ref, right_ref, length):

        self.left_ref = left_ref

        self.key = key

        self.value_ref = value_ref

        self.right_ref = right_ref

        self.length = length


    def store_refs(self, storage):

        self.value_ref.store(storage)
        self.left_ref.store(storage)
        self.right_ref.store(storage)


class BinaryNodeRef(ValueRef):

    def prepare_to_store(self, storage):

        if self._referent:
            self._referent.store_refs(storage)

    @property
    def length(self):

        if self._referent is None and self._address:

            raise RuntimeError('Asking for BinaryNodeRef length of unloaded node')

        if self._referent:

            return self._referent.length

        else:

            return 0

    @staticmethod
    def referent_to_string(referent):
        return pickle.dumps({
            'left': referent.left_ref.address,
            'key': referent.key,
            'value': referent.value_ref.address,
            'right': referent.right_ref.address,
            'length': referent.length
        })

    @staticmethod
    def string_to_referent(string):
        d = pickle.loads(string)
        return BinaryNode(
            BinaryNodeRef(address=d['left']),
            d['key'],
            ValueRef(address=d['value']),
            BinaryNodeRef(address=d['right']),
            d['length']
        )
