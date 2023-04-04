import re
import openpyxl
import requests
from openpyxl.styles import PatternFill
from openpyxl.utils import get_column_letter

SERVER_URLS = [
    "https://hapi.fhir.org/baseR4",
    "https://blaze.imi.uni-luebeck.de/fhir",
    "https://r4.ontoserver.csiro.au/fhir",
    "http://tx.fhir.org/r4",
    "https://tergi.elga.gv.at/fhir-server/api/v4"
]
PATHS_TO_CHECK = [
    # CodeSystem
    "/CodeSystem/$validate-code",
    "/CodeSystem/$lookup",
    "/CodeSystem/$subsumes",
    "/CodeSystem/$find-matches",

    # ConceptMap
    "/ConceptMap/$translate",
    "/ConceptMap/$closure",

    # ValueSet
    "/ValueSet/$expand",
    "/ValueSet/$validate-code",

    # Closure
    "/$closure"
]


def get_capability_statement(fhir_base_url):
    url = f"{fhir_base_url}/metadata"
    headers = {"Accept": "application/fhir+json"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Error getting capability statement: {response.status_code}")

    return response.json()


def check_endpoint_support(capability_statement, endpoint_paths):
    rest_resources = capability_statement.get("rest", [])
    supported_endpoints = []

    for endpoint_path in endpoint_paths:
        match = re.match(r"/([^/]+)/\$(.+)", endpoint_path)
        if match:
            resource_type, operation_of_interest = match.groups()
        else:
            resource_type = None
            operation_of_interest = endpoint_path[2:]

        supported = False
        for rest_resource in rest_resources:
            if resource_type is None:
                operation_list = rest_resource.get("operation", [])
            else:
                resource_list = rest_resource.get("resource", [])
                operation_list = [
                    operation
                    for resource in resource_list
                    if resource.get("type") == resource_type
                    for operation in resource.get("operation", [])
                ]

            for operation in operation_list:
                if operation.get("name") == operation_of_interest:
                    print(operation)
                    supported = True
                    break

            if supported:
                break

        supported_endpoints.append(supported)

    return supported_endpoints


def auto_size_columns(ws):
    for column_cells in ws.columns:
        length = max(len(str(cell.value)) for cell in column_cells)
        ws.column_dimensions[get_column_letter(column_cells[0].column)].width = length


def auto_size_rows(ws):
    for row_cells in ws.iter_rows():
        height = max(cell.value.count("\n") for cell in row_cells if cell.value) + 1
        ws.row_dimensions[row_cells[0].row].height = 15 * height


def main():
    results = [["Endpoint"] + SERVER_URLS]

    wb = openpyxl.Workbook()
    ws = wb.active

    for server_index, server_url in enumerate(SERVER_URLS, start=1):
        for index, endpoint_path in enumerate(PATHS_TO_CHECK, start=1):
            row = [endpoint_path]
            ws.cell(row=index + 1, column=1, value=endpoint_path)

            try:
                capability_statement = get_capability_statement(server_url)
                supported = check_endpoint_support(
                    capability_statement, [endpoint_path]
                )[0]
                row.append("Yes" if supported else "No")

                cell = ws.cell(row=index + 1, column=server_index + 1)
                cell.value = "Yes" if supported else "No"

                if supported:
                    cell.fill = PatternFill(
                        start_color="22bb45", end_color="22bb45", fill_type="solid"
                    )
                else:
                    cell.fill = PatternFill(
                        start_color="D22B2B", end_color="D22B2B", fill_type="solid"
                    )

            except Exception as e:
                print(f"Error checking {server_url}: {e}")
                row.append("Error")

        results.append(row)

    for index, server_url in enumerate(SERVER_URLS, start=1):
        ws.cell(row=1, column=index + 1, value=server_url)

    auto_size_columns(ws)
    auto_size_rows(ws)

    wb.save("endpoint_support.xlsx")

    print("Results saved to endpoint_support.xlsx")


if __name__ == "__main__":
    main()
