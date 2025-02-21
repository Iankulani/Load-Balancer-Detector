import requests

def is_load_balancer(ip_address):
    # Define some common load balancer header patterns
    load_balancer_headers = [
        "X-Forwarded-For", 
        "X-Load-Balancer", 
        "X-Real-IP", 
        "X-Cluster-Client-IP", 
        "X-Proxy-Client-IP",
        "X-Forwarded-Host"
    ]
    
    try:
        # Send a request to the IP address
        response = requests.get(f'http://{ip_address}')
        
        # Check for common load balancer headers in the response
        for header in load_balancer_headers:
            if header in response.headers:
                print(f"Load balancer detected! Header found: {header}")
                return True

        # Check if the IP is a known public cloud IP (optional, for a better guess)
        # Some public cloud providers (AWS, GCP, Azure) often use load balancers.
        cloud_providers = ['aws', 'google', 'azure']
        for provider in cloud_providers:
            if provider in response.text.lower():
                print(f"Likely load balancer (from {provider} provider) detected!")
                return True
        
        print("No obvious load balancer indicators found.")
        return False

    except requests.RequestException as e:
        print(f"Error contacting IP: {e}")
        return False

def main():
    # Prompt the user to enter the public IP address
    ip_address = input("Enter the IP address to check if it's a Load Balancer: ")
    
    # Detect if the IP address is a load balancer
    if is_load_balancer(ip_address):
        print(f"The IP {ip_address} is likely a load balancer.")
    else:
        print(f"The IP {ip_address} does not seem to be a load balancer.")

if __name__ == "__main__":
    main()
