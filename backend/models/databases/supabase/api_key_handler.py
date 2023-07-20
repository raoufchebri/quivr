from models.databases.repository import Repository
from datetime import datetime
from supabase.client import Client


class ApiKeyHandler(Repository):
    supabase_client: Client

    def __init__(self, supabase_client: Client):
        self.supabase_client = supabase_client

    def create_api_key(self, new_key_id, new_api_key, user_id):
        response = (
            self.supabase_client.table("api_keys")
            .insert(
                [
                    {
                        "key_id": str(new_key_id),
                        "user_id": str(user_id),
                        "api_key": str(new_api_key),
                        "creation_time": datetime.utcnow().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                        "is_active": True,
                    }
                ]
            )
            .execute()
        )
        return response

    def delete_api_key(self, key_id, user_id):
        return (
            self.supabase_client.table("api_keys")
            .update(
                {
                    "is_active": False,
                    "deleted_time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                }
            )
            .match({"key_id": key_id, "user_id": user_id})
            .execute()
        )

    def get_active_api_key(self, api_key):
        response = (
            self.supabase_client.table("api_keys")
            .select("api_key", "creation_time")
            .filter("api_key", "eq", str(api_key))
            .filter("is_active", "eq", "true")
            .execute()
        )
        return response

    def get_user_id_by_api_key(self, api_key):
        response = (
            self.supabase_client.table("api_keys")
            .select("user_id")
            .filter("api_key", "eq", str(api_key))
            .execute()
        )
        return response

    def get_user_api_keys(self, user_id):
        response = (
            self.supabase_client.table("api_keys")
            .select("key_id, creation_time")
            .filter("user_id", "eq", user_id)
            .filter("is_active", "eq", "true")
            .execute()
        )
        return response.data
