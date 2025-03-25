import re
import json
import os

 

class Document:

    def __init__(self, content, metadata):

        self.content = content

        self.metadata = metadata

 

    def __repr__(self):

        return f"Document(content={self.content[:100]}, metadata={self.metadata})"

 

 

def extract_text_from_txt(txt_path):

    try:

        with open(txt_path, 'r', encoding='utf-8') as file:

            text = file.read()

        return text

    except Exception as e:

        print(f"Error reading {txt_path}: {e}")

        return ""

 

 

def split_into_sections(text, headings):

    sections = {}

    current_section = None

    current_content = []

 

    # Split text into lines

    lines = text.split("\n")

 

    # Define a regex pattern to match the headings

    heading_pattern = re.compile(r"^\d+[\.\s]+([A-Za-z0-9\s\-]+)$")

 

    for line in lines:

        # Check if the line is a heading

        match = heading_pattern.match(line.strip())

        if match:

            heading = match.group(1).strip()

            if heading in headings:

                # If we have accumulated content, store it

                if current_section:

                    sections[current_section] = "\n".join(current_content)

                

                # Start a new section

                current_section = heading

                current_content = []

        elif current_section:

            # Accumulate content under the current section

            current_content.append(line.strip())

 

    # Add the last section

    if current_section:

        sections[current_section] = "\n".join(current_content)

 

    return sections

 

 

def create_metadata(file_name, section=None, topic=None, doc_type="text"):

    import datetime

    metadata = {

        "file_name": file_name,

        "section": section,

        "topic": topic,

        "doc_type": doc_type,

        "creation_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

    }

    return metadata

 

 

def process_txt_files_in_directory(directory, headings):

    txt_files = [f for f in os.listdir(directory) if f.endswith(".txt")]

    documents = []

 

    for txt_file in txt_files:

        txt_path = os.path.join(directory, txt_file)

        print(f"Processing file: {txt_file}")

 

        # Extract text from the .txt file

        file_text = extract_text_from_txt(txt_path)

 

        # Split the document into sections based on the provided headings

        sections = split_into_sections(file_text, headings)

 

        # Create metadata (you can add more logic for section-specific metadata)

        for section, content in sections.items():

            metadata = create_metadata(file_name=txt_file, section=section, topic="Metadata Handling")

            doc = Document(content=content, metadata=metadata)

            documents.append(doc)

 

    return documents

 
def save_documents_to_json(documents, output_file="output.json"):
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump([{"content": doc.content, "metadata": doc.metadata} for doc in documents], f, indent=4)
 

if __name__ == "__main__":

    # List of headings you provided

    headings = [

        "INTRODUCTION", "AN IN-DEPTH LOOK", "AN IN-DEPTH LOOK CONTINUED", 

        "NECP ALIGNMENT", "RESOURCES", "ABSTRACT", "CCS CONCEPTS", "KEYWORDS",

        "1 INTRODUCTION", "2 BACKGROUND", "3 A THREAT MODEL FOR WEB-BASED EMERGENCY COMMUNICATION",

        "4 METHOD AND DATA CORPUS", "5 DNS NAMESPACE ANALYSIS", "6 WEB PKI ANALYSIS",

        "7 RELATED WORK", "8 KEY FINDINGS AND DISCUSSIONS", "9 CONCLUSION AND OUTLOOK", 

        "REFERENCES", "Abstract", "1 Introduction", "2 Methods", "3 Results", "4 Discussion", 

        "5 Conclusion", "Appendix 1: List of studies included", "Abstract", 

        "1 | L I T E R A T U R E R E V I E W", "2 | M E T H O D S", "3 | R E S U L T S", 

        "4 | D IS C U S S IO N", "5 | C O N C L U S I O N", "R E F E R E N C E S", 

        "Table of Contents", "1 Results in Brief", "1.1 Executive Summary", "2 Definitions", 

        "3 Introduction", "3.1 CSRIC Structure", "4 Objective, Scope, and Methodology", 

        "5 Background", "6 Alert Dissemination Techniques", "7 Capabilities Needed to Improve Public Safety", 

        "8 Recommendations", "9 Conclusions", "Appendix A – Alert Originators Use Cases", 

        "Appendix B – ATSC 3.0 Primer", "FEDERAL COMMUNICATIONS COMMISSION", 

        "FEDERAL RESERVE SYSTEM", "FEDERAL MINE SAFETY AND HEALTH REVIEW COMMISSION", 

        "Cybersecurity Framework (CSF) Overview", "Introduction to the CSF Core", 

        "Introduction to CSF Profiles and Tiers", "Improving Cybersecurity Risk Communication and Integration",

        "Appendix A. CSF Core", "Appendix B. CSF Tiers", "Appendix C. Glossary", 

        "List of Figures", "EXECUTIVE SUMMARY", "ALERTS, WARNINGS & NOTIFICATIONS", 

        "1. ESTABLISH GOVERNANCE", "2. IDENTIFY AND COORDINATE WITH OTHERS", "3. DEVELOP PLANS, POLICIES AND PROCEDURES", 

        "CONCLUSION", "APPENDIX A: ACRONYMS", "APPENDIX B: DISCLAIMER OF LIABILITY"

    ]

    

    directory = "text-files-2025"

    documents = process_txt_files_in_directory(directory, headings)
    save_documents_to_json(documents)

