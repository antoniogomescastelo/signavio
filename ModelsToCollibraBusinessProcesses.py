#!/usr/bin/env python
# coding: utf-8

import os
import requests
from requests.auth import HTTPBasicAuth
import streamlit as st
import pandas as pd


# change
def x(l, k, v): l[k] = v


# search signavio
def search(signavio, q, limit=None, offset=None, types=None):
    try:                  
        url = f"{signavio.get('host')}/p/search?q={q}"
        
        url = f"{url}&limit={limit}" if limit is not None else f"{url}"

        url = f"{url}&offset={offset}" if offset is not None else f"{url}"

        url = f"{url}{''.join([f'&types={t}' for t in types])}" if types is not None else f"{url}"

        headers = {"x-signavio-id": signavio.get("authToken"), "accept": "application/json"}

        cookies = {"JSESSIONID": signavio.get("jsessionId"), "LBROUTEID": signavio.get("lbrouteId")}

        request = requests.get(url, headers=headers, cookies=cookies)

        return request.json()

    except Exception as e:
        return e


# get a signavio folder
def getFolder(signavio, folder):
    try:                  
        url = f"{signavio.get('host')}/p{folder.get('href')}"

        headers = {"x-signavio-id": signavio.get("authToken"), "accept": "application/json"}

        cookies = {"JSESSIONID": signavio.get("jsessionId"), "LBROUTEID": signavio.get("lbrouteId")}

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

        headers = {"x-signavio-id": signavio.get("authToken"), "accept": "application/json"}

        cookies = {"JSESSIONID": signavio.get("jsessionId"), "LBROUTEID": signavio.get("lbrouteId")}

        request = requests.get(url, headers=headers, cookies=cookies)

        return request.json()

    except Exception as e:
        return e


# get the properties of a signavio model
def getModelProperties(signavio, model):
    try:                  
        url = f"{signavio.get('host')}/p{'/'.join(model.get('href').split('/')[0:-1])}/json"
        
        headers = {"x-signavio-id": signavio.get("authToken"), "accept": "application/json"}

        cookies = {"JSESSIONID": signavio.get("jsessionId"), "LBROUTEID": signavio.get("lbrouteId")}

        request = requests.get(url, headers=headers, cookies=cookies)

        return request.json().get("properties")
    
    except Exception as e:
        return e


# get the network graphics of a signavio model
def getModelPng(signavio, model):
    try:                  
        url = f"{signavio.get('host')}/p{'/'.join(model.get('href').split('/')[0:-1])}/png"

        headers = {"x-signavio-id": signavio.get("authToken"), "content-type": "image/png;charset=utf-8"}

        cookies = {"JSESSIONID": signavio.get("jsessionId"), "LBROUTEID": signavio.get("lbrouteId")}

        request = requests.get(url, headers=headers, cookies=cookies)

        return request.content
    
    except Exception as e:
        return e


# get the vector graphics of a signavio model
def getModelSvg(signavio, model):
    try:                  
        url = f"{signavio.get('host')}/p{'/'.join(model.get('href').split('/')[0:-1])}/svg"

        headers = {"x-signavio-id": signavio.get("authToken"), "content-type": "image/svg+xml;charset=utf-8"}

        cookies = {"JSESSIONID": signavio.get("jsessionId"), "LBROUTEID": signavio.get("lbrouteId")}

        request = requests.get(url, headers=headers, cookies=cookies)

        return request.content
    
    except Exception as e:
        return e


# get the linked models of a signavio model
def getModelLinks(signavio, model):
    try:                  
        url = f"{signavio.get('host')}/p{'/'.join(model.get('href').split('/')[0:-1])}/link"

        headers = {"x-signavio-id": signavio.get("authToken"), "accept": "application/json"}

        cookies = {"JSESSIONID": signavio.get("jsessionId"), "LBROUTEID": signavio.get("lbrouteId")}

        request = requests.get(url, headers=headers, cookies=cookies)

        return request.json()
    
    except Exception as e:
        return e


# get the dictionary items of a signavio model 
def getModelDictionary(signavio, model):
    try:                  
        url = f"{signavio.get('host')}/p{'/'.join(model.get('href').split('/')[0:-1])}/glossaryinfo"

        headers = {"x-signavio-id": signavio.get("authToken"), "accept": "application/json"}

        cookies = {"JSESSIONID": signavio.get("jsessionId"), "LBROUTEID": signavio.get("lbrouteId")}

        request = requests.get(url, headers=headers, cookies=cookies)

        return request.json()
    
    except Exception as e:
        return e


