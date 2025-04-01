import os
import requests
import json

from pydantic import BaseModel
from typing import List, Optional

API_BASE_URL = "https://api.1shotapi.com/v0"

# API credentials (replace with your actual key and secret)
API_KEY = os.getenv("API_KEY", "your_api_key")
API_SECRET = os.getenv("API_SECRET", "your_api_secret")
BUSINESS_ID = os.getenv("BUSINESS_ID", "your_api_secret")  # Replace with the business ID

class EndpointParam(BaseModel):
    arraySize: Optional[int]
    description: str
    id: str
    index: int
    isArray: bool
    name: str
    structId: str
    type: str
    typeSize: Optional[int]
    typeSize2: Optional[int]
    typeStruct: Optional[str]
    typeStructId: Optional[str]
    value: Optional[str]

class Endpoint(BaseModel):
    businessId: str
    callbackUrl: Optional[str]
    chain: int
    contractAddress: str
    created: int
    description: str
    escrowWalletId: str
    functionName: str
    id: str
    name: str
    nativeTransaction: bool
    params: List[EndpointParam]
    payable: bool
    publicKey: Optional[str]
    updated: int

class ExecutionResponse(BaseModel):
    apiCredentialId: str
    apiKey: str
    chain: int
    chainTransactionId: str
    completedTimestamp: Optional[int]  # Can be None
    contractAddress: str
    createdTimestamp: int
    deleted: bool
    functionName: str
    id: str
    name: str
    status: str
    transactionHash: Optional[str]  # Can be None
    transactionId: str
    updatedTimestamp: int
    userId: Optional[str]  # Can be None

# Helper function to get a bearer token
def get_bearer_token():
    url = f"{API_BASE_URL}/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = {
        "grant_type": "client_credentials",
        "client_id": API_KEY,
        "client_secret": API_SECRET,
    }
    response = requests.post(url, headers=headers, data=payload)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception(f"Failed to get token: {response.status_code}, {response.text}")
    
# Helper function to fetch available transaction endpoints
def get_endpoints(bearer_token):
    url = f"{API_BASE_URL}/business/{BUSINESS_ID}/transactions"
    headers = {"Authorization": f"Bearer {bearer_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        transactions = response.json()["response"]
        return [Endpoint(**transaction) for transaction in transactions]
    else:
        raise Exception(f"Failed to fetch transactions: {response.status_code}, {response.text}")
    
# Helper function to fetch a specific transaction endpoint
def get_endpoint(bearer_token, transactionId):
    url = f"{API_BASE_URL}/transactions/{transactionId}"
    headers = {"Authorization": f"Bearer {bearer_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return Endpoint(**response.json())
    else:
        raise Exception(f"Failed to fetch transactions: {response.status_code}, {response.text}")
    
# Helper function to call a specific transaction endpoint
def call_endpoint(bearer_token: str, endpoint: Endpoint):
    url = f"{API_BASE_URL}/transactions/{endpoint.id}/execute"
    print(f"Calling endpoint: {url}")
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json"  # Added Content-Type header
    }
    params = json.dumps(build_payload(endpoint))
    print(f"Calling endpoint with params: {params}")
    response = requests.post(url, headers=headers, data=params)
    if response.status_code == 200:
        return ExecutionResponse(**response.json())
    else:
        raise Exception(f"Failed to fetch transactions: {response.status_code}, {response.text}")

def build_payload(endpoint: Endpoint) -> dict:
    payload = {"params": {}}
    for param in endpoint.params:
        # Use the parameter's name as the key and its value as the value
        # If the value is None, you can set a default or leave it as None
        payload["params"][param.name] = str(param.value) if param.value is not None else "default_value"
    return payload