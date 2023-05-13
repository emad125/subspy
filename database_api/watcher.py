import pymongo, json, requests
from pymongo import MongoClient
from datetime import datetime

collection_name = "assets"
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["subspy"]
collection = db[collection_name]
headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/112.0"}

def create_db():
    with open('schema.json') as f:
        file_data = json.load(f)
    collection.insert_many(file_data)

def is_exist(collection: str, db):
    if collection_name in db.list_collection_names():
        return
    else:
        create_db()

def read(orgname:str=None, domain:str=None, subdomain:str=None, status_code:str=None, date_from=None, date_to=None):
    search_query = {}
    if orgname: 
        search_query["OrgName"] = orgname
    if domain:
        search_query["Domains.domain"] = domain
    if subdomain:
        search_query["Domains.subdomains.url"] = subdomain
    if status_code:
        search_query["Domains.subdomains.status_code"] = status_code
    if date_from:
        search_query["Domains.subdomains.date"] = {'$gte': date_from, '$lte': date_to}

    data = collection.find(search_query)
    results = {}
    if any(value for value in [orgname, domain, subdomain, status_code, date_from, date_to]):
        for document in data:
            for domains in document["Domains"]:
                subdomains_to_add = []
                if domains["domain"] == domain or not domain:
                    for sub in domains["subdomains"]:
                        if sub["url"] == subdomain or not subdomain:
                            if sub["status_code"] == status_code or not status_code:
                                if (not date_from or sub["date"] >= date_from) and (not date_to or sub["date"] <= date_to):
                                    subdomains_to_add.append(sub)

                if subdomains_to_add:
                    key = (document["OrgName"], domains["domain"])
                    value = [sub["url"]+' -> '+sub["status_code"]+' - '+sub["date"] for sub in subdomains_to_add]
                    results[key] = value

        if len(results) > 0:
            return results
        else:
            return 'Not found'
    else:
        return 'No input'


def insert(orgname, domain, subdomains):
    check_org = collection.find_one({"OrgName": orgname})
    check_domain = collection.find_one({"OrgName": orgname, 'Domains.domain': domain})
    subdomains_list = subdomains.replace(' ', '').split(',')

    if not check_org:
        new_doc = {}
        new_doc['OrgName'] = orgname
        new_doc['Domains'] = [{"domain": domain}]
        new_doc["Domains"][0]["subdomains"] = [
            {
                "url": sub,
                "date": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S"),
                "status_code": str(requests.get("https://"+sub, headers=headers).status_code)
            }
            for sub in subdomains_list
        ]
        collection.insert_one(new_doc)
    elif not check_domain:
        new_doc = {}
        new_doc['Domains'] = {"domain": domain}
        new_doc["Domains"]["subdomains"] = [
            {
                "url": sub,
                "date": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S"),
                "status_code": str(requests.get("https://"+sub, headers=headers).status_code)
            }
            for sub in subdomains_list
        ]
        collection.update_one(
            {"OrgName": orgname},
            {"$push": new_doc}
        )
    else:
        doc = collection.find_one({"OrgName": orgname})
        index = [i for i, d in enumerate(doc["Domains"]) if d["domain"] == domain][0]
        subdomains = subdomains.replace(' ', '').split(',')

        for sub in subdomains:
            new_doc = {
                "url": sub,
                "date": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S"),
                "status_code": str(requests.get("https://"+sub, headers=headers).status_code)
            }

            collection.update_one(
                {"OrgName": orgname, "Domains.domain": domain},
                {"$push": {"Domains.{0}.subdomains".format(index): new_doc}}
            )

def main():
    is_exist(collection, db)
    # insert(orgname="org5", domain="mha4065.com", subdomains="r.mha4065.com")
    print(read(date_from="2023-05-01T07:32:05", date_to="2023-05-12T07:00:15"))


if __name__ == "__main__":
    main()
