from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.customer import CustomerCreate, CustomerResponse
from app.crud.customer import customer_crud

router = APIRouter()


@router.get("/", response_model=list[CustomerResponse])
def get_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return customer_crud.get_multi(db, skip=skip, limit=limit)


@router.post("/", response_model=CustomerResponse)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    return customer_crud.create(db, customer.model_dump())


@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    return customer_crud.get_or_404(db, customer_id, "客户未找到")
