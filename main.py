from fastapi import FastAPI, Depends, HTTPException
from classes import PhoneBook, PhoneBookRecord, NotExistingRecordError, DatabaseIntegrityError
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import ValidationError, PositiveInt

app = FastAPI()
security = HTTPBasic()
phone_book = PhoneBook()


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    allowed_username = "admin"
    allowed_password = "password"

    if credentials.username != allowed_username or credentials.password != allowed_password:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    return credentials.username


@app.get("/phone-book-api/records/")
def read_records(username: str = Depends(get_current_username)):
    try:
        records = phone_book.get_records()
        response = {"status": 200, "body": {"records": records}}
    except Exception as e:
        response = {"status": 400, "message": str(e)}
    finally:
        return response


@app.get("/phone-book-api/records/{id}")
def read_record(id: PositiveInt, username: str = Depends(get_current_username)):
    try:
        record = phone_book.get_record_by_id(id)
        response = {"status": 200, "body": {"record": record}}
    except NotExistingRecordError as e:
        response = {"status": 404, "message": e.message}
    except DatabaseIntegrityError as e:
        response = {"status": 400, "message": e.message}
    except ValidationError as e:
        response = {"status": 409, "message": e.message}
    finally:
        return response


@app.post("/phone-book-api/records/")
def create_record(new_record: PhoneBookRecord, username: str = Depends(get_current_username)):
    try:
        new_record_id = phone_book.add_record(new_record)
        response = {"status": 200, "message": f"Record was added with id={new_record_id}"}
    except NotExistingRecordError as e:
        response = {"status": 404, "message": e.message}
    except DatabaseIntegrityError as e:
        response = {"status": 400, "message": e.message}
    except ValidationError as e:
        response = {"status": 409, "message": e.message}
    finally:
        return response


@app.put("/phone-book-api/records/{id}")
def update_record(id: PositiveInt, updated_record: PhoneBookRecord, username: str = Depends(get_current_username)):
    try:
        phone_book.update_record(id, updated_record)
        response = {"status": 200, "message": f"Record with id={id} was updated"}
    except NotExistingRecordError as e:
        response = {"status": 404, "message": e.message}
    except DatabaseIntegrityError as e:
        response = {"status": 400, "message": e.message}
    except ValidationError as e:
        response = {"status": 409, "message": e.message}
    finally:
        return response


@app.delete("/phone-book-api/records/{id}")
def delete_record(id: PositiveInt, username: str = Depends(get_current_username)):
    try:
        phone_book.delete_record(id)
        response = {"status": 200, "message": f"Record with id={PositiveInt} was deleted"}
    except NotExistingRecordError as e:
        response = {"status": 404, "message": e.message}
    except DatabaseIntegrityError as e:
        response = {"status": 400, "message": e.message}
    except ValidationError as e:
        response = {"status": 409, "message": e.message}
    finally:
        return response
