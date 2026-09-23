from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    aadhar_number=db.Column(db.String(12),unique=True,nullable=False)
    Voter_id=db.Column(db.String(12),unique=True,nullable=False)
    contact = db.Column(db.String(20))
    role = db.Column(db.String(20), nullable=False)   # admin / voter / candidate
    is_approved = db.Column(db.Boolean, default=False)
    is_blacklisted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class VoterProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    full_name = db.Column(db.String(120))
    aadhar_number=db.Column(db.String(12),unique=True,nullable=False)
    Voter_id=db.Column(db.String(12),unique=True,nullable=False)
    date_of_birth = db.Column(db.String(20))
    address = db.Column(db.String(255))
    phone_number = db.Column(db.String(20))
    id_proof_number = db.Column(db.String(50))
    verification_status = db.Column(db.String(20), default='pending')   # pending / approved / rejected

    user = db.relationship('User', backref='voter_profile', uselist=False)


class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    full_name = db.Column(db.String(120))
    party_name = db.Column(db.String(120))
    bio = db.Column(db.Text)
    verification_status = db.Column(db.String(20), default='pending')   # pending / approved / rejected

    user = db.relationship('User', backref='candidate_profile', uselist=False)


class Election(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='upcoming')   # upcoming / active / completed

    contract_address = db.Column(db.String(120))


class ElectionCandidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    election_id = db.Column(db.Integer, db.ForeignKey('election.id'))
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'))


    contract_candidate_index = db.Column(db.Integer)

    election = db.relationship('Election', backref='election_candidates')
    candidate = db.relationship('Candidate', backref='election_candidates')


class VotingStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    election_id = db.Column(db.Integer, db.ForeignKey('election.id'))
    has_voted = db.Column(db.Boolean, default=False)
    voted_at = db.Column(db.DateTime)

    # blockchain transaction hash returned after the vote is recorded 
    tx_hash = db.Column(db.String(120))

    # stops the same voter getting two rows for the same election at the DB level
    __table_args__ = (
        db.UniqueConstraint('user_id', 'election_id', name='uq_voter_election'),
    )

    voter = db.relationship('User', backref='voting_statuses')
    election = db.relationship('Election', backref='voting_statuses')


class FaceAuthData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    face_encoding = db.Column(db.Text)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)
    #"handle failed authentication attempts"
    last_verified_at = db.Column(db.DateTime)
    failed_attempts = db.Column(db.Integer, default=0)

    user = db.relationship('User', backref='face_auth_data', uselist=False)













































































































































































































































































































































































































































from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    contact = db.Column(db.String(20))
    role = db.Column(db.String(20), nullable=False)   # admin / voter / candidate
    is_approved = db.Column(db.Boolean, default=False)
    is_blacklisted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class VoterProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    full_name = db.Column(db.String(120))
    date_of_birth = db.Column(db.String(20))
    address = db.Column(db.String(255))
    phone_number = db.Column(db.String(20))
    id_proof_number = db.Column(db.String(50))
    verification_status = db.Column(db.String(20), default='pending')

    user = db.relationship('User', backref='voter_profile', uselist=False)


class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    full_name = db.Column(db.String(120))
    party_name = db.Column(db.String(120))
    bio = db.Column(db.Text)
    verification_status = db.Column(db.String(20), default='pending')

    user = db.relationship('User', backref='candidate_profile', uselist=False)


class Election(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='upcoming')   # upcoming / active / completed


class ElectionCandidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    election_id = db.Column(db.Integer, db.ForeignKey('election.id'))
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'))

    election = db.relationship('Election', backref='election_candidates')
    candidate = db.relationship('Candidate', backref='election_candidates')


class VotingStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    election_id = db.Column(db.Integer, db.ForeignKey('election.id'))
    has_voted = db.Column(db.Boolean, default=False)
    voted_at = db.Column(db.DateTime)

    voter = db.relationship('User', backref='voting_statuses')
    election = db.relationship('Election', backref='voting_statuses')





























































































































































































class FaceAuthData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    face_encoding = db.Column(db.Text)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='face_auth_data', uselist=False)