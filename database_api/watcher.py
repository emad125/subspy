import config
import requests
import pymongo
import re
from time import sleep
from discord_webhook import DiscordWebhook, DiscordEmbed
import json
from pymongo import MongoClient
from datetime import datetime


client = pymongo.MongoClient("mongodb://localhost:27017")
# Select database and collection
db = client["subsby"]
collection = db["Asset"]


def create_DB():
    with open('schema.json') as f:
        file_data = json.load(f)

    collection.insert_many(file_data)

    client.close()


def read( orgname:str=None, domain:str=None, subdomain:str=None, status_code:int=None, date_from:datetime=None, date_to:datetime=None):
    # Retrieve data with specific fields included
    search_query = {}
    if orgname: 
        search_query["OrgName"] = orgname
    if domain:
        search_query["Domains.domain"] = domain
    if subdomain:
        search_query["Domains.subdomains.url"] = subdomain

    data = collection.find(search_query)
    

    # Print the data
    for document in data:
        domains = document["Domains"]
        for d in domains:
            if d["domain"] == domain:
                for sub in d["subdomains"]:
                    if sub["url"] == subdomain:
                        print(sub)


def insert():
    return


def main():
    # Create_DB()
    read(orgname="org1", domain="domain1", subdomain="text2")



if __name__ == "__main__":
    main()






