# get the comments of a signavio model
def getModelComments(signavio, model):
    try:                  
        url = f"{signavio.get('host')}/p{'/'.join(model.get('href').split('/')[0:-1])}/comments"

        headers = {"x-signavio-id": signavio.get("authToken"), "accept": "application/json"}

        cookies = {"JSESSIONID": signavio.get("jsessionId"), "LBROUTEID": signavio.get("lbrouteId")}

        request = requests.get(url, headers=headers, cookies=cookies)

        return request.json()
    
    except Exception as e:
        return e


# get a signavio model info given a href
def getModelInfo(signavio, href):
    try:                  
        url = f"{signavio.get('host')}/p{href}/info"

        headers = {"x-signavio-id": signavio.get("authToken"), "accept": "application/json"}

        cookies = {"JSESSIONID": signavio.get("jsessionId"), "LBROUTEID": signavio.get("lbrouteId")}

        request = requests.get(url, headers=headers, cookies=cookies)

        return request.json()

    except Exception as e:
        return e
    

# get a signavio model json given a href
def getModelJson(signavio, href):
    try:                  
        url = f"{signavio.get('host')}/p{href}/json"

        headers = {"x-signavio-id": signavio.get("authToken"), "accept": "application/json"}

        cookies = {"JSESSIONID": signavio.get("jsessionId"), "LBROUTEID": signavio.get("lbrouteId")}

        request = requests.get(url, headers=headers, cookies=cookies)

        return request.json()

    except Exception as e:
        return e
        

# check if a given signavio model is valid
def isModelValid(model, modelType=None, deployedOnly=False, approvedOnly=False, publishedOnly=False):
    result = True 

    try:
        result = False if model.get("rel") != "mod" else result 

        result = False if model.get("rep").get("deleted") == True else result
    
        result = False if model.get("rep").get("status").get("deleted") == True else result

        if deployedOnly: result = False if model.get("rep").get("isDeployed") == False else result

        if approvedOnly: result = False if model.get("rep").get("status").get("approve") == False else result

        if publishedOnly: result = False if model.get("rep").get("status").get("publish") == False else result

        if modelType is not None: result = False if model.get("rep").get("type") not in modelType else result

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
        "comment": "updated"
    }

    headers = {"x-signavio-id": signavio.get("authToken"), "accept":"application/json", 'content-type': 'application/x-www-form-urlencoded'}

    cookies = {"JSESSIONID": signavio.get("jsessionId"), "LBROUTEID": signavio.get("lbrouteId")}

    request = requests.put(url, headers=headers, cookies=cookies, data=data)

    return request.json()


# get all custom attributes defined in the dictionary 
def getattributes(signavio):
    url = f"{signavio.get('host')}/p/meta"

    headers = {"x-signavio-id": signavio.get("authToken"), "accept":"application/json"}

    cookies = {"JSESSIONID": signavio.get("jsessionId"), "LBROUTEID": signavio.get("lbrouteId")}

    request = requests.get(url, headers=headers, cookies=cookies)

    return request.json()


# get a dictionary entry from the dictionary
def getEntry(signavio, entry):
    url = f"{signavio.get('host')}/p{entry}/info"

    headers = {"x-signavio-id": signavio.get("authToken"), "accept":"application/json"}

    cookies = {"JSESSIONID": signavio.get("jsessionId"), "LBROUTEID": signavio.get("lbrouteId")}

    request = requests.get(url, headers=headers, cookies=cookies)

    return request.json()


# get all dictionary categories found in the dictionary
def getcategories(signavio):
    url = f"{signavio.get('host')}/p/glossarycategory?allCategories=true"

    headers = {"x-signavio-id": signavio.get("authToken"), "accept":"application/json"}

    cookies = {"JSESSIONID": signavio.get("jsessionId"), "LBROUTEID": signavio.get("lbrouteId")}

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
                    "Signifier": {
                        "name": "assetName"
                    },
                    "Id": {
                        "name": "assetId"
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
                                    "name": "assetTypeId",
                                    "operator": "IN", 
                                    "values": [assetType.get("id") for assetType in assetTypes]
                                }                                
                            },
                            {
                                "Field": {
                                    "name": "assetName",
                                    "operator": "IN",
                                    "value": [name for name in assetNames]
                                }
                            }
                            # {
                            #     "Field": {
                            #         "name": "hrefAttributeValue",
                            #         "operator": "NOT_NULL"
                            #     }
                            # }
                        ]
                    }              
                }
            }
        }
    }

 
    response = collibra.get("session").post(f"{collibra.get('endpoint')}/outputModule/export/json?validationEnabled=false", json=viewConfig)

    return response.json().get("view").get("Assets")


