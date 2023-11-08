#!/usr/bin/env python
# coding: utf-8

import os
import sys
import json
import html
import logging
import argparse
import requests
from requests.auth import HTTPBasicAuth
from os.path import exists


# change
def x(l, k, v): l[html.unescape(k)] = v


# is custom attribute being used by dictionary category
def isCustomAttributeValid(attribute, category):
    try:
        return len([binding for binding in attribute.get("rep").get("glossaryBindings") if binding.get("category") == category])>0
        
    except Exception as e:
        return False
        

# get all custom attributes defined in the dictionary 
def getAttributes(signavio):
    url = f"{signavio.get('host')}/p/meta"

    headers = {"x-signavio-id": signavio.get("authToken"), "accept":"application/json"}

    cookies = {"JSESSIONID": signavio.get("jsessionId"), "LBROUTEID": signavio.get("lbrouteId")}

    request = requests.get(url, headers=headers, cookies=cookies)

    return request.json()


# get all dictionary categories found in the dictionary
def getCategories(signavio):
    url = f"{signavio.get('host')}/p/glossarycategory?allCategories=true"

    headers = {"x-signavio-id": signavio.get("authToken"), "accept":"application/json"}

    cookies = {"JSESSIONID": signavio.get("jsessionId"), "LBROUTEID": signavio.get("lbrouteId")}

    request = requests.get(url, headers=headers, cookies=cookies)

    return request.json()


# add a dictionary entry with a given name and category
def addEntry(signavio, category, uuidAttribute, typeAttribute, hrefAttribute, collibra, asset):
    url = f"{signavio.get('host')}/p/glossary"

    headers = {"x-signavio-id": signavio.get("authToken"), "accept":"application/json", 'content-type': 'application/x-www-form-urlencoded'}

    cookies = {"JSESSIONID": signavio.get("jsessionId"), "LBROUTEID": signavio.get("lbrouteId")}

    metaDataValues= f"{{\"{uuidAttribute.get('rep').get('id')}\":\"{asset.get('id')}\", \"{typeAttribute.get('rep').get('id')}\":\"{asset.get('assetType')[0].get('assetTypeId')}\", \"{hrefAttribute.get('rep').get('id')}\":{{\"label\":\"\", \"url\":\"{collibra.get('host')}/asset/{asset.get('id')}\"}}}}"
    
    payload = f"title={asset.get('name')}&category={category.get('href').split('/')[-1]}&description={asset.get('description')[0].get('descriptionAttributeValue') if 'description' in asset else ''}&metaDataValues={metaDataValues}"
    
    request = requests.post(url, headers=headers, cookies=cookies, data=payload)

    return request.json()
    

# update a dictionary entry with a given name and category
def updateEntry(signavio, category, uuidAttribute, typeAttribute, hrefAttribute, collibra, asset):
    url = f"{signavio.get('host')}/p/glossary/{asset.get('href')[0].get('hrefAttributeValue').split('/')[-1]}/info"

    headers = {"x-signavio-id": signavio.get("authToken"), "accept":"application/json", 'content-type': 'application/x-www-form-urlencoded'}

    cookies = {"JSESSIONID": signavio.get("jsessionId"), "LBROUTEID": signavio.get("lbrouteId")}

    metaDataValues= f"{{\"{uuidAttribute.get('rep').get('id')}\":\"{asset.get('id')}\", \"{typeAttribute.get('rep').get('id')}\":\"{asset.get('assetType')[0].get('assetTypeId')}\", \"{hrefAttribute.get('rep').get('id')}\":{{\"label\":\"\", \"url\":\"{collibra.get('host')}/asset/{asset.get('id')}\"}}}}"

    payload = f"title={asset.get('name')}&category={category.get('href').split('/')[-1]}&description={asset.get('description')[0].get('descriptionAttributeValue') if 'description' in asset else ''}&metaDataValues={metaDataValues}"
    
    request = requests.put(url, headers=headers, cookies=cookies, data=payload)

    return request.json()
    

