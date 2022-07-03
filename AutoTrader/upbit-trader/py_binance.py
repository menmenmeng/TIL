import requests
import json
import jwt
import uuid
import hashlib
from urllib.parse import urlencode


baseUrl = 'https://api.binance.com'

# spare base Urls
baseUrl_spare = [
    'https://api1.binance.com',
    'https://api2.binance.com',
    'https://api3.binance.com'
]
# All endpoints return either a JSON object or array. Data is returned in ascending order. Oldest first, newest last. All time and timestamp related fields are in milliseconds.

