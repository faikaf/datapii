Build a production-ready Python application that anonymizes PII from PDF files using Microsoft Presidio.

Requirements:

1. Input

   * Accept a PDF file as input.
   * Support both text-based PDFs and scanned/image-based PDFs.
   * Automatically detect whether OCR is required.

2. OCR Processing

   * For scanned PDFs, use OCR (Tesseract or EasyOCR).
   * Extract text and preserve page coordinates.
   * Maintain page layout as accurately as possible.

3. PII Detection

   * Use Microsoft Presidio Analyzer for entity detection.
   * Detect:

     * PERSON
     * EMAIL_ADDRESS
     * PHONE_NUMBER
     * CREDIT_CARD
     * IBAN_CODE
     * US_SSN
     * DATE_TIME
     * LOCATION
     * URL
     * ORGANIZATION
     * MEDICAL_LICENSE
     * Any additional supported Presidio entities
   * Allow custom recognizers and regex patterns.

4. Name Replacement Logic

   * Replace names with deterministic pseudonyms.
   * Example:

     * "faikaf" → "fabcdf"
     * "John Smith" → "Person_001"
     * "Jane Doe" → "Person_002"
   * The same name must always map to the same replacement throughout the entire document.
   * Store mappings in a dictionary.
   * Support loading mappings from a JSON configuration file.

5. Anonymization Strategy

   * Replace detected values instead of simply redacting.
   * Examples:

     * Email → [email_redacted@example.com](mailto:email_redacted@example.com)
     * Phone → XXX-XXX-XXXX
     * Credit Card → XXXX-XXXX-XXXX-1234
     * SSN → XXX-XX-XXXX
     * Address → ADDRESS_REDACTED
     * Organization → ORG_001
   * Make replacement strategies configurable.

6. PDF Reconstruction

   * Preserve:

     * Page count
     * Formatting
     * Fonts (where possible)
     * Images
     * Tables
     * Layout
   * Generate a new anonymized PDF.

7. Coordinate-Based Redaction

   * For scanned PDFs:

     * Use OCR bounding boxes.
     * Locate PII coordinates.
     * Replace or redact directly on the page.
   * Ensure original PII cannot be recovered.

8. Configuration
   Create a config.json file containing:

   * Input folder
   * Output folder
   * OCR engine
   * Entity types
   * Replacement mappings
   * Custom regex patterns
   * Logging level

9. Performance

   * Process PDFs with 1000+ pages.
   * Use multiprocessing where appropriate.
   * Stream pages instead of loading entire PDFs into memory.

10. Logging
    Generate:

* Processing logs
* Error logs
* Detection logs
* Audit report

11. Audit Report
    Produce a JSON report containing:
    {
    "file_name": "",
    "pages_processed": 0,
    "entities_found": {
    "PERSON": 0,
    "EMAIL_ADDRESS": 0,
    "PHONE_NUMBER": 0
    },
    "replacements": [
    {
    "original": "faikaf",
    "replacement": "fabcdf",
    "page": 1
    }
    ]
    }

12. Security

* Ensure original PII is permanently removed from output.
* Do not store extracted PII in logs.
* Sanitize temporary files after processing.

13. CLI
    Support:
    python anonymize.py input.pdf output.pdf

Optional flags:
--audit
--ocr
--config config.json
--verbose

14. Testing
    Create:

* Unit tests
* Integration tests
* Sample PDFs
* Validation tests for replacement consistency

15. Deliverables

* Complete Python source code
* requirements.txt
* README.md
* Example config.json
* Test suite
* Modular architecture with classes:

  * PDFProcessor
  * OCRProcessor
  * PresidioDetector
  * PIIReplacer
  * ReportGenerator

The final solution should be enterprise-grade, modular, maintainable, and suitable for processing sensitive healthcare, education, legal, and financial PDFs while preserving document usability.
