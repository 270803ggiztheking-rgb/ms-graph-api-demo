import urllib.request
import os

# Using a reliable placeholder service since the AI generator is returning placeholders
url = "https://placehold.co/1200x675/0d1117/58a6ff.png?text=Microsoft+Graph+API+Demo&font=roboto"
output_dir = "assets"
final_path = os.path.join(output_dir, "project-banner.png")

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

try:
    print(f"Downloading from {url}...")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        data = response.read()
        print(f"Downloaded {len(data)} bytes")
        
        with open(final_path, 'wb') as out_file:
            out_file.write(data)
            
        print(f"Saved to {final_path}")

except Exception as e:
    print(f"Error: {e}")
