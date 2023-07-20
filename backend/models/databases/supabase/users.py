from models.databases.repository import Repository
from supabase.client import Client

from logger import get_logger

logger = get_logger(__name__)


class User(Repository):
    supabase_client: Client

    def __init__(self, supabase_client: Client):
        self.supabase_client = supabase_client
        
    def create_user(self, user_id, user_email, date):
        return (
            self.supabase_client.table("users")
            .insert(
                {
                    "user_id": user_id,
                    "email": user_email,
                    "date": date,
                    "requests_count": 1,
                }
            )
            .execute()
        )

    def get_user_request_stats(self, user_id):
        """
        Fetch the user request stats from the database
        """
        requests_stats = (
            self.supabase_client.from_("users")
            .select("*")
            .filter("user_id", "eq", user_id)
            .execute()
        )
        return requests_stats

    def fetch_user_requests_count(self, user_id, date):
        """
        Fetch the user request count from the database
        """
        response = (
            self.supabase_client.from_("users")
            .select("*")
            .filter("user_id", "eq", str(user_id))
            .filter("date", "eq", date)
            .execute()
        )

        return response

    def update_user_request_count(self, user_id, requests_count, date):
        response = (
            self.supabase_client.table("users")
            .update({"requests_count": requests_count})
            .match({"user_id": user_id, "date": date})
            .execute()
        )

        return response

    def get_user_email(self, user_id):
        """
        Fetch the user email from the database
        """
        response = (
            self.supabase_client.from_("users")
            .select("email")
            .filter("user_id", "eq", str(user_id))
            .execute()
        )

        return response

    def get_user_stats(self, user_email, date):
        response = (
            self.supabase_client.from_("users")
            .select("*")
            .filter("email", "eq", user_email)
            .filter("date", "eq", str(date))
            .execute()
        )

        return response