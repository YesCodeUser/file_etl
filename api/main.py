import tempfile
from fastapi import FastAPI, UploadFile, File, HTTPException

from core.application import Application
from config import REQUIREMENTS_HEADERS
from report.console_reporter_json import ConsoleReporterJSON

app = FastAPI(title='csv Validator Api')

@app.post('/validate')
async def validate_csv(file: UploadFile = File(...)):
    if not file.filename.endswith("csv"):
        raise HTTPException(status_code=400, detail='Only cvs files are allowed')

    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    application = Application(file_path=tmp_path, requirements_headers=REQUIREMENTS_HEADERS)

    class Args:
        no_db = True
        json = True
        file_path = tmp_path

    validation_result, exit_code, db_result = application.run(Args())

    reporter = ConsoleReporterJSON()
    reporter.print_report(validation_result, db_result)

    return {
        "exit_code": exit_code,
        "reporter": reporter.json_data
    }
