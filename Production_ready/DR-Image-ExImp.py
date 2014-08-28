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

from __future__ import print_function

import os
import pyrax
import time

pyrax.set_setting("identity_type", "rackspace")
creds_file = os.path.expanduser("/root/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)
cs = pyrax.cloudservers
servers = cs.servers.list()
srv_dict = {}
print("Select a server from which an image will be created.")
for pos, srv in enumerate(servers):
    print("%s: %s" % (pos, srv.name))
    srv_dict[str(pos)] = srv.id
selection = None
while selection not in srv_dict:
    if selection is not None:
        print(" -- Invalid choice")
    selection = raw_input("Enter the number for your choice: ")

server_id = srv_dict[selection]
print()
nm = raw_input("Enter a name for the image: ")

img_id = cs.servers.create_image(server_id, nm)

print("Image '%s' is being created. Its ID is: %s" % (nm, img_id))
img = pyrax.cloudservers.images.get(img_id)
while img.status != "ACTIVE":
     time.sleep(60)
     img = pyrax.cloudservers.images.get(img_id)
     print ("...still waiting")

print("Image created.")

cf_dfw = pyrax.connect_to_cloudfiles("DFW")

cont = cf_dfw.create_container("Export")

cf_dfw.make_container_public("Export", ttl=900)

pyrax.set_default_region("IAD")

cf_iad = pyrax.connect_to_cloudfiles("IAD")

cont = cf_iad.create_container("Import")
cf_iad.make_container_public("Import", ttl=900)
imgs = pyrax.images
cf = pyrax.cloudfiles

print("You will need to select an image to export, and a Container into which "
        "the exported image will be placed.")
images = imgs.list(visibility="private")

print()
print("Select an image to export:")
for pos, image in enumerate(images):
    print("[%s] %s" % (pos, image.name))
snum = raw_input("Enter the number of the image you want to share: ")
if not snum:
    exit()
try:
    num = int(snum)
except ValueError:
    print("'%s' is not a valid number." % snum)
    exit()
if not 0 <= num < len(images):
    print("'%s' is not a valid image number." % snum)
    exit()
image = images[num]

conts = cf.list()
print()
print("Select the target container to place the exported image:")
for pos, cont in enumerate(conts):
    print("[%s] %s" % (pos, cont.name))
snum = raw_input("Enter the number of the container: ")
if not snum:
	exit()
try:
    num = int(snum)
except ValueError:
    print("'%s' is not a valid number." % snum)
    exit()
if not 0 <= num < len(conts):
    print("'%s' is not a valid container number." % snum)
    exit()
cont = conts[num]

task = imgs.export_task(image, cont)
print("Task ID=%s" % task.id)
print()
answer = raw_input("Do you want to track the task until completion? This may "
        "take several minutes. [y/N]: ")
if answer and answer[0].lower() == "y":
    pyrax.utils.wait_until(task, "status", ["success", "failure"],
            verbose=True, interval=30)

TURBOLIFT="turbolift -u davi5652 -a d0cf0ae5007b421ba7371d9a7c469953 --os-auth-url dfw clone -sc Export -tc Import -tr iad"
print("You will need an image file stored in a Cloud Files container.")
conts = cf_iad.list()
print()
print("Select the container containing the image to import:")
for pos, cont in enumerate(conts):
    print("[%s] %s" % (pos, cont.name))
snum = raw_input("Enter the number of the container: ")
if not snum:
    exit()
try:
    num = int(snum)
except ValueError:
    print("'%s' is not a valid number." % snum)
    exit()
if not 0 <= num < len(conts):
    print("'%s' is not a valid container number." % snum)
    exit()
cont = conts[num]

print()
print("Select the image object:")
objs = cont.get_objects()
for pos, obj in enumerate(objs):
    print("[%s] %s" % (pos, obj.name))
snum = raw_input("Enter the number of the image object: ")
if not snum:
    exit()
try:
    num = int(snum)
except ValueError:
    print("'%s' is not a valid number." % snum)
    exit()
if not 0 <= num < len(objs):
    print("'%s' is not a valid object number." % snum)
    exit()
obj = objs[num]

fmt = raw_input("Enter the format of the image [VHD]: ")
fmt = fmt or "VHD"
base_name = os.path.splitext(os.path.basename(obj.name))[0]
obj_name = raw_input("Enter a name for the imported image ['%s']: " % base_name)
obj_name = obj_name or base_name

task = imgs.import_task(obj, cont, img_format=fmt, img_name=obj_name)
print("Task ID=%s" % task.id)
print()
answer = raw_input("Do you want to track the task until completion? This may "
        "take several minutes. [y/N]: ")
if answer and answer[0].lower() == "y":
    pyrax.utils.wait_until(task, "status", ["success", "failure"],
            verbose=True, interval=30)
    print()
    if task.status == "success":
        print("Success!")
        print("Your new image:")
        new_img = imgs.find(name=obj_name)
        print(" ID: %s" % new_img.id)
        print(" Name: %s" % new_img.name)
        print(" Status: %s" % new_img.status)
        print(" Size: %s" % new_img.size)
        print(" Tags: %s" % new_img.tags)
    else:
        print("Image import failed!")
        print("Reason: %s" % task.message)
