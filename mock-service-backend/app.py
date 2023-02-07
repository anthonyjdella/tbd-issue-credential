from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Hello, Flask!"


@app.route("/v1/dids/key", methods=["PUT"])
def create_key():
    data = request.get_json()
    key_type = data.get('keyType')
    did_type = data.get('didType')
    print(f"Creating a key for keytpe: {key_type} and didtype: {did_type}")

    issuer_did = 'did:key:z6MkpEQY4FCCtJEVpZ6gGK541fYWynH2ya7D1RikTGfdydCF'
    subject_did = 'did:key:z6MkqcFHFXqzsYyDYrEUA2pVCfQGJz2rYoCZy5WWszzSW3o6'

    if key_type == 'Ed25519' and did_type == "issuer":
        response_data = {
            "did" : {
                "id": issuer_did
            },
            "keyType": key_type
        }
        response = Response(
            response=json.dumps(response_data),
            status=201,
            mimetype='application/json'
        )
    elif key_type == 'Ed25519' and did_type == "subject":
        response_data = {
            "did": {
                "id": subject_did
            },
            "keyType": key_type
        }
        response = Response(
            response=json.dumps(response_data),
            status=201,
            mimetype='application/json'
        )
    else:
        response_data = {
            "Error": "Make sure the Key Type is correct"
        }
        response = Response(
            response=json.dumps(response_data),
            status=400,
            mimetype='application/json'
        )

    return response


@app.route("/v1/schemas", methods=["PUT"])
def create_schema():
    data = request.get_json()
    issuer_did = data.get('author')
    print(f"Creating a schema for issuerDid: {issuer_did}")

    if issuer_did == 'did:key:z6MkpEQY4FCCtJEVpZ6gGK541fYWynH2ya7D1RikTGfdydCF':
        response_data = {
            "id": "b28feb61-e0b8-454a-86ed-d487a46e8584",
            "schema" : {
                "name": "Acme"
            }
        }
        response = Response(
            response=json.dumps(response_data),
            status=201,
            mimetype='application/json'
        )
    else:
        response_data = {
            "Error": "Make sure the DID is correct (use the Issuer's)"
        }
        response = Response(
            response=json.dumps(response_data),
            status=400,
            mimetype='application/json'
        )
    return response


@app.route("/v1/credentials", methods=["PUT"])
def validate_credentials():
    data = request.get_json()
    issuer_did = data.get('issuer')
    subject_did = data.get('subject')
    schema_id = data.get('schema')
    print(f"Validating a credential for issuer: {issuer_did}, subject: {subject_did}, schema: {schema_id}")

    if issuer_did == 'did:key:z6MkpEQY4FCCtJEVpZ6gGK541fYWynH2ya7D1RikTGfdydCF' and subject_did == 'did:key:z6MkqcFHFXqzsYyDYrEUA2pVCfQGJz2rYoCZy5WWszzSW3o6' and schema_id == 'b28feb61-e0b8-454a-86ed-d487a46e8584':
        response_data = {
            "credential": {
                "@context": ["https://www.w3.org/2018/credentials/v1"],
                "id": "2b5b0cfb-5023-4dc4-ae98-1cb94c65a22c",
                "type": ["VerifiableCredential"],
                "issuer": "did:key:z6MkpEQY4FCCtJEVpZ6gGK541fYWynH2ya7D1RikTGfdydCF",
                "issuanceDate": "2022-12-09T18:41:10Z",
                "expirationDate": "2051-10-05T14:48:00.000Z",
                "credentialSubject": {
                    "employedAt": "2022-08-20T13:20:10.000+0000",
                    "givenName": "Alice",
                    "id": "did:key:z6MkqcFHFXqzsYyDYrEUA2pVCfQGJz2rYoCZy5WWszzSW3o6"
                },
                "credentialSchema": {
                    "id": "b28feb61-e0b8-454a-86ed-d487a46e8584",
                    "type": "JsonSchemaValidator2018"
                }
            },
            "credentialJwt": "eyJhbGciOiJFZERTQSIsImtpZCI6ImRpZDprZXk6ejZNa3Y0MVQ5ZHMzWm5ncEpxcGpjYjVBOXpUeHFIN1FqOHA5bm81TVk2MzViZFRaIiwidHlwIjoiSldUIn0.eyJleHAiOjI1ODAxMzAwODAsImlzcyI6ImRpZDprZXk6ejZNa3Y0MVQ5ZHMzWm5ncEpxcGpjYjVBOXpUeHFIN1FqOHA5bm81TVk2MzViZFRaIiwianRpIjoiMmI1YjBjZmItNTAyMy00ZGM0LWFlOTgtMWNiOTRjNjVhMjJjIiwibmJmIjoxNjcwNjExMjcwLCJzdWIiOiJkaWQ6a2V5Ono2TWtxY0ZIRlhxenNZeURZckVVQTJwVkNmUUdKejJyWW9DWnk1V1dzenpTVzNvNiIsInZjIjp7IkBjb250ZXh0IjpbImh0dHBzOi8vd3d3LnczLm9yZy8yMDE4L2NyZWRlbnRpYWxzL3YxIl0sImlkIjoiMmI1YjBjZmItNTAyMy00ZGM0LWFlOTgtMWNiOTRjNjVhMjJjIiwidHlwZSI6WyJWZXJpZmlhYmxlQ3JlZGVudGlhbCJdLCJpc3N1ZXIiOiJkaWQ6a2V5Ono2TWt2NDFUOWRzM1puZ3BKcXBqY2I1QTl6VHhxSDdRajhwOW5vNU1ZNjM1YmRUWiIsImlzc3VhbmNlRGF0ZSI6IjIwMjItMTItMDlUMTg6NDE6MTBaIiwiZXhwaXJhdGlvbkRhdGUiOiIyMDUxLTEwLTA1VDE0OjQ4OjAwLjAwMFoiLCJjcmVkZW50aWFsU3ViamVjdCI6eyJlbXBsb3llZEF0IjoiMjAyMi0wOC0yMFQxMzoyMDoxMC4wMDArMDAwMCIsImdpdmVuTmFtZSI6IkFsaWNlIiwiaWQiOiJkaWQ6a2V5Ono2TWtxY0ZIRlhxenNZeURZckVVQTJwVkNmUUdKejJyWW9DWnk1V1dzenpTVzNvNiJ9LCJjcmVkZW50aWFsU2NoZW1hIjp7ImlkIjoiYjI4ZmViNjEtZTBiOC00NTRhLTg2ZWQtZDQ4N2E0NmU4NTg0IiwidHlwZSI6Ikpzb25TY2hlbWFWYWxpZGF0b3IyMDE4In19fQ.LxcBOYC9DzqUXcpNRnW29BSg2QrHWNb98tm4h8Agz-MuoCHaOfJ2_sVat9ChyU8d9XYtIf6A4elr8JVE6hERBw"
        }
        response = Response(
            response=json.dumps(response_data),
            status=201,
            mimetype='application/json'
        )
    else:
        response_data = {
            "Error": "Make sure to supply the correct values"
        }
        response = Response(
            response=json.dumps(response_data),
            status=400,
            mimetype='application/json'
        )
    return response


if __name__ == "__main__":
    app.run(host='localhost', port=8080)