# save attachment
def save(collibra, assetId, data, fileType): 
    with open(f"{assetId}.{fileType}", "wb") as f:
        f.write(data)

    file = open(f"{assetId}.{fileType}", "rb").read()

    files = {"file": file}

    payload = {"fileName": f"{assetId}.{fileType}", "resourceType": "Asset", "resourceId": assetId}

    response = collibra.get("session").post(f"{collibra.get('endpoint')}/attachments", files=files, data=payload)

    os.remove(f"{assetId}.{fileType}")

    return response.json()


# connect to signavio 
st.title(':blue[Signavio]')

signavio = {}

signavio["host"] = st.text_input("Host", "https://editor.signavio.com")

signavio["tenant"] = st.text_input("Tenant", "93ab506a8d87439f9fbb680fdbc95d4b")

signavio["username"] = st.text_input("Username", "antonio.castelo@collibra.com")

signavio["password"] = st.text_input("Password", type="password", key="p2")

if not signavio["password"]:
    st.warning('Please connect.')
    st.stop()

try:
    url = f"{signavio.get('host')}/p/login"

    data = {"name": signavio.get("username"), "password": signavio.get("password"), "tenant": signavio.get("tenant"), "tokenonly": "true"}

    request = requests.post(url, data)

    authToken = request.content.decode("utf-8")

    jsessionId = request.cookies.get("JSESSIONID")

    lbrouteId = request.cookies.get("LBROUTEID")

    signavio = {"host": signavio.get("host"), "tenant": signavio.get("tenant"), "authToken": authToken, "jsessionId": jsessionId, "lbrouteId": lbrouteId}

except Exception as e:
    st.error('[login] Something went wrong. Please try again.')
    st.stop()


# list all the signavio folders
folders = {}

try:
    _=[x(folders, folder.get("rep").get("name"), folder) for folder in search(signavio, q='*', types=["DIR"]) if isFolderValid(folder)]

except Exception as e:
    st.error('[folders] Something went wrong. Please try again.')
    st.stop()


# choose the signavio folders to query 
options = st.multiselect(label='Choose which folders to search for process models', options=sorted([f"{k}" for k,v in folders.items()]))

foldersToQuery = [getFolder(signavio, folders.get(folder)) for folder in options] if options else st.warning("Please specify.") & st.stop()


# get the custom attributes used by the signavio category 
attributes = {}

try:
    _=[x(attributes, attribute.get("rep").get("name"), attribute) for attribute in getattributes(signavio)]

except Exception as e:
    st.error('[meta] Something went wrong. Please try again.')
    st.stop()


# choose the custom attribute holding the consuming data assets
option = st.selectbox(label='Choose which attribute holds the consumed assets', options=sorted([f"{k}" for k,v in attributes.items()]), index=None)

consumesAttributeToGet = attributes.get(option) if option else st.warning("Please specify.") & st.stop()


# choose the custom attribute holding the producing data assets
option = st.selectbox(label='Choose which attribute holds the produced assets', options=sorted([f"{k}" for k,v in attributes.items()]), index=None)

producesAttributeToGet = attributes.get(option) if option else st.warning("Please specify.") & st.stop()


# choose the custom attribute which will hold the collibra asset id
option = st.selectbox(label='Choose which attribute holds the collibra asset id', options=sorted([f"{k}" for k,v in attributes.items()]), index=None)

uuidAttributeToSet = attributes.get(option) if option else st.warning("Please specify.") & st.stop()


# choose the custom attribute which will hold the collibra asset type id
option = st.selectbox(label='Choose which attribute holds the collibra type id', options=sorted([f"{k}" for k,v in attributes.items()]), index=None)

typeAttributeToSet = attributes.get(option) if option else st.warning("Please specify.") & st.stop()


