q5 = {
  "conversation": "Here are the routes for garbage collection",
  "payload": {
    "knowledge": [
      {
        "routeInfo": {
          "routeId": "unique_route_identifier",
          "name": "Route from A to B",
          "totalDistance": 15.2,
          "estimatedTime": 1800,
          "startPoint": {
            "latitude": 40.712776,
            "longitude": -74.005974,
            "name": "Location A"
          },
          "endPoint": {
            "latitude": 40.733572,
            "longitude": -73.993027,
            "name": "Location B"
          },
          "waypoints": [
            {
              "latitude": 40.721564,
              "longitude": -74.004605,
              "name": "Waypoint 1"
            },
            {
              "latitude": 40.728177,
              "longitude": -73.998227,
              "name": "Waypoint 2"
            }
          ],
          "pathSegments": [
            {
              "pathId": "path_segment_1",
              "startLatitude": 40.712776,
              "startLongitude": -74.005974,
              "endLatitude": 40.721564,
              "endLongitude": -74.004605,
              "distance": 1.2,
              "geometry": "LineString"
            },
            {
              "pathId": "path_segment_2",
              "startLatitude": 40.721564,
              "startLongitude": -74.004605,
              "endLatitude": 40.728177,
              "endLongitude": -73.998227,
              "distance": 1,
              "geometry": "LineString"
            }
          ]
        }
      }
    ],
    "widgetType": "MAP_ROUTES",
    "actionKey": "event_1_Garbage_Routes"
  }
}

q6 = {
  "conversation": "Converted to Incident",
  "payload": {
    "knowledge": [],
    "widgetType": "N/A",
    "actionKey": "event1_converted_incident"
  }
}

q7 = {
  "conversation": "I found few incidents smilar to the post in reference",
  "payload": {
    "knowledge": [
      {
        "source": "Facebook group 'JOM - Jews of Melbourne'",
        "latLang": "",
        "content": {
          "text": "Just seen a suspicious-looking man seemingly take a bunch of pictures of our house at Briggs st in Caulfield... I’m a little creeped out, did anyone else see something like that?",
          "postDatetime": "25/02/2024, 10:07",
          "reacts": {
            "likes": 17,
            "loves": 3,
            "cares": 9,
            "hahas": 0,
            "wows": 2,
            "sads": 1,
            "angry": 1
          },
          "shares": 2,
          "totalComments": 15,
          "originalPostLink": "URL_to_Original_Post"
        }
      }
    ]
  },
  "widgetType": "N/A",
  "actionKey": "event1_similar_posts"
}

q8 = {
  "conversation": "Added a note to the Orrong and Glen Eiira post",
  "payload": {
    "knowledge": [
      {
        "notes": [
          "The event in Orrong and Glen Eiira was a performed by a municipality worker, claiming he was mapping out routes for garbage disposal"
        ],
        "assumption": "Suspect may be municipality worker"
      }
    ],
    "widgetType": "N/A",
    "actionKey": "event1_update_notes"
  }
}

q9 = {
  "conversation": "Here are property crimes in the region requested ",
  "payload": {
    "knowledge": [
      {
        "crimes": [
          {
            "incidentType": "Theft",
            "latitude": "34.052235",
            "longitude": "-118.243683",
            "address": "625 S Broadway, Los Angeles, CA 90014, USA",
            "linkToGoogleMaps": "https://www.google.com/maps/place/625+S+Broadway,+Los+Angeles,+CA+90014,+USA/",
            "date": "2024-04-13"
          }
        ]
      }
    ],
    "widgetType": "N/A",
    "actionKey": "event1_display_property_crimes"
  }
}

q10 = {
  "conversation": "Decreased the General Crime Risk Level associated to the incident",
  "payload": {
    "knowledge": [
      {
        "assumption": "minor correlation to property crime in the area"
      }
    ],
    "widgetType": "N/A",
    "actionKey": "event1_update_property_crime"
  }
}

