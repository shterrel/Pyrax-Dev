__author__ = 'davi5652'
import pyrax
import requests
import json


#API_Key = raw_input("Enter API Key: ")
#username = raw_input("Enter username:  ")
auth_token = raw_input("Enter Auth Token: ")

pyrax.set_setting("identity_type", "rackspace")
pyrax.set_default_region("DFW")
pyrax.set_credentials('asholty', 'd3351bf3d54dc52a9214a796cc3d46a9')

cs_dfw = pyrax.connect_to_cloudservers(region='DFW')
cs_iad = pyrax.connect_to_cloudservers(region='IAD')
cs_ord = pyrax.connect_to_cloudservers(region='ORD')
cf = pyrax.cloudfiles
cbs_dfw = pyrax.cloud_blockstorage
cdb = pyrax.cloud_databases
clb = pyrax.cloud_loadbalancers
dns = pyrax.cloud_dns
cnw = pyrax.cloud_networks

cslimits_iad = cs_iad.limits.get()
  # Convert the generator to a list
cslimits_iad_list = [rate for rate in cslimits_iad.absolute]
  # Pull out max_ram api limit and total used ram from list
max_ram_IAD = [x.value for x in cslimits_iad_list if x.name == "maxTotalRAMSize"][0]
total_ram_IAD = [x.value for x in cslimits_iad_list if x.name == "totalRAMUsed"][0]
#Get the percent ram used and round it up for clean output
percent_ram_IAD = (float(total_ram_IAD) / float(max_ram_IAD)) * 100
percent_ram_used_IAD = round(float(("%.2f" % percent_ram_IAD)))

print ("Datacenter - IAD cloudserver RAM limit: %s Mb" % max_ram_IAD)
print ("    total IAD Server RAM used: %s Mb" % total_ram_IAD)
print ("    total percent of RAM used: %s percentage " % percent_ram_used_IAD)

cslimits_ord = cs_ord.limits.get()
  # Convert the generator to a list
cslimits_ord_list = [rate for rate in cslimits_ord.absolute]
  # Pull out max_ram api limit and total used ram from list
max_ram_ord = [x.value for x in cslimits_ord_list if x.name == "maxTotalRAMSize"][0]
total_ram_ord = [x.value for x in cslimits_ord_list if x.name == "totalRAMUsed"][0]
#Get the percent ram used and round it up for clean output
percent_ram_ord = (float(total_ram_ord) / float(max_ram_ord)) * 100
percent_ram_used_ord = round(float(("%.2f" % percent_ram_ord)))

print ("Datacenter - ORD cloudserver RAM limit: %s Mb" % max_ram_ord)
print ("    total ORD Server RAM used: %s Mb" % total_ram_ord)
print ("    total percent of RAM used: %s percentage " % percent_ram_used_ord)


#IAD Cloud Block Storage Limits
headers_dfw = {'User-Agent': 'python-cinderclient','accept': 'application/json','X-Auth-Token': ("%s" % auth_token)}
r_iad = requests.get("https://iad.blockstorage.api.rackspacecloud.com/v1/914425/os-quota-sets/914425?usage=True",data=0, headers=headers_dfw)
data_iad = json.loads(r_iad.text)
iad_volumes_SSD = data_iad['quota_set']['volumes_SATA']
iad_gb_SATA = data_iad['quota_set']['gigabytes_SATA']
iad_gb_SSD = data_iad['quota_set']['gigabytes_SSD']
iad_snapshots = data_iad['quota_set']['snapshots']
iad_snapshots_SATA = data_iad['quota_set']['snapshots_SATA']
iad_snapshots_SSD = data_iad['quota_set']['snapshots_SSD']
iad_volumes = data_iad['quota_set']['volumes']
iad_volumes_SATA = data_iad['quota_set']['volumes_SATA']
iad_volumes_SSD = data_iad['quota_set']['volumes_SSD']

print ("Cloud Block Storage Usage IAD: ")
print ("    CBS volumes_SATA: %s" % iad_volumes_SSD)
print ("    CBS Gigabytes_SATA: %s" % iad_gb_SATA)
print ("    CBS Snapshots: %s" % iad_snapshots)
print ("    CBS Snapshots_SATA: %s" % iad_snapshots_SATA)
print ("    CBS Snapshots_SSD: %s" % iad_snapshots_SSD)
print ("    CBS Volumes: %s" % iad_volumes)
print ("    CBS Volumes_SATA: %s" % iad_volumes_SATA)
print ("    CBS Volumes_SSD: %s" % iad_volumes_SSD)