# get assets of type and status from a given community
def getAssets(collibra, communities, assetTypes, statuses, hrefAttributeType):
    viewConfig = {
        "ViewConfig": {
            "maxCountLimit": "-1",
            "Resources": {
                "Asset": {
                    "name": "Assets",
                    "Signifier": {
                        "name": "name"
                    },
                    "Id": {
                        "name": "id"
                    },
                    "AssetType": {
                        "name": "assetType",
                        "Id": {
                            "name": "assetTypeId"
                        }
                    },
                    "Status": {
                        "name": "assetStatus",
                        "Id": {
                            "name": "assetStatusId"
                        }
                    },
                    "Domain": {
                        "name": "assetDomain",
                        "Id": {
                            "name": "assetDomainId"
                        },
                        "Community": {
                            "name": "assetCommunity",
                            "Id": {
                                "name": "assetCommunityId"
                            }
                        }
                    },
                    "StringAttribute": [
                        {
                            "name": "description",
                            "labelId": "00000000-0000-0000-0000-000000003114",
                            "Id": {
                                "name": "descriptionAttributeId"
                            },
                            "LongExpression": {
                                "name": "descriptionAttributeValue"
                            }
                        },
                        {
                            "name": "href",
                            "labelId": hrefAttributeType,
                            "Id": {
                                "name": "hrefAttributeId"
                            },
                            "LongExpression": {
                                "name": "hrefAttributeValue"
                            }
                        }  
                    ],
                    "Filter": {
                        "AND": [
                            {
                                "Field": {
                                    "name": "assetCommunityId",
                                    "operator": "IN", 
                                    "values": [community.get("id") for community in communities],
                                    "descendants": "true"
                                }                                
                            },
                            {
                                "Field": {
                                    "name": "assetTypeId",
                                    "operator": "IN", 
                                    "values": [assetType.get("id") for assetType in assetTypes]
                                }                                
                            },
                            {
                                "Field": {
                                    "name": "assetStatusId",
                                    "operator": "IN",
                                    "value": [status.get("id") for status in statuses]
                                }
                            }
                        ]
                    }              
                }
            }
        }
    }
 
    response = collibra.get("session").post(f"{collibra.get('endpoint')}/outputModule/export/json?validationEnabled=false", json=viewConfig)

    return response.json().get("view").get("Assets") if "view" in response.json() else []


# logger
logger = logging.getLogger()

logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stderr)

formatter = logging.Formatter('%(levelname)s: %(message)s ')

handler.setFormatter(formatter)

logger.handlers = [handler]


# arg parser
parser = argparse.ArgumentParser()

parser.add_argument(
    "--config",
    dest="config",
    required=True,
    help="configuration file (json)")

args, options= parser.parse_known_args(sys.argv)
    
if not exists(args.config): 
    logger.error(f"{__file__.split('/')[-1]}: error: the following arguments are required: --config")
    logger.error('[parser] Something went wrong. Please try again.')
    exit(-1)


# get config file
logger.info('get config file')

with open(args.config, "r") as f:
    config = json.load(f)


# reset logger
logger.setLevel(config.get("logger").get("level"))

formatter = logging.Formatter(config.get("logger").get("formatter"))

handler.setFormatter(formatter)


# connect to collibra                  
logger.info('connect to collibra')

collibra = config.get("collibra")

collibra["endpoint"] = f"{collibra['host']}/rest/2.0"

collibra = {"host": collibra.get("host"), "endpoint": collibra.get("endpoint"), "username": collibra.get("username"), "password": collibra.get("password")}

collibra["endpoint"] = f"{collibra['host']}/rest/2.0"

collibra = {"host": collibra.get("host"), "endpoint": collibra.get("endpoint"), "username": collibra.get("username"), "password": collibra.get("password")}

collibra["session"] = requests.Session()
    
collibra.get("session").auth = HTTPBasicAuth(collibra.get("username"), collibra.get("password"))


# get the collibra asset types
logger.info('get the collibra asset types')

assetTypes = {}

try:
    response = collibra.get("session").get(f"{collibra.get('endpoint')}/assetTypes")

    _=[x(assetTypes, assetType.get("name"), assetType) for assetType in response.json()["results"]] 

except Exception as e:
    logger.error(e.message)
    logger.error('[assetTypes] Something went wrong. Please try again.')
    exit(-1)


# get the collibra attribute types
logger.info('get the collibra attribute types')

attributeTypes = {}

