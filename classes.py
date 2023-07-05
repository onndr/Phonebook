from pydantic import BaseModel, PositiveInt, EmailStr, validator, Field
from re import search, I
from typing import Optional


class NotExistingRecordError(Exception):
    def __init__(self, id, message="Record with given id doesn't exist"):
        self.id = id
        self.message = message
        super().__init__(self.message)


class DatabaseIntegrityError(Exception):
    def __init__(self, message="Internal database integrity error"):
        self.message = message
        super().__init__(self.message)


class PhoneBookRecord(BaseModel):
    id: Optional[PositiveInt]
    name: str = Field(min_length=1, max_length=30)
    surname: str = Field(min_length=1, max_length=30)
    email: EmailStr
    phone_number: str

    @validator("phone_number")
    def phone_validation(cls, v):
        regex = r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$"
        if v and not search(regex, v, I):
            raise ValueError("invalid phone number")
        return v


class PhoneBook:
    def __init__(self):
        self._records = []
        self._next_id = 1

    def add_record(self, record: PhoneBookRecord) -> PositiveInt:
        record.id = self._next_id
        self._records.append(record)
        self._next_id += 1
        return record.id

    def update_record(self, id, record: PhoneBookRecord):
        record_to_be_updated = self.get_record_by_id(id)
        record_to_be_updated.name = record.name
        record_to_be_updated.surname = record.surname
        record_to_be_updated.email = record.email
        record_to_be_updated.phone_number = record.phone_number

    def delete_record(self, record_id: int):
        record_to_be_deleted = self.get_record_by_id(record_id)
        self._records.remove(record_to_be_deleted[0])

    def get_records(self) -> list[PhoneBookRecord]:
        return self._records

    def get_record_by_id(self, id: int) -> PhoneBookRecord:
        matching_records = list(filter(lambda r: r.id == id, self._records))
        records_found_count = len(matching_records)
        if records_found_count == 0:
            raise NotExistingRecordError(id)
        elif records_found_count == 1:
            return matching_records[0]
        else:
            raise DatabaseIntegrityError()
