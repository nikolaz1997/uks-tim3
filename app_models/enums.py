from enumfields import Enum


class PullRequestStatus(Enum):
    OPENED = 'OPENED'
    CLOSED = 'CLOSED'
    DRAFT = 'DRAFT'
    MERGED = 'MERGED'


class IssueStatus(Enum):
    OPENED = 'OPENED'
    CLOSED = 'CLOSED'


class ReactionType(Enum):
    LIKE = 1
    DISLIKE = 2

class MilestoneState(Enum):
    OPEN = 1
    CLOSED = 2
    ALL = 3


class PullRequestActions(Enum):
    OPENED = 'OPENED',
    CLOSED = 'CLOSED',
    APPROVED = 'APPROVED',