#ORD Cloud Block Storage Limits
headers_ord = {'User-Agent': 'python-cinderclient','accept': 'application/json','X-Auth-Token': ("%s" % auth_token)}
r_ord = requests.get("https://ord.blockstorage.api.rackspacecloud.com/v1/914425/os-quota-sets/914425?usage=True",data=0, headers=headers_ord)
data_ord = json.loads(r_ord.text)
ord_volumes_SSD = data_ord['quota_set']['volumes_SATA']
ord_gb_SATA = data_ord['quota_set']['gigabytes_SATA']
ord_gb_SSD = data_ord['quota_set']['gigabytes_SSD']
ord_snapshots = data_ord['quota_set']['snapshots']
ord_snapshots_SATA = data_ord['quota_set']['snapshots_SATA']
ord_snapshots_SSD = data_ord['quota_set']['snapshots_SSD']
ord_volumes = data_ord['quota_set']['volumes']
ord_volumes_SATA = data_ord['quota_set']['volumes_SATA']
ord_volumes_SSD = data_ord['quota_set']['volumes_SSD']

print ("Cloud Block Storage Usage ORD: ")
print ("    CBS volumes_SATA: %s" % ord_volumes_SSD)
print ("    CBS Gigabytes_SATA: %s" % ord_gb_SATA)
print ("    CBS Snapshots: %s" % ord_snapshots)
print ("    CBS Snapshots_SATA: %s" % ord_snapshots_SATA)
print ("    CBS Snapshots_SSD: %s" % ord_snapshots_SSD)
print ("    CBS Volumes: %s" % ord_volumes)
print ("    CBS Volumes_SATA: %s" % ord_volumes_SATA)
print ("    CBS Volumes_SSD: %s" % ord_volumes_SSD)

#ORD Cloud Loadbalancer Absolute limits
headers_lb_ord = {'accept': 'application/json','X-Auth-Token': ("%s" % auth_token)}
r_lb_ord = requests.get("https://ord.loadbalancers.api.rackspacecloud.com/v1.0/914425/loadbalancers/absolutelimits/",data=0, headers=headers_lb_ord)
data_lb_ord = json.loads(r_lb_ord.text)
ord_lb_IPV6_LIMIT = data_lb_ord['absolute'][0]
ord_lb_LOADBALANCER_LIMIT = data_lb_ord['absolute'][1]
ord_lb_BATCH_DELETE_LIMIT = data_lb_ord['absolute'][2]
ord_lb_ACCESS_LIST_LIMIT = data_lb_ord['absolute'][3]
ord_lb_NODE_LIMIT = data_lb_ord['absolute'][4]
ord_lb_NODE_META_LIMIT = data_lb_ord['absolute'][5]
ord_lb_LOADBALANCER_META_LIMIT = data_lb_ord['absolute'][6]
ord_lb_CERTIFICATE_MAPPING_LIMIT = data_lb_ord['absolute'][7]

print ("Cloud Loadbalancer Usage ORD: ")
print ("    %s" % ord_lb_IPV6_LIMIT)
print ("    %s" % ord_lb_LOADBALANCER_LIMIT)
print ("    %s" % ord_lb_BATCH_DELETE_LIMIT)
print ("    %s" % ord_lb_ACCESS_LIST_LIMIT)
print ("    %s" % ord_lb_NODE_LIMIT)
print ("    %s" % ord_lb_NODE_META_LIMIT)
print ("    %s" % ord_lb_LOADBALANCER_META_LIMIT)
print ("    %s" % ord_lb_CERTIFICATE_MAPPING_LIMIT)

#IAD Cloud Loadbalancer Absolute limits
headers_lb_iad = {'accept': 'application/json','X-Auth-Token': ("%s" % auth_token)}
r_lb_iad = requests.get("https://iad.loadbalancers.api.rackspacecloud.com/v1.0/914425/loadbalancers/absolutelimits/",data=0, headers=headers_lb_iad)
data_lb_iad = json.loads(r_lb_iad.text)
iad_lb_IPV6_LIMIT = data_lb_iad['absolute'][0]
iad_lb_LOADBALANCER_LIMIT = data_lb_iad['absolute'][1]
iad_lb_BATCH_DELETE_LIMIT = data_lb_iad['absolute'][2]
iad_lb_ACCESS_LIST_LIMIT = data_lb_iad['absolute'][3]
iad_lb_NODE_LIMIT = data_lb_iad['absolute'][4]
iad_lb_NODE_META_LIMIT = data_lb_iad['absolute'][5]
iad_lb_LOADBALANCER_META_LIMIT = data_lb_iad['absolute'][6]
iad_lb_CERTIFICATE_MAPPING_LIMIT = data_lb_iad['absolute'][7]

print ("Cloud Loadbalancer Usage IAD: ")
print ("    %s" % iad_lb_IPV6_LIMIT)
print ("    %s" % iad_lb_LOADBALANCER_LIMIT)
print ("    %s" % iad_lb_BATCH_DELETE_LIMIT)
print ("    %s" % iad_lb_ACCESS_LIST_LIMIT)
print ("    %s" % iad_lb_NODE_LIMIT)
print ("    %s" % iad_lb_NODE_META_LIMIT)
print ("    %s" % iad_lb_LOADBALANCER_META_LIMIT)
print ("    %s" % iad_lb_CERTIFICATE_MAPPING_LIMIT)
