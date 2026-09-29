from pathlib import Path
import glob
from datetime import datetime
import csv
import shutil

def validation_filename(filename)->bool:
    try:
        parts = filename.split("_")
        if len(parts[1])==8:
            stryear = int(parts[1][:4])
            strmonth = int(parts[1][4:6])
            strday = int(parts[1][6:])
            print(f"stryear:{stryear} strmonth:{strmonth} strday:{strday}")
            dt = datetime(stryear, strmonth, strday)
            print(f"filename: {dt}")
            return True
        else:
            return False
    except Exception:
        return False

base_root = Path.cwd()

input_folder = base_root / "input"
output_folder = base_root / "output"
error_folder = base_root / "error"
archive_folder = base_root / "archive"

input_folder.mkdir(exist_ok=True)
output_folder.mkdir(exist_ok=True)
error_folder.mkdir(exist_ok=True)
archive_folder.mkdir(exist_ok=True)

input_file_pattern = input_folder / "transactions_*.csv"

inputfiles = glob.glob(str(input_file_pattern))

required_fields = [
    "transaction_id",
    "customer_name",
    "amount",
    "status"
]

for filestr in inputfiles:
    
    print(f"{filestr} if valid:{validation_filename(Path(filestr).stem)}")
    if(validation_filename(Path(filestr).stem)):
        #good
        try:
            with open(filestr,"r", encoding="utf-8", newline="") as file:
                valid_records = []
                bad_records = []
                csvobject = csv.DictReader(file)
                for item in csvobject:
                    try:
                        fieldgood = True
                        for field in required_fields:
                            value = item.get(field)
                            if value is None or value.strip() == "":
                                print(f"Missing required value: {field}")
                                fieldgood = False
                        print(item["transaction_id"])
                        if fieldgood:
                            item["transaction_id"] = int(item["transaction_id"])
                            item["customer_name"] = item["customer_name"].strip()
                            item["amount"] = float(item["amount"])
                            item["status"] = item["status"][0].upper() + item["status"][1:].lower()
                            test =""
                            valid_records.append(item)
                        else:
                            bad_records.append(item)
                    except Exception:
                        bad_records.append(item)
                if len(valid_records)>0:
                    filename = str(Path(filestr).stem) + "_"+datetime.now().strftime("%H%M%S")+Path(filestr).suffix
                    output_file = output_folder/ filename
                    test = ""
                    #write records to output.
                    with open(output_file, "w", encoding="utf-8", newline="") as ffile:
                        writer = csv.DictWriter(ffile, fieldnames=required_fields)
                        writer.writeheader()
                        writer.writerows(valid_records)
                if len(bad_records)> 0:
                    filename = str(Path(filestr).stem) + "_"+datetime.now().strftime("%H%M%S")+Path(filestr).suffix
                    output_file = error_folder/ filename
                    test = ""
                    #write records to output.
                    with open(output_file, "w", encoding="utf-8", newline="") as ffile:
                        writer = csv.DictWriter(ffile, fieldnames=required_fields)
                        writer.writeheader()
                        writer.writerows(bad_records)
                #move file to archive use timestamp in filename
                filename = str(Path(filestr).stem) + "_"+datetime.now().strftime("%H%M%S")+Path(filestr).suffix
                output_file = archive_folder/ filename
            shutil.move(filestr, output_file)
        except Exception:
            filename = str(Path(filestr).stem) + "_"+datetime.now().strftime("%H%M%S")+Path(filestr).suffix
            output_file = error_folder/ filename
            shutil.move(filestr, output_file)    
    else:
        filename = str(Path(filestr).stem) + "_"+datetime.now().strftime("%H%M%S")+Path(filestr).suffix
        output_file = error_folder/ filename
        shutil.move(filestr, output_file)
        #bad...move to error folder
        
