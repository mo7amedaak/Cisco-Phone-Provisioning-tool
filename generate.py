import pandas as pd
import xml.etree.ElementTree as ET
import os

# ==========================
# Configuration
# ==========================
TEMPLATE_FILE = "template.xml"
EXCEL_FILE = "phones.xlsx"
OUTPUT_FOLDER = "output"

SERVER_IP = "192.168.1.180"
SIP_PASSWORD = "1234"

# ==========================
# Create output folder
# ==========================
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ==========================
# Read Excel
# ==========================
phones = pd.read_excel(EXCEL_FILE)

# ==========================
# Generate XML files
# ==========================
for _, phone in phones.iterrows():

    mac = str(phone["MAC"]).upper().replace(":", "").replace("-", "")
    extension = str(phone["Extension"])
    display = str(phone["DisplayName"])

    tree = ET.parse(TEMPLATE_FILE)
    root = tree.getroot()

    # PBX Server
    root.find("./devicePool/callManagerGroup/members/member/callManager/processNodeName").text = SERVER_IP
    root.find("./sipProfile/sipLines/line/proxy").text = SERVER_IP

    # Extension
    root.find("./sipProfile/sipLines/line/name").text = extension
    root.find("./sipProfile/sipLines/line/authName").text = extension
    root.find("./sipProfile/sipLines/line/contact").text = extension

    # Password
    root.find("./sipProfile/sipLines/line/authPassword").text = SIP_PASSWORD

    # Display
    root.find("./sipProfile/sipLines/line/displayName").text = display
    root.find("./sipProfile/sipLines/line/featureLabel").text = display

    output_file = os.path.join(
        OUTPUT_FOLDER,
        f"SEP{mac}.cnf.xml"
    )

    tree.write(output_file, encoding="utf-8", xml_declaration=True)

print(f"Done! Generated {len(phones)} configuration files.")