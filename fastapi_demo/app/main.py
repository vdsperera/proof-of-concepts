"""_summary_
"""
from fastapi import FastAPI
from fastapi_demo.app.routers import item_router

app = FastAPI(
    title="FastAPI Demo",
    description="A demonstration of a FastAPI application with professional structure.",
    version="1.0.0",
)
app.include_router(router=item_router.router, tags=["Items"])
