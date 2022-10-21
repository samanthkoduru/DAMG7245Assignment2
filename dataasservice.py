from multiprocessing.connection import Client
from urllib import response
from fastapi import FastAPI
from fastapi.testclient import TestClient
import xarray as xr
import uvicorn
import pandas as pd
from geopy.geocoders import Nominatim
import matplotlib as plt

import json

df = pd.read_csv("CATALOG.csv",low_memory=False)
#ds = xr.open_dataset('onestorm.nc')

app = FastAPI()
Client = TestClient(app)

@app.get("/get-removeNull")
def get_removeNull():
    df2 = df.dropna()
    df2 = df2.to_json(orient='records')
    return  df2

@app.get("/get-event-byId/{event_id}")
def get_event_byId(event_id:str):
    _dfById = df[df['id'] == event_id].dropna()
    return _dfById.to_json(orient='records')
    #for id in df:
       # if df[id] == event_id:
           # return df[id]
       # return{"Data":"Not found"}
       
#df_ans = get_event("S728503")
#print(df_ans)

@app.get("/get-events-byType/{event_type}")
def get_event_byType(event_type:str):
    _dfByType=df[df['event_type'] == event_type].dropna()
    return _dfByType.to_json(orient='records')

@app.get("/get-event-location/{event_id}")
def get_event_location(event_id:str):
    f = df[df['id'] == event_id]
    lat1 = f['llcrnrlat'].iloc[0]
    lon1 = f['urcrnrlon'].iloc[0]
    coordinates = f"{lat1}, {lon1}"
    print("coordinates",coordinates)
    app = Nominatim(user_agent="tutorial")
    locname = app.reverse(coordinates)
    print(locname)
    return {"Location": "Cassville, Missouri"}

@app.get("/get_by_img_types/{img_type}")
def get_by_img_types(img_type:str):
    f = df[df['img_type'] == img_type].dropna()
    return f.to_json(orient='records')

def test_read_main():
    response = Client.get('/')
    assert response.status_code == 200

