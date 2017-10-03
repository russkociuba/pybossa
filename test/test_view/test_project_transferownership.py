# -*- coding: utf8 -*-
# This file is part of PYBOSSA.
#
# Copyright (C) 2017 Scifabric 
#
# PYBOSSA is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PYBOSSA is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with PYBOSSA.  If not, see <http://www.gnu.org/licenses/>.
from default import db, with_context
from factories import ProjectFactory, UserFactory
from helper import web
from pybossa.repositories import UserRepository, ProjectRepository
import json

project_repo = ProjectRepository(db)
user_repo = UserRepository(db)

class TestProjectTransferOwnership(web.Helper):

    @with_context
    def test_transfer_anon_get(self):
        """Test transfer ownership page is not shown to anon."""
        project = ProjectFactory.create()
        url = '/project/%s/transferownership' % project.short_name
        res = self.app_get_json(url, follow_redirects=True)
        assert 'signin' in res.data, res.data

    @with_context
    def test_transfer_auth_not_owner_get(self):
        """Test transfer ownership page is forbidden for not owner."""
        admin, owner, user = UserFactory.create_batch(3)
        project = ProjectFactory.create(owner=owner)
        url = '/project/%s/transferownership?api_key=%s' % (project.short_name,
                                                            user.api_key)
        res = self.app_get_json(url, follow_redirects=True)
        data = json.loads(res.data)
        assert data['code'] == 403, data
