from __future__ import print_function

import pyrax
import time
# Input cloud account information
un=raw_input('Enter your username : ')
API_Key=raw_input('Enter your API Key : ')
region=raw_input('What datacenter is your server in? : ').upper()
pyrax.set_setting("identity_type", "rackspace")
pyrax.set_credentials(un, API_Key)

cs_dfw = pyrax.connect_to_cloudservers(region="DFW")
cs_hkg = pyrax.connect_to_cloudservers(region="HKG")
cs_syd = pyrax.connect_to_cloudservers(region="SYD")
cs_ord = pyrax.connect_to_cloudservers(region="ORD")
cs_iad = pyrax.connect_to_cloudservers(region="IAD")
syd_servers = cs_syd.list()
hkg_servers = cs_hkg.list()
dfw_servers = cs_dfw.list()
ord_servers = cs_ord.list()
iad_servers = cs_iad.list()
all_servers = dfw_servers + ord_servers + iad_servers + hkg_servers + syd_servers
cf_hkg = pyrax.connect_to_cloudfiles("HKG")
cf_syd = pyrax.connect_to_cloudfiles("SYD")
cf_dfw = pyrax.connect_to_cloudfiles("DFW")
cf_iad = pyrax.connect_to_cloudfiles("IAD")
cf_ord = pyrax.connect_to_cloudfiles("ORD")
imgs_hkg = pyrax.connect_to_images("HKG")
imgs_syd = pyrax.connect_to_images("SYD")
imgs_dfw = pyrax.connect_to_images("DFW")
imgs_iad = pyrax.connect_to_images("IAD")
imgs_ord = pyrax.connect_to_images("ORD")

srv_dict = {}
if region == "SYD":
    print("Select a server from which an image will be created.")
    for pos, srv in enumerate(syd_servers):
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

    img_id = cs_syd.servers.create_image(server_id, nm)

    print("Image '%s' is being created. Its ID is: %s" % (nm, img_id))
    img = cs_syd.images.get(img_id)
    while img.status != "ACTIVE":
        time.sleep(60)
        img = cs_syd.images.get(img_id)
        print ("...still waiting")

    print("Image created.")
    cont = cf_syd.create_container("Export")
    cf_syd.make_container_public("Export", ttl=str(900))
    print("You will need to select an image to export, and a Container into which "
            "the exported image will be placed.")
    images = imgs_syd.list(visibility="private")

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
        num = int(snum)
    except ValueError:
        print("'%s' is not a valid number." % snum)
        exit()
    if not 0 <= num < len(images):
        print("'%s' is not a valid image number." % snum)
        exit()
    image = images[num]

    conts = cf_syd.list()
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

    task = imgs_syd.export_task(image, cont)
    print("Task ID=%s" % task.id)
    print()
    answer = raw_input("Do you want to track the task until completion? This may "
            "take several minutes. [y/N]: ")
    if answer and answer[0].lower() == "y":
        pyrax.utils.wait_until(task, "status", ["success", "failure"],
                verbose=True, interval=30)

if region == "HKG":
    print("Select a server from which an image will be created.")
    for pos, srv in enumerate(hkg_servers):
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

    img_id = cs_hkg.servers.create_image(server_id, nm)

    print("Image '%s' is being created. Its ID is: %s" % (nm, img_id))
    img = cs_iad.images.get(img_id)
    while img.status != "ACTIVE":
        time.sleep(60)
        img = cs_hkg.images.get(img_id)
        print ("...still waiting")

    print("Image created.")
    cont = cf_hkg.create_container("Export")
    cf_hkg.make_container_public("Export", ttl=str(900))
    print("You will need to select an image to export, and a Container into which "
            "the exported image will be placed.")
    images = imgs_hkg.list(visibility="private")

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
        num = int(snum)
    except ValueError:
        print("'%s' is not a valid number." % snum)
        exit()
    if not 0 <= num < len(images):
        print("'%s' is not a valid image number." % snum)
        exit()
    image = images[num]

    conts = cf_hkg.list()
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

    task = imgs_hkg.export_task(image, cont)
    print("Task ID=%s" % task.id)
    print()
    answer = raw_input("Do you want to track the task until completion? This may "
            "take several minutes. [y/N]: ")
    if answer and answer[0].lower() == "y":
        pyrax.utils.wait_until(task, "status", ["success", "failure"],
                verbose=True, interval=30)

