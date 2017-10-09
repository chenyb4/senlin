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

from oslo_config import cfg
from oslo_log import log as logging
from stevedore import named

from senlin.common.i18n import _LW, _LI
from senlin.events import database as DB


LOG = logging.getLogger(__name__)
FMT = '%(name)s [%(id)s] %(action)s - %(phase)s: %(reason)s'
dispatchers = None


def load_dispatcher():
    """Load dispatchers."""
    global dispatchers

    LOG.debug("Loading dispatchers")
    dispatchers = named.NamedExtensionManager(
        namespace="senlin.dispatchers",
        names=cfg.CONF.dispatchers,
        invoke_on_load=True,
        propagate_map_exceptions=True)
    if not list(dispatchers):
        LOG.warning(_LW("No dispatchers configured for 'senlin.disaptchers'"))
    else:
        LOG.info(_LI("Loaded dispatchers: %s"), dispatchers.names())


def _event_data(action, phase=None, reason=None):
    return dict(name=action.entity.name,
                id=action.entity.id[:8],
                action=action.action,
                phase=phase,
                reason=reason)


def critical(action, phase=None, reason=None, timestamp=None):
    DB.DBEvent.dump(action.context, logging.CRITICAL, action.entity, action,
                    status=phase, reason=reason, timestamp=timestamp)

    LOG.critical(FMT, _event_data(action, phase, reason))


def error(action, phase=None, reason=None, timestamp=None):
    DB.DBEvent.dump(action.context, logging.ERROR, action.entity, action,
                    status=phase, reason=reason, timestamp=timestamp)

    LOG.error(FMT, _event_data(action, phase, reason))


def warning(action, phase=None, reason=None, timestamp=None):
    DB.DBEvent.dump(action.context, logging.WARNING, action.entity, action,
                    status=phase, reason=reason, timestamp=timestamp)

    LOG.warning(FMT, _event_data(action, phase, reason))


def info(action, phase=None, reason=None, timestamp=None):
    DB.DBEvent.dump(action.context, logging.INFO, action.entity, action,
                    status=phase, reason=reason, timestamp=timestamp)

    LOG.info(FMT, _event_data(action, phase, reason))


def debug(action, phase=None, reason=None, timestamp=None):
    DB.DBEvent.dump(action.context, logging.DEBUG, action.entity, action,
                    status=phase, reason=reason, timestamp=timestamp)

    LOG.debug(FMT, _event_data(action, phase, reason))
