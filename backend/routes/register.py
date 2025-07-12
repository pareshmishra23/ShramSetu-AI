from fastapi import APIRouter, HTTPException, status
from typing import List
from models.laborer import Laborer, LaborerCreate, LaborerUpdate
from database import laborers_collection
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/register", response_model=Laborer, status_code=status.HTTP_201_CREATED)
async def register_laborer(laborer_data: LaborerCreate):
    """Register a new laborer"""
    try:
        # Check if laborer with same phone already exists
        existing_laborer = await laborers_collection.find_one({"phone": laborer_data.phone})
        if existing_laborer:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A laborer with this phone number already exists"
            )
        
        # Create new laborer
        laborer = Laborer(**laborer_data.dict())
        
        # Insert into database
        result = await laborers_collection.insert_one(laborer.dict())
        
        if result.inserted_id:
            logger.info(f"Laborer registered successfully: {laborer.name}")
            return laborer
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to register laborer"
            )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error registering laborer: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/", response_model=List[Laborer])
async def get_laborers():
    """Get all registered laborers"""
    try:
        laborers = await laborers_collection.find().to_list(1000)
        return [Laborer(**laborer) for laborer in laborers]
    except Exception as e:
        logger.error(f"Error fetching laborers: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch laborers"
        )

@router.get("/{laborer_id}", response_model=Laborer)
async def get_laborer(laborer_id: str):
    """Get a specific laborer by ID"""
    try:
        laborer = await laborers_collection.find_one({"id": laborer_id})
        if not laborer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Laborer not found"
            )
        return Laborer(**laborer)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching laborer: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.put("/{laborer_id}", response_model=Laborer)
async def update_laborer(laborer_id: str, laborer_update: LaborerUpdate):
    """Update a laborer's information"""
    try:
        # Check if laborer exists
        existing_laborer = await laborers_collection.find_one({"id": laborer_id})
        if not existing_laborer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Laborer not found"
            )
        
        # Update only provided fields
        update_data = {k: v for k, v in laborer_update.dict().items() if v is not None}
        
        if update_data:
            await laborers_collection.update_one(
                {"id": laborer_id},
                {"$set": update_data}
            )
        
        # Return updated laborer
        updated_laborer = await laborers_collection.find_one({"id": laborer_id})
        return Laborer(**updated_laborer)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating laborer: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.delete("/{laborer_id}")
async def delete_laborer(laborer_id: str):
    """Delete a laborer"""
    try:
        result = await laborers_collection.delete_one({"id": laborer_id})
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Laborer not found"
            )
        return {"message": "Laborer deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting laborer: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )