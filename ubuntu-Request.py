import requests
import os
from urllib.parse import urlparse
import sys

# Define the directory for saved images
IMAGE_DIR = "Fetched_Images"

# Sample URL for testing purposes (a small, reliable image)
SAMPLE_URL = "https://www.w3.org/People/Raggett/site/img/logo.gif"

def get_filename_from_url(url):
    """
    Extracts the filename from the URL path.
    If the path is empty, it returns a default name.
    """
    try:
        # Parse the URL
        parsed_url = urlparse(url)
        # Extract the base path (the part after the last '/')
        filename = os.path.basename(parsed_url.path)
        
        # If no filename is found, provide a default
        # Also check if it looks like a file (e.g., has an extension)
        if not filename or '.' not in filename:
            # You might want to try to get the content-disposition header here,
            # but for simplicity, we stick to the URL path as per assignment starter code.
            return "downloaded_image.jpg"
            
        return filename
        
    except Exception as e:
        print(f"Error parsing URL for filename: {e}", file=sys.stderr)
        return "downloaded_image.jpg"


def main():
    """
    Main function to run the Ubuntu Image Fetcher.
    """
    # 1. Terminal Output Welcome Text
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web")
    print("-" * 40)

    # 2. Prompt the user for a URI, including the sample URL for easy copy/paste testing
    print(f"Sample URL for testing: {SAMPLE_URL}")
    # The user can copy the sample URL or enter their own.
    url = input("Please enter the image URL: ")

    # Check for empty input and use the sample as a fallback (optional, but helpful)
    if not url:
         print(f"\nNo URL entered. Using sample URL: {SAMPLE_URL}")
         url = SAMPLE_URL

    try:
        # 3. Create a directory called "Fetched_Images" if it doesn't exist
        os.makedirs(IMAGE_DIR, exist_ok=True)
        
        # Set a timeout for the request to prevent hanging
        timeout_seconds = 10
        
        # 4. Downloads the image from the provided URL
        # Use a stream for efficient handling of large files
        response = requests.get(url, timeout=timeout_seconds, stream=True)
        
        # Check for HTTP errors (e.g., 404, 500)
        # 5. Handles errors gracefully - part 1: HTTP errors
        response.raise_for_status() 

        # Extract an appropriate filename
        filename = get_filename_from_url(url)
        
        # Create the full file path
        filepath = os.path.join(IMAGE_DIR, filename)
        
        # Print success message for fetching
        print(f"✓ Successfully fetched: {filename}")

        # Save the image to the Fetched_Images directory with an appropriate filename
        # Save in binary mode ('wb') as required
        with open(filepath, 'wb') as f:
            # Write the content in chunks, better for large files
            for chunk in response.iter_content(chunk_size=8192):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)

        # Print success message for saving
        print(f"✓ Image saved to {filepath}")
        
    # 5. Handles errors gracefully - part 2: Connection and Request errors
    except requests.exceptions.RequestException as e:
        # This catches all requests-related errors (network issues, timeouts, HTTP errors from raise_for_status)
        print(f"✗ Error: Could not fetch image from URL: {e}", file=sys.stderr)
    except OSError as e:
        # This catches errors related to file system (e.g., directory creation/writing permissions)
        print(f"✗ File System Error: Could not save the image: {e}", file=sys.stderr)
    except Exception as e:
        # Catch any other unexpected errors
        print(f"✗ An unexpected error occurred: {e}", file=sys.stderr)
    finally:
        # Final message in the spirit of Ubuntu
        print("-" * 40)
        print("Connection strengthened. Community enriched.")


if __name__ == "__main__":
    main()