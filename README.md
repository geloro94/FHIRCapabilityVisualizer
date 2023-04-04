# FHIR Capability Visualizer

This Python script checks the support for specific FHIR endpoints by querying the capability statement of FHIR servers. It then outputs the results in an Excel file, with each cell indicating if the corresponding operation is supported by the server. The supported endpoints are color-coded for easy visualization (green for "Yes" and red for "No").

## Prerequisites

- Python 3.6 or newer
- `requests` library
- `openpyxl` library

You can install the required libraries using the following command:

```bash
pip install requests openpyxl
```

## Usage

1. Clone the repository:

```bash
git clone https://github.com/geloro94/FHIRCapabilityVisualizer.git
```

2. Navigate to the cloned repository:

```bash
cd fhir-endpoint-support-checker
```

3. Edit the `script.py` file to customize the `SERVER_URLS` and `PATHS_TO_CHECK` variables with the FHIR server URLs and the endpoint paths you want to check, respectively.

For example:

```python
SERVER_URLS = ["https://hapi.fhir.org/baseR4"]
PATHS_TO_CHECK = ["/ConceptMap/$translate", "/ValueSet/$validate", "/ValueSet/$expand", "/ConceptMap/$closure", "/CodeSystem/$validate-code", "/CodeSystem/$lookup"]
```

4. Run the script:

```bash
python main.py
```

The script will generate an Excel file named `endpoint_support.xlsx` in the same directory, containing the results of the supported endpoints for each specified FHIR server.

## Contributing

Feel free to fork the repository and submit pull requests with any improvements or bug fixes. If you find any issues or have suggestions, please submit them through the GitHub issue tracker.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
