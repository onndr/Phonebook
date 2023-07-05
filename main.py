from fastapi import FastAPI, Depends, HTTPException
from classes import PhoneBook, PhoneBookRecord, NotExistingRecordError, DatabaseIntegrityError
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import ValidationError, PositiveInt

app = FastAPI()
security = HTTPBasic()
phone_book = PhoneBook()


def handle_request(callback):
    try:
        return callback()
    except NotExistingRecordError as e:
        raise HTTPException(status_code=404, detail=e.message)
    except DatabaseIntegrityError as e:
        raise HTTPException(status_code=400, detail=e.message)
    except ValidationError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=409, detail=str(e))


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    allowed_username = "admin"
    allowed_password = "password"

    if credentials.username != allowed_username or credentials.password != allowed_password:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    return credentials.username


@app.get("/phone-book-api/records/")
def read_records(username: str = Depends(get_current_username)):
    data = handle_request(lambda: phone_book.get_records())
    return {"body": {"records": data}}


@app.get("/phone-book-api/records/{id}")
def read_record(id: PositiveInt, username: str = Depends(get_current_username)):
    data = handle_request(lambda: phone_book.get_record_by_id(id))
    return {"body": {"record": data}}


@app.post("/phone-book-api/records/")
def create_record(new_record: PhoneBookRecord, username: str = Depends(get_current_username)):
    new_record_id = handle_request(lambda: phone_book.add_record(new_record))
    return {"message": f"Record was added with id={new_record_id}"}


@app.put("/phone-book-api/records/{id}")
def update_record(id: PositiveInt, updated_record: PhoneBookRecord, username: str = Depends(get_current_username)):
    handle_request(lambda: phone_book.update_record(id, updated_record))
    return {"message": f"Record with id={id} was updated"}


@app.delete("/phone-book-api/records/{id}")
def delete_record(id: PositiveInt, username: str = Depends(get_current_username)):
    handle_request(lambda: phone_book.delete_record(id))
    return {"message": f"Record with id={id} was deleted"}
