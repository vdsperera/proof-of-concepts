"""_summary_
"""
from fastapi import FastAPI
from fastapi_demo.app.routers import items

app = FastAPI(
    title="FastAPI Demo",
    description="A demonstration of a FastAPI application with professional structure.",
    version="1.0.0",
)
app.include_router(router=items.router, tags=["Items"])
