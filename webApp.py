from flask import Flask, url_for, request, render_template, jsonify
import requests

import json

app = Flask(__name__)
 
@app.route('/')
def index():
   return render_template ('index.html')


@app.route("/wetter", methods = ['POST', 'GET'])
def wetter():
   global stadt
   temperature = ''
   if request.method == "POST":
      stadt = request.form['stadt']

      import requests

      # Define the API endpoint and the query parameters
      endpoint = "https://nominatim.openstreetmap.org/search"
      params = {
         "q": stadt,  # The address to geocode
         "format": "jsonv2"  # The response format
      }

      # Send a GET request to the API endpoint
      response = requests.get(endpoint, params=params)

      # Check if the request was successful
      if response.status_code == 200:
         # Parse the JSON response
         data = response.json()

         # Extract the latitude and longitude from the response
         lat = data[0]["lat"]
         lon = data[0]["lon"]

         # Print the coordinates
      else:
         print("An error occurred while fetching the coordinates.")




      api_key = "f37908b35efdf1d8201b485bd80510ab"
      url = f"http://api.openweathermap.org/data/2.5/weather?q={stadt}&appid={api_key}"


      response = requests.get(url).json()
      # get current temperature and convert it into Celsius
      current_temperature = response.get('main', {}).get('temp')
      if current_temperature:
         current_temperature_celsius = int(current_temperature - 273.15)
         return render_template('temperature.html', stadt = stadt.title(), temperature = current_temperature_celsius, Latitude =lat, Longitude = lon)

      else:
         return f'Error getting temperature for {stadt.title()}'


   else:
      return 'Fehler'



@app.route('/uhrzeit')
def uhrzeit():
      response = requests.get(
         f"https://timezone.abstractapi.com/v1/current_time/?api_key=fbdee759315c4fffa16bfd803165e9fd&location={stadt}, Germany")
      zeit = response.get('b', {}).get('datetime')
      return render_template('uhrzeit.html', stadt = stadt, data = zeit)



if __name__ == '__main__':
   app.run(port = 1337, debug= True)