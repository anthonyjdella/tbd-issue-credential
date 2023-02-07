# Issue a Verifiable Credential

## Prompt:
> Implement a web page that contains a form field (for DID) and a button. Upon clicking the button, a credential should be issued to the DID subject

---

## How to use it?:
0. Start the SSI Service locally
    - `docker-compose up --build`
1. Run ngrok (wondering why? [see explaination details](#if-ssi-service-is-up))
    - `ngrok http --region=us --hostname=ngrok.anthonydellavecchia.com 8080`
    - Or your ngrok hostname, i.e. `ngrok http 8080`
2. Run a proxy (wondering why? [see explaination details](#if-ssi-service-is-up))
    - `lcp --proxyUrl https://ngrok.anthonydellavecchia.com`
    - Or `lcp --proxyUrl https://{YOUR-NGROK-URL}`
3. Go to [https://acme-frontend.vercel.app/](https://acme-frontend.vercel.app/)
4. Create Issuer DID
    - Enter the keytype: `Ed25519`
    - Copy the Issuer DID
5. Create Subject DID
    - Enter the keytype: `Ed25519`
6. Create Schema
    - Paste the Issuer DID created from Step 4 (Create Issuer DID)
    - For example, `did:key:z6MkpEQY4FCCtJEVpZ6gGK541fYWynH2ya7D1RikTGfdydCF`
7. Verify Credential
    - Paste the Issuer DID associated to the schema ID
    - For example, `did:key:z6MkpEQY4FCCtJEVpZ6gGK541fYWynH2ya7D1RikTGfdydCF`

---

## Screenshots:
Create Issuer DID
![Create Issuer DID Gif](/assets/create-issuer.gif)
Create Subject
![Create Subject DID Gif](/assets/create-subject.gif)
Create Schema
![Create Schema ID Gif](/assets/create-schema.gif)
Validate Credential
![Validate Credential Gif](/assets/validate-credential.gif)

---

## Technical Solution:

### How does it work?
- When you click on each button, an API call is made to the SSI Service.
    - To create Issuer DID, the arg is the keytype.
    - To create Subject DID, the arg is the keytype.
    - To create Schema, the arg is the Issuer DID.
    - To verify the credential, the args are the Issuer DID and Schema ID.

### Tech used:
1. Vercel and Next.js for the frontend (my first time using them)
    - Also includes Typescript
2. SSI Service in Golang for the backend
3. Python for the mock backend (wondering why? [see explaination details](#mock-backend))
    - Flask as the web server

### Challenges:
1. During initial development, the SSI Service was down, so I created my own mock service in Python `/mock-service-backend`
2. I am running 2 servers: the SSI Service, and my development server. They are both on `localhost`, but different ports (8080 and 3000). But the SSI Service throws a CORS error, because no 'Access-Control-Allow-Origin' header is present. In order to fix it, I had to run the SSI service through a proxy.

### Submodules:
This repo contains two submodules
1. The frontend in `/acme-frontend`
2. The backend service in `/ssi-service`

> Note: Because SSI Service was down, I created a mock backend in `/mock-service-backend`.

### Mock Backend:
`/mock-service-backend` is a Mocked Python backend with 3 endpoints:
1. `/v1/dids/key` to create a key - [Postman screenshot](/mock-service-backend/assets/create-key.png)
2. `/v1/schemas` to create a schema - [Postman screenshot](/mock-service-backend/assets/create-schema.png)
3. `/v1/credentials` to validate a credential - [Postman screenshot](/mock-service-backend/assets/validate-credentials.png)

> All 3 endpoints return a similar Response from their respective endpoint in the SSI service

---

## How to Run:

### Frontend:
- `cd` into `/acme-frontend`
- `yarn install`
- `yarn dev`

### Backend:

#### If SSI Service is Down:
- `cd` into `/mock-service-backend`
- Run `python3 app.py`

> Note: `/mock-service-backend` is running on localhost:8080, so it will only work if you run it locally.

#### If SSI Service is Up:
- `cd ssi-service/build`
- Run `docker-compose up`

#### Proxy and Ngrok:
There is a CORS issue, so this is how to fix it:

- Run `ngrok http --region=us --hostname=ngrok.anthonydellavecchia.com 8080`
    - This creates a tunnel and points `http://localhost:8080` to `https://ngrok.anthonydellavecchia.com`
- Run `lcp --proxyUrl https://ngrok.anthonydellavecchia.com`
    - This creates a proxy on `http://localhost:8010/proxy`
    - So, if you want to hit a SSI Service endpoint it might look like: `http://localhost:8010/proxy/v1/credentials`

---

## Reference:
- [Manually Issue a Verifiable Credential](https://developer.tbd.website/docs/tutorials/issue-verifiable-credential-manually/)
