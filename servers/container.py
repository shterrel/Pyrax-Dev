#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c)2012 Rackspace US, Inc.

# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import pyrax

pyrax.set_default_region("DFW")
pyrax.set_setting("identity_type", "rackspace")
pyrax.set_credential_file("/root/.rackspace_cloud_credentials")
# not needed
#cf = pyrax.cloudfiles
cf_dfw = pyrax.connect_to_cloudfiles("DFW")

# this was the problem
#cont = cf.create_container("Export")
cont = cf_dfw.create_container("Export")

cf_dfw.make_container_public("Export", ttl=900)

pyrax.set_default_region("IAD")

#cf = pyrax.cloudfiles
cf_iad = pyrax.connect_to_cloudfiles("IAD")

cont = cf_iad.create_container("Import")
cf_iad.make_container_public("Import", ttl=900)
