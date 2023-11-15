#!/usr/bin/env python
# coding: utf-8

import requests
from requests.auth import HTTPBasicAuth
import streamlit as st
import pandas as pd


# change
def x(l, k, v):
    l[k] = v


# is custom attribute being used by dictionary category
def isCustomAttributeValid(attribute, category):
    try:
        return (
            len(
                [
                    binding
                    for binding in attribute.get("rep").get("glossaryBindings")
                    if binding.get("category") == category
                ]
            )
            > 0
        )

    except Exception as e:
        return False


# get all custom attributes defined in the dictionary
def getAttributes(signavio):
    url = f"{signavio.get('host')}/p/meta"

    headers = {
        "x-signavio-id": signavio.get("authToken"), "accept": "application/json"}

    cookies = {
        "JSESSIONID": signavio.get("jsessionId"),
        "LBROUTEID": signavio.get("lbrouteId"),
    }

    request = requests.get(url, headers=headers, cookies=cookies)

    return request.json()


# get all dictionary categories found in the dictionary
def getCategories(signavio):
    url = f"{signavio.get('host')}/p/glossarycategory?allCategories=true"

    headers = {
        "x-signavio-id": signavio.get("authToken"), "accept": "application/json"}

    cookies = {
        "JSESSIONID": signavio.get("jsessionId"),
        "LBROUTEID": signavio.get("lbrouteId"),
    }

    request = requests.get(url, headers=headers, cookies=cookies)

    return request.json()


# add a dictionary entry with a given name and category
def addEntry(
    signavio, category, uuidAttribute, typeAttribute, hrefAttribute, collibra, asset
):
    url = f"{signavio.get('host')}/p/glossary"

    headers = {
        "x-signavio-id": signavio.get("authToken"),
        "accept": "application/json",
        "content-type": "application/x-www-form-urlencoded",
    }

    cookies = {
        "JSESSIONID": signavio.get("jsessionId"),
        "LBROUTEID": signavio.get("lbrouteId"),
    }

    metaDataValues = f"{{\"{uuidAttribute.get('rep').get('id')}\":\"{asset.get('id')}\", \"{typeAttribute.get('rep').get('id')}\":\"{asset.get('assetType')[0].get('assetTypeId')}\", \"{hrefAttribute.get('rep').get('id')}\":{{\"label\":\"\", \"url\":\"{collibra.get('host')}/asset/{asset.get('id')}\"}}}}"

    payload = f"title={asset.get('name')}&category={category.get('href').split('/')[-1]}&description={asset.get('description')[0].get('descriptionAttributeValue') if 'description' in asset else ''}&metaDataValues={metaDataValues}"

    request = requests.post(url, headers=headers,
                            cookies=cookies, data=payload)

    return request.json()


