# Issue a Verifiable Credential

## Prompt:

> Implement a web page that contains a form field (for DID) and a button. Upon clicking the button, a credential should be issued to the DID subject

---

## How to use it?:

1. Go to [https://acme-frontend.vercel.app/](https://github.com/vercel/virtual-event-starter-kit)
2. Create Issuer DID
    - Enter the keytype: `Ed25519`
3. Create Subject DID
    - Enter the keytype: `Ed25519`
4. Create Schema
    - Enter the Issuer DID: `did:key:z6MkpEQY4FCCtJEVpZ6gGK541fYWynH2ya7D1RikTGfdydCF`
5. Verify Credential
    - Enter the Issuer DID: `did:key:z6MkpEQY4FCCtJEVpZ6gGK541fYWynH2ya7D1RikTGfdydCF`

---

## Screenshot:

![Web Page Screenshot](/assets/screenshot.png)

---

## Technical Solution:

### Tech used:
1. Vercel and Next.js for the frontend (my first time using them)
    - Also includes Typescript
2. Python for the backend
    - Flask as the web server

### Submodules:
This repo contains two submodules
1. The frontend in `/acme-frontend`
2. The backend service in `/ssi-service`

> Note: Because SSI Service was down, I created a test backend in `/service-backend`.

### Local Backend:
`/service-backend` is a Python backend with 3 endpoints:
1. `/v1/dids/key` to create a key - [Postman screenshot](/service-backend/assets/create-key.png)
2. `/v1/schemas` to create a schema - [Postman screenshot](/service-backend/assets/create-schema.png)
3. `/v1/credentials` to validate a credential - [Postman screenshot](/service-backend/assets/validate-credentials.png)

> All 3 endpoints return a similar Response from their respective endpoint in the SSI service

---

## Run:

### Frontend:

- `cd` into `/acme-frontend`
- `yarn install`
- `yarn dev`

### Backend:

#### If SSI Service is Down:

- `cd` into `/service-backend`
- Run `python3 app.py`

#### If SSI Service is Up:

- `cd ssi-service/build`
- Run `docker-compose up`

---

## Reference:

- [Manually Issue a Verifiable Credential](https://developer.tbd.website/docs/tutorials/issue-verifiable-credential-manually/)
