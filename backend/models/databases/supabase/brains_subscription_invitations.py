from models.databases.repository import Repository
from supabase.client import Client

from logger import get_logger

logger = get_logger(__name__)


class BrainSubscription(Repository):
    supabase_client: Client  # Add this line

    def __init__(self, supabase_client: Client):
        self.supabase_client = supabase_client

    def create_subscription_invitation(self, brain_id, user_email, rights):
        logger.info("Creating subscription invitation")
        response = (
            self.supabase_client.table("brain_subscription_invitations")
            .insert({"brain_id": str(brain_id), "email": user_email, "rights": rights})
            .execute()
        )
        return response.data

    def update_subscription_invitation(self, brain_id, user_email, rights):
        logger.info("Updating subscription invitation")
        response = (
            self.supabase_client.table("brain_subscription_invitations")
            .update({"rights": rights})
            .eq("brain_id", str(brain_id))
            .eq("email", user_email)
            .execute()
        )
        return response.data

    def get_subscription_invitations_by_brain_id_and_email(self, brain_id, user_email):
        response = (
            self.supabase_client.table("brain_subscription_invitations")
            .select("*")
            .eq("brain_id", str(brain_id))
            .eq("email", user_email)
            .execute()
        )

        return response