# update a dictionary entry with a given name and category
def updateEntry(
    signavio, category, uuidAttribute, typeAttribute, hrefAttribute, collibra, asset
):
    url = f"{signavio.get('host')}/p/glossary/{asset.get('href')[0].get('hrefAttributeValue').split('/')[-1]}/info"

    headers = {
        "x-signavio-id": signavio.get("authToken"),
        "accept": "application/json",
        "content-type": "application/x-www-form-urlencoded",
    }

    cookies = {
        "JSESSIONID": signavio.get("jsessionId"),
        "LBROUTEID": signavio.get("lbrouteId"),
    }

    metaDataValues = f"{{\"{uuidAttribute.get('rep').get('id')}\":\"{asset.get('id')}\", \"{typeAttribute.get('rep').get('id')}\":\"{asset.get('assetType')[0].get('assetTypeId')}\", \"{hrefAttribute.get('rep').get('id')}\":{{\"label\":\"\", \"url\":\"{collibra.get('host')}/asset/{asset.get('id')}\"}}}}"

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
                    "Signifier": {"name": "name"},
                    "Id": {"name": "id"},
                    "AssetType": {"name": "assetType", "Id": {"name": "assetTypeId"}},
                    "Status": {"name": "assetStatus", "Id": {"name": "assetStatusId"}},
                    "Domain": {
                        "name": "assetDomain",
                        "Id": {"name": "assetDomainId"},
                        "Community": {
                            "name": "assetCommunity",
                            "Id": {"name": "assetCommunityId"},
                        },
                    },
                    "StringAttribute": [
                        {
                            "name": "description",
                            "labelId": "00000000-0000-0000-0000-000000003114",
                            "Id": {"name": "descriptionAttributeId"},
                            "LongExpression": {"name": "descriptionAttributeValue"},
                        },
                        {
                            "name": "href",
                            "labelId": hrefAttributeType,
                            "Id": {"name": "hrefAttributeId"},
                            "LongExpression": {"name": "hrefAttributeValue"},
                        },
                    ],
                    "Filter": {
                        "AND": [
                            {
                                "Field": {
                                    "name": "assetCommunityId",
                                    "operator": "IN",
                                    "values": [
                                        community.get("id") for community in communities
                                    ],
                                    "descendants": "true",
                                }
                            },
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
                                    "name": "assetStatusId",
                                    "operator": "IN",
                                    "value": [status.get("id") for status in statuses],
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

    return (
        response.json().get("view").get("Assets") if "view" in response.json() else []
    )


# connect to collibra
st.title(":blue[Collibra]")

collibra = {}

collibra["host"] = st.text_input("Host", "https://print.collibra.com")

collibra["username"] = st.text_input("Username", "DataLakeAdmin")

collibra["password"] = st.text_input("Password", type="password", key="p1")

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

if not collibra["password"]:
    st.warning("Please connect.")
    st.stop()


# get collibra asset types
assetTypes = {}

try:
    response = collibra.get("session").get(
        f"{collibra.get('endpoint')}/assetTypes")

    _ = [
        x(assetTypes, assetType.get("name"), assetType)
        for assetType in response.json()["results"]
    ]

except Exception as e:
    st.warning("Something went wrong. Please try again.")
    st.stop()


# get collibra attribute types
attributeTypes = {}

try:
    response = collibra.get("session").get(
        f"{collibra.get('endpoint')}/attributeTypes")

    _ = [
        x(attributeTypes, attributeType.get("name"), attributeType)
        for attributeType in response.json()["results"]
    ]

except Exception as e:
    st.warning("Something went wrong. Please try again.")
    st.stop()


# get collibra statuses types
statuses = {}

try:
    response = collibra.get("session").get(
        f"{collibra.get('endpoint')}/statuses")

    _ = [
        x(statuses, status.get("name"), status) for status in response.json()["results"]
    ]

except Exception as e:
    st.warning("Something went wrong. Please try again.")
    st.stop()


# get all collibra communities
communities = {}

try:
    response = collibra.get("session").get(
        f"{collibra.get('endpoint')}/communities")

    _ = [
        x(communities, community.get("name"), community)
        for community in response.json()["results"]
    ]

except Exception as e:
    st.warning("Something went wrong. Please try again.")
    st.stop()


# choose collibra communities to query
options = st.multiselect(
    label="Select the communities you want to search on",
    options=sorted([f"{k}" for k, v in communities.items()]),
)

communitiesToQuery = (
    [communities.get(community) for community in options]
    if options
    else st.warning("Please specify.") & st.stop()
)


# choose the collibra asset types to list
options = st.multiselect(
    label="Choose the asset types you want to search for",
    options=sorted([f"{k}" for k, v in assetTypes.items()]),
)

assetTypesToList = (
    [assetTypes.get(assetType) for assetType in options]
    if options
    else st.warning("Please specify.") & st.stop()
)


# choose the collibra status types to include
options = st.multiselect(
    label="Choose the status types you want to search for ",
    options=sorted([f"{k}" for k, v in statuses.items()]),
)

statusTypesToGet = (
    [statuses.get(status) for status in options]
    if options
    else st.warning("Please specify.") & st.stop()
)


# choose the collibra attribute holding href
option = st.selectbox(
    label="Choose the attribute holding the signavio href ",
    options=sorted([f"{k}" for k, v in attributeTypes.items()]),
    index=None,
)

attributeTypeToSet = (
    attributeTypes.get(option) if option else st.warning(
        "Please specify.") & st.stop()
)


# get assets of a given list of types and statuses found within a list of communities
assetsToCreate = []

assetsToUpdate = []

try:
    with st.spinner():
        _ = [
            assetsToUpdate.append(asset)
            if "href" in asset
            else assetsToCreate.append(asset)
            for asset in getAssets(
                collibra,
                communitiesToQuery,
                assetTypesToList,
                statusTypesToGet,
                attributeTypeToSet.get("id"),
            )
        ]

except Exception as e:
    st.warning(" Something went wrong. Please try again.")
    st.stop()

if not assetsToUpdate and not assetsToCreate:
    st.warning("Please specify.")
    st.stop()


# connect to signavio
st.title(":blue[Signavio]")

signavio = {}

signavio["host"] = st.text_input("Host", "https://editor.signavio.com")

signavio["tenant"] = st.text_input(
    "Tenant", "93ab506a8d87439f9fbb680fdbc95d4b")

signavio["username"] = st.text_input(
    "Username", "antonio.castelo@collibra.com")

signavio["password"] = st.text_input("Password", type="password", key="p2")

if not signavio["password"]:
    st.warning("Please connect.")
    st.stop()


signavio = {
    "host": signavio.get("host"),
    "tenant": signavio.get("tenant"),
    "username": signavio.get("username"),
    "password": signavio.get("password"),
}

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
    st.warning("Something went wrong. Please try again.")
    st.stop()


# get all signavio dictionary categories
categories = {}

try:
    _ = [
        x(categories, category.get("rep").get("name"), category)
        for category in getCategories(signavio)
        if category.get("rel") == "cat"
    ]

except Exception as e:
    st.warning("Something went wrong. Please try again.")
    st.stop()


# choose the signavio dictionary category to map
option = st.selectbox(
    label="Tell us what data category you want to register",
    options=sorted([f"{k}" for k, v in categories.items()]),
    index=None,
)

categoryToUpdate = (
    categories.get(option) if option else st.warning(
        "Please specify.") & st.stop()
)


# get the custom attributes used by the signavio category
attributes = {}

try:
    _ = [
        x(attributes, asset.get("rep").get("name"), asset)
        for asset in getAttributes(signavio)
        if isCustomAttributeValid(asset, categoryToUpdate.get("href").split("/")[-1])
    ]

except Exception as e:
    st.warning("Something went wrong. Please try again.")
    st.stop()


# choose the custom attribute which will hold the collibra asset id
option = st.selectbox(
    label="Choose your category asset id custom attribute",
    options=sorted([f"{k}" for k, v in attributes.items()]),
    index=None,
)

uuidAttributeToSet = (
    attributes.get(option) if option else st.warning(
        "Please specify.") & st.stop()
)


# choose the custom attribute which will hold the collibra asset type id
option = st.selectbox(
    label="Choose your category type id custom attribute",
    options=sorted([f"{k}" for k, v in attributes.items()]),
    index=None,
)

typeAttributeToSet = (
    attributes.get(option) if option else st.warning(
        "Please specify.") & st.stop()
)


# choose the custom attribute which will hold the collibra asset url for reference
option = st.selectbox(
    label="Choose your category href id custom attribute",
    options=sorted([f"{k}" for k, v in attributes.items()]),
    index=None,
)

hrefAttributeToSet = (
    attributes.get(option) if option else st.warning(
        "Please specify.") & st.stop()
)


# create dictionary items when no href attribute set is found, list dictionary items which fail to create
try:
    with st.spinner():
        entriesCreated = [
            addEntry(
                signavio,
                categoryToUpdate,
                uuidAttributeToSet,
                typeAttributeToSet,
                hrefAttributeToSet,
                collibra,
                asset,
            )
            for asset in assetsToCreate
        ]

        entriesThatFailed = [
            entry for entry in entriesCreated if "errors" in entry]

        df = pd.DataFrame(
            [
                [entry.get("categoryNames"), entry.get(
                    "title"), entry.get("message")]
                for entry in entriesThatFailed
            ],
            columns=["category", "title", "error"],
        )

        if not df.empty:
            st.write("errors found while :red[creating] dictionary items:")
            st.dataframe(df, use_container_width=True)

except Exception as e:
    st.warning("Something went wrong. Please try again.")
    st.stop()


# update collibra, when the href attribute set is found, build payload with all href attributes to add
def p(entry, uuidAttribute, attributeType):
    return {
        "assetId": entry.get("rep").get("metaDataValues").get(uuidAttribute),
        "typeId": attributeType,
        "value": f"dictionary/entry/{entry.get('rep').get('id')}",
    }


try:
    payload = [
        p(entry, uuidAttributeToSet.get("rep").get(
            "id"), attributeTypeToSet.get("id"))
        for entry in entriesCreated
        if "rep" in entry
    ]

    response = collibra.get("session").post(
        f"{collibra.get('endpoint')}/attributes/bulk", json=payload
    )

except Exception as e:
    st.warning("Something went wrong. Please try again.")
    st.stop()


# update dictionary items when href attribute set is found, list dictionary items which fail to update
try:
    with st.spinner():
        entriesUpdated = [
            updateEntry(
                signavio,
                categoryToUpdate,
                uuidAttributeToSet,
                typeAttributeToSet,
                hrefAttributeToSet,
                collibra,
                asset,
            )
            for asset in assetsToUpdate
        ]

        entriesThatFailed = [
            entry for entry in entriesUpdated if "errors" in entry]

        df = pd.DataFrame(
            [
                [entry.get("categoryNames"), entry.get(
                    "title"), entry.get("message")]
                for entry in entriesThatFailed
            ],
            columns=["category", "title", "error"],
        )

        if not df.empty:
            st.write("errors found while :red[updating] dictionary items:")
            st.dataframe(df, use_container_width=True)

except Exception as e:
    st.warning("Something went wrong. Please try again.")
    st.stop()

st.success("Completed!")

st.toast("Completed!", icon="😍")
