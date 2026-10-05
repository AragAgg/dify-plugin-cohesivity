# Privacy Policy

## Data Collection

This plugin connects to the Cohesivity API at `https://cohesivity.ai`. It sends requests to create and manage ephemeral backend tenants on your behalf.

## What Data Is Sent

- **Tenant creation**: No personal data is sent. A tenant ID and management key are returned.
- **Resource provisioning**: The tenant ID, management key, and requested resource name are sent to provision infrastructure.
- **Tenant status**: The tenant ID and management key are sent to retrieve tenant state.
- **Claim tenant**: The tenant ID and management key are sent to generate an approval URL.
- **Documentation**: No data is sent. Documentation is fetched read-only.

## What Data Is Stored

This plugin does not store any data locally. All state is held by the Cohesivity API. Ephemeral tenants expire after 72 hours unless claimed.

## Third-Party Services

All requests go to `https://cohesivity.ai`. No other third-party services are contacted. See [Cohesivity's privacy policy](https://cohesivity.ai/privacy?ref=gh-dify-plugins) for details on how Cohesivity handles data.

## Contact

For privacy questions, contact: arag@cohesivity.ai
