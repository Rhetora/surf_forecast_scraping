import requests
from bs4 import BeautifulSoup as bs
import re

cheese_sandwich_energy = 1489.5

class ForecastDay:
    def __init__(self, day, energies, times):
        if day.get_text()[-2].isdigit():
            self.day = day.get_text()[0:-2]
        else:
            self.day = day.get_text()[0:-1]
        if day.get_text()[-2].isdigit():
            self.date = day.get_text()[-2:]
        else:
            self.date = day.get_text()[-1]
        self.eod = 0
        self.cols = int(day['colspan'])
        self.energies = energies
        for i in range(0, len(self.energies)):
            self.energies[i] = int(self.energies[i].get_text())
            
        self.times = times
        if len(self.times) != len(self.energies):
            raise Exception("Times and energies length mismatch")

    def display_energy(self, format):
        if format == 1:
            energy_text = "kJ"
        elif format == 2:
            energy_text = " CO-OP Cheese Sandwiches"
            for i in range(0, len(self.energies)):
                self.energies[i] = round(self.energies[i]/cheese_sandwich_energy, 2)
        print(self.day + " "+ self.date)
        for i in range(0, len(self.energies)):
            print(str(self.energies[i]) + energy_text + " at " + self.times[i].get_text())
        print("\n")

# User Input
def UserInput():
    print("Enter forecast location:")
    location = input()
    print("type 1 for wave power in kJ, or 2 for cheese sandwiches")
    energy_format = int(input())
    return location, energy_format

def buildParser(location):
    url = f"https://www.surf-forecast.com/breaks/{location}/forecasts/latest"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'http://google.com'
    }
    
    try:
        # Use requests to handle headers properly
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return bs(response.text, "html.parser")
        else:
            print(f"Error: Received status code {response.status_code}")
            return None
    except Exception as e:
        print(f"Error with url: {url} - {str(e)}")
        return None

location, energy_format = UserInput()

soup = buildParser(location)

if soup:
    energies = soup.find_all("td", attrs={"class": "forecast-table-energy__cell"})    
    days = soup.find_all("td", attrs={"class": "forecast-table-days__cell"})
    days = days[:-int(len(days)/2) or None]
    times = soup.find_all("td", attrs={"class": "forecast-table-time__cell"})

    energy_index = 0
    forecastDays = []
    for day in days:
        cols = int(day['colspan'])
        day_energies = energies[energy_index:energy_index+cols]
        day_times = times[energy_index:energy_index+cols]
        energy_index += cols
        forecastDays.append(ForecastDay(day, day_energies, day_times))

    for day in forecastDays[-5:-2]:
        day.display_energy(energy_format)
else:
    print("Failed to retrieve forecast data.")

