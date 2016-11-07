# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from senlin.common import consts
from senlin.objects import base
from senlin.objects import fields


@base.SenlinObjectRegistry.register
class ReceiverCreateRequestBody(base.SenlinObject):

    fields = {
        'name': fields.NameField(),
        'type': fields.ReceiverTypeField(),
        'cluster_id': fields.StringField(nullable=True),
        'action': fields.ClusterActionNameField(nullable=True),
        'actor': fields.JsonField(nullable=True, default={}),
        'params': fields.JsonField(nullable=True, default={})
    }


@base.SenlinObjectRegistry.register
class ReceiverCreateRequest(base.SenlinObject):

    fields = {
        'receiver': fields.ObjectField('ReceiverCreateRequestBody')
    }


@base.SenlinObjectRegistry.register
class ReceiverListRequest(base.SenlinObject):

    fields = {
        'name': fields.ListOfStringsField(nullable=True),
        'type': fields.ReceiverTypeField(nullable=True),
        'action': fields.ClusterActionNameField(nullable=True),
        'cluster_id': fields.StringField(nullable=True),
        'limit': fields.NonNegativeIntegerField(nullable=True),
        'marker': fields.UUIDField(nullable=True),
        'sort': fields.SortField(
            valid_keys=list(consts.NODE_SORT_KEYS), nullable=True),
        'project_safe': fields.FlexibleBooleanField(default=True)
    }