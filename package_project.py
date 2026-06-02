import os
import zipfile
import subprocess
import sys

def run_pdf_generation():
    print("Starting PDF compilation...")
    # Run build_pdfs.py as a subprocess using the current python interpreter
    result = subprocess.run([sys.executable, 'build_pdfs.py'], capture_output=True, text=True, encoding='utf-8')
    if result.returncode != 0:
        print("PDF compilation failed!", file=sys.stderr)
        print("STDOUT:", file=sys.stderr)
        print(result.stdout, file=sys.stderr)
        print("STDERR:", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        sys.exit(1)
    else:
        print(result.stdout)
        print("PDF compilation succeeded.")

def create_zip_archive():
    zip_filename = "LB-Projekt-M347_Morina_Fluri.zip"
    print(f"Creating ZIP archive: {zip_filename}...")
    
    files_to_include = [
        ("Projektdokumentation.pdf", "Projektdokumentation.pdf"),
        ("Präsentation.pdf", "Präsentation.pdf"),
    ]
    
    project_dir = "Projekt"
    
    # Walk the Projekt directory to find configurations
    project_files = []
    if not os.path.exists(project_dir):
        print(f"Error: {project_dir} directory does not exist!", file=sys.stderr)
        sys.exit(1)
        
    for root, dirs, files in os.walk(project_dir):
        for file in files:
            full_path = os.path.join(root, file)
            # Relative path should start with 'Projekt/'
            rel_path = os.path.relpath(full_path, start=os.getcwd())
            project_files.append((full_path, rel_path))
            
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add PDFs to root of zip
        for filepath, arcname in files_to_include:
            if not os.path.exists(filepath):
                print(f"Error: Required file {filepath} not found!", file=sys.stderr)
                sys.exit(1)
            zipf.write(filepath, arcname)
            print(f"Added to ZIP: {arcname}")
            
        # Add all files in Projekt/
        for filepath, arcname in project_files:
            zipf.write(filepath, arcname)
            print(f"Added to ZIP: {arcname}")
            
    print(f"ZIP archive {zip_filename} successfully created.")

if __name__ == '__main__':
    run_pdf_generation()
    create_zip_archive()
    print("Packaging completed successfully.")
