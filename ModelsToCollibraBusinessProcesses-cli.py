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
def x(l, k, v):
    l[html.unescape(k)] = v


# search signavio
def search(signavio, q, limit=None, offset=None, types=None):
    try:
        url = f"{signavio.get('host')}/p/search?q={q}"

        url = f"{url}&limit={limit}" if limit is not None else f"{url}"

        url = f"{url}&offset={offset}" if offset is not None else f"{url}"

        url = (
            f"{url}{''.join([f'&types={t}' for t in types])}"
            if types is not None
            else f"{url}"
        )

        headers = {
            "x-signavio-id": signavio.get("authToken"),
            "accept": "application/json",
        }

        cookies = {
            "JSESSIONID": signavio.get("jsessionId"),
            "LBROUTEID": signavio.get("lbrouteId"),
        }

        request = requests.get(url, headers=headers, cookies=cookies)

        return request.json()

    except Exception as e:
        return e


# get a signavio folder
def getFolder(signavio, folder):
    try:
        url = f"{signavio.get('host')}/p{folder.get('href')}"

        headers = {
            "x-signavio-id": signavio.get("authToken"),
            "accept": "application/json",
        }

        cookies = {
            "JSESSIONID": signavio.get("jsessionId"),
            "LBROUTEID": signavio.get("lbrouteId"),
        }

        request = requests.get(url, headers=headers, cookies=cookies)

        return request.json()

    except Exception as e:
        return e


# check if a given signavio folder is valid
def isFolderValid(folder):
    result = True

    try:
        result = False if folder.get("rel") != "dir" else result

        result = False if folder.get("rep").get("deleted") == True else result

        result = False if folder.get("rep").get("visible") != True else result

        return result

    except Exception as e:
        return False


# get a signavio model
def getModel(signavio, model):
    try:
        url = f"{signavio.get('host')}/p{model.get('href')}"

        headers = {
            "x-signavio-id": signavio.get("authToken"),
            "accept": "application/json",
        }

        cookies = {
            "JSESSIONID": signavio.get("jsessionId"),
            "LBROUTEID": signavio.get("lbrouteId"),
        }

        request = requests.get(url, headers=headers, cookies=cookies)

        return request.json()

    except Exception as e:
        return e


# get the properties of a signavio model
def getModelProperties(signavio, model):
    try:
        url = f"{signavio.get('host')}/p{'/'.join(model.get('href').split('/')[0:-1])}/json"

        headers = {
            "x-signavio-id": signavio.get("authToken"),
            "accept": "application/json",
        }

        cookies = {
            "JSESSIONID": signavio.get("jsessionId"),
            "LBROUTEID": signavio.get("lbrouteId"),
        }

        request = requests.get(url, headers=headers, cookies=cookies)

        return request.json().get("properties")

    except Exception as e:
        return e


# get the network graphics of a signavio model
def getModelPng(signavio, model):
    try:
        url = f"{signavio.get('host')}/p{'/'.join(model.get('href').split('/')[0:-1])}/png"

        headers = {
            "x-signavio-id": signavio.get("authToken"),
            "content-type": "image/png;charset=utf-8",
        }

        cookies = {
            "JSESSIONID": signavio.get("jsessionId"),
            "LBROUTEID": signavio.get("lbrouteId"),
        }

        request = requests.get(url, headers=headers, cookies=cookies)

        return request.content

    except Exception as e:
        return e


# get the vector graphics of a signavio model
def getModelSvg(signavio, model):
    try:
        url = f"{signavio.get('host')}/p{'/'.join(model.get('href').split('/')[0:-1])}/svg"

        headers = {
            "x-signavio-id": signavio.get("authToken"),
            "content-type": "image/svg+xml;charset=utf-8",
        }

        cookies = {
            "JSESSIONID": signavio.get("jsessionId"),
            "LBROUTEID": signavio.get("lbrouteId"),
        }

        request = requests.get(url, headers=headers, cookies=cookies)

        return request.content

    except Exception as e:
        return e


# get the linked models of a signavio model
def getModelLinks(signavio, model):
    try:
        url = f"{signavio.get('host')}/p{'/'.join(model.get('href').split('/')[0:-1])}/link"

        headers = {
            "x-signavio-id": signavio.get("authToken"),
            "accept": "application/json",
        }

        cookies = {
            "JSESSIONID": signavio.get("jsessionId"),
            "LBROUTEID": signavio.get("lbrouteId"),
        }

        request = requests.get(url, headers=headers, cookies=cookies)

        return request.json()

    except Exception as e:
        return e


# get the dictionary items of a signavio model
def getModelDictionary(signavio, model):
    try:
        url = f"{signavio.get('host')}/p{'/'.join(model.get('href').split('/')[0:-1])}/glossaryinfo"

        headers = {
            "x-signavio-id": signavio.get("authToken"),
            "accept": "application/json",
        }

        cookies = {
            "JSESSIONID": signavio.get("jsessionId"),
            "LBROUTEID": signavio.get("lbrouteId"),
        }

        request = requests.get(url, headers=headers, cookies=cookies)

        return request.json()

    except Exception as e:
        return e