# choose the custom attribute which will hold the collibra asset url for reference
option = st.selectbox(label='Choose which attribute holds the collibra href url', options=sorted([f"{k}" for k,v in attributes.items()]), index=None)

hrefAttributeToSet = attributes.get(option) if option else st.warning("Please specify.") & st.stop()


# get all signavio dictionary categories
categories = {}

try:
    _=[x(categories, category.get("rep").get("name"), category) for category in getcategories(signavio) if category.get("rel") == "cat"]

except Exception as e:
    st.error('[glossarycategory] Something went wrong. Please try again.')
    st.stop()


# choose the signavio dictionary category to get
option = st.selectbox(label='Tell us what data category you want to look out for', options=sorted([f"{k}" for k,v in categories.items()]), index=None)

categoryToGet = categories.get(option) if option else st.warning("Please specify.") & st.stop()


# list all signavio models found on the selected folders ignoring any child folders
modelsToGet = [getModel(signavio, model) for folder in foldersToQuery for model in folder if isModelValid(model, modelType=["Business Process Diagram (BPMN 2.0)"])]

if not modelsToGet:
    st.error('[models] Something went wrong. Please try again.')
    st.stop()


# get the details of all selected signavio folders to create or update
foldersToUpsert = [info for folder in foldersToQuery for info in folder if info.get("rel") == "info"]


# connect to collibra                  
st.title(':blue[Collibra]')

collibra = {}

collibra["host"] = st.text_input("Host", "https://print.collibra.com")  

collibra["username"] = st.text_input("Username", "DataLakeAdmin") 

collibra["password"] = st.text_input("Password", type="password", key="p1") 

collibra["endpoint"] = f"{collibra['host']}/rest/2.0"

collibra = {"host": collibra.get("host"), "endpoint": collibra.get("endpoint"), "username": collibra.get("username"), "password": collibra.get("password")}

collibra["session"] = requests.Session()
    
collibra.get("session").auth = HTTPBasicAuth(collibra.get("username"), collibra.get("password"))

if not collibra["password"]:
    st.warning('Please connect.')
    st.stop()


# get the collibra asset types
assetTypes = {}

try:
    response = collibra.get("session").get(f"{collibra.get('endpoint')}/assetTypes")

    _=[x(assetTypes, assetType.get("name"), assetType) for assetType in response.json()["results"]] 

except Exception as e:
    st.error('[assetTypes] Something went wrong. Please try again.')
    st.stop()


# get the collibra attribute types
attributeTypes = {}

try:
    response = collibra.get("session").get(f"{collibra.get('endpoint')}/attributeTypes")

    _=[x(attributeTypes, attributeType.get("name"), attributeType) for attributeType in response.json()["results"]]

except Exception as e:
    st.error('[attributeTypes] Something went wrong. Please try again.')
    st.stop()


# get the collibra relation types
relationTypes = {}

try:
    response = collibra.get("session").get(f"{collibra.get('endpoint')}/relationTypes")

    _=[x(relationTypes, f"{relationType.get('sourceType').get('name')} {relationType.get('role')} {relationType.get('targetType').get('name')}", relationType) for relationType in response.json()["results"]]

except Exception as e:
    st.error('[relationTypes] Something went wrong. Please try again.')
    st.stop()


# get the collibra statuses
statuses = {}

try:
    response = collibra.get("session").get(f"{collibra.get('endpoint')}/statuses")

    _=[x(statuses, status.get("name"), status) for status in response.json()["results"]]

except Exception as e:
    st.error('[statuses] Something went wrong. Please try again.')
    st.stop()


# get the collibra communities
communities = {}

try:
    response = collibra.get("session").get(f"{collibra.get('endpoint')}/communities")

    _=[x(communities, community.get("name"), community) for community in response.json()["results"]]

except Exception as e:
    st.error('[communities] Something went wrong. Please try again.')
    st.stop()


# choose the collibra community where to save the new models
option = st.selectbox(label='Choose the community where to store new models', options=sorted([f"{k}" for k,v in communities.items()]), index=None)

communityToUpdate = communities.get(option) if option else st.warning("Please specify.") & st.stop()


# get all the collibra domains found under the selected community 
domains = {}

