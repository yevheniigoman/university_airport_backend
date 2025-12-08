from dependencies import get_session
from models import Flight
from sqlalchemy import select, exc
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException


router = APIRouter()