if region == "DFW":
    print("Select a server from which an image will be created.")
    for pos, srv in enumerate(dfw_servers):
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

    img_id = cs_dfw.servers.create_image(server_id, nm)

    print("Image '%s' is being created. Its ID is: %s" % (nm, img_id))
    img = pyrax.cloudservers.images.get(img_id)
    while img.status != "ACTIVE":
        time.sleep(60)
        img = pyrax.cloudservers.images.get(img_id)
        print ("...still waiting")

    print("Image created.")
    cont = cf_dfw.create_container("Export")
    cf_dfw.make_container_public("Export", ttl=str(900))
    print("You will need to select an image to export, and a Container into which "
            "the exported image will be placed.")
    images = imgs_dfw.list(visibility="private")

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
        num = int(snum)
    except ValueError:
        print("'%s' is not a valid number." % snum)
        exit()
    if not 0 <= num < len(images):
        print("'%s' is not a valid image number." % snum)
        exit()
    image = images[num]

    conts = cf_dfw.list()
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

    task = imgs_dfw.export_task(image, cont)
    print("Task ID=%s" % task.id)
    print()
    answer = raw_input("Do you want to track the task until completion? This may "
            "take several minutes. [y/N]: ")
    if answer and answer[0].lower() == "y":
        pyrax.utils.wait_until(task, "status", ["success", "failure"],
                verbose=True, interval=30)

if region == "IAD":
    print("Select a server from which an image will be created.")
    for pos, srv in enumerate(iad_servers):
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

    img_id = cs_iad.servers.create_image(server_id, nm)

    print("Image '%s' is being created. Its ID is: %s" % (nm, img_id))
    img = cs_iad.images.get(img_id)
    while img.status != "ACTIVE":
        time.sleep(60)
        img = cs_iad.images.get(img_id)
        print ("...still waiting")

    print("Image created.")
    cont = cf_iad.create_container("Export")
    cf_iad.make_container_public("Export", ttl=str(900))
    print("You will need to select an image to export, and a Container into which "
            "the exported image will be placed.")
    images = imgs_iad.list(visibility="private")

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
        num = int(snum)
    except ValueError:
        print("'%s' is not a valid number." % snum)
        exit()
    if not 0 <= num < len(images):
        print("'%s' is not a valid image number." % snum)
        exit()
    image = images[num]

    conts = cf_iad.list()
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

    task = imgs_iad.export_task(image, cont)
    print("Task ID=%s" % task.id)
    print()
    answer = raw_input("Do you want to track the task until completion? This may "
            "take several minutes. [y/N]: ")
    if answer and answer[0].lower() == "y":
        pyrax.utils.wait_until(task, "status", ["success", "failure"],
                verbose=True, interval=30)

if region == "ORD":
    print("Select a server from which an image will be created.")
    for pos, srv in enumerate(ord_servers):
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

    img_id = cs_ord.servers.create_image(server_id, nm)

    print("Image '%s' is being created. Its ID is: %s" % (nm, img_id))
    img = cs_ord.images.get(img_id)
    while img.status != "ACTIVE":
        time.sleep(60)
        img = cs_ord.images.get(img_id)
        print ("...still waiting")

    print("Image created.")
    cont = cf_ord.create_container("Export")
    cf_ord.make_container_public("Export", ttl=str(900))
    print("You will need to select an image to export, and a Container into which "
            "the exported image will be placed.")
    images = imgs_ord.list(visibility="private")

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
        num = int(snum)
    except ValueError:
        print("'%s' is not a valid number." % snum)
        exit()
    if not 0 <= num < len(images):
        print("'%s' is not a valid image number." % snum)
        exit()
    image = images[num]

    conts = cf_ord.list()
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

    task = imgs_ord.export_task(image, cont)
    print("Task ID=%s" % task.id)
    print()
    answer = raw_input("Do you want to track the task until completion? This may "
            "take several minutes. [y/N]: ")
    if answer and answer[0].lower() == "y":
        pyrax.utils.wait_until(task, "status", ["success", "failure"],
                verbose=True, interval=30)