# get the comments of a signavio model
def getModelComments(signavio, model):
    try:
        url = f"{signavio.get('host')}/p{'/'.join(model.get('href').split('/')[0:-1])}/comments"

        headers = {
            "x-signavio-id": signavio.get("authToken"),
            "accept": "application/json",
        }

        cookies = {
            "JSESSIONID": signavio.get("jsessionId"),
            "LBROUTEID": signavio.get("lbrouteId"),
        }

        request = requests.get(url, headers=headers, cookies=cookies)

        return request.json()

    except Exception as e:
        return e


# get a signavio model info given a href
def getModelInfo(signavio, href):
    try:
        url = f"{signavio.get('host')}/p{href}/info"

        headers = {
            "x-signavio-id": signavio.get("authToken"),
            "accept": "application/json",
        }

        cookies = {
            "JSESSIONID": signavio.get("jsessionId"),
            "LBROUTEID": signavio.get("lbrouteId"),
        }

        request = requests.get(url, headers=headers, cookies=cookies)

        return request.json()

    except Exception as e:
        return e


# get a signavio model json given a href
def getModelJson(signavio, href):
    try:
        url = f"{signavio.get('host')}/p{href}/json"

        headers = {
            "x-signavio-id": signavio.get("authToken"),
            "accept": "application/json",
        }

        cookies = {
            "JSESSIONID": signavio.get("jsessionId"),
            "LBROUTEID": signavio.get("lbrouteId"),
        }

        request = requests.get(url, headers=headers, cookies=cookies)

        return request.json()

    except Exception as e:
        return e


# check if a given signavio model is valid
def isModelValid(
    model, modelType=None, deployedOnly=False, approvedOnly=False, publishedOnly=False
):
    result = True

    try:
        result = False if model.get("rel") != "mod" else result

        result = False if model.get("rep").get("deleted") == True else result

        result = (
            False if model.get("rep").get("status").get(
                "deleted") == True else result
        )

        if deployedOnly:
            result = False if model.get("rep").get(
                "isDeployed") == False else result

        if approvedOnly:
            result = (
                False
                if model.get("rep").get("status").get("approve") == False
                else result
            )

        if publishedOnly:
            result = (
                False
                if model.get("rep").get("status").get("publish") == False
                else result
            )

        if modelType is not None:
            result = False if model.get("rep").get(
                "type") not in modelType else result

        return result

    except Exception as e:
        return False


# update a model given a new model revision
def updateModel(signavio, asset):
    url = f"{signavio.get('host')}/p{asset.get('href')}"

    data = {
        "name": asset.get("name"),
        "json_xml": str(asset.get("json")).encode("utf-8"),
        "parent": asset.get("info").get("parent"),
        "comment": "updated",
    }

    headers = {
        "x-signavio-id": signavio.get("authToken"),
        "accept": "application/json",
        "content-type": "application/x-www-form-urlencoded",
    }

    cookies = {
        "JSESSIONID": signavio.get("jsessionId"),
        "LBROUTEID": signavio.get("lbrouteId"),
    }

    request = requests.put(url, headers=headers, cookies=cookies, data=data)

    return request.json()


# get all custom attributes defined in the dictionary
def getattributes(signavio):
    url = f"{signavio.get('host')}/p/meta"

    headers = {
        "x-signavio-id": signavio.get("authToken"), "accept": "application/json"}

    cookies = {
        "JSESSIONID": signavio.get("jsessionId"),
        "LBROUTEID": signavio.get("lbrouteId"),
    }

    request = requests.get(url, headers=headers, cookies=cookies)

    return request.json()


# get a dictionary entry from the dictionary
def getEntry(signavio, entry):
    url = f"{signavio.get('host')}/p{entry}/info"

    headers = {
        "x-signavio-id": signavio.get("authToken"), "accept": "application/json"}

    cookies = {
        "JSESSIONID": signavio.get("jsessionId"),
        "LBROUTEID": signavio.get("lbrouteId"),
    }

    request = requests.get(url, headers=headers, cookies=cookies)

    return request.json()


# get all dictionary categories found in the dictionary
def getcategories(signavio):
    url = f"{signavio.get('host')}/p/glossarycategory?allCategories=true"

    headers = {
        "x-signavio-id": signavio.get("authToken"), "accept": "application/json"}

    cookies = {
        "JSESSIONID": signavio.get("jsessionId"),
        "LBROUTEID": signavio.get("lbrouteId"),
    }

    request = requests.get(url, headers=headers, cookies=cookies)

    return request.json()


