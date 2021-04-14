from django.shortcuts import render,HttpResponseRedirect,reverse
import geocoder,json,requests,locale

# Create your views here.
detail = []
def home(request):
    locale.setlocale(locale.LC_ALL,'')
    g = geocoder.ip('me')
    # print(g.country)
    url = 'https://api.covid19api.com/summary'
    req = requests.get(url)
    data = req.json()
    country_data = dict()  
    print(data)
    country_data['TotalInfected'] = f"{data['Global']['TotalConfirmed']:,d}"
    country_data['TotalRecovered'] = f"{data['Global']['TotalRecovered']:,d}"
    country_data['TotalDeaths'] = f"{data['Global']['TotalDeaths']:,d}"
    country_data['NewCases'] = f"{data['Global']['NewConfirmed']:,d}"
    country_data['NewDeaths'] = f"{data['Global']['NewDeaths']:,d}"
    country_data['NewRecovered'] = f"{data['Global']['NewRecovered']:,d}"
    country_data['Country'] = []
    country_data['Cases'] = [] 
    country_data['CountryCode'] = []
    countries = data['Countries']
    for i in countries:
        print(f"Country: {i['Country']}")
        print(f"Infected: {i['TotalConfirmed']}")
        print()
        country_data["Country"].append(i['Country']) 
        country_data["Cases"].append(i['TotalConfirmed'])  
        country_data["CountryCode"].append(i['CountryCode'])
    print(country_data.get('Country')[0])
    print(country_data.get('Cases')[0])
    print()             
    print(country_data) 
    detail.append(data)
    detail.append(country_data)
    return render(request,'tracker/index.html', {'data':country_data})

def country_detail(request,country_name):   
    data = detail[0]
    country_data = dict()
    country_data['Country'] = []
    country_data['Cases'] = []
    country_data['Deaths'] = []
    country_data['Recovered'] = []
    country_data['NewCases'] = []
    country_data['NewRecovered'] = []
    country_data['NewDeaths'] = []
    countries = data['Countries']
    for i in countries:
        if i['Country'] == country_name:
            country_data['Country'] = i['Country']
            country_data['Cases'] = f"{i['TotalConfirmed']:,d}"
            country_data['Recovered'] = f"{i['TotalRecovered']:,d}"
            country_data['Deaths'] = f"{i['TotalDeaths']:,d}"
            country_data['NewCases'] = f"{i['NewConfirmed']:,d}"
            country_data['NewRecovered'] = f"{i['NewRecovered']:,d}"
            country_data['NewDeaths'] = f"{i['NewDeaths']:,d}"            
            break

    return render(request,'tracker/index.html',{'country':country_data,'data':detail[1]})   

def about(request):
    return render(request,'tracker/about.html')
    
                 