try:
    response = collibra.get("session").get(f"{collibra.get('endpoint')}/attributeTypes")

    _=[x(attributeTypes, attributeType.get("name"), attributeType) for attributeType in response.json()["results"]]

except Exception as e:
    logger.error(e.message)
    logger.error('[attributeTypes] Something went wrong. Please try again.')
    exit(-1)


# get the collibra statuses
logger.info('get the collibra statuses')

statuses = {}

try:
    response = collibra.get("session").get(f"{collibra.get('endpoint')}/statuses")

    _=[x(statuses, status.get("name"), status) for status in response.json()["results"]]

except Exception as e:
    logger.error(e.message)
    logger.error('[statuses] Something went wrong. Please try again.')
    exit(-1)


# get the collibra communities
logger.info('get the collibra communities')

communities = {}

try:
    response = collibra.get("session").get(f"{collibra.get('endpoint')}/communities")

    _=[x(communities, community.get("name"), community) for community in response.json()["results"]]

except Exception as e:
    logger.error(e.message)
    logger.error('[communities] Something went wrong. Please try again.')
    exit(-1)


# choose collibra communities to query
logger.info('choose collibra communities to query')

communitiesToQuery = [communities.get(community) for community in config.get("collibra").get("communitiesToQuery") if communities.get(community)] 

if not communitiesToQuery:
    logger.error(f"{__file__.split('/')[-1]}: error: missing collibra:communitiesToQuery or no community found")
    logger.error('[communities] Something went wrong. Please try again.')
    exit(-1)


# choose the collibra asset types to list
logger.info('choose the collibra asset types to list')

assetTypesToGet = [assetTypes.get(assetType) for assetType in config.get("collibra").get("assetTypesToGet") if assetTypes.get(assetType)] 

if not assetTypesToGet:
    logger.error(f"{__file__.split('/')[-1]}: error: missing collibra:assetTypesToGet or no asset type found")
    logger.error('[assetTypes] Something went wrong. Please try again.')
    exit(-1)


# choose the collibra status types to include
logger.info('choose the collibra status types to include')

statusTypesToGet = [statuses.get(status) for status in config.get("collibra").get("statusTypesToGet") if statuses.get(status)] 

if not statusTypesToGet:
    logger.error(f"{__file__.split('/')[-1]}: error: missing collibra:statusTypesToGet or no status found")
    logger.error('[statuses] Something went wrong. Please try again.')
    exit(-1)


# choose the collibra attribute holding the signavio model references
logger.info('choose the collibra attribute holding the signavio model references')

signavioHrefAttributeToSet = attributeTypes.get(config.get("collibra").get("signavioHrefAttributeToSet"))

if not signavioHrefAttributeToSet:
    logger.error(f"{__file__.split('/')[-1]}: error: missing collibra:signavioHrefAttributeToSet or no attribute found")
    logger.error('[attributeTypes] Something went wrong. Please try again.')
    exit(-1)


# get assets of a given list of types and statuses found within a list of communities
assetsToCreate = []

assetsToUpdate = []

try:
    _=[assetsToUpdate.append(asset) if "href" in asset else assetsToCreate.append(asset) for asset in getAssets(collibra, communitiesToQuery, assetTypesToGet, statusTypesToGet, signavioHrefAttributeToSet.get("id"))]

except Exception as e:
    logger.error(e.message)
    logger.error('[communities] Something went wrong. Please try again.')
    exit(-1)



# connect to signavio
logger.info('connect to signavio')

signavio = config.get("signavio")

try:
    url = f"{signavio.get('host')}/p/login"

    data = {"name": signavio.get("username"), "password": signavio.get("password"), "tenant": signavio.get("tenant"), "tokenonly": "true"}

    request = requests.post(url, data)

    authToken = request.content.decode("utf-8")

    jsessionId = request.cookies.get("JSESSIONID")

    lbrouteId = request.cookies.get("LBROUTEID")

    signavio = {"host": signavio.get("host"), "tenant": signavio.get("tenant"), "authToken": authToken, "jsessionId": jsessionId, "lbrouteId": lbrouteId}

except Exception as e:
    logger.error(e.message)
    logger.error('[communities] Something went wrong. Please try again.')
    exit(-1)


# get all signavio dictionary categories
categories = {}

