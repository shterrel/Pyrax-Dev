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
