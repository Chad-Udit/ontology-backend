q5 = {
  "conversation": "Here are the routes for garbage collection",
  "payload": {
    "knowledge": [
      {
  "routeInfo": {
    "routeID": "unique_route_identifier",
    "name": "Route from A to B",
    "totalDistance": 15.2, # in kilometers
    "estimatedTime": 1800, # in seconds
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
      # Additional waypoints can be included here
    ],
    "pathSegments": [
      {
        "pathID": "path_segment_1",
        "startLatitude": 40.712776,
        "startLongitude": -74.005974,
        "endLatitude": 40.721564,
        "endLongitude": -74.004605,
        "distance": 1.2, # Distance of this segment in kilometers
        "geometry": "LineString" # This can be a detailed LineString geometry in WKT or GeoJSON format if needed
      },
      {
        "pathID": "path_segment_2",
        "startLatitude": 40.721564,
        "startLongitude": -74.004605,
        "endLatitude": 40.728177,
        "endLongitude": -73.998227,
        "distance": 1.0,
        "geometry": "LineString"
      }
      # Additional path segments can be included here
    ]
  }
}

    ],
    "widget_type": "Map Routes",
    "action_key":"event_1_Garbage_Routes"
  }
}

q6 = {
  "conversation": "Converted to Incident",
  "payload": {
    "knowledge": [],
    "widget_type": "N/A",
    "action_key":"event1_converted_incident"
  }
}

q7 = {
  "conversation": "I found few incidents smilar to the post in reference",
  "payload": {
    "knowledge": [ 

    {
      "source": "Facebook group 'JOM - Jews of Melbourne'",
      "lat_lang":"",
      "content": {
        "text": "Just seen a suspicious-looking man seemingly take a bunch of pictures of our house at Briggs st in Caulfield... I’m a little creeped out, did anyone else see something like that?",
        "postDatetime": "25/02/2024, 10:07",
        "reacts": {
          "likes": 17,
          "loves": 3,
          "cares": 9,
          "hahas": 0, # Assuming hahas is required even if 0
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
    "widget_type": "N/A",
    "action_key":"event1_similar_posts"
}

q8 = {
  "conversation": "Added a note to the Orrong and Glen Eiira post",
  "payload": {
    "knowledge": [ {
      "notes": ["The event in Orrong and Glen Eiira was a performed by a municipality worker, claiming he was mapping out routes for garbage disposal"],
      "assumption":"Suspect may be municipality worker"}
    ],
    "widget_type": "N/A",
    "action_key":"event1_update_notes"
  }
}

q9 = {
  "conversation": "Here are property crimes in the region requested ",
  "payload": {
    "knowledge": [ {
     "crimes":[{
  "incidentType": "Theft",
  "latitude": "34.052235",
  "longitude": "-118.243683",
  "address": "625 S Broadway, Los Angeles, CA 90014, USA",
  "linkToGoogleMaps": "https://www.google.com/maps/place/625+S+Broadway,+Los+Angeles,+CA+90014,+USA/",
  "date": "2024-04-13"
}]
    }],
    "widget_type": "N/A",
    "action_key":"event1_display_property_crimes"
  }
}

q10 = {
  "conversation": "Decreased the General Crime Risk Level associated to the incident",
  "payload": {
    "knowledge": [ {
     
      "assumption":"minor correlation to property crime in the area"}
    ],
    "widget_type": "N/A",
    "action_key":"event1_update_property_crime"
  }
}

q11 = {
  "conversation": "Added Patterns of Hate Spech",
  "payload": {
    "knowledge": [ {"date:"", count:"}
    ],
    "widget_type": "N/A",
    "action_key":"event1_hate_speech_pattern"
  }
}

q12 = {
  "conversation": "Reduced Hate Crime to low risk level as there are insignificant hate crimes in past few months",
  "payload": {
   "assumption":"Insignificant change in hate speech in the past 3 months"},
    "widget_type": "N/A",
    "action_key":"event1_modify_hate_crime"
  }

q13 = {
  "conversation": "Please provide a reason for closing the incident",
  "payload": {
    "knowledge": [ ],
    "widget_type": "N/A",
    "action_key":"N/A"
  }
}

q14 = {
  "conversation": "the incident is closed and a summary was sent to the JC security officer",
  "payload": {
    "knowledge": [ ],
    "widget_type": "N/A",
    "action_key":"event1_reporte_gen"
  }
}