# get assets of type and name
def getAssets(collibra, assetTypes, assetNames, hrefAttributeType):
    viewConfig = {
        "ViewConfig": {
            "maxCountLimit": "-1",
            "Resources": {
                "Asset": {
                    "name": "Assets",
                    "Id": {"name": "assetId"},
                    "Signifier": {"name": "assetName"},
                    "AssetType": {"name": "assetType", "Id": {"name": "assetTypeId"}},
                    "Status": {"name": "assetStatus", "Id": {"name": "assetStatusId"}},
                    "Domain": {"name": "assetDomain", "Id": {"name": "assetDomainId"}},
                    "StringAttribute": [
                        {
                            "name": "href",
                            "labelId": hrefAttributeType,
                            "LongExpression": {"name": "hrefValue"},
                        }
                    ],
                    "Filter": {
                        "AND": [
                            {
                                "Field": {
                                    "name": "assetTypeId",
                                    "operator": "IN",
                                    "values": [
                                        assetType.get("id") for assetType in assetTypes
                                    ],
                                }
                            },
                            {
                                "Field": {
                                    "name": "assetName",
                                    "operator": "IN",
                                    "value": [name for name in assetNames],
                                }
                            },
                        ]
                    },
                }
            },
        }
    }

    response = collibra.get("session").post(
        f"{collibra.get('endpoint')}/outputModule/export/json?validationEnabled=false",
        json=viewConfig,
    )

    return response.json().get("view").get("Assets")


# save attachment
def save(collibra, assetId, data, fileType):
    with open(f"{assetId}.{fileType}", "wb") as f:
        f.write(data)

    file = open(f"{assetId}.{fileType}", "rb").read()

    files = {"file": file}

    payload = {
        "fileName": f"{assetId}.{fileType}",
        "resourceType": "Asset",
        "resourceId": assetId,
    }

    response = collibra.get("session").post(
        f"{collibra.get('endpoint')}/attachments", files=files, data=payload
    )

    os.remove(f"{assetId}.{fileType}")

    return response.json()


# logger
logger = logging.getLogger()

logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stderr)

formatter = logging.Formatter("%(levelname)s: %(message)s ")

handler.setFormatter(formatter)

logger.handlers = [handler]


# arg parser
parser = argparse.ArgumentParser()

parser.add_argument(
    "--config", dest="config", required=True, help="configuration file (json)"
)

args, options = parser.parse_known_args(sys.argv)

if not exists(args.config):
    logger.error(
        f"{__file__.split('/')[-1]}: error: the following arguments are required: --config"
    )
    logger.error("[parser] Something went wrong. Please try again.")
    exit(-1)

# get config file
logger.info("get config file")

with open(args.config, "r") as f:
    config = json.load(f)


# reset logger
logger.setLevel(config.get("logger").get("level"))

formatter = logging.Formatter(config.get("logger").get("formatter"))

handler.setFormatter(formatter)

# connect to signavio
logger.info("connect to signavio")

signavio = config.get("signavio")

try:
    url = f"{signavio.get('host')}/p/login"

    data = {
        "name": signavio.get("username"),
        "password": signavio.get("password"),
        "tenant": signavio.get("tenant"),
        "tokenonly": "true",
    }

    request = requests.post(url, data)

    authToken = request.content.decode("utf-8")

    jsessionId = request.cookies.get("JSESSIONID")

    lbrouteId = request.cookies.get("LBROUTEID")

    signavio = {
        "host": signavio.get("host"),
        "tenant": signavio.get("tenant"),
        "authToken": authToken,
        "jsessionId": jsessionId,
        "lbrouteId": lbrouteId,
    }

except Exception as e:
    logger.error(e.message)
    logger.error("[login] Something went wrong. Please try again.")
    exit(-1)


# get all the signavio folders
logger.info("get all signavio folders")

folders = {}

try:
    _ = [
        x(folders, folder.get("rep").get("name"), folder)
        for folder in search(signavio, q="*", types=["DIR"])
        if isFolderValid(folder)
    ]

except Exception as e:
    logger.error(e.message)
    logger.error("[login] Something went wrong. Please try again.")
    exit(-1)


# get the signavio folders to query
logger.info("get the signavio folders to query")

foldersToQuery = []

try:
    foldersToQuery = [
        getFolder(signavio, folders.get(folder))
        for folder in config.get("signavio").get("foldersToQuery")
        if folders.get(folder)
    ]

except Exception as e:
    logger.error(e.message)
    logger.error("[folders] Something went wrong. Please try again.")
    exit(-1)

if not foldersToQuery:
    logger.error(
        f"{__file__.split('/')[-1]}: error: missing signavio:foldersToQuery or no folders found"
    )
    logger.error("[folders] Something went wrong. Please try again.")
    exit(-1)


# get the custom attributes used by the signavio category
logger.info("get the custom attributes used by the signavio category")

attributes = {}

try:
    _ = [
        x(attributes, attribute.get("rep").get("name"), attribute)
        for attribute in getattributes(signavio)
    ]

except Exception as e:
    logger.error(e.message)
    logger.error("[meta] Something went wrong. Please try again.")
    exit(-1)


