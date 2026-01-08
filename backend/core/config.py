"""
EVIDENT Configuration Management

This module handles all application configuration using environment variables
and pydantic-settings for validation.
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional, List
import os
from pathlib import Path


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    app_name: str = "EVIDENT"
    app_version: str = "1.0.0"
    debug: bool = Field(default=False, description="Debug mode")
    
    # Database
    database_url: str = Field(
        ...,
        description="PostgreSQL database connection URL"
    )
    
    # JWT Authentication
    jwt_secret_key: str = Field(
        ...,
        description="Secret key for JWT token signing"
    )
    jwt_algorithm: str = Field(
        default="HS256",
        description="JWT algorithm"
    )
    jwt_access_token_expire_minutes: int = Field(
        default=30,
        description="Access token expiration time in minutes"
    )
    jwt_refresh_token_expire_days: int = Field(
        default=7,
        description="Refresh token expiration time in days"
    )
    
    # Paths
    base_dir: Path = Path(__file__).parent.parent.parent
    raw_docs_path: Path = Field(
        default_factory=lambda: Path(__file__).parent.parent.parent / "data" / "raw_docs",
        description="Path to store raw documents"
    )
    vector_store_path: Path = Field(
        default_factory=lambda: Path(__file__).parent.parent.parent / "data" / "vector_store",
        description="Path to store FAISS vector store"
    )
    llm_model_path: Path = Field(
        ...,
        description="Path to llama.cpp model file"
    )
    
    # Vector Store Settings
    embedding_model_name: str = Field(
        default="intfloat/e5-base",
        description="Sentence transformer model for embeddings"
    )
    embedding_dimension: int = Field(
        default=768,
        description="Dimension of embedding vectors"
    )
    
    # LLM Settings
    llm_n_ctx: int = Field(
        default=4096,
        description="LLM context window size"
    )
    llm_n_threads: int = Field(
        default=4,
        description="Number of threads for LLM inference"
    )
    llm_temperature: float = Field(
        default=0.1,
        description="LLM temperature (lower = more deterministic)"
    )
    llm_max_tokens: int = Field(
        default=500,
        description="Maximum tokens in LLM response"
    )
    
    # RAG Settings
    rag_top_k: int = Field(
        default=5,
        description="Number of chunks to retrieve"
    )
    rag_similarity_threshold: float = Field(
        default=0.7,
        description="Minimum similarity score for retrieval"
    )
    rag_confidence_threshold: float = Field(
        default=0.7,
        description="Minimum confidence score to accept answer"
    )
    
    # Chunking Settings
    chunk_size: int = Field(
        default=500,
        description="Default chunk size in tokens"
    )
    chunk_overlap: int = Field(
        default=50,
        description="Overlap between chunks in tokens"
    )
    
    # Server Settings
    host: str = Field(
        default="0.0.0.0",
        description="Server host"
    )
    port: int = Field(
        default=8000,
        description="Server port"
    )
    
    # CORS Settings
    cors_origins: List[str] = Field(
        default=["http://localhost:3000"],
        description="Allowed CORS origins"
    )
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Create settings instance
settings = Settings()

# Ensure directories exist
settings.raw_docs_path.mkdir(parents=True, exist_ok=True)
settings.vector_store_path.mkdir(parents=True, exist_ok=True)
