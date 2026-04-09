from pydantic import BaseModel, HttpUrl, ConfigDict

class URLCreate(BaseModel):
    full_url: HttpUrl

class URLInfo(BaseModel):
    short_id: str
    
    model_config = ConfigDict(from_attributes=True)

class URLStats(BaseModel):
    clicks: int
    
    model_config = ConfigDict(from_attributes=True)
