import pandas as pd
from pathlib import Path
import glob
import shutil

def addNewName(filePath, type, papercode):
    # quizetype allowed
    df = pd.read_csv(filePath)
    if type == 'mcqs':
        oldstr = r'^(pc\d{2}_)' ## Update Pattern 
        newstr = f'mcqs_pc_{papercode}_'
    elif type == 'pointers':
        oldstr = r'^(pointers_pc\d{2}_)' ## Update Pattern 
        newstr = f'pointers_pc_{papercode}_'
    elif type == 'fillers' :
        oldstr = r'^(fillers_pc\d{2}_)' ## Update Pattern 
        newstr = f'fillers_pc_{papercode}_'
    elif type == 'mocks' :
        oldstr = r'^(mocks_pc\d{2}_)' ## Update Pattern 
        newstr = f'mokcs_pc_{papercode}_'
    else:
        print('Invalide Type')
        return 
    
    df.quizefile = df.quizefile_old.str.replace(oldstr, newstr, regex=True ).str.strip()
    df.to_csv(filePath, index=False)
    print(f'Add new name in {filePath.name} at {filePath.parent}')


def copy_files_from_csv(file: Path, source: Path, destination: Path):
    df = pd.read_csv(file)
    files_to_copy = df['quizefile_old'].dropna().unique()
    destination.mkdir(parents=True, exist_ok=True)
    for filename in files_to_copy:
        filename =f'{filename}.csv'
        source_file = source / filename
        if source_file.exists() and source_file.is_file():
            shutil.copy2(source_file, destination / filename)
            print(f"File copied succesfully : {source_file}")
        else:
            print(f"File not found: {source_file}")


def renameFiles(filePath, directory):
    df = pd.read_csv(filePath)  
    for _, row in df.iterrows():
        old_file = directory / f'{row['quizefile_old']}.csv'
        new_file = directory / f'{row['quizefile']}.csv'
        
        # Check if the old file exists, then rename
        if old_file.exists():
            old_file.rename(new_file)
            print(f"Renamed '{old_file.name}' to '{new_file.name}'")
        else:
            print(f"File '{old_file.name}' not found.")




def addHeader(dir_path, type):
    if type == 'mcqs' or type == 'mocks':   
        header = ['question', 'option_a', 'option_b', 'option_c', 'option_d', 'answer', 'hint']
    elif type == 'pointers' or type == 'fillers':
        header = ['question', 'answer']
    else:
        print('Wrong Type')
        return
    
    print(dir_path)

    for file_path in list(dir_path.glob('*.csv')):
     
        df = pd.read_csv(file_path, header=None)
        if    type == 'mcqs' or type == 'mocks': 
            df = df.iloc[:, :7].copy()
        if type == 'pointers' or type == 'fillers':
            df = df.iloc[:, :2].copy()

        print('Read:', file_path)    
        
        df.columns = header      
        df.to_csv(file_path, index=False)
        print('saved:', file_path)


def mcqs_remove_quesiton_number_option_number(file_path):
    patternSrNo = r'^(\d+[A-Za-z]*\.*)'
    patternOption = r'^(\([A-Za-z]\)\.*)'
    
    df = pd.read_csv(file_path)
    # print('Read:', file_path)    

    df['srno'] = df.question.str.strip().str.extract(patternSrNo)
    df['srno'] =df['srno'].str.strip()
    df.question= df.question.str.strip().str.replace(patternSrNo, '', regex=True ).str.strip()

    for col in df.columns[1:5]:
        df[col]= df[col].str.replace(patternOption, '', regex=True ).str.strip()
    
    df.to_csv(file_path, index=False)
    print('Added Header and saved:', file_path)

def pointers_remove_qnum(file_path):
    patternSrNo = r'^(\d+[A-Za-z]*:*)'
    df = pd.read_csv(file_path)
    print('Read:', file_path)  
    
    df['srno'] = df.question.str.strip().str.extract(patternSrNo)
    df['srno'] =df['srno'].str.strip()
    
    df.question= df.question.str.strip().str.replace(patternSrNo, '', regex=True ).str.strip()
    df.to_csv(file_path, index=False)
    print('saved:', file_path)

def clean_question_option(directory, type):
    for file in list(directory.glob('*.csv')):
        if type == 'mcqs' or type =='mocks':
            mcqs_remove_quesiton_number_option_number(file)
        if type == 'pointers' or type == 'fillers':
            pointers_remove_qnum(file)
          

def main():
    # filePath= Path(r'C:\Users\AG(A&E)\MKT_Workstation\Personal_Projects\sasquizzer2025\data\quizlists\quiz_list_pc04_pointers.csv') # Update it 
    filePath= Path(r'C:\Users\AG(A&E)\MKT_Workstation\Personal_Projects\sasquizzer2025\data\quizlists\quiz_list_pc04_fillers.csv') # Update it 
    directorySource = Path(r'C:\Users\AG(A&E)\MKT_Workstation\Personal_Projects\SAS Quizzer Web App\data_back\fillers')

    directoryDestination = Path(r'C:\Users\AG(A&E)\MKT_Workstation\Personal_Projects\sasquizzer2025\data\fillers')
    
    # type = 'pointers'
    type = 'fillers'
    papercode = '04'
    # Step 01
    # addNewName(filePath, type=type, papercode=papercode)

    # # # # step 02
    # copy_files_from_csv(filePath, directorySource , directoryDestination)
    
    # # # # Step 03
    # renameFiles(filePath, directoryDestination) 
    
    # # # Step 04
    # addHeader(directoryDestination, type=type)
    

    # # # Step 05
    # clean_question_option(directoryDestination, type=type)



if __name__ == "__main__":
    main()