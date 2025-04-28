from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

router = APIRouter()

@router.post("/tags/", response_model=Tag)
def create_tag(tag: Tag, session: Session = Depends(get_session)):
    session.add(tag)
    session.commit()
    session.refresh(tag)
    return tag


@router.get("/tags/", response_model=List[Tag])
def get_tags(session: Session = Depends(get_session)):
    tags = session.execute(select(Tag)).scalars().all()
    return tags


@router.post("/transactions/", response_model=Transaction)
def create_transaction(transaction: Transaction, session: Session = Depends(get_session)):
    session.add(transaction)
    session.commit()
    session.refresh(transaction)
    return transaction


@router.get("/transactions/", response_model=List[Transaction])
def get_transactions(session: Session = Depends(get_session)):
    transactions = session.execute(select(Transaction)).scalars().all()
    return transactions


@router.post("/transactions/{transaction_id}/tags/{tag_id}/", response_model=Transaction)
def add_tag_to_transaction(transaction_id: int, tag_id: int, session: Session = Depends(get_session)):
    transaction = session.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    tag = session.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    transaction.tags.append(tag)
    session.commit()
    session.refresh(transaction)
    return transaction


@router.get("/transactions/{transaction_id}/tags/", response_model=List[Tag])
def get_tags_for_transaction(transaction_id: int, session: Session = Depends(get_session)):
    transaction = session.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction.tags