# choose the custom attribute holding the consuming data assets
logger.info("choose the custom attribute holding the consuming data assets")

consumesAttributeToGet = attributes.get(
    config.get("signavio").get("consumesAttributeToGet")
)

if not consumesAttributeToGet:
    logger.error(
        f"{__file__.split('/')[-1]}: error: missing signavio:consumesAttributeToGet or no attributes found"
    )
    logger.error("[meta] Something went wrong. Please try again.")
    exit(-1)


# choose the custom attribute holding the producing data assets
logger.info("choose the custom attribute holding the producing data assets")

producesAttributeToGet = attributes.get(
    config.get("signavio").get("producesAttributeToGet")
)

if not producesAttributeToGet:
    logger.error(
        f"{__file__.split('/')[-1]}: error: missing signavio:producesAttributeToGet or no attributes found"
    )
    logger.error("[meta] Something went wrong. Please try again.")
    exit(-1)


# choose the custom attribute which will hold the collibra asset id
logger.info("choose the custom attribute which will hold the collibra asset id")

uuidAttributeToSet = attributes.get(
    config.get("signavio").get("uuidAttributeToSet"))

if not uuidAttributeToSet:
    logger.error(
        f"{__file__.split('/')[-1]}: error: missing signavio:uuidAttributeToSet or no attributes found"
    )
    logger.error("[meta] Something went wrong. Please try again.")
    exit(-1)


# choose the custom attribute which will hold the collibra asset type id
logger.info(
    "choose the custom attribute which will hold the collibra asset type id")

typeAttributeToSet = attributes.get(
    config.get("signavio").get("typeAttributeToSet"))

if not typeAttributeToSet:
    logger.error(
        f"{__file__.split('/')[-1]}: error: missing signavio:typeAttributeToSet or no attributes found"
    )
    logger.error("[meta] Something went wrong. Please try again.")
    exit(-1)


# choose the custom attribute which will hold the collibra asset url for reference
logger.info(
    "choose the custom attribute which will hold the collibra asset url for reference"
)

hrefAttributeToSet = attributes.get(
    config.get("signavio").get("hrefAttributeToSet"))

if not hrefAttributeToSet:
    logger.error(
        f"{__file__.split('/')[-1]}: error: missing signavio:hrefAttributeToSet or no attributes found"
    )
    logger.error("[meta] Something went wrong. Please try again.")
    exit(-1)


# get all signavio dictionary categories
logger.info("get all signavio dictionary categories")

categories = {}

try:
    _ = [
        x(categories, category.get("rep").get("name"), category)
        for category in getcategories(signavio)
        if category.get("rel") == "cat"
    ]

except Exception as e:
    logger.error(e.message)
    logger.error("[glossarycategory] Something went wrong. Please try again.")
    exit(-1)


# choose the signavio dictionary category to get
logger.info("choose the signavio dictionary category to get")

categoryToGet = categories.get(config.get("signavio").get("categoryToGet"))

if not categoryToGet:
    logger.error(
        f"{__file__.split('/')[-1]}: error: missing signavio:categoryToGet or no category found"
    )
    logger.error("[glossarycategory] Something went wrong. Please try again.")
    exit(-1)


# get the details of all selected signavio folders to create or update
logger.info(
    "get the details of all selected signavio folders to create or update")

foldersToUpsert = [
    info for folder in foldersToQuery for info in folder if info.get("rel") == "info"
]


# list all signavio models found on the selected folders ignoring any child folders
logger.info(
    "list all signavio models found on the selected folders ignoring any child folders"
)

modelsToUpsert = [
    getModel(signavio, model)
    for folder in foldersToQuery
    for model in folder
    if isModelValid(model, modelType=["Business Process Diagram (BPMN 2.0)"])
]

if not modelsToUpsert:
    logger.error(e.message)
    logger.error("[models] Something went wrong. Please try again.")
    exit(-1)


# connect to collibra
logger.info("connect to collibra")

collibra = config.get("collibra")

collibra["endpoint"] = f"{collibra['host']}/rest/2.0"

collibra = {
    "host": collibra.get("host"),
    "endpoint": collibra.get("endpoint"),
    "username": collibra.get("username"),
    "password": collibra.get("password"),
}

collibra["session"] = requests.Session()

collibra.get("session").auth = HTTPBasicAuth(
    collibra.get("username"), collibra.get("password")
)


# get the collibra asset types
logger.info("get the collibra asset types")

assetTypes = {}

try:
    response = collibra.get("session").get(
        f"{collibra.get('endpoint')}/assetTypes")

    _ = [
        x(assetTypes, assetType.get("name"), assetType)
        for assetType in response.json()["results"]
    ]

except Exception as e:
    logger.error(e.message)
    logger.error("[assetTypes] Something went wrong. Please try again.")
    exit(-1)


# get the collibra attribute types
logger.info("get the collibra attribute types")

attributeTypes = {}