q11 = {
  "conversation": "Added Patterns of Hate Spech",
  "payload": {
    "knowledge": [
      {
        "date": "",
        "count": ""
      }
    ],
    "widgetType": "N/A",
    "actionKey": "event1_hate_speech_pattern"
  }
}

q12 = {
  "conversation": "Reduced Hate Crime to low risk level as there are insignificant hate crimes in past few months",
  "payload": {
    "knowledge": [
      {
        "assumption": "Insignificant change in hate speech in the past 3 months"
      }
    ],
    "widgetType": "N/A",
    "actionKey": "event1_modify_hate_crime"
  }
}

q13 = {
  "conversation": "Please provide a reason for closing the incident",
  "payload": {
    "knowledge": [],
    "widgetType": "N/A",
    "actionKey": "N/A"
  }
}

q14 = {
  "conversation": "the incident is closed and a summary was sent to the JC security officer",
  "payload": {
    "knowledge": [],
    "widgetType": "N/A",
    "actionKey": "event1_reporte_gen"
  }
}

q15 ={
  "conversation": "Linguistic analysis detected potential antisemitic content. We recommend further review and appropriate actions.",
  "payload": {
    "knowledge": [ ],
    "widgetType": "N/A",
    "actionKey": "event2_lang"
  }
}

q16 = {
  "conversation": "Converted to alert please update assumptions",
  "payload": {
    "knowledge": [ ],
    "widgetType": "N/A",
    "actionKey":"event2_notification_alert"
  }
}

q17 = {
  "conversation": " You have couple of options to update which one do you prefer",
  "payload": {
    "knowledge": [
      "Upload CSV",
      "Free flowing text"
    ],
    "widgetType": "SINGLE_SELECT_LIST"
  }
}

q18 = {
  "conversation": "Incident suspicious person watching JC homes(#236754),  and alert problematic iconography by person of interest(#258483) connected.Incident suspicious person watching JC homes(#236754) new level of risk is Raised from Low to HighPerson of interest Bilal Elcheikh new level of risk is High Note that level of risk for incident(#236754)  now exceeds the threashold for opening a case according to JC policy",
  "payload": {
    "knowledge": [ ],
    "widgetType": "N/A", 
    "actionKey":"event3_incident_raised"
  }
}

q19 = {
  "conversation": "Created a case #277652",
  "payload": {
    "knowledge": [ 
    {
  "datetime": "25/2/2024 10:50",
  "type": "Case",
  "policyScore": "High",
  "assignedTo": "Analyst name"
    }],
    "widgetType": "N/A",
    "actionKey":"event3_case_created"
  }
}

