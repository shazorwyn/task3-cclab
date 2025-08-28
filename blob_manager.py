from azure.storage.blob import BlobServiceClient
from config import STORAGE_CONNECTION_STRING, CONTAINER_NAME
import os

blob_service_client = BlobServiceClient.from_connection_string(
    STORAGE_CONNECTION_STRING)


def upload_file(local_file, blob_name):
    blob_client = blob_service_client.get_blob_client(
        container=CONTAINER_NAME, blob=blob_name)
    with open(local_file, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)
    print(f"Uploaded {local_file} as {blob_name}")


def download_file(blob_name, local_file):
    blob_client = blob_service_client.get_blob_client(
        container=CONTAINER_NAME, blob=blob_name)
    with open(local_file, "wb") as file:
        file.write(blob_client.download_blob().readall())
    print(f"Downloaded {blob_name} as {local_file}")


def list_blobs():
    container_client = blob_service_client.get_container_client(CONTAINER_NAME)
    print(f"Blobs in container '{CONTAINER_NAME}':")
    for blob in container_client.list_blobs():
        print(f" - {blob.name}")


def list_versions(blob_name):
    container_client = blob_service_client.get_container_client(CONTAINER_NAME)
    print(f"Versions for blob '{blob_name}':")
    versions = container_client.list_blobs(
        name_starts_with=blob_name, include=["versions"])
    for v in versions:
        print(
            f" - Name: {v.name}, VersionId: {v.version_id}, IsCurrent: {v.is_current_version}")


def menu():
    while True:
        print("\n=== Azure Blob Manager ===")
        print("1. Upload File")
        print("2. Download File")
        print("3. List Blobs")
        print("4. List Blob Versions")
        print("5. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            local_file = input("Enter local file path to upload: ").strip()
            blob_name = input("Enter blob name (e.g., test.txt): ").strip()
            if os.path.exists(local_file):
                upload_file(local_file, blob_name)
            else:
                print("File does not exist.")

        elif choice == "2":
            blob_name = input("Enter blob name to download: ").strip()
            local_file = input("Enter local file name to save as: ").strip()
            download_file(blob_name, local_file)

        elif choice == "3":
            list_blobs()

        elif choice == "4":
            blob_name = input("Enter blob name to check versions: ").strip()
            list_versions(blob_name)

        elif choice == "5":
            print("exiting")
            break

        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    menu()