try:
    response = collibra.get("session").get(
        f"{collibra.get('endpoint')}/attributeTypes")

    _ = [
        x(attributeTypes, attributeType.get("name"), attributeType)
        for attributeType in response.json()["results"]
    ]

except Exception as e:
    logger.error(e.message)
    logger.error("[attributeTypes] Something went wrong. Please try again.")
    exit(-1)


# get the collibra relation types
logger.info("get the collibra relation types")

relationTypes = {}

try:
    response = collibra.get("session").get(
        f"{collibra.get('endpoint')}/relationTypes")

    _ = [
        x(
            relationTypes,
            f"{relationType.get('sourceType').get('name')} {relationType.get('role')} {relationType.get('targetType').get('name')}",
            relationType,
        )
        for relationType in response.json()["results"]
    ]

except Exception as e:
    logger.error(e.message)
    logger.error("[relationTypes] Something went wrong. Please try again.")
    exit(-1)


# get the collibra statuses
logger.info("get the collibra statuses")

statuses = {}

try:
    response = collibra.get("session").get(
        f"{collibra.get('endpoint')}/statuses")

    _ = [
        x(statuses, status.get("name"), status) for status in response.json()["results"]
    ]

except Exception as e:
    logger.error(e.message)
    logger.error("[statuses] Something went wrong. Please try again.")
    exit(-1)


# get the collibra communities
logger.info("get the collibra communities")

communities = {}

try:
    response = collibra.get("session").get(
        f"{collibra.get('endpoint')}/communities")

    _ = [
        x(communities, community.get("name"), community)
        for community in response.json()["results"]
    ]

except Exception as e:
    logger.error(e.message)
    logger.error("[communities] Something went wrong. Please try again.")
    exit(-1)


# choose the collibra community where to save the new models
logger.info("choose the collibra community where to save the new models")

communityToUpdate = communities.get(
    config.get("collibra").get("communityToUpdate"))

if not communityToUpdate:
    logger.error(
        f"{__file__.split('/')[-1]}: error: missing collibra:communityToUpdate or no community found"
    )
    logger.error("[communities] Something went wrong. Please try again.")
    exit(-1)


# get all the collibra domains found under the selected community
logger.info("get all the collibra domains found under the selected community")

domains = {}

try:
    response = collibra.get("session").get(
        f"{collibra.get('endpoint')}/domains?communityId={communityToUpdate.get('id')}&includeSubCommunities=true"
    )

    _ = [
        x(domains, domain.get("name"), domain) for domain in response.json()["results"]
    ]

except Exception as e:
    logger.error(e.message)
    logger.error("[domains] Something went wrong. Please try again.")
    exit(-1)


# choose the collibra domain where to save the new models
logger.info("choose the collibra domain where to save the new models")

domainToUpdate = domains.get(config.get("collibra").get("domainToUpdate"))

if not domainToUpdate:
    logger.error(
        f"{__file__.split('/')[-1]}: error: missing collibra:domainToUpdate or no domain found"
    )
    logger.error("[domains] Something went wrong. Please try again.")
    exit(-1)


# choose the collibra asset type for the new models
logger.info("choose the collibra asset type for the new models")

assetTypeToSet = assetTypes.get(config.get("collibra").get("assetTypeToSet"))

if not assetTypeToSet:
    logger.error(
        f"{__file__.split('/')[-1]}: error: missing collibra:assetTypeToSet or no asset type found"
    )
    logger.error("[assetTypes] Something went wrong. Please try again.")
    exit(-1)


# choose the collibra status your models should be created with
logger.info("choose the collibra status your models should be created with")

statusToSet = statuses.get(config.get("collibra").get("statusToSet"))

if not statusToSet:
    logger.error(
        f"{__file__.split('/')[-1]}: error: missing collibra:statusToSet or no status found"
    )
    logger.error("[statuses] Something went wrong. Please try again.")
    exit(-1)


# choose the collibra attribute holding the signavio model references
logger.info("choose the collibra attribute holding the signavio model references")

signavioHrefAttributeToSet = attributeTypes.get(
    config.get("collibra").get("signavioHrefAttributeToSet")
)

if not signavioHrefAttributeToSet:
    logger.error(
        f"{__file__.split('/')[-1]}: error: missing collibra:signavioHrefAttributeToSet or no attribute found"
    )
    logger.error("[attributeTypes] Something went wrong. Please try again.")
    exit(-1)


# choose the collibra relation between the process and the consuming assets
logger.info(
    "choose the collibra relation between the process and the consuming assets")

consumesRelationToSet = relationTypes.get(
    config.get("collibra").get("consumesRelationToSet")
)

if not consumesRelationToSet:
    logger.error(
        f"{__file__.split('/')[-1]}: error: missing collibra:consumesRelationToSet or no relation found"
    )
    logger.error("[relationTypes] Something went wrong. Please try again.")
    exit(-1)


# choose the collibra relation between the process and the producing assets
logger.info(
    "choose the collibra relation between the process and the producing assets")

