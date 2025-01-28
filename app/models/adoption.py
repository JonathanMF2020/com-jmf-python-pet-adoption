from sqlalchemy import Column, Integer, ForeignKey, Date, Float, Boolean, Text, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.sql import func

class Adoption(Base):
    __tablename__ = "adoptions"
    id = Column(Integer, primary_key=True, index=True)
    pet_id = Column(Integer, ForeignKey("pets.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    adopter_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    latitude = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    longitude = Column(Float, nullable=False)
    available = Column(Boolean, default=True)
    adoption_date = Column(Date, nullable=True)
    pet = relationship("Pet", back_populates="adoption")
    comments = relationship("AdoptionComment", back_populates="adoption")  # Cambiado 'adoptions' a 'adoption'

class AdoptionComment(Base):
    __tablename__ = "adoptions_comments"
    id = Column(Integer, primary_key=True, index=True)
    comment = Column(Text, nullable=False)
    adoption_id = Column(Integer, ForeignKey("adoptions.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    datetime = Column(DateTime, nullable=False, default=func.now())
    reactions = relationship("Reaction", secondary="adoptions_comments_reactions")
    adoption = relationship("Adoption", back_populates="comments")  # Cambiado 'adoptions' a 'comments'

class AdoptionCommentReaction(Base):
    __tablename__ = "adoptions_comments_reactions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    comment_id = Column(Integer, ForeignKey("adoptions_comments.id", ondelete="CASCADE"), nullable=False)
    reaction_id = Column(Integer, ForeignKey("reactions.id", ondelete="CASCADE"), nullable=False)

class Reaction(Base):
    __tablename__ = "reactions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
