from __future__ import print_function

import os
import pyrax
import time

# Input cloud account information
un=raw_input('Enter your username : ')
API_Key=raw_input('Enter your API Key : ')
region=raw_input('What datacenter is your server in? : ').upper()
pyrax.set_setting("identity_type", "rackspace")
pyrax.set_credentials(un, API_Key)


cs_dfw = pyrax.connect_to_cloudservers(region="DFW")
cs_ord = pyrax.connect_to_cloudservers(region="ORD")
cs_iad = pyrax.connect_to_cloudservers(region="IAD")
dfw_servers = cs_dfw.list()
ord_servers = cs_ord.list()
iad_servers = cs_iad.list()
all_servers = dfw_servers + ord_servers + iad_servers
cf_dfw = pyrax.connect_to_cloudfiles("DFW")
cf_iad = pyrax.connect_to_cloudfiles("IAD")
cf_ord = pyrax.connect_to_cloudfiles("ORD")
imgs_dfw = pyrax.connect_to_images("DFW")
imgs_iad = pyrax.connect_to_images("IAD")
imgs_ord = pyrax.connect_to_images("ORD")

if region == "IAD":
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

    task = imgs_iad.import_task(obj, cont, img_format=fmt, img_name=obj_name)
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
            new_img = imgs_iad.find(name=obj_name)
            print(" ID: %s" % new_img.id)
            print(" Name: %s" % new_img.name)
            print(" Status: %s" % new_img.status)
            print(" Size: %s" % new_img.size)
            print(" Tags: %s" % new_img.tags)
        else:
            print("Image import failed!")
            print("Reason: %s" % task.message)

if region == "DFW":
    print("You will need an image file stored in a Cloud Files container.")
    conts = cf_dfw.list()
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

    task = imgs_dfw.import_task(obj, cont, img_format=fmt, img_name=obj_name)
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
            new_img = imgs_iad.find(name=obj_name)
            print(" ID: %s" % new_img.id)
            print(" Name: %s" % new_img.name)
            print(" Status: %s" % new_img.status)
            print(" Size: %s" % new_img.size)
            print(" Tags: %s" % new_img.tags)
        else:
            print("Image import failed!")
            print("Reason: %s" % task.message)

if region == "ORD":
    print("You will need an image file stored in a Cloud Files container.")
    conts = cf_ord.list()
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

    task = imgs_ord.import_task(obj, cont, img_format=fmt, img_name=obj_name)
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
            new_img = imgs_ord.find(name=obj_name)
            print(" ID: %s" % new_img.id)
            print(" Name: %s" % new_img.name)
            print(" Status: %s" % new_img.status)
            print(" Size: %s" % new_img.size)
            print(" Tags: %s" % new_img.tags)
        else:
            print("Image import failed!")
            print("Reason: %s" % task.message)
