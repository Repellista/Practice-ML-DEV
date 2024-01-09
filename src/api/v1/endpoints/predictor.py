from fastapi import APIRouter, Depends, HTTPException
from model.user import User
from schema.predictor_schema import ModelRequest, ChooseModelRequest, UploadDataRequest, PredictionResult
from services.billing_service import BillingService
from tasks import predict_task  # Import the Celery task
from core.dependencies import get_current_active_user 

router = APIRouter(prefix="/predictor", tags=["predictor"])

@router.post("/run_prediction")
async def run_model(
    model_request: ModelRequest,
    current_user: User = Depends(get_current_active_user),
):
    # Send prediction task to Celery worker
    task_result = predict_task.delay(model_request.dict(), current_user.dict())
    return {"task_id": str(task_result.id)}

@router.post("/choose_model")
async def choose_model(
    choose_model_request: ChooseModelRequest,
    current_user: User = Depends(get_current_active_user),
):
    # Implement the logic to choose the model in the billing service
    billing_service = BillingService(container.user_repository)
    billing_service.choose_model(current_user, choose_model_request.model_id)
    return {"message": "Model chosen successfully"}

@router.post("/upload-data")
async def upload_data(
    upload_data_request: UploadDataRequest,
    current_user: User = Depends(get_current_active_user),
):
    # Implement the logic to upload data in the billing service
    billing_service = BillingService(container.user_repository)
    billing_service.upload_data(current_user, upload_data_request.model_id, upload_data_request.data)
    return {"message": "Data uploaded successfully"}

@router.get("/get-prediction-result/{prediction_id}", response_model=PredictionResult)
async def get_prediction_result(prediction_id: str, current_user: User = Depends(get_current_active_user)):
    # Implement the logic to get the prediction result in the billing service
    billing_service = BillingService(container.user_repository)
    prediction_result = billing_service.get_prediction_result(current_user, prediction_id)
    
    if not prediction_result:
        raise HTTPException(status_code=404, detail="Prediction result not found")

    return prediction_result

