from fastapi import FastAPI, APIRouter, status, Request
from fastapi.responses import JSONResponse
import logging
from.schemes import PushRequest, SearchRequest
from models.ProjectModel import ProjectModel
from models.ChunkModel import ChunkModel
from controllers import NLPController
from models.enums.ResponseEnums import ResponseSignal
from stores.llm import DocumentTypeEnum


logger = logging.getLogger('uvicorn.error')
nlp_router = APIRouter(
    prefix = "/api/v1/nlp",
    tags = ["api_v1", "nlp"]
)


@nlp_router.post("/index/push/{project_id}")
async def index_project(request: Request, project_id: str, push_request: PushRequest):
    
    project_model = await ProjectModel.create_instance(
        db_client=request.app.db_client,
    )

    chunk_model = await ChunkModel.create_instance(
        db_client= request.app.db_client,
    )

    project = await project_model.get_project_or_create_one(
        project_id = project_id,
    )

    if not project:
        return JSONResponse(
            status_code = status.HTTP_404_NOT_FOUND,
            content = {
                "signal": ResponseSignal.PROJECT_NOT_FOUND_ERROR.value,
            }
        )
    


    nlp_controller = NLPController(
        vector_db_client = request.app.vector_db_client , 
        generation_client = request.app.generation_client , 
        embedding_client = request.app.embedding_client 
    )



    records = True
    page_no = 1 
    inserted_items_count = 0
    idx = 0

    while records:

        page_chunks = await chunk_model.get_project_chunks(
        project_id = project.id,
        page_no = page_no,
        )

        if page_chunks:
            page_no += 1 
            
        if not page_chunks or len(page_chunks) == 0:
            records = False
            break

        chunk_ids = [ c.id for c in page_chunks ]
        idx += len(page_chunks)

        inserted_items_count += len(page_chunks)

    
        is_inserted = nlp_controller.index_into_vector_db(
            project = project,
            chunks = page_chunks,
            do_reset = push_request.do_reset,
            chunk_ids = chunk_ids
        )

        if not is_inserted:
            return JSONResponse(
                status_code = status.HTTP_404_NOT_FOUND,
                content = {
                    "signal": ResponseSignal.INSERT_INTO_VECTOR_DB_ERROR.value,
                }
            )
    
    return JSONResponse(
            status_code = status.HTTP_200_OK,
            content = {
                "signal": ResponseSignal.INSERT_INTO_VECTOR_DB_SUCCESS.value,
                "inserted_items_count": inserted_items_count,
            }
        )



@nlp_router.get("/index/info/{project_id}")
async def get_project_index_info(request: Request, project_id: str):

    project_model = await ProjectModel.create_instance(
        db_client=request.app.db_client,
    )

    project = await project_model.get_project_or_create_one(
        project_id = project_id,
    )

    nlp_controller = NLPController(
        vector_db_client = request.app.vector_db_client , 
        generation_client = request.app.generation_client , 
        embedding_client = request.app.embedding_client 
    )

    collection_info = nlp_controller.get_vector_db_collection_info(project = project)

    return JSONResponse(
            status_code = status.HTTP_200_OK,
            content = {
                "signal":  ResponseSignal.VECTOR_DB_COLLECTION_RETRIVED.value,
                "collection_info" : collection_info,
            }
        )




@nlp_router.post("/index/search/{project_id}")
async def search_index(request: Request, project_id: str, search_request: SearchRequest):

    project_model = await ProjectModel.create_instance(
        db_client=request.app.db_client,
    )

    project = await project_model.get_project_or_create_one(
        project_id = project_id,
    )

    nlp_controller = NLPController(
        vector_db_client = request.app.vector_db_client , 
        generation_client = request.app.generation_client , 
        embedding_client = request.app.embedding_client 
    )

 

    results = nlp_controller.search_vector_db_collection(
        project = project,
        text = search_request.text,
        limit = search_request.limit
    )


    if not results:
        return JSONResponse(
            status_code = status.HTTP_404_NOT_FOUND,
            content = {
                "signal": ResponseSignal.VECTOR_DB_SEARCH_ERROR.value,
            }
        )
    

    
    return JSONResponse(
            status_code = status.HTTP_200_OK,
            content = {
                "signal":  ResponseSignal.VECTOR_DB_SEARCH_SUCCESS.value,
                "results" : [result.dict() for result in results]
            }
        )