try:
    _=[x(categories, category.get("rep").get("name"), category) for category in getCategories(signavio) if category.get("rel") == "cat"]

except Exception as e:
    logger.error(e.message)
    logger.error('[glossarycategory] Something went wrong. Please try again.')
    exit(-1)


# choose the signavio dictionary category to map
logger.info('choose the signavio dictionary category to map')

categoryToUpdate = categories.get(config.get("signavio").get("categoryToUpdate"))

if not categoryToUpdate:
    logger.error(f"{__file__.split('/')[-1]}: error: missing signavio:categoryToUpdate or no attribute found")
    logger.error('[glossarycategory] Something went wrong. Please try again.')
    exit(-1)


# get the custom attributes used by the signavio category 
attributes = {}

try:
    _=[x(attributes, asset.get("rep").get("name"), asset) for asset in getAttributes(signavio) if isCustomAttributeValid(asset, categoryToUpdate.get("href").split("/")[-1])]
    
except Exception as e:
    logger.error(e.message)
    logger.error('[meta] Something went wrong. Please try again.')
    exit(-1)


# choose the custom attribute which will hold the collibra asset id
logger.info('choose the custom attribute which will hold the collibra asset id')

uuidAttributeToSet = attributes.get(config.get("signavio").get("uuidAttributeToSet"))

if not uuidAttributeToSet:
    logger.error(f"{__file__.split('/')[-1]}: error: missing signavio:uuidAttributeToSet or no attributes found")
    logger.error('[meta] Something went wrong. Please try again.')
    exit(-1)


# choose the custom attribute which will hold the collibra asset type id
logger.info('choose the custom attribute which will hold the collibra asset type id')

typeAttributeToSet = attributes.get(config.get("signavio").get("typeAttributeToSet"))

if not typeAttributeToSet:
    logger.error(f"{__file__.split('/')[-1]}: error: missing signavio:typeAttributeToSet or no attributes found")
    logger.error('[meta] Something went wrong. Please try again.')
    exit(-1)
    

# choose the custom attribute which will hold the collibra asset url for reference
logger.info('choose the custom attribute which will hold the collibra asset url for reference')

hrefAttributeToSet = attributes.get(config.get("signavio").get("hrefAttributeToSet"))

if not hrefAttributeToSet:
    logger.error(f"{__file__.split('/')[-1]}: error: missing signavio:hrefAttributeToSet or no attributes found")
    logger.error('[meta] Something went wrong. Please try again.')
    exit(-1)



# create dictionary items when no href attribute set is found, list dictionary items which fail to create
try:
    entriesCreated = [addEntry(signavio, categoryToUpdate, uuidAttributeToSet, typeAttributeToSet, hrefAttributeToSet, collibra, asset) for asset in assetsToCreate]

    entriesThatFailed = [entry for entry in entriesCreated if 'errors' in entry]

except Exception as e:
    logger.error(e.message)
    logger.error('[glossary] Something went wrong. Please try again.')
    exit(-1)



# update collibra, when the href attribute set is found, build payload with all href attributes to add
def p(entry, uuidAttribute, attributeType): 
    return {"assetId": entry.get("rep").get("metaDataValues").get(uuidAttribute), "typeId": attributeType, "value": f"dictionary/entry/{entry.get('rep').get('id')}"}

try:
    payload = [p(entry, uuidAttributeToSet.get("rep").get("id"), signavioHrefAttributeToSet.get("id")) for entry in entriesCreated if "rep" in entry]
    
    response = collibra.get("session").post(f"{collibra.get('endpoint')}/attributes/bulk", json=payload)

except Exception as e:
    logger.error(e.message)
    logger.error('[attributes] Something went wrong. Please try again.')
    exit(-1)


# update dictionary items when href attribute set is found, list dictionary items which fail to update
try:
    entriesUpdated = [updateEntry(signavio, categoryToUpdate, uuidAttributeToSet, typeAttributeToSet, hrefAttributeToSet, collibra, asset) for asset in assetsToUpdate]
                                
    entriesThatFailed = [entry for entry in entriesUpdated if 'errors' in entry]

except Exception as e:
    logger.error(e.message)
    logger.error('[glossary] Something went wrong. Please try again.')
    exit(-1)


logger.info('done')

exit(0)