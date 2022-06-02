from __future__ import annotations
from dataclasses import dataclass
from dataclass_wizard import JSONWizard


@dataclass
class ExtendApiSigninResult(JSONWizard):
    token: str
    refreshToken: str


@dataclass
class ExtendApiRefreshResult(JSONWizard):
    token: str


@dataclass
class ExtendApiCardResult(JSONWizard):
    virtualCards: list[ExtendApiVirtualCard]


@dataclass
class ExtendApiVirtualCard(JSONWizard):
    id: str
    displayName: str
    limitCents: int
    balanceCents: int
    last4: str
    status: str


@dataclass
class ExtendApiTransactionResult(JSONWizard):
    transactions: list[ExtendApiTransaction]


@dataclass
class ExtendApiTransaction:
    status: str
    authBillingAmountCents: int
    mccGroup: str
    merchantName: str
    virtualCardId: str
    nameOnCard: str
    vcnDisplayName: str
    vcnLast4: str
    authedAt: str
