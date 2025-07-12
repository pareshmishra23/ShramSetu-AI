from fastapi import APIRouter, HTTPException, status
from typing import List
from models.job import Job, JobCreate, JobUpdate, LaborerAssignment
from database import laborers_collection
import logging

# We need to add jobs collection to database.py or import it here
from database import db

router = APIRouter()
logger = logging.getLogger(__name__)

# Jobs collection
jobs_collection = db.jobs

@router.post("/create", response_model=Job, status_code=status.HTTP_201_CREATED)
async def create_job(job_data: JobCreate):
    """Create a new job posting"""
    try:
        # Create new job
        job = Job(**job_data.dict())
        
        # Insert into database
        result = await jobs_collection.insert_one(job.dict())
        
        if result.inserted_id:
            logger.info(f"Job created successfully: {job.title}")
            return job
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create job"
            )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating job: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/", response_model=List[Job])
async def get_all_jobs():
    """Get all job postings"""
    try:
        jobs = await jobs_collection.find().to_list(1000)
        return [Job(**job) for job in jobs]
    except Exception as e:
        logger.error(f"Error fetching jobs: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch jobs"
        )

@router.get("/{job_id}", response_model=Job)
async def get_job(job_id: str):
    """Get a specific job by ID"""
    try:
        job = await jobs_collection.find_one({"job_id": job_id})
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found"
            )
        return Job(**job)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching job: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.patch("/{job_id}/assign")
async def assign_laborers_to_job(job_id: str, assignment: LaborerAssignment):
    """Assign laborers to a job by their phone numbers"""
    try:
        # Check if job exists
        existing_job = await jobs_collection.find_one({"job_id": job_id})
        if not existing_job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found"
            )
        
        # Validate that all phone numbers correspond to existing laborers
        valid_phone_numbers = []
        invalid_phone_numbers = []
        
        for phone_number in assignment.phone_numbers:
            laborer = await laborers_collection.find_one({"phone": phone_number})
            if laborer:
                valid_phone_numbers.append(phone_number)
            else:
                invalid_phone_numbers.append(phone_number)
        
        if invalid_phone_numbers:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Laborers not found for phone numbers: {invalid_phone_numbers}"
            )
        
        # Check if laborers are available
        unavailable_laborers = []
        for phone_number in valid_phone_numbers:
            laborer = await laborers_collection.find_one({"phone": phone_number})
            if not laborer.get("available", True):
                unavailable_laborers.append(phone_number)
        
        if unavailable_laborers:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Laborers are not available: {unavailable_laborers}"
            )
        
        # Get current assigned laborers and merge with new ones (avoid duplicates)
        current_assigned = existing_job.get("assigned_laborers", [])
        updated_assigned = list(set(current_assigned + valid_phone_numbers))
        
        # Update job with assigned laborers and change status to 'assigned'
        update_data = {
            "assigned_laborers": updated_assigned,
            "status": "assigned"
        }
        
        await jobs_collection.update_one(
            {"job_id": job_id},
            {"$set": update_data}
        )
        
        # Mark assigned laborers as unavailable
        for phone_number in valid_phone_numbers:
            await laborers_collection.update_one(
                {"phone": phone_number},
                {"$set": {"available": False}}
            )
        
        # Return updated job
        updated_job = await jobs_collection.find_one({"job_id": job_id})
        logger.info(f"Assigned {len(valid_phone_numbers)} laborers to job {job_id}")
        
        return {
            "message": f"Successfully assigned {len(valid_phone_numbers)} laborers to job",
            "job": Job(**updated_job),
            "assigned_laborers": valid_phone_numbers
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error assigning laborers to job: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.put("/{job_id}", response_model=Job)
async def update_job(job_id: str, job_update: JobUpdate):
    """Update a job's information"""
    try:
        # Check if job exists
        existing_job = await jobs_collection.find_one({"job_id": job_id})
        if not existing_job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found"
            )
        
        # Update only provided fields
        update_data = {k: v for k, v in job_update.dict().items() if v is not None}
        
        if update_data:
            await jobs_collection.update_one(
                {"job_id": job_id},
                {"$set": update_data}
            )
        
        # Return updated job
        updated_job = await jobs_collection.find_one({"job_id": job_id})
        return Job(**updated_job)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating job: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.delete("/{job_id}")
async def delete_job(job_id: str):
    """Delete a job"""
    try:
        # Get job details before deleting to free up assigned laborers
        job = await jobs_collection.find_one({"job_id": job_id})
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found"
            )
        
        # Free up assigned laborers (make them available again)
        assigned_laborers = job.get("assigned_laborers", [])
        for phone_number in assigned_laborers:
            await laborers_collection.update_one(
                {"phone": phone_number},
                {"$set": {"available": True}}
            )
        
        # Delete the job
        result = await jobs_collection.delete_one({"job_id": job_id})
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found"
            )
        
        logger.info(f"Job deleted and {len(assigned_laborers)} laborers freed up")
        return {"message": "Job deleted successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting job: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/skill/{skill_name}", response_model=List[Job])
async def get_jobs_by_skill(skill_name: str):
    """Get all jobs requiring a specific skill"""
    try:
        jobs = await jobs_collection.find({"skill_required": skill_name}).to_list(1000)
        return [Job(**job) for job in jobs]
    except Exception as e:
        logger.error(f"Error fetching jobs by skill: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch jobs by skill"
        )