producesRelationToSet = relationTypes.get(
    config.get("collibra").get("producesRelationToSet")
)

if not producesRelationToSet:
    logger.error(
        f"{__file__.split('/')[-1]}: error: missing collibra:producesRelationToSet or no relation found"
    )
    logger.error("[relationTypes] Something went wrong. Please try again.")
    exit(-1)


# choose the collibra relation between the process and the used assets
logger.info(
    "choose the collibra relation between the process and the used assets")

usesRelationToSet = relationTypes.get(
    config.get("collibra").get("usesRelationToSet"))

if not usesRelationToSet:
    logger.error(
        f"{__file__.split('/')[-1]}: error: missing collibra:usesRelationToSet or no relation found"
    )
    logger.error("[relationTypes] Something went wrong. Please try again.")
    exit(-1)


# choose the collibra relation between the process and and run processes
logger.info(
    "choose the collibra relation between the process and and run processes")

runsRelationToSet = relationTypes.get(
    config.get("collibra").get("runsRelationToSet"))

if not runsRelationToSet:
    logger.error(
        f"{__file__.split('/')[-1]}: error: missing collibra:runsRelationToSet or no relation found"
    )
    logger.error("[relationTypes] Something went wrong. Please try again.")
    exit(-1)


logger.info("get the details of all selected signavio models to create or update")

try:
    # get the details of all selected signavio models to create or update
    modelsToUpsert = [
        info for model in modelsToUpsert for info in model if info.get("rel") == "info"
    ]

    # get the properties of all signavio models found on the selected folders
    _ = [
        model.update({"properties": getModelProperties(signavio, model)})
        for model in modelsToUpsert
    ]

    # get the network graphics of all signavio models found on the selected folders
    _ = [
        model.update({"png": getModelPng(signavio, model)}) for model in modelsToUpsert
    ]

    # get the vector graphics of all signavio models found on the selected folders
    _ = [
        model.update({"svg": getModelSvg(signavio, model)}) for model in modelsToUpsert
    ]

    # get the linked models of all signavio models found on the selected folders
    _ = [
        model.update({"links": getModelLinks(signavio, model)})
        for model in modelsToUpsert
    ]

    # get the dictionary items of all signavio models found on the selected folders
    _ = [
        model.update({"dictionary": getModelDictionary(signavio, model)})
        for model in modelsToUpsert
    ]

    # get the comments of all signavio models found on the selected folders
    _ = [
        model.update({"comments": getModelComments(signavio, model)})
        for model in modelsToUpsert
    ]

except Exception as e:
    logger.error(e.message)
    logger.error("[models] Something went wrong. Please try again.")
    exit(-1)


# get all the collibra assets found under the selected domain
logger.info("get all the collibra assets found under the selected domain")

assets = []

try:
    assets = [
        getAssets(
            collibra,
            [assetTypeToSet],
            [model.get("rep").get("name")],
            signavioHrefAttributeToSet.get("id"),
        )
        for model in modelsToUpsert
    ]

except Exception as e:
    logger.error(e.message)
    logger.error("[viewconfig] Something went wrong. Please try again.")
    exit(-1)


# create all new collibra assets under the selected domain
logger.info("create all new collibra assets under the selected domain")


def p(model, assetId, assetType, assetStatus, assetDomain):
    return {
        "id": assetId,
        "name": model.get("rep").get("name"),
        "displayName": model.get("rep").get("name"),
        "typeId": assetType.get("id"),
        "statusId": assetStatus.get("id"),
        "domainId": assetDomain.get("id"),
        "href": "/".join(model.get("href").split("/")[0:-1]),
    }


assetsToCreate = []

assetsToUpdate = []

try:
    _ = [
        assetsToUpdate.append(
            p(
                modelsToUpsert[i],
                asset[0].get("assetId"),
                assetTypeToSet,
                statusToSet,
                domainToUpdate,
            )
        )
        if asset
        else assetsToCreate.append(
            p(modelsToUpsert[i], None, assetTypeToSet,
              statusToSet, domainToUpdate)
        )
        for i, asset in enumerate(assets)
    ]

    response = collibra.get("session").post(
        f"{collibra.get('endpoint')}/assets/bulk", json=assetsToCreate
    )

    _ = [
        assetsToCreate[i].update({"id": asset.get("id")})
        for i, asset in enumerate(response.json())
    ]

    assetsToUpdate.extend(assetsToCreate)

except Exception as e:
    logger.error(e.message)
    logger.error("[assets] Something went wrong. Please try again.")
    exit(-1)


# update the model in signavio with the collibra asset id and type, new revision
logger.info(
    "update the model in signavio with the collibra asset id and type, new revision"
)


def p(asset, assetHost, modelUuid, modelType, modelHref):
    href = {"label": "", "url": f"{assetHost}/asset/{asset.get('id')}"}

    return {
        modelUuid.get("rep").get("id"): asset.get("id"),
        modelType.get("rep").get("id"): asset.get("typeId"),
        modelHref.get("rep").get("id"): href,
    }


