"""
Cost Calculator API - Azure Function (HTTP Trigger)
Project 4: The Serverless Logic
DecodeLabs Cloud Computing Internship (Azure Track)

Receives two numbers (num1, num2) via the HTTP request body (JSON),
adds them, and returns the result as JSON - {"Sum": total}.
No infrastructure to manage, and it costs nothing when idle.
"""

import json
import logging
import azure.functions as func

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.route(route="costcalculator", methods=["POST", "GET"])
def costcalculator(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Cost Calculator function triggered.")

    # Try to read JSON body first (POST), fall back to query params (GET)
    try:
        body = req.get_json()
    except ValueError:
        body = {}

    num1 = body.get("num1") if body else req.params.get("num1")
    num2 = body.get("num2") if body else req.params.get("num2")

    if num1 is None or num2 is None:
        return func.HttpResponse(
            json.dumps({"error": "Both 'num1' and 'num2' are required."}),
            status_code=400,
            mimetype="application/json"
        )

    try:
        num1 = float(num1)
        num2 = float(num2)
    except (TypeError, ValueError):
        return func.HttpResponse(
            json.dumps({"error": "'num1' and 'num2' must be numeric values."}),
            status_code=400,
            mimetype="application/json"
        )

    total = num1 + num2
    if total.is_integer():
        total = int(total)

    return func.HttpResponse(
        json.dumps({"Sum": total}),
        status_code=200,
        mimetype="application/json"
    )
