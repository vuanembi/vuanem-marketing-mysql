from google.cloud import secretmanager

client = secretmanager.SecretManagerServiceClient()


def get_secret(key: str) -> str:
    name = f"projects/voltaic-country-280607/secrets/{key}/versions/latest"

    response = client.access_secret_version(request={"name": name})

    return response.payload.data.decode("UTF-8")
