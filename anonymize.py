#!/usr/bin/env python
import argparse
import json
import os
import logging
import sys

from datapii.processor import PDFProcessor
from datapii.utils import load_config

# Configure root logger to output to console
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("anonymize")

def main():
    parser = argparse.ArgumentParser(
        description="Enterprise-grade PDF PII Anonymizer using Microsoft Presidio and PyMuPDF."
    )
    parser.add_argument("input_pdf", help="Path to the input PDF file to anonymize.")
    parser.add_argument("output_pdf", help="Path where the anonymized output PDF will be saved.")
    parser.add_argument(
        "--config", 
        default="config.json", 
        help="Path to the JSON configuration file (default: config.json)."
    )
    parser.add_argument(
        "--ocr", 
        action="store_true", 
        help="Force OCR processing on all pages of the document, bypassing auto-detection."
    )
    parser.add_argument(
        "--audit", 
        nargs="?", 
        const=True, 
        default=False, 
        help="Generate a JSON audit report of all redactions. Optional argument specifies custom file path."
    )
    parser.add_argument(
        "--verbose", 
        action="store_true", 
        help="Enable detailed debug-level logging."
    )

    args = parser.parse_args()

    # Enable verbose logging if requested
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)
        logger.debug("Verbose logging enabled.")

    logger.info("Initializing PDF Anonymizer application...")

    # Load configuration
    config = {}
    if os.path.exists(args.config):
        logger.info(f"Loading configuration from {args.config}")
        config = load_config(args.config)
    else:
        logger.warning(f"Configuration file {args.config} not found. Running with default configurations.")
        # If default config.json is next to the script, load it
        default_config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
        if os.path.exists(default_config_path):
            logger.info(f"Loading default configuration from {default_config_path}")
            config = load_config(default_config_path)

    # Initialize Processor
    try:
        processor = PDFProcessor(config)
    except Exception as e:
        logger.critical(f"Failed to initialize PDFProcessor: {e}", exc_info=True)
        sys.exit(1)

    # Process Document
    try:
        audit_report = processor.process_pdf(
            input_path=args.input_pdf,
            output_path=args.output_pdf,
            force_ocr=args.ocr,
            run_audit=bool(args.audit)
        )
    except Exception as e:
        logger.error(f"Error during PDF processing: {e}", exc_info=True)
        sys.exit(1)

    # Write Audit Report if requested
    if args.audit:
        # Determine path
        if isinstance(args.audit, str):
            audit_path = args.audit
        else:
            base, _ = os.path.splitext(args.output_pdf)
            audit_path = f"{base}_audit.json"
            
        logger.info(f"Writing audit report to {audit_path}...")
        try:
            processor.report_generator.write_report_to_file(args.input_pdf, audit_path)
            logger.info("Audit report written successfully.")
        except Exception as e:
            logger.error(f"Failed to write audit report to {audit_path}: {e}")

    logger.info(f"Successfully processed PDF. Anonymized file saved to: {args.output_pdf}")

if __name__ == "__main__":
    main()
