from core.schemas.camel import CamelModel


class FileBaseSchema(CamelModel):
    file_id: int | None
    source_file_name: str
    cdn_file_name: str
    mime_type: str
    file_size: int
    url: str

    class Config:
        from_attributes = True


class FileResponseDTO(FileBaseSchema):
    pass


class FileDTO(FileBaseSchema):
    file_id: int | None = None
