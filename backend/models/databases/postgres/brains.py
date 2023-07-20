from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.databases.postgres.sqlalchemy_repository import (
    Brain,
    BrainUser,
    BrainVector,
)
from uuid import UUID
from models.databases.repository import Repository


class Brain(Repository):
    def __init__(self, database_url):
        self.engine = create_engine(database_url)
        self.Session = sessionmaker(bind=self.engine)

    def get_user_brains(self, user_id):
        session = self.Session()
        user_brains = (
            session.query(Brain)
            .join(BrainUser)
            .filter(BrainUser.user_id == user_id)
            .all()
        )
        session.close()
        return user_brains

    def get_brain_for_user(self, user_id, brain_id):
        session = self.Session()
        user_brain = (
            session.query(Brain)
            .join(BrainUser)
            .filter(BrainUser.user_id == user_id, BrainUser.brain_id == brain_id)
            .first()
        )
        session.close()
        return user_brain

    def get_brain_details(self, brain_id):
        session = self.Session()
        brain = session.query(Brain).filter(Brain.brain_id == brain_id).first()
        session.close()
        return brain

    def delete_brain_user_by_id(self, user_id, brain_id):
        session = self.Session()
        session.query(BrainUser).filter(
            BrainUser.user_id == user_id,
            BrainUser.brain_id == brain_id,
            BrainUser.rights == "Owner",
        ).delete()
        session.commit()
        session.close()

    def delete_brain_vector(self, brain_id):
        session = self.Session()
        session.query(BrainVector).filter(BrainVector.brain_id == brain_id).delete()
        session.commit()
        session.close()

    def delete_brain_user(self, brain_id):
        session = self.Session()
        session.query(BrainUser).filter(BrainUser.brain_id == brain_id).delete()
        session.commit()
        session.close()

    def delete_brain(self, brain_id):
        session = self.Session()
        session.query(Brain).filter(Brain.brain_id == brain_id).delete()
        session.commit()
        session.close()

    def create_brain(self, name):
        session = self.Session()
        new_brain = Brain(name=name)
        session.add(new_brain)
        session.commit()
        session.close()
        return new_brain

    def create_brain_user(self, user_id: UUID, brain_id, rights, default_brain):
        session = self.Session()
        new_brain_user = BrainUser(
            user_id=user_id,
            brain_id=brain_id,
            rights=rights,
            default_brain=default_brain,
        )
        session.add(new_brain_user)
        session.commit()
        session.close()
        return new_brain_user

    def create_brain_vector(self, brain_id, vector_id, file_sha1):
        session = self.Session()
        new_brain_vector = BrainVector(
            brain_id=brain_id, vector_id=vector_id, file_sha1=file_sha1
        )
        session.add(new_brain_vector)
        session.commit()
        session.close()
        return new_brain_vector

    def get_vector_ids_from_file_sha1(self, file_sha1: str):
        session = self.Session()
        vector_ids = (
            session.query(BrainVector.vector_id)
            .filter(BrainVector.file_sha1 == file_sha1)
            .all()
        )
        session.close()
        return [vector_id[0] for vector_id in vector_ids]

    def update_brain_fields(self, brain_id, brain_name):
        session = self.Session()
        session.query(Brain).filter(Brain.brain_id == brain_id).update(
            {Brain.name: brain_name}
        )
        session.commit()
        session.close()

    def get_brain_vector_ids(self, brain_id):
        session = self.Session()
        vector_ids = (
            session.query(BrainVector.vector_id)
            .filter(BrainVector.brain_id == brain_id)
            .all()
        )
        session.close()
        return [vector_id[0] for vector_id in vector_ids]

    def delete_file_from_brain(self, brain_id, file_name: str):
        # This method is a bit more complex and might need to be adjusted based on your specific requirements
        session = self.Session()
        vector_ids = (
            session.query(BrainVector.vector_id)
            .filter(BrainVector.file_sha1 == file_name)
            .all()
        )
        for vector_id in vector_ids:
            session.query(BrainVector).filter(
                and_(
                    BrainVector.vector_id == vector_id[0],
                    BrainVector.brain_id == brain_id,
                )
            ).delete()
            if (
                not session.query(BrainVector)
                .filter(BrainVector.vector_id == vector_id[0])
                .first()
            ):
                session.query(BrainVector).filter(
                    BrainVector.vector_id == vector_id[0]
                ).delete()
        session.commit()
        session.close()
        return {"message": f"File {file_name} in brain {brain_id} has been deleted."}

    def get_default_user_brain_id(self, user_id: UUID):
        session = self.Session()
        brain_id = (
            session.query(BrainUser.brain_id)
            .filter(and_(BrainUser.user_id == user_id, BrainUser.default_brain == True))
            .first()
        )
        session.close()
        return brain_id[0] if brain_id else None

    def get_brain_by_id(self, brain_id: UUID):
        session = self.Session()
        brain = session.query(Brain).filter(Brain.brain_id == brain_id).first()
        session.close()
        return brain
