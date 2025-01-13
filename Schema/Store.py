from pydantic import BaseModel, Field
from typing import List, Optional, Union
from datetime import datetime

class PriceMarkupSchema(BaseModel):
    type: str = Field(..., description="Type of price markup, either 'percentage' or 'flat'")
    value: Union[float, int] = Field(..., description="Markup value")

class CategorySchema(BaseModel):
    paltform: str = Field(..., description="WooCommerce category ID")
    keywords: List[str] = Field(..., description="List of keywords associated with the category")

class WooCommerceConfigSchema(BaseModel):
    store_id: str = Field(..., description="Unique identifier for the WooCommerce store")
    store_name: str = Field(..., description="Friendly name for the WooCommerce store")
    domain: str = Field(..., description="Store domain (e.g., www.example.com)")
    api_key: str = Field(..., description="API key for the WooCommerce store")
    api_secret: str = Field(..., description="API secret for the WooCommerce store")
    price_markup: PriceMarkupSchema = Field(..., description="Customizable price markup configuration")
    categories: List[CategorySchema] = Field(..., description="List of categories and associated keywords")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Timestamp when the configuration was created")
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Timestamp of the last update")