try:
    response = collibra.get("session").get(f"{collibra.get('endpoint')}/domains?communityId={communityToUpdate.get('id')}&includeSubCommunities=true")

    _=[x(domains, domain.get("name"), domain) for domain in response.json()["results"]]

except Exception as e:
    st.error('[domains] Something went wrong. Please try again.')
    st.stop()


# choose the collibra domain where to save the new models
option = st.selectbox(label='Choose the domain where to save the new models', options=sorted([f"{k}" for k,v in domains.items()]), index=None)

domainToUpdate = domains.get(option) if option else st.warning("Please specify.") & st.stop()


# choose the collibra asset type for the new models
option = st.selectbox(label='Tell us the asset type to create all new models with', options=sorted([f"{k}" for k,v in assetTypes.items()]), index=None)

assetTypeToSet = assetTypes.get(option) if option else st.warning("Please specify.") & st.stop()


# choose the collibra status your models should be created with
option = st.selectbox(label='Tell us the status new models should be saved with', options=sorted([f"{k}" for k,v in statuses.items()]), index=None)

statusToSet = statuses.get(option) if option else st.warning("Please specify.") & st.stop()


# choose the collibra attribute holding the signavio model references
option = st.selectbox(label='Choose the attribute holding your model reference', options=sorted([f"{k}" for k,v in attributeTypes.items()]), index=None)

signavioHrefAttributeToSet = attributeTypes.get(option) if option else st.warning("Please specify.") & st.stop()


# choose the collibra relation between the process and the consuming assets
option = st.selectbox(label='Choose how consumed assets should be connected', options=sorted([f"{k}" for k,v in relationTypes.items()]), index=None)

consumesRelationToSet = relationTypes.get(option) if option else st.warning("Please specify.") & st.stop()


# choose the collibra relation between the process and the producing assets
option = st.selectbox(label='Choose how produced assets should be connected', options=sorted([f"{k}" for k,v in relationTypes.items()]), index=None)

producesRelationToSet = relationTypes.get(option) if option else st.warning("Please specify.") & st.stop()


# choose the collibra relation between the process and the used assets
option = st.selectbox(label='Choose how the used assets should be connected', options=sorted([f"{k}" for k,v in relationTypes.items()]), index=None)

usesRelationToSet = relationTypes.get(option) if option else st.warning("Please specify.") & st.stop()


# choose the collibra relation between the process and and run processes
option = st.selectbox(label='Choose how the linked assets should be connected', options=sorted([f"{k}" for k,v in relationTypes.items()]), index=None)

runsRelationToSet = relationTypes.get(option) if option else st.warning("Please specify.") & st.stop()


modelsToUpsert = []

with st.spinner('get models..'):
    try:
        # get the details of all selected signavio models to create or update
        modelsToUpsert = [info for model in modelsToGet for info in model if info.get("rel") == "info"]


        # get the properties of all signavio models found on the selected folders 
        _=[model.update({"properties": getModelProperties(signavio, model)}) for model in modelsToUpsert]


        # get the network graphics of all signavio models found on the selected folders 
        _=[model.update({"png": getModelPng(signavio, model)}) for model in modelsToUpsert]


        # get the vector graphics of all signavio models found on the selected folders 
        _=[model.update({"svg": getModelSvg(signavio, model)}) for model in modelsToUpsert]


        # get the linked models of all signavio models found on the selected folders 
        _=[model.update({"links": getModelLinks(signavio, model)}) for model in modelsToUpsert]


        # get the dictionary items of all signavio models found on the selected folders 
        _=[model.update({"dictionary": getModelDictionary(signavio, model)}) for model in modelsToUpsert]


        # get the comments of all signavio models found on the selected folders 
        _=[model.update({"comments": getModelComments(signavio, model)}) for model in modelsToUpsert]

    except Exception as e:
        st.error('[models] Something went wrong. Please try again.')
        st.stop()


# get all the collibra assets found under the selected domain
assetsThatExist = []

with st.spinner('search assets..'):
    try:
        assetsThatExist = [getAssets(collibra, [assetTypeToSet], [model.get("rep").get("name")], signavioHrefAttributeToSet.get("id")) for model in modelsToUpsert]

    except Exception as e:
        st.error('[viewconfig] Something went wrong. Please try again.')
        st.stop()


