import os
import shutil

base_dir = r"c:\image converter new"
tools_to_localize = [
    "compress-image-to-500kb",
    "compress-image-to-200kb",
    "compress-image-to-100kb",
    "compress-image-to-50kb",
    "compress-image-to-30kb",
    "compress-image-to-20kb",
    "compress-image-to-10kb",
    "compress-jpg-to-100kb",
    "compress-png-to-100kb",
    "compress-jpeg-to-100kb",
    "jpg-to-avif",
    "photo-to-black-and-white",
    "png-to-avif",
    "png-to-ico",
    "svg-to-jpg",
    "svg-to-png",
    "resize-image",
    "watermark-image",
    "jpg-to-pdf"
]
languages = ["de", "es", "fr", "hi", "zh"]

def main():
    for tool in tools_to_localize:
        src_path = os.path.join(base_dir, tool, "index.html")
        if not os.path.exists(src_path):
            print(f"Warning: Base tool {tool} index.html not found.")
            continue
        
        with open(src_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        for lang in languages:
            dest_dir = os.path.join(base_dir, lang, tool)
            os.makedirs(dest_dir, exist_ok=True)
            
            dest_path = os.path.join(dest_dir, "index.html")
            # Set correct HTML lang tag for proper localized sync
            localized_content = content.replace('<html lang="en">', f'<html lang="{lang}">')
            with open(dest_path, 'w', encoding='utf-8') as f:
                f.write(localized_content)
            print(f"Created {lang}/{tool}/index.html")

if __name__ == "__main__":
    main()
