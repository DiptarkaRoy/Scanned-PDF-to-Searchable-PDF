import pytesseract
from pdf2image import convert_from_path
from PyPDF2 import PdfWriter, PdfReader
import io, os, argparse, tempfile, time, platform
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm

# --- DYNAMIC CONFIGURATION ---
SYSTEM = platform.system()

if SYSTEM == "Windows":
    # Paths for your HP EliteBook
    pytesseract.pytesseract.tesseract_cmd = r'C:\Users\eydipro\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
    POPPLER_PATH = r'C:\poppler-25.12.0\Library\bin'
    WORKERS = 6
else:
    # Paths for your MacBook Air M3 (Homebrew)
    pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'
    POPPLER_PATH = None # macOS finds brew-installed poppler automatically
    WORKERS = 8 # Optimized for M3 Performance + Efficiency cores

LOCK_FILE = os.path.join(tempfile.gettempdir(), "ocr_automation.lock")

def ocr_single_page(img_path):
    """The heavy lifting: Converting one image to a PDF layer"""
    try:
        return pytesseract.image_to_pdf_or_hocr(img_path, extension='pdf', config=r'--oem 1 --psm 1')
    except Exception as e:
        return f"Error: {e}"

def process_pdf(input_path):
    if not os.path.exists(input_path):
        print(f"❌ File not found: {input_path}")
        return

    # Queue management
    while os.path.exists(LOCK_FILE):
        print("⏳ Waiting for current OCR job to finish... (Checking every 60s)")
        time.sleep(60)

    try:
        with open(LOCK_FILE, "w") as f: f.write("locked")
        
        start_time = time.time()
        output_path = f"{os.path.splitext(input_path)[0]}_searchable.pdf"

        with tempfile.TemporaryDirectory() as temp_dir:
            print(f"\n🚀 Processing on {SYSTEM} using {WORKERS} workers...")
            
            # Step 1: Convert PDF to Images
            images = convert_from_path(input_path, dpi=200, poppler_path=POPPLER_PATH, 
                                       output_folder=temp_dir, fmt="jpeg", paths_only=True)

            # Step 2: Parallel OCR
            results = {}
            with ProcessPoolExecutor(max_workers=WORKERS) as executor:
                futures = {executor.submit(ocr_single_page, path): i for i, path in enumerate(images)}
                for future in tqdm(as_completed(futures), total=len(images), desc="OCR Progress"):
                    results[futures[future]] = future.result()

            # Step 3: Merge
            writer = PdfWriter()
            for i in range(len(images)):
                if isinstance(results[i], bytes):
                    writer.add_page(PdfReader(io.BytesIO(results[i])).pages[0])

            with open(output_path, "wb") as f:
                writer.write(f)

            duration = time.time() - start_time
            print(f"\n✅ SUCCESS! File saved as: {os.path.basename(output_path)}")
            print(f"⏱️  Time: {int(duration // 60)}m {int(duration % 60)}s")
            print(f"📈 Speed: {round(len(images)/(duration/60), 2)} pages/min")

    finally:
        if os.path.exists(LOCK_FILE): os.remove(LOCK_FILE)

def main():
    parser = argparse.ArgumentParser(description="Parallel OCR Converter")
    parser.add_argument("path", help="Path to the scanned PDF")
    args = parser.parse_args()
    process_pdf(args.path)

if __name__ == "__main__":
    main()