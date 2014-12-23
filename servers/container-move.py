
import os
import sys
import pyrax
import pyrax.exceptions as exc
import pyrax.utils as utils

pyrax.set_setting("identity_type", "rackspace")
creds_file = os.path.expanduser("/root/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)
#cf = pyrax.cloudfiles

cf_dfw = pyrax.connect_to_cloudfiles("DFW")
oldcont = cf_dfw.get_container("Export")

cf_iad = pyrax.connect_to_cloudfiles("IAD")
newcont = cf_iad.get_container("Import")
objects = oldcont.get_objects()
counter = 0
for obj in objects:
 cf_dfw.move_object(oldcont, obj.name, newcont)
 counter += 1
 print "[%d] %s moved from %s to %s" % (counter, obj.name, oldcont.name, newcont.name