try:
    _ = [
        asset.update({"info": getModelInfo(signavio, asset.get("href"))})
        for asset in assetsToUpdate
    ]

    _ = [
        asset.update({"json": getModelJson(signavio, asset.get("href"))})
        for asset in assetsToUpdate
    ]

    _ = [
        asset.get("json")
        .get("properties")
        .update(
            p(
                asset,
                collibra.get("host"),
                uuidAttributeToSet,
                typeAttributeToSet,
                hrefAttributeToSet,
            )
        )
        for asset in assetsToUpdate
    ]

    responses = [updateModel(signavio, asset) for asset in assetsToUpdate]

except Exception as e:
    logger.error(e.message)
    logger.error("[model] Something went wrong. Please try again.")
    exit(-1)


# remove
_ = [asset.pop("info") for asset in assetsToUpdate if "info" in asset]

_ = [asset.pop("json") for asset in assetsToUpdate if "json" in asset]


# index
assets = {}

_ = [x(assets, asset.get("name"), asset) for asset in assetsToUpdate]


# update all collibra assets attributes in scope
logger.info("update all collibra assets attributes in scope")


def p(asset, attributeType, attributeValue):
    return {
        "assetId": asset.get("id"),
        "typeId": attributeType.get("id"),
        "values": [attributeValue],
    }


attributesInScope = config.get("mappings").get("attributesInScope")

if not attributesInScope:
    logger.error(
        f"{__file__.split('/')[-1]}: error: missing mappings:attributesInScope or no mappings found"
    )
    logger.error("[mappings] Something went wrong. Please try again.")
    exit(-1)

try:
    payloads = [
        p(
            assets.get(model.get("rep").get("name")),
            attributeTypes.get(attributesInScope["href"]),
            "/".join(model.get("href").split("/")[0:-1]),
        )
        for model in modelsToUpsert
    ]

    payloads.extend(
        [
            p(
                assets.get(model.get("rep").get("name")),
                attributeTypes.get(attributesInScope[k]),
                v,
            )
            for model in modelsToUpsert
            for k, v in model.get("rep").items()
            if k in attributesInScope
        ]
    )

    payloads.extend(
        [
            p(
                assets.get(x.get("rep").get("name")),
                attributeTypes.get(attributesInScope[k]),
                v,
            )
            for x in modelsToUpsert
            for k, v in x.get("rep").get("status").items()
            if k in attributesInScope
        ]
    )

    responses = [
        collibra.get("session")
        .put(
            f"{collibra.get('endpoint')}/assets/{payload.get('assetId')}/attributes",
            json=payload,
        )
        .json()
        for payload in payloads
    ]

except Exception as e:
    logger.error(e.message)
    logger.error("[attributes] Something went wrong. Please try again.")
    exit(-1)


# get all consumed and produced asset relations
logger.info("get all consumed and produced asset relations")

consumesAssets = []

try:
    entries = [
        {
            model.get("rep")
            .get("name"): model.get("properties")
            .get(consumesAttributeToGet.get("rep").get("id"))
        }
        for model in modelsToUpsert
    ]

    consumesAssets = [
        {
            assets.get(k)
            .get("id"): getEntry(signavio, i)
            .get("metaDataValues")
            .get(uuidAttributeToSet.get("rep").get("id"))
        }
        for model in entries
        for k, v in model.items()
        if v is not None
        for i in v
    ]

except Exception as e:
    logger.error(e.message)
    logger.error("[dictionary] Something went wrong. Please try again.")
    exit(-1)


producesAssets = []

try:
    entries = [
        {
            model.get("rep")
            .get("name"): model.get("properties")
            .get(producesAttributeToGet.get("rep").get("id"))
        }
        for model in modelsToUpsert
    ]

    producesAssets = [
        {
            assets.get(k)
            .get("id"): getEntry(signavio, i)
            .get("metaDataValues")
            .get(uuidAttributeToSet.get("rep").get("id"))
        }
        for model in entries
        for k, v in model.items()
        if v is not None
        for i in v
    ]

except Exception as e:
    logger.error(e.message)
    logger.error("[dictionary] Something went wrong. Please try again.")
    exit(-1)


usesAssets = []

try:
    usesAssets = [
        {
            assets.get(model.get("rep").get("name"))
            .get("id"): document.get("rep")
            .get("metaDataValues")
            .get(uuidAttributeToSet.get("rep").get("id"))
        }
        for model in modelsToUpsert
        for document in model.get("dictionary")
        if document.get("rep").get("categoryName")
        == categoryToGet.get("rep").get("name")
    ]

except Exception as e:
    logger.error(e.message)
    logger.error("[dictionary] Something went wrong. Please try again.")
    exit(-1)


# create all the consumed asset relations
logger.info("create all the consumed asset relations")


def p(sourceUuid, targetUuid, relationType):
    return {
        "sourceId": sourceUuid,
        "targetId": targetUuid,
        "typeId": relationType.get("id"),
    }


