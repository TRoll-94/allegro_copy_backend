from enum import Enum


class RestActions(Enum):
    """ rest actions """
    create = 'create'
    retrieve = 'retrieve'
    list = 'list'
    partial_update = 'partial_update'
    destroy = 'destroy'

    @staticmethod
    def safe():
        """ safe actions """
        return [RestActions.retrieve.value, RestActions.list.value]