# create all new collibra assets under the selected domain 
def p(model, assetId, assetType, status, domain):   
    return {"id": assetId, "name": model.get("rep").get("name"), "displayName": model.get("rep").get("name"), "typeId": assetType.get("id"), "statusId": status.get("id"), "domainId": domain.get("id"), "href": "/".join(model.get("href").split('/')[0:-1])}

assetsToCreate = []

assetsToUpdate = []

with st.spinner('create assets..'):
    try:
        _=[assetsToUpdate.append(p(modelsToUpsert[i], asset[0].get("assetId"), assetTypeToSet, statusToSet, domainToUpdate)) if asset else assetsToCreate.append(p(modelsToUpsert[i], None, assetTypeToSet, statusToSet, domainToUpdate)) for i, asset in enumerate(assetsThatExist)]

        response = collibra.get("session").post(f"{collibra.get('endpoint')}/assets/bulk", json=assetsToCreate)

        _=[assetsToCreate[i].update({"id": asset.get("id")}) for i, asset in enumerate(response.json())]

        assetsToUpdate.extend(assetsToCreate)

    except Exception as e:
        st.error('[assets] Something went wrong. Please try again.')
        st.stop()


# update the model in signavio with the collibra asset id and type, new revision
def p(collibra, asset, uuidAttribute, typeAttribute, hrefAttribute): 
    href = {"label": "", "url": f"{collibra.get('host')}/asset/{asset.get('id')}"}

    return {uuidAttribute.get("rep").get("id"): asset.get("id"), typeAttribute.get("rep").get("id"): asset.get("typeId"), hrefAttribute.get("rep").get("id"): href}

with st.spinner('update models..'):
    try:
        _=[asset.update({"info": getModelInfo(signavio, asset.get("href"))}) for asset in assetsToUpdate]

        _=[asset.update({"json": getModelJson(signavio, asset.get("href"))}) for asset in assetsToUpdate]

        _=[asset.get("json").get("properties").update(p(collibra, asset, uuidAttributeToSet, typeAttributeToSet, hrefAttributeToSet)) for asset in assetsToUpdate]

        responses = [updateModel(signavio, asset) for asset in assetsToUpdate]

    except Exception as e:
        st.error('[model] Something went wrong. Please try again.')
        st.stop()


df = pd.DataFrame([[asset.get("name"), asset.get("id"), asset.get("typeId"), asset.get("href")] for asset in assetsToUpdate], columns =['name', 'id', 'type', 'href'])

if not df.empty: 
    st.write("updated:")
    st.dataframe(df, use_container_width=True) 


# change
assets = {}

_=[x(assets, asset.get("name"), asset) for asset in assetsToUpdate]


# update all collibra assets attributes in scope
def p(asset, attributeType, value): 
     return {"assetId": asset.get("id"), "typeId": attributeType.get("id"), "values": [value]}

with st.spinner("update asset attributes.."):
    try:
        attributesInScope = {"href": "Signavio href", "parent": "Parent Folder", "parentName": "Parent Folder Name", "description": "Description", "isDeployed": "Deployed", "rev": "Revision", "author": "Author", "authorName": "Author Name", "approve": "Approved", "publish": "Published"}

        payloads = [p(assets.get(model.get("rep").get("name")), attributeTypes.get(attributesInScope["href"]), "/".join(model.get("href").split('/')[0:-1])) for model in modelsToUpsert] 

        payloads.extend([p(assets.get(model.get("rep").get("name")), attributeTypes.get(attributesInScope[k]), v) for model in modelsToUpsert for k,v in model.get("rep").items() if k in attributesInScope])

        payloads.extend([p(assets.get(x.get("rep").get("name")), attributeTypes.get(attributesInScope[k]), v) for x in modelsToUpsert for k,v in x.get("rep").get("status").items() if k in attributesInScope])

        responses = [collibra.get("session").put(f"{collibra.get('endpoint')}/assets/{payload.get('assetId')}/attributes", json=payload).json() for payload in payloads]

    except Exception as e:
        st.error('[attributes] Something went wrong. Please try again.')
        st.stop()


# get all consumed and produced asset relations
consumesAssets = []

with st.spinner("get consumed asset relations.."):
    try:
        entries = [{model.get("rep").get("name"): model.get("properties").get(consumesAttributeToGet.get("rep").get("id"))} for model in modelsToUpsert]

        consumesAssets = [{assets.get(k).get("id"): getEntry(signavio, i).get("metaDataValues").get(uuidAttributeToSet.get("rep").get("id"))} for model in entries for k,v in model.items() if v is not None for i in v ]
        
    except Exception as e:
        st.error('[dictionary] Something went wrong. Please try again.')
        st.stop()