ontology_data = [
  {
    "name": "Municipility 01",
    "url": "",
    "imageUrl": "https://img.freepik.com/free-vector/city-hall-concept-illustration_114360-17135.jpg?w=826&t=st=1712125219~exp=1712125819~hmac=ddf33753238a9b2be82ac528c2850c4621ea9600284c243276986ab3c1d9d3b5",
    "latitude": "-37.845985",
    "longitude": "145.000935",
    "description": "",
    "address": "32 Motherwell St, South Yarra VIC 3141, Australia",
    "sensitivity": "0.0",
    "color": "#556B2F",
    "mapIcon": "municiple.png",
    "social": [],
    "create_date": "",
    "create_user": "",
    "status": "",
    "interestLevel": "",
    "occupation": "",
    "workplace": "",
    "type": "municipility"
  },
  {
    "name": "Municipility 02",
    "url": "",
    "imageUrl": "https://img.freepik.com/free-vector/city-hall-concept-illustration_114360-17135.jpg?w=826&t=st=1712125219~exp=1712125819~hmac=ddf33753238a9b2be82ac528c2850c4621ea9600284c243276986ab3c1d9d3b5",
    "latitude": "-37.895103",
    "longitude": "144.992387",
    "description": "",
    "address": "32 Drake St, Brighton VIC 3186, Australia",
    "sensitivity": "0.0",
    "color": "#556B2F",
    "mapIcon": "municiple.png",
    "social": [],
    "create_date": "",
    "create_user": "",
    "status": "",
    "interestLevel": "",
    "occupation": "",
    "workplace": "",
    "type": "municipility"
  },
  {
    "name": "Municipility 03",
    "url": "",
    "imageUrl": "https://img.freepik.com/free-vector/city-hall-concept-illustration_114360-17135.jpg?w=826&t=st=1712125219~exp=1712125819~hmac=ddf33753238a9b2be82ac528c2850c4621ea9600284c243276986ab3c1d9d3b5",
    "latitude": "-37.922107",
    "longitude": "144.996483",
    "description": "",
    "address": "19 Windermere Cres, Brighton VIC 3186, Australia",
    "sensitivity": "0.0",
    "color": "#556B2F",
    "mapIcon": "municiple.png",
    "social": [],
    "create_date": "",
    "create_user": "",
    "status": "",
    "interestLevel": "",
    "occupation": "",
    "workplace": "",
    "type": "municipility"
  },
  {
    "name": "Municipility 04",
    "url": "",
    "imageUrl": "https://img.freepik.com/free-vector/city-hall-concept-illustration_114360-17135.jpg?w=826&t=st=1712125219~exp=1712125819~hmac=ddf33753238a9b2be82ac528c2850c4621ea9600284c243276986ab3c1d9d3b5",
    "latitude": "-37.873972",
    "longitude": "145.010783",
    "description": "",
    "address": "12 St Aubins Ave, Caulfield North VIC 3161, Australia",
    "sensitivity": "0.0",
    "color": "#556B2F",
    "mapIcon": "municiple.png",
    "social": [],
    "create_date": "",
    "create_user": "",
    "status": "",
    "interestLevel": "",
    "occupation": "",
    "workplace": "",
    "type": "municipility"
  },
  {
    "name": "Municipility 05",
    "url": "",
    "imageUrl": "https://img.freepik.com/free-vector/city-hall-concept-illustration_114360-17135.jpg?w=826&t=st=1712125219~exp=1712125819~hmac=ddf33753238a9b2be82ac528c2850c4621ea9600284c243276986ab3c1d9d3b5",
    "latitude": "-37.884232",
    "longitude": "145.058022",
    "description": "",
    "address": "Carnegie VIC 3163, Australia",
    "sensitivity": "0.0",
    "color": "#556B2F",
    "mapIcon": "municiple.png",
    "social": [],
    "create_date": "",
    "create_user": "",
    "status": "",
    "interestLevel": "",
    "occupation": "",
    "workplace": "",
    "type": "municipility"
  },
  {
    "name": "Municipility 06",
    "url": "",
    "imageUrl": "https://img.freepik.com/free-vector/city-hall-concept-illustration_114360-17135.jpg?w=826&t=st=1712125219~exp=1712125819~hmac=ddf33753238a9b2be82ac528c2850c4621ea9600284c243276986ab3c1d9d3b5",
    "latitude": "-37.907224",
    "longitude": "145.027034",
    "description": "",
    "address": "18 Norman St, McKinnon VIC 3204, Australia",
    "sensitivity": "0.0",
    "color": "#556B2F",
    "mapIcon": "municiple.png",
    "social": [],
    "create_date": "",
    "create_user": "",
    "status": "",
    "interestLevel": "",
    "occupation": "",
    "workplace": "",
    "type": "municipility"
  },
  {
    "name": "Municipility 07",
    "url": "",
    "imageUrl": "https://img.freepik.com/free-vector/city-hall-concept-illustration_114360-17135.jpg?w=826&t=st=1712125219~exp=1712125819~hmac=ddf33753238a9b2be82ac528c2850c4621ea9600284c243276986ab3c1d9d3b5",
    "latitude": "-37.855392",
    "longitude": "145.02504",
    "description": "",
    "address": "14 Tower Ct, Armadale VIC 3143, Australia",
    "sensitivity": "0.0",
    "color": "#556B2F",
    "mapIcon": "municiple.png",
    "social": [],
    "create_date": "",
    "create_user": "",
    "status": "",
    "interestLevel": "",
    "occupation": "",
    "workplace": "",
    "type": "municipility"
  },
  {
    "name": "Municipility 08",
    "url": "",
    "imageUrl": "https://img.freepik.com/free-vector/city-hall-concept-illustration_114360-17135.jpg?w=826&t=st=1712125219~exp=1712125819~hmac=ddf33753238a9b2be82ac528c2850c4621ea9600284c243276986ab3c1d9d3b5",
    "latitude": "-37.85926",
    "longitude": "145.021668",
    "description": "",
    "address": "13 Inverness Ave, Armadale VIC 3143, Australia",
    "sensitivity": "0.0",
    "color": "#556B2F",
    "mapIcon": "municiple.png",
    "social": [],
    "create_date": "",
    "create_user": "",
    "status": "",
    "interestLevel": "",
    "occupation": "",
    "workplace": "",
    "type": "municipility"
  },
  {
    "name": "Municipility 09",
    "url": "",
    "imageUrl": "https://img.freepik.com/free-vector/city-hall-concept-illustration_114360-17135.jpg?w=826&t=st=1712125219~exp=1712125819~hmac=ddf33753238a9b2be82ac528c2850c4621ea9600284c243276986ab3c1d9d3b5",
    "latitude": "-37.85926",
    "longitude": "145.021668",
    "description": "",
    "address": "13 Inverness Ave, Armadale VIC 3143, Australia",
    "sensitivity": "0.0",
    "color": "#556B2F",
    "mapIcon": "municiple.png",
    "social": [],
    "create_date": "",
    "create_user": "",
    "status": "",
    "interestLevel": "",
    "occupation": "",
    "workplace": "",
    "type": "municipility"
  },
  {
    "name": "Municipility 10",
    "url": "",
    "imageUrl": "https://img.freepik.com/free-vector/city-hall-concept-illustration_114360-17135.jpg?w=826&t=st=1712125219~exp=1712125819~hmac=ddf33753238a9b2be82ac528c2850c4621ea9600284c243276986ab3c1d9d3b5",
    "latitude": "-37.835204",
    "longitude": "145.052392",
    "description": "",
    "address": "58 Pleasant Rd, Hawthorn East VIC 3123, Australia",
    "sensitivity": "0.0",
    "color": "#556B2F",
    "mapIcon": "municiple.png",
    "social": [],
    "create_date": "",
    "create_user": "",
    "status": "",
    "interestLevel": "",
    "occupation": "",
    "workplace": "",
    "type": "municipility"
  },
  {
    "name": "National 'social'ist Network",
    "url": "",
    "imageUrl": "https://t4.ftcdn.net/jpg/00/84/33/59/360_F_84335986_8kvtezwbvYl99MOIhT67tRxx3ZEC7fM6.jpg",
    "latitude": "-37.806261721099204",
    "longitude": "144.94108963946522",
    "description": "Displayed a banner reading “Expose Jewish Power” in front of a train station in Melbourne, boarded a train, handed out materials and asked passengers if they were Jewish. People affiliated with NSN posted picture of the incident and propagating the antisemitic Great Replacement conspiracy theory and on the 'social' media platform Gab, and asserted “Expose Jewish power because Jews slander gentile nationalists as baby-killers and terrorists, all the while Israel fires a missile into a Palestinian hospital killing hundreds of women and children.”",
    "address": "189 Railway Pl, West Melbourne VIC 3003, Australia",
    "sensitivity": "0.0",
    "color": "#B22222",
    "mapIcon": "past_incidents.png",
    "social": [],
    "create_date": "14/10/2023",
    "create_user": "",
    "status": "",
    "interestLevel": "",
    "occupation": "",
    "workplace": "",
    "type": "past_incidents"
  },
  {
    "name": "Arab descent",
    "url": "",
    "imageUrl": "https://t4.ftcdn.net/jpg/00/84/33/59/360_F_84335986_8kvtezwbvYl99MOIhT67tRxx3ZEC7fM6.jpg",
    "latitude": "-37.8026082291746",
    "longitude": "144.94112182597388",
    "description": " Two pieces of graffiti, both composed of “Kill JEWS”, were written on the pavement in south Melbourne.",
    "address": "103 Laurens St, North Melbourne VIC 3051, Australia",
    "sensitivity": "0.0",
    "color": "#B22222",
    "mapIcon": "past_incidents.png",
    "social": [],
    "create_date": "13/10/2023",
    "create_user": "",
    "status": "",
    "interestLevel": "",
    "occupation": "",
    "workplace": "",
    "type": "past_incidents"
  },
  {
    "name": "Group of Arab descents",
    "url": "",
    "imageUrl": "https://t4.ftcdn.net/jpg/00/84/33/59/360_F_84335986_8kvtezwbvYl99MOIhT67tRxx3ZEC7fM6.jpg",
    "latitude": "-37.83616136793307",
    "longitude": "144.9766517670443",
    "description": "A car full of men of ‘Arab descent’ reportedly boasted they were ‘on the hunt to kill Jews’ as they cruised around a Melbourne suburb, with police on alert for anti-Semitic threats in the wake of the Israel-Hamas war",
    "address": "2/8 Toorak Rd, South Yarra VIC 3141, Australia",
    "sensitivity": "0.0",
    "color": "#B22222",
    "mapIcon": "past_incidents.png",
    "social": [],
    "create_date": "11/10/2023",
    "create_user": "",
    "status": "",
    "interestLevel": "",
    "occupation": "",
    "workplace": "",
    "type": "past_incidents"
  },
  {
    "name": "The man, a self-proclaimed 'Nazi'",
    "url": "",
    "imageUrl": "https://t4.ftcdn.net/jpg/00/84/33/59/360_F_84335986_8kvtezwbvYl99MOIhT67tRxx3ZEC7fM6.jpg",
    "latitude": "-37.882925549488306",
    "longitude": "145.00492131063197",
    "description": "Jewish students threatened with a knife on a bus in Melbourne, Australia. Jewish Students from the Leibler Yavneh College in Australia were traveling on a public bus when they were abused with antisemitic obscenities by a knife-wielding man on Thursday, according to a press release from the Anti-Defamation Commission (ADC).",
    "address": "22 Staniland Grove, Elsternwick VIC 3185, Australia",
    "sensitivity": "0.0",
    "color": "#B22222",
    "mapIcon": "past_incidents.png",
    "social": [],
    "create_date": "05/08/2023",
    "create_user": "",
    "status": "",
    "interestLevel": "",
    "occupation": "",
    "workplace": "",
    "type": "past_incidents"
  },
  {
    "name": "Children in a public school",
    "url": "",
    "imageUrl": "https://t4.ftcdn.net/jpg/00/84/33/59/360_F_84335986_8kvtezwbvYl99MOIhT67tRxx3ZEC7fM6.jpg",
    "latitude": "-37.80165672201562",
    "longitude": "144.9798424238497",
    "description": "A Jewish family from Melbourne told Daily Mail Australia that their teenage daughter had been targeted by high school students. Her mother, who wished to remain anonymous, said a series of antisemitic incidents had been directed at her daughter since the start of the year, well before the current Israel/Hamas conflict. 'She has been sent swastikas online. One child repeatedly approached her and told her 'Knock Knock' jokes in which the butt of the jokes are 'dead Jews,' she said. 'Another student approached her and declared: I will gas you and your whole family.'",
    "address": "Whitlam Place, Fitzroy VIC 3065, Australia",
    "sensitivity": "0.0",
    "color": "#B22222",
    "mapIcon": "past_incidents.png",
    "social": [],
    "create_date": "01/09/2023",
    "create_user": "",
    "status": "",
    "interestLevel": "",
    "occupation": "",
    "workplace": "",
    "type": "past_incidents"
  },
  {
    "name": "Free Palestine Melbourne activists",
    "url": "",
    "imageUrl": "https://t4.ftcdn.net/jpg/00/84/33/59/360_F_84335986_8kvtezwbvYl99MOIhT67tRxx3ZEC7fM6.jpg",
    "latitude": "-37.886531299065524",
    "longitude": "145.02208483972316",
    "description": "Clashes between pro-Palestinian and pro-Israeli groups in Melbourne's south-east. A rally was organised on Friday, with a spokesperson for Free Palestine Melbourne saying it was organised in response to an arson attack on a burger shop on Glenhuntly Road in Caulfield, owned by a man of Palestinian heritage. Police said on Friday they were treating the fire at Burgertory as suspicious, but repeatedly said they did not believe it was linked to the owner's attendance at an earlier pro-Palestinian rally. Small numbers of people, some draped in Israeli flags, had gathered near the boarded-up burger store throughout the day.",
    "address": "340 Hawthorn Rd, Caulfield VIC 3162, Australia",
    "sensitivity": "0.0",
    "color": "#B22222",
    "mapIcon": "past_incidents.png",
    "social": [],
    "create_date": "11/11/2023",
    "create_user": "",
    "status": "",
    "interestLevel": "",
    "occupation": "",
    "workplace": "",
    "type": "past_incidents"
  },
  {
    "name": "Unknown",
    "url": "",
    "imageUrl": "https://t4.ftcdn.net/jpg/00/84/33/59/360_F_84335986_8kvtezwbvYl99MOIhT67tRxx3ZEC7fM6.jpg",
    "latitude": "-37.88513402181724",
    "longitude": "145.02137483642312",
    "description": "The word 'genocide' and a picture of the Palestinian flag were found spray-painted across the Beth Weizmann Community Centre.",
    "address": "304 Hawthorn Rd, Caulfield South VIC 3162, Australia",
    "sensitivity": "0.0",
    "color": "#B22222",
    "mapIcon": "past_incidents.png",
    "social": [],
    "create_date": "07/10/2023",
    "create_user": "",
    "status": "",
    "interestLevel": "",
    "occupation": "",
    "workplace": "",
    "type": "past_incidents"
  },
  {
    "name": "Muslim Crowd",
    "url": "",
    "imageUrl": "https://t4.ftcdn.net/jpg/00/84/33/59/360_F_84335986_8kvtezwbvYl99MOIhT67tRxx3ZEC7fM6.jpg",
    "latitude": "-37.89368640521054",
    "longitude": "145.0227894868903",
    "description": "A synagogue in the Australian city of Melbourne was evacuated on police order on Shabbat as pro-Palestinian protesters demonstrated nearby.",
    "address": "Caulfield South VIC 3162, Australia",
    "sensitivity": "0.0",
    "color": "#B22222",
    "mapIcon": "past_incidents.png",
    "social": [],
    "create_date": "13/11/2023",
    "create_user": "",
    "status": "",
    "interestLevel": "",
    "occupation": "",
    "workplace": "",
    "type": "past_incidents"
  },
  {
    "name": "A group of young men inside the car",
    "url": "",
    "imageUrl": "https://t4.ftcdn.net/jpg/00/84/33/59/360_F_84335986_8kvtezwbvYl99MOIhT67tRxx3ZEC7fM6.jpg",
    "latitude": "-37.880527532151596",
    "longitude": "145.0305463950657",
    "description": "Rabbi walking with young child on Melbourne street confronted with alleged antisemitic threats",
    "address": "84 Bambra Rd, Caulfield North VIC 3161, Australia",
    "sensitivity": "0.0",
    "color": "#B22222",
    "mapIcon": "past_incidents.png",
    "social": [],
    "create_date": "11/10/2023",
    "create_user": "",
    "status": "",
    "interestLevel": "",
    "occupation": "",
    "workplace": "",
    "type": "past_incidents"
  },
  {
    "name": "Pro-Palestinian protestors",
    "url": "",
    "imageUrl": "https://t4.ftcdn.net/jpg/00/84/33/59/360_F_84335986_8kvtezwbvYl99MOIhT67tRxx3ZEC7fM6.jpg",
    "latitude": "-37.81497538763534",
    "longitude": "144.96664039908464",
    "description": "A member of Melbourne’s Jewish community claims she and her husband were attacked by pro-Palestinian protestors outside the Melbourne Town Hall. The attack happened last night as the City of Melbourne voted down a motion for the council to call for a ceasefire in Gaza.",
    "address": "Melbourne Town Hall, Melbourne VIC 3000, Australia",
    "sensitivity": "0.0",
    "color": "#B22222",
    "mapIcon": "past_incidents.png",
    "social": [],
    "create_date": "21/02/2024",
    "create_user": "",
    "status": "",
    "interestLevel": "",
    "occupation": "",
    "workplace": "",
    "type": "past_incidents"
  },
  {
    "name": "Layla Ahmed Ibrahim",
    "url": "",
    "imageUrl": "/images/layla_ahmed_ibrahim.png",
    "latitude": "-37.817677963769526",
    "longitude": "144.99396042575503",
    "description": "Took photos of the jewish community ",
    "address": "123 Bridge Rd, Richmond VIC 3121",
    "sensitivity": "0.0",
    "color": "#e8ada0",
    "mapIcon": "poi_marker.png",
    "social": [],
    "create_date": "4/24/2023",
    "create_user": "",
    "status": "existing",
    "interestLevel": "high",
    "occupation": "Barista",
    "workplace": "Richmond",
    "type": "poi"
  },
  {
    "name": "Jamal Hassan Reza",
    "url": "",
    "imageUrl": "/images/jamal_hassan_reza.png",
    "latitude": "-37.814688456905664",
    "longitude": "144.96318302575494",
    "description": "wrote antisemitic post on Facebook",
    "address": "Level 12, 500 Bourke St, Melbourne VIC 3000",
    "sensitivity": "0.0",
    "color": "#e8ada0",
    "mapIcon": "poi_marker.png",
    "social": [],
    "create_date": "3/13/2024",
    "create_user": "",
    "status": "new",
    "interestLevel": "medium",
    "occupation": "Architect",
    "workplace": "Collingwood",
    "type": "poi"
  },
  {
    "name": "Yasmin Aisha Khatun",
    "url": "",
    "imageUrl": "/images/yasmin_aisha_khatun.png",
    "latitude": "-37.82336905157906",
    "longitude": "144.95808456808447",
    "description": "Antesemitic comment on Twitter",
    "address": "Crown Melbourne, 8 Whiteman St, Southbank VIC 3006",
    "sensitivity": "0.0",
    "color": "#e8ada0",
    "mapIcon": "poi_marker.png",
    "social": [],
    "create_date": "8/22/2022",
    "create_user": "",
    "status": "exisiting ",
    "interestLevel": "medium ",
    "occupation": "Chef",
    "workplace": "Southbank",
    "type": "poi"
  },
  {
    "name": "Amir Mohammed Farhan",
    "url": "",
    "imageUrl": "/images/amir_mohammed_farhan.png",
    "latitude": "-37.82040394544925",
    "longitude": "144.9499054680843",
    "description": "Clashed with young Jews near a synagogue",
    "address": "WeWork, 727 Collins St, Docklands VIC 3008",
    "sensitivity": "0.0",
    "color": "#e8ada0",
    "mapIcon": "poi_marker.png",
    "social": [],
    "create_date": "8/22/2022",
    "create_user": "",
    "status": "new",
    "interestLevel": "high",
    "occupation": "Web Developer",
    "workplace": "Docklands",
    "type": "poi"
  },
  {
    "name": "Sara bint Abdullah",
    "url": "",
    "imageUrl": "/images/sara_bint_abdullah.png",
    "latitude": "-37.784075790402554",
    "longitude": "144.9841956680829",
    "description": "Antesemitic comment on Twitter",
    "address": "Fitzroy North Primary School, 25 Brunswick St, Fitzroy North VIC 3065",
    "sensitivity": "0.0",
    "color": "#e8ada0",
    "mapIcon": "poi_marker.png",
    "social": [],
    "create_date": "7/12/2023",
    "create_user": "",
    "status": "new",
    "interestLevel": "medium",
    "occupation": "Teacher",
    "workplace": "Fitzroy North",
    "type": "poi"
  },
  {
    "name": "Khalid Reza Ali",
    "url": "",
    "imageUrl": "/images/khalid_reza_ali.png",
    "latitude": "-37.82713651118103",
    "longitude": "145.03482539692",
    "description": "Threatening a Jewish student",
    "address": "Studio K, 564 Glenferrie Rd, Hawthorn VIC 3122",
    "sensitivity": "0.0",
    "color": "#e8ada0",
    "mapIcon": "poi_marker.png",
    "social": [],
    "create_date": "3/14/2024",
    "create_user": "",
    "status": "new",
    "interestLevel": "high",
    "occupation": "Graphic Designer",
    "workplace": "Hawthorn",
    "type": "poi"
  },
  {
    "name": "Noor Fatima bint Mohammed",
    "url": "",
    "imageUrl": "/images/noor_fatima_bint_mohammed.png",
    "latitude": "-37.795858179989104",
    "longitude": "144.8853806969189",
    "description": "Laughing emoji under antesemitic post",
    "address": "Rapid Plumbing, 1/24 Essex St, Footscray VIC 3011",
    "sensitivity": "0.0",
    "color": "#e8ada0",
    "mapIcon": "poi_marker.png",
    "social": [],
    "create_date": "8/10/2023",
    "create_user": "",
    "status": "exisiting",
    "interestLevel": "low",
    "occupation": "Plumber",
    "workplace": "Footscray",
    "type": "poi"
  },
  {
    "name": "Ibrahim Hassan Omar",
    "url": "",
    "imageUrl": "/images/ibrahim_hassan_omar.png",
    "latitude": "-37.7691146423713",
    "longitude": "144.9615048935992",
    "description": "Antesemitic comment on Twitter",
    "address": "Petal Power, 353 Sydney Rd, Brunswick VIC 3056",
    "sensitivity": "0.0",
    "color": "#e8ada0",
    "mapIcon": "poi_marker.png",
    "social": [],
    "create_date": "2/7/2024",
    "create_user": "",
    "status": "new",
    "interestLevel": "medium",
    "occupation": "Florist",
    "workplace": "Brunswick",
    "type": "poi"
  },
  {
    "name": "Aisha bint Khalid",
    "url": "",
    "imageUrl": "/images/aisha_bint_khalid.png",
    "latitude": "-37.859590630628745",
    "longitude": "144.97794122575675",
    "description": "Antesemitic comment on Facebook",
    "address": "St Kilda Road Medical Centre, 127 Fitzroy St, St Kilda VIC 3182",
    "sensitivity": "0.0",
    "color": "#e8ada0",
    "mapIcon": "poi_marker.png",
    "social": [],
    "create_date": "3/3/2024",
    "create_user": "",
    "status": "new",
    "interestLevel": "meium",
    "occupation": "Doctord",
    "workplace": "St Kilda",
    "type": "poi"
  },
  {
    "name": "Omar Ali Mohammed",
    "url": "",
    "imageUrl": "/images/omar_ali_monammed.png",
    "latitude": "-37.741596509857374",
    "longitude": "144.96628593924586",
    "description": "Laughing emoji under antesemitic post",
    "address": "Sparks R Us, 485 Sydney Rd, Coburg VIC 3058",
    "sensitivity": "0.0",
    "color": "#e8ada0",
    "mapIcon": "poi_marker.png",
    "social": [],
    "create_date": "2/27/2024",
    "create_user": "",
    "status": "new",
    "interestLevel": "low",
    "occupation": "Electrician",
    "workplace": "Coburg",
    "type": "poi"
  }
]