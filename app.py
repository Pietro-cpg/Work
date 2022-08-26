import requests
from requests.structures import CaseInsensitiveDict
import json
from flask import Flask
app=Flask(__name__)
@app.route('/')
def main():
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6Ing4aVhDWS1uVUZWY1pZOEd3dzVMeUpoWkhBNXhuY25Ub3NYYnNRNXhpV1kifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6InN0ZWYtdG9rZW4tZnB3a3IiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoic3RlZiIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6ImEyN2VkY2YxLTE1MTEtNGQ3My1iOWI2LTVkM2ZlMjEwZDAzYyIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OnN0ZWYifQ.VcoZgBLA8NW2iZo3qDnwtBLVFjXfXlbSzA9XpFsOH0aXZvSLKK_98z9OU4-PzFESIhOqBkIFwB3zbZaK_wWjUWjXgoVqfeNpwt7JBvlLetaY4M9WzM7GwiA8vFSUA11rPbEw8_qW5lPY_UfcoYyiFU2I7L8zYwHQckRdqQtTQtvpELh0sPN9oTIJaQ7kAgvG-OCC1-b-Wg6ONjDr5mR8qVzbesymwTqmLSq5iCfYMaAhuYypeLcfPjzx4e9VUR4x_7B4LyXNdTYs_0lhqfzJWPv5FtpQp_sxXglcs8yy0jnpZ3UgL2l_f3h7YMqxlCc9QMp5aRq1_JxRa35ExefAcA"
    ra2=requests.get("https://kubernetes:6443/api/v1/namespaces/",headers=headers,verify=False).json()
    data=len(ra2["items"])*[""]
    req=len(ra2["items"])*["https://kubernetes:6443/api/v1/namespaces/"]
    req1=len(ra2["items"])*[""]
    valeur,valeurinv=0
    for b in range(len(ra2["items"])):
        data[b]=ra2["items"][b]["metadata"]["name"]
        req[b]= req[b] + data[b] + "/pods"
        req1[b]=requests.get(req[b],headers=headers,verify=False).json()
        valeur+=len(req1[b]["items"])
    tab={}
    for a in range(valeur):
        tab[a]=None
    for b in range(len(ra2["items"])):
        for c in range(len(req1[b]["items"])):
            middle={
            "Name":req1[b]["items"][c]["metadata"]["name"],
            "Namespace":req1[b]["items"][c]["metadata"]["namespace"],
            "Creation":req1[b]["items"][c]["metadata"]["creationTimestamp"],
            "Node name":req1[b]["items"][c]["spec"]["nodeName"]
            }
            if(req1[b]["items"][c]["status"]["phase"])!="Failed":
                middle1={"Pode IP":req1[b]["items"][c]["status"]["podIP"]}
            else:
                middle1={"Pode IP":"none"}
            if "containerStatuses" in req1[b]["items"][c]["status"]:            
                middle2={"Restart Count":req1[b]["items"][c]["status"]["containerStatuses"][0]["restartCount"]}
            else:
                middle2={"Restart Count":0}
            middle1.update(middle2)
            middle.update(middle1)
            tab[valeurinv]=middle
            valeurinv+=1
    return json.dumps(tab)
app.run()













