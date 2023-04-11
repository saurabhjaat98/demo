###############################################################################
# Copyright (c) 2022-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Manik Sidana <manik@coredge.io>, Feb 2023                        #
# Modified by Deepak Pant <deepak.pant@coredge.io>, Feb 2023                  #
###############################################################################
import json

from ccp_server.util.constants import Constants
from ccp_server.util.logger import KGLogger
from ccp_server.util.logger import log
LOG = KGLogger(__name__)


class TokenInfo(object):
    def __init__(self, user_info: dict):
        self._user_info = user_info
        self._preferred_username = None
        self._username = None
        self._name = None
        self._email = None
        self._realm = None
        self._domain = None
        self._realm_roles = []
        self._ccp_roles = []
        self._is_email_verified = None
        self._project_scope = None
        self._active = None
        self._profile_completed = None

    def _get_value(self, varname, key):
        try:
            if not varname:
                varname = self._user_info[key]
        except KeyError:
            LOG.warn(f'Cannot locate {key} key in token')
            varname = None
        finally:
            return varname

    @property
    def preferred_username(self):
        return self._get_value(self._preferred_username, 'preferred_username')

    @property
    @log
    def username(self):
        return self._get_value(self._username, 'email')

    @property
    def name(self):
        return self._get_value(self._name, 'name')

    @property
    def email(self):
        return self._get_value(self._email, 'email')

    @property
    def realm(self):
        return self._get_value(self._realm, 'realm')

    @property
    def domain(self):
        return self._get_value(self._domain, 'domain')

    @property
    def is_email_verified(self):
        return self._get_value(self._is_email_verified, 'email_verified')

    @property
    def active(self):
        return self._get_value(self._active, 'active')

    @property
    def realm_roles(self):
        try:
            self._realm_roles = self._user_info['realm_access']['roles'] or []
        except KeyError:
            LOG.warn(f'Cannot locate domain roles key in token')
            self._realm_roles = []
        finally:
            return self._realm_roles

    @property
    def project_scope(self):
        try:
            self._project_scope = self._user_info['project_scopes'] or []
        except KeyError:
            LOG.warn(f'Cannot locate project roles key in token')
            self._project_scope = []
        finally:
            return self._project_scope

    @property
    def ccp_roles(self):
        try:
            self._ccp_roles = self._user_info['resource_access'][Constants.KEYCLOAK_CLIENT_ID]['roles'] or [
            ]
        except KeyError:
            LOG.warn(f'Cannot locate CCP roles in token')
            self._ccp_roles = []
        finally:
            return self._ccp_roles

    @property
    def is_profile_completed(self):
        try:
            self._profile_completed = json.loads(
                self._user_info['profile_completed'])
            return self._profile_completed
        except Exception as e:
            LOG.warn(
                f'Cannot locate profile_complete in token due to {str(e)}')
            return False