producesAssets = []

with st.spinner("get produced asset relations.."):
    try:
        entries = [{model.get("rep").get("name"): model.get("properties").get(producesAttributeToGet.get("rep").get("id"))} for model in modelsToUpsert]

        producesAssets = [{assets.get(k).get("id"): getEntry(signavio, i).get("metaDataValues").get(uuidAttributeToSet.get("rep").get("id"))} for model in entries for k,v in model.items() if v is not None for i in v ]

    except Exception as e:
        st.error('[dictionary] Something went wrong. Please try again.')
        st.stop()


usesAssets = []

with st.spinner("get all used asset relations.."):
    try:
        usesAssets = [{assets.get(model.get("rep").get("name")).get("id"):document.get("rep").get("metaDataValues").get(uuidAttributeToSet.get("rep").get("id"))} for model in modelsToUpsert  for document in model.get("dictionary") if document.get("rep").get("categoryName") == categoryToGet.get("rep").get("name")]

    except Exception as e:
        st.error('[dictionary] Something went wrong. Please try again.')
        st.stop()


# create all the consumed asset relations 
def p(sourceId, targetId, relationType): 
    return {'sourceId': sourceId, 'targetId': targetId, 'typeId': relationType.get("id")}

with st.spinner("create consumed asset relations.."):
    try: 
        payloads = [p(k,v, consumesRelationToSet) for x in consumesAssets for k,v in x.items()]

        responses = [collibra.get("session").post(f"{collibra.get('endpoint')}/relations", json=payload).json() for payload in payloads]

    except Exception as e:
        st.error('[relations] Something went wrong. Please try again.')
        st.stop()


# create all the produced asset relations 
with st.spinner("create produced asset relations.."):
    try:
        payloads = [p(k,v, producesRelationToSet) for x in producesAssets for k,v in x.items()]

        responses = [collibra.get("session").post(f"{collibra.get('endpoint')}/relations", json=payload).json() for payload in payloads]

    except Exception as e:
        st.error('[relations] Something went wrong. Please try again.')
        st.stop()


# create all the used asset relations
with st.spinner("create all used asset relations.."):
    try:
        payloads = [p(k,v, usesRelationToSet) for x in usesAssets for k,v in x.items()]

        responses = [collibra.get("session").post(f"{collibra.get('endpoint')}/relations", json=payload).json() for payload in payloads]

    except Exception as e:
        st.error('[relations] Something went wrong. Please try again.')
        st.stop()


# upload all png attachments to the correspondent collibra assets
pngs = []

with st.spinner("save asset portable network graphics"):
    try:
        pngs = [save(collibra, assets.get(x.get("rep").get("name")).get("id"), x.get("png"), "png") for x in modelsToUpsert]

    except Exception as e:
        st.error('[attachments] Something went wrong. Please try again.')
        st.stop()


# upload all svg attachments to the correspondent collibra assets
svgs = []

with st.spinner("save asset scalable vector graphics.."):
    try:
        svgs = [save(collibra, assets.get(x.get("rep").get("name")).get("id"), x.get("svg"), "svg") for x in modelsToUpsert]

    except Exception as e:
        st.error('[attachments] Something went wrong. Please try again.')
        st.stop()


# update the collibra assets report image attribute with svg 
def p(asset, attributeType, file): 
     return {"assetId": asset.get("id"), "typeId": attributeType.get("id"), "values": [f"<img src='/rest/2.0/attachments/{file.get('id')}/file'>"]}

with st.spinner("update asset image attribute with svg.."):
    try:
        payloads = [p(svg.get("baseResource"), attributeTypes.get("Report Image"), svg) for svg in svgs] 

        responses = [collibra.get("session").put(f"{collibra.get('endpoint')}/assets/{payload.get('assetId')}/attributes", json=payload).json() for payload in payloads]

    except Exception as e:
        st.error('[attributes] Something went wrong. Please try again.')
        st.stop()


# comments, it systems, links, documents, roles (?), depts (?), units (?), participants (?), risks and controls
st.success("Completed!")

st.toast('Completed!', icon='😍')