try:
    payloads = [
        p(k, v, consumesRelationToSet) for x in consumesAssets for k, v in x.items()
    ]

    responses = [
        collibra.get("session")
        .post(f"{collibra.get('endpoint')}/relations", json=payload)
        .json()
        for payload in payloads
    ]

except Exception as e:
    logger.error(e.message)
    logger.error("[relations] Something went wrong. Please try again.")
    exit(-1)


# create all the produced asset relations
logger.info("create all the produced asset relations")

try:
    payloads = [
        p(k, v, producesRelationToSet) for x in producesAssets for k, v in x.items()
    ]

    responses = [
        collibra.get("session")
        .post(f"{collibra.get('endpoint')}/relations", json=payload)
        .json()
        for payload in payloads
    ]

except Exception as e:
    logger.error(e.message)
    logger.error("[relations] Something went wrong. Please try again.")
    exit(-1)


# create all the used asset relations
logger.info("create all the used asset relations")

try:
    payloads = [p(k, v, usesRelationToSet)
                for x in usesAssets for k, v in x.items()]

    responses = [
        collibra.get("session")
        .post(f"{collibra.get('endpoint')}/relations", json=payload)
        .json()
        for payload in payloads
    ]

except Exception as e:
    logger.error(e.message)
    logger.error("[relations] Something went wrong. Please try again.")
    exit(-1)


# upload all png attachments to the correspondent collibra assets
logger.info("upload all png attachments to the correspondent collibra assets")

pngs = []

try:
    pngs = [
        save(
            collibra,
            assets.get(x.get("rep").get("name")).get("id"),
            x.get("png"),
            "png",
        )
        for x in modelsToUpsert
    ]

except Exception as e:
    logger.error(e.message)
    logger.error("[attachments] Something went wrong. Please try again.")
    exit(-1)


# upload all svg attachments to the correspondent collibra assets
logger.info("upload all svg attachments to the correspondent collibra assets")

svgs = []

try:
    svgs = [
        save(
            collibra,
            assets.get(x.get("rep").get("name")).get("id"),
            x.get("svg"),
            "svg",
        )
        for x in modelsToUpsert
    ]

except Exception as e:
    logger.error(e.message)
    logger.error("[attachments] Something went wrong. Please try again.")
    exit(-1)


# update the collibra assets report image attribute with svg
logger.info("update the collibra assets report image attribute with svg")


def p(asset, attributeType, attributeValue):
    return {
        "assetId": asset.get("id"),
        "typeId": attributeType.get("id"),
        "values": [
            f"<img src='/rest/2.0/attachments/{attributeValue.get('id')}/file'>"
        ],
    }


try:
    payloads = [
        p(svg.get("baseResource"), attributeTypes.get("Report Image"), svg)
        for svg in svgs
    ]

    responses = [
        collibra.get("session")
        .put(
            f"{collibra.get('endpoint')}/assets/{payload.get('assetId')}/attributes",
            json=payload,
        )
        .json()
        for payload in payloads
    ]

except Exception as e:
    logger.error(e.message)
    logger.error("[attributes] Something went wrong. Please try again.")
    exit(-1)


# create all the business process runs business process relations
logger.info("create all the business process runs business process relations")


def p(sourceUuid, targetUuid, relationType):
    return {
        "sourceId": sourceUuid,
        "targetId": targetUuid,
        "typeId": relationType.get("id"),
    }


try:
    modelsToGet = [
        {link.get("rep").get("name"): assets.get(link.get("rep").get("name"))}
        for model in modelsToUpsert
        for link in model["links"]
        if isModelValid(link, modelType=["Business Process Diagram (BPMN 2.0)"])
        and assets.get(link.get("rep").get("name")) is None
    ]

    assetsToAdd = [
        getAssets(collibra, [assetTypeToSet], [k],
                  signavioHrefAttributeToSet.get("id"))
        for model in modelsToGet
        for k, v in model.items()
    ]

    _ = [
        assets.update(
            {
                asset[0].get("assetName"): {
                    "id": asset[0].get("assetId"),
                    "name": asset[0].get("assetName"),
                }
            }
        )
        for asset in assetsToAdd
    ]

    payloads = [
        p(
            assets.get(model.get("rep").get("name")).get("id"),
            assets.get(link.get("rep").get("name")).get("id"),
            runsRelationToSet,
        )
        for model in modelsToUpsert
        for link in model["links"]
        if isModelValid(link, modelType=["Business Process Diagram (BPMN 2.0)"])
    ]

    responses = [
        collibra.get("session")
        .post(f"{collibra.get('endpoint')}/relations", json=payload)
        .json()
        for payload in payloads
    ]

except Exception as e:
    logger.error(e.message)
    logger.error("[relations] Something went wrong. Please try again.")
    exit(-1)


logger.info("done")

# comments, it systems, roles (?), depts (?), units (?), participants (?), risks and controls
exit(0)
