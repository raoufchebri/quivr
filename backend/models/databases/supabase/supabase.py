from models.databases.supabase import (
    Brain,
    User,
    File,
    BrainSubscription,
    ApiKeyHandler,
    Chats,
    Vector,
)
from supabase.client import Client


class SupabaseDB(Brain, User, File, BrainSubscription, ApiKeyHandler, Chats, Vector):
    def __init__(self, supabase_client: Client):
        super().__init__(supabase_client=supabase_client)
        # Brain.__init__(self, supabase_client=supabase_client)
        # User.__init__(self, supabase_client=supabase_client)
        # File.__init__(self, supabase_client=supabase_client)
        # BrainSubscription.__init__(self, supabase_client=supabase_client)
        # ApiKeyHandler.__init__(self, supabase_client=supabase_client)
        # Chats.__init__(self, supabase_client=supabase_client)
        # Vector.__init__(self, supabase_client=supabase_client)
