import requests
import sys

def lookup_ip(ip):
    try:
        url = f"http://ip-api.com/json/{ip}"
        response = requests.get(url)
        data = response.json()
        
        if data['status'] == 'fail':
            print(f"Error: {data['message']}")
            return

        print(f"IP: {data['query']}")
        print(f"Country: {data.get('country')}")
        print(f"Region: {data.get('regionName')}")
        print(f"City: {data.get('city')}")
        print(f"ISP: {data.get('isp')}")
        print(f"Org: {data.get('org')}")
        print(f"AS: {data.get('as')}")
        print(f"Lat/Lon: {data.get('lat')}, {data.get('lon')}")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        lookup_ip(sys.argv[1])
    else:
        # If no IP provided, look up the current machine's public IP
        lookup_ip("")
