#!/usr/bin/env python3
# Author: Dr. Aaron Schulman, Assistant Professor @ UCSD CSE
import sys
from Cryptodome.Cipher import AES
import base64
import argparse
import urllib.parse
import base64
import requests
import hashlib
import xml.etree.ElementTree as ET

EPIC_CRYPTO_IV = bytes([222, 173, 190, 239, 222, 173, 190, 239, 222, 173, 190, 239, 222, 173, 190, 239])
EPIC_CRYPTO_URL_KEY = bytes([57, 70, 69, 51, 67, 56, 54, 69, 57, 54, 67, 53, 67, 67, 57, 67])
   
def is_base64(s):
  try:
    # Check if the string is a valid base64 string
    if base64.b64encode(base64.b64decode(s)).decode('utf-8') == s:
        return True
    return False
  except Exception:
    return False

def decrypt_base64(base64_str, key, iv):
  # Step 1: Decode the base64 string to bytes
  encrypted_data = base64.b64decode(base64_str)
    
  # Step 2: Decrypt the data using AES with PKCS5 padding
  cipher = AES.new(key, AES.MODE_CBC, iv)
  decrypted_data = cipher.decrypt(encrypted_data)
    
  # If the result is padded, remove the padding
  def unpad(s):
    return s[:-s[-1]]
    
  # Step 3: Unpad the decrypted data
  decrypted_data = unpad(decrypted_data)
    
  # Print the decrypted result as a string
  return decrypted_data.decode('utf-8')

def create_config_crypto_key(password):
  key_str = f"{password}Epic Scrambler"

  # Step 1: Hash the input string using SHA-1
  hash_object = hashlib.sha1(key_str.encode("utf-16le"))
  
  # Step 2: Convert the hash to an uppercase hexadecimal string
  hex_string = hash_object.hexdigest().upper()
  print(hex_string)
  
  # Step 3: Take the first 16 characters of the hex string
  first_16_chars = hex_string[:16]
  
  # Step 4: Convert the first 16 characters into a byte array
  return bytearray([ord(char) for char in first_16_chars])

def download_and_decrypt_config(url, password):
  # Download the XML content
  response = requests.get(url)
  
  # Check if the request was successful
  if response.status_code == 200:
    # Parse the XML content
    root = ET.fromstring(response.content)
  else:
    sys.exit(f"Failed to download XML. Status code: {response.status_code}")

  # Check if the Data element was found and decrypt its contents
  data_element = root.find('Data')
  if data_element is not None:
    base64_str = data_element.text
  else:
    sys.exit("Data element not found in the XML.")

  # Decrypt the config file and XML parse it
  try:
    config_key = create_config_crypto_key(password)
    decrypted_data = decrypt_base64(base64_str, config_key, EPIC_CRYPTO_IV)
    decrypted_data_root = ET.fromstring(decrypted_data)

    # Add the decrypted config file to the XML tree
    data_element.clear()
    data_element.append(decrypted_data_root)
  except:
    print("Error: Failed to decrypt config data, brute forcing password for config.")

  # Now you can work with the XML tree 'root'
  print(ET.tostring(root, encoding='utf-8').decode('utf-8'))

def main():
    parser = argparse.ArgumentParser(description="Downloads and decrypts the config file for a Epic Haiku Instance.")
    parser.add_argument('url', type=str, help='Epic Haiku Setup URL')
    parser.add_argument('--password', type=str, default='', help='Password (Often supplied in Epic setup instructions)')
    args = parser.parse_args()

    # Parse the URL and extract the path
    parsed_url = urllib.parse.urlparse(args.url)
    path = parsed_url.path
    
    # Get the last part of the path
    last_part = path.split('/')[-1]
    
    # URL decode the last part
    decoded_string = urllib.parse.unquote(last_part)
    
    # Check if the decoded config string is valid Base64
    if (not is_base64(decoded_string)):
      sys.exit("The URL path does not not end in a valid Base64 string.")

    # Decrypt the config file URL from the base64 string
    config_file_url = decrypt_base64(decoded_string, EPIC_CRYPTO_URL_KEY, EPIC_CRYPTO_IV)
    print(f"Decrypted Config File URL: {config_file_url}")

    download_and_decrypt_config(config_file_url, args.password)

if __name__ == '__main__':
    main()
