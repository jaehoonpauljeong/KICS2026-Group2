from lxml import etree
import sys

def validate_xml_full_report(xml_path, xsd_path):
    report = 'XML Validation Report\n'
    try:
        # Parse XSD
        with open(xsd_path, 'rb') as f:
            schema_doc = etree.parse(f)
        schema = etree.XMLSchema(schema_doc)

        # Parse XML
        with open(xml_path, 'rb') as f:
            xml_doc = etree.parse(f)

        # Validate and capture ALL errors
        is_valid = schema.validate(xml_doc)

        if is_valid:
            # print("XML is VALID!")
            report += "  XML is VALID!\n"
            return report
        else:
            # print("XML is INVALID. All errors:")
            # schema.error_log contains ALL errors (not just first)
            for error in schema.error_log:
                # print(f"  [Line {error.line}] {error.message}")
                report += f"  [Line {error.line}] {error.message}\n"
            return report

    except IOError as e:
        print(f"File error: {e}")
        return report
    except etree.XMLSyntaxError as e:
        print(f"XML syntax error: {e}")
        return report
    except Exception as e:
        print(f"Unexpected error: {e}")
        return report

if __name__ == "__main__":
    xml_file = "generated_policy.xml"
    xsd_file = "i2nsf-cfi-policy.xsd"

    print(validate_xml_full_report(xml_file, xsd_file))