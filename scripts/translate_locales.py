import os
import re
import json

base_dir = r"c:\image converter new"

languages = ["de", "es", "fr", "hi", "zh"]

# Common / Global translated UI phrases
COMMON_UI = {
    'de': {
        'drop_images_here': 'Bilder hierher ziehen',
        'supports_formats': 'Unterstützt Formate wie JPG, PNG, WEBP, HEIC, SVG',
        'device': 'Gerät auswählen',
        'select_file_start': 'Wählen Sie hier Ihre Datei aus, um zu beginnen',
        'or_drop_here': 'oder ziehen Sie Ihre Datei hierher.',
        'trust_badge': '100% sicher — Bilder verlassen Ihr Gerät nie',
        'converted_successfully': 'Erfolgreich konvertiert!',
        'download': 'Herunterladen',
        'related_free_tools': 'Verwandte kostenlose Werkzeuge',
        'footer_copy': 'Ihre Dateien verlassen Ihr Gerät nie — 100% clientseitige Verarbeitung.',
        'privacy_policy': 'Datenschutz-Bestimmungen',
        'terms_of_service': 'Nutzungsbedingungen',
        'about_us': 'Über uns',
        'contact': 'Kontakt',
        'convert_images': 'Bilder konvertieren'
    },
    'es': {
        'drop_images_here': 'Arrastra imágenes aquí',
        'supports_formats': 'Soporta formatos incluyendo JPG, PNG, WEBP, HEIC, SVG',
        'device': 'Seleccionar archivo',
        'select_file_start': 'Selecciona tu archivo aquí para comenzar',
        'or_drop_here': 'o arrastra tu archivo aquí.',
        'trust_badge': '100% seguro — las imágenes nunca salen de tu dispositivo',
        'converted_successfully': '¡Convertido con éxito!',
        'download': 'Descargar',
        'related_free_tools': 'Herramientas gratuitas relacionadas',
        'footer_copy': 'Tus archivos nunca salen de tu dispositivo — renderizado 100% del lado del cliente.',
        'privacy_policy': 'Política de Privacidad',
        'terms_of_service': 'Términos de Servicio',
        'about_us': 'Sobre Nosotros',
        'contact': 'Contacto',
        'convert_images': 'Convertir imágenes'
    },
    'fr': {
        'drop_images_here': 'Déposez les images ici',
        'supports_formats': 'Prend en charge les formats JPG, PNG, WEBP, HEIC, SVG',
        'device': 'Sélectionner le fichier',
        'select_file_start': 'Sélectionnez votre fichier ici pour commencer',
        'or_drop_here': 'ou déposez votre fichier ici.',
        'trust_badge': '100% sécurisé — les images ne quittent jamais votre appareil',
        'converted_successfully': 'Converti avec succès !',
        'download': 'Télécharger',
        'related_free_tools': 'Outils gratuits connexes',
        'footer_copy': 'Vos fichiers ne quittent jamais votre appareil — rendu 100% côté client.',
        'privacy_policy': 'Politique de Confidentialité',
        'terms_of_service': 'Conditions d\'Utilisation',
        'about_us': 'À Propos',
        'contact': 'Contact',
        'convert_images': 'Convertir les images'
    },
    'hi': {
        'drop_images_here': 'यहाँ चित्र खींचें और छोड़ें',
        'supports_formats': 'JPG, PNG, WEBP, HEIC, SVG सहित सभी प्रारूप समर्थित',
        'device': 'फ़ाइल चुनें',
        'select_file_start': 'शुरू करने के लिए यहाँ अपनी फ़ाइल चुनें',
        'or_drop_here': 'या अपनी फ़ाइल यहाँ छोड़ें।',
        'trust_badge': '100% सुरक्षित — चित्र कभी भी आपके डिवाइस से बाहर नहीं जाते हैं',
        'converted_successfully': 'सफलतापूर्वक कनवर्ट किया गया!',
        'download': 'डाउनलोड करें',
        'related_free_tools': 'संबंधित मुफ्त टूल्स',
        'footer_copy': 'आपकी फ़ाइलें कभी भी आपके डिवाइस से बाहर नहीं जाती हैं — 100% क्लाइंट-साइड रेंडरिंग।',
        'privacy_policy': 'गोपनीयता नीति',
        'terms_of_service': 'सेवा की शर्तें',
        'about_us': 'हमारे बारे में',
        'contact': 'संपर्क',
        'convert_images': 'इमेज कन्वर्ट करें'
    },
    'zh': {
        'drop_images_here': '将图片拖放到此处',
        'supports_formats': '支持 JPG、PNG、WEBP、HEIC、SVG 等格式',
        'device': '选择文件',
        'select_file_start': '选择您的文件开始转换',
        'or_drop_here': '或将您的文件拖放到这里。',
        'trust_badge': '100% 安全 — 图片永远不会离开您的设备',
        'converted_successfully': '转换成功！',
        'download': '下载',
        'related_free_tools': '相关免费工具',
        'footer_copy': '您的文件永远不会离开您的设备 — 100% 浏览器客户端本地转换。',
        'privacy_policy': '隐私政策',
        'terms_of_service': '服务条款',
        'about_us': '关于我们',
        'contact': '联系我们',
        'convert_images': '转换图片'
    }
}

# Rich tool translations matrices

FAQ_TEMPLATES = {
    'en': {
        'format_image': 'image',
        'q1': 'How do I compress a {format} to {size}KB?',
        'a1': 'Upload your {format} into our local compressor. The client-side engine will automatically optimize resolution and quality parameters to fit within the {size}KB limit.',
        'q2': 'Can I compress PNG to {size}KB without losing quality?',
        'a2': 'Compressing to exactly {size}KB requires lossy optimization. While our kb reducer uses smart local canvas serialization to minimize quality loss, PNGs (especially with text or fine details) will be optimized to meet the target threshold.',
        'q3': 'Is my image uploaded to a server?',
        'a3': 'Absolutely not. Our compressor runs 100% locally in your web browser. Your images never leave your device, ensuring maximum privacy and security.',
        'q4': 'Can I compress images offline?',
        'a4': 'Yes! Since the processing is done client-side, the tool functions entirely offline without any internet connection once the page is loaded.',
        'q5': 'Does this work on mobile phones?',
        'a5': 'Yes, it works seamlessly on all Android devices, iPhones (including HEIC formats), and tablets directly through your mobile web browser.',
        'q6': 'Can I compress multiple images at once?',
        'a6': 'Yes, our tool supports bulk image compression. Drag and drop multiple files to optimize them in a single batch.',
        'q7': 'What image formats are supported?',
        'a7': 'We support JPG, JPEG, PNG, WEBP, HEIC, and TIFF formats. Uploaded HEIC or TIFF files are automatically processed and converted.'
    },
    'de': {
        'format_image': 'Bild',
        'q1': 'Wie komprimiere ich ein {format} auf {size}KB?',
        'a1': 'Laden Sie Ihr {format} in unseren lokalen Kompressor hoch. Die clientseitige Engine optimiert Auflösung und Qualität automatisch, um das Limit von {size}KB einzuhalten.',
        'q2': 'Kann ich PNG ohne Qualitätsverlust auf {size}KB komprimieren?',
        'a2': 'Das Komprimieren auf exakt {size}KB erfordert eine verlustbehaftete Optimierung. Unser Tool nutzt intelligente Canvas-Serialisierung, um den Qualitätsverlust zu minimieren.',
        'q3': 'Werden meine Bilder auf einen Server hochgeladen?',
        'a3': 'Nein. Unser Kompressor läuft zu 100% lokal in Ihrem Webbrowser. Ihre Bilder verlassen Ihr Gerät nie, was maximale Privatsphäre garantiert.',
        'q4': 'Kann ich Bilder offline komprimieren?',
        'a4': 'Ja! Da die Verarbeitung clientseitig erfolgt, funktioniert das Tool nach dem Laden der Seite vollständig offline.',
        'q5': 'Funktioniert das auch auf Mobiltelefonen?',
        'a5': 'Ja, es läuft nahtlos auf allen Android-Geräten, iPhones (inkl. HEIC) und Tablets direkt im mobilen Browser.',
        'q6': 'Kann ich mehrere Bilder gleichzeitig komprimieren?',
        'a6': 'Ja, unser Tool unterstützt die Stapelkomprimierung. Ziehen Sie mehrere Dateien hinein, um sie in einem Rutsch zu optimieren.',
        'q7': 'Welche Bildformate werden unterstützt?',
        'a7': 'Wir unterstützen JPG, JPEG, PNG, WEBP, HEIC und TIFF. Hochgeladene HEIC- oder TIFF-Dateien werden automatisch verarbeitet.'
    },
    'es': {
        'format_image': 'imagen',
        'q1': '¿Cómo comprimo un {format} a {size}KB?',
        'a1': 'Sube tu {format} a nuestro compresor local. El motor del lado del cliente optimizará la resolución y la calidad para ajustarse al límite de {size}KB.',
        'q2': '¿Puedo comprimir PNG a {size}KB sin perder calidad?',
        'a2': 'Comprimir a exactamente {size}KB requiere optimización con pérdida. Nuestra herramienta utiliza serialización inteligente en el navegador para minimizar la pérdida visual.',
        'q3': '¿Se suben mis imágenes a algún servidor?',
        'a3': 'No. Nuestro compresor funciona 100% local en tu navegador. Tus fotos nunca salen de tu dispositivo, garantizando máxima seguridad.',
        'q4': '¿Puedo comprimir imágenes sin conexión (offline)?',
        'a4': 'Sí, al procesarse en el cliente, el compresor funciona completamente sin conexión una vez que se carga la página.',
        'q5': '¿Funciona en teléfonos móviles?',
        'a5': 'Sí, funciona perfectamente en Android, iPhone (incluyendo HEIC) y tabletas desde el navegador web móvil.',
        'q6': '¿Puedo comprimir varias imágenes a la vez?',
        'a6': 'Sí, admitimos compresión por lotes. Arrastra múltiples archivos para optimizarlos en un solo paso.',
        'q7': '¿Qué formatos de imagen son compatibles?',
        'a7': 'Soportamos JPG, JPEG, PNG, WEBP, HEIC y TIFF. Los archivos HEIC o TIFF se procesan y convierten de forma automática.'
    },
    'fr': {
        'format_image': 'image',
        'q1': 'Comment compresser un {format} à {size}Ko ?',
        'a1': 'Téléversez votre {format} dans notre compresseur local. Le moteur côté client optimisera automatiquement la résolution et la qualité sous la limite de {size}Ko.',
        'q2': 'Puis-je compresser un PNG à {size}Ko sans perte de qualité ?',
        'a2': 'Compresser à exactement {size}Ko nécessite une compression avec perte. Notre outil utilise une sérialisation canvas intelligente pour minimiser la perte visuelle.',
        'q3': 'Mes images sont-elles téléversées sur un serveur ?',
        'a3': 'Absolument pas. Notre compresseur fonctionne à 100% localement dans votre navigateur. Vos photos ne quittent jamais votre appareil.',
        'q4': 'Puis-je compresser des images hors ligne ?',
        'a4': 'Oui ! Comme tout le traitement se fait côté client, l\'outil fonctionne entièrement hors ligne après le chargement initial de la page.',
        'q5': 'Est-ce que cela fonctionne sur les téléphones portables ?',
        'a5': 'Oui, il fonctionne parfaitement sur Android, iPhone (y compris HEIC) et tablettes directement dans votre navigateur mobile.',
        'q6': 'Puis-je compresser plusieurs images à la fois ?',
        'a6': 'Oui, notre outil prend en charge la compression par lots. Glissez-déposez plusieurs fichiers pour les optimiser en une seule fois.',
        'q7': 'Quels formats d\'image sont pris en charge ?',
        'a7': 'Nous prenons en charge les formats JPG, JPEG, PNG, WEBP, HEIC et TIFF. Les fichiers HEIC ou TIFF sont automatiquement convertis.'
    },
    'hi': {
        'format_image': 'इमेज',
        'q1': '{format} को {size}KB में कैसे कंप्रेस करें?',
        'a1': 'अपने {format} को हमारे लोकल कंप्रेसर पर अपलोड करें। हमारा क्लाइंट-साइड इंजन {size}KB सीमा में फिट होने के लिए रेजोल्यूशन और क्वालिटी को खुद ब खुद ऑप्टिमाइज़ कर देगा।',
        'q2': 'क्या मैं बिना गुणवत्ता नुकसान के PNG को {size}KB तक कंप्रेस कर सकता हूँ?',
        'a2': 'ठीक {size}KB तक कंप्रेस करने के लिए कुछ नुकसानदेह (lossy) ऑप्टिमाइज़ेशन की आवश्यकता होती है। हमारा टूल गुणवत्ता के नुकसान को कम करने के लिए स्मार्ट कैनवास एल्गोरिदम का उपयोग करता है।',
        'q3': 'क्या मेरी इमेज सर्वर पर अपलोड की जाती है?',
        'a3': 'बिल्कुल नहीं। हमारा कंप्रेसर आपके वेब ब्राउज़र में 100% स्थानीय रूप से चलता है। आपकी तस्वीरें कभी भी आपके डिवाइस से बाहर नहीं जाती हैं।',
        'q4': 'क्या मैं छवियों को ऑफलाइन कंप्रेस कर सकता हूँ?',
        'a4': 'हाँ! चूंकि प्रोसेसिंग क्लाइंट-साइड होती है, इसलिए पेज लोड होने के बाद यह टूल बिना इंटरनेट कनेक्शन के पूरी तरह से काम करता है।',
        'q5': 'क्या यह मोबाइल फोन पर काम करता है?',
        'a5': 'हाँ, यह मोबाइल वेब ब्राउज़र के माध्यम से सभी एंड्रॉइड डिवाइस, आईफोन (HEIC फॉर्मेट सहित) और टैबलेट पर आसानी से काम करता है।',
        'q6': 'क्या मैं एक बार में कई इमेज कंप्रेस कर सकता हूँ?',
        'a6': 'हाँ, हमारा टूल बैच कंप्रेसन का समर्थन करता है। एक बार में कई फाइलों को ऑप्टिमाइज़ करने के लिए ड्रैग और ड्रॉप करें।',
        'q7': 'कौन-से इमेज फॉर्मेट समर्थित हैं?',
        'a7': 'हम JPG, JPEG, PNG, WEBP, HEIC और TIFF फॉर्मेट का समर्थन करते हैं। अपलोड की गई HEIC या TIFF फाइलें स्वचालित रूप से कनवर्ट हो जाती हैं।'
    },
    'zh': {
        'format_image': '图片',
        'q1': '如何将 {format} 压缩到 {size}KB？',
        'a1': '将您的 {format} 上传到本地压缩器。前端浏览器端引擎将自动调整分辨率和质量参数，使其符合 {size}KB 的限制。',
        'q2': '如何无损压缩 PNG 到 {size}KB？',
        'a2': '压缩至恰好 {size}KB 需要进行有损优化。虽然我们的 kb 减小工具使用智能本地 Canvas 序列化来尽量减少画质损失，但仍会对图像进行适当压缩以达标。',
        'q3': '我的图片会被上传到服务器吗？',
        'a3': '绝对不会。我们的压缩器 100% 在您的浏览器本地运行。您的图片永远不会离开您的设备，从而确保了最高的隐私和安全性。',
        'q4': '我可以离线压缩图片吗？',
        'a4': '可以！由于所有处理均在客户端进行，页面加载后，该工具即可完全在无网络连接的状态下离线工作。',
        'q5': '此工具支持在手机上运行吗？',
        'a5': '支持，它可以在安卓、iPhone（包括 HEIC 格式）和 iPad 的移动端浏览器中无缝运行。',
        'q6': '我可以一次压缩多张图片吗？',
        'a6': '可以，我们的工具支持批量图片压缩。拖放多个文件即可在单次批处理中优化它们。',
        'q7': '支持哪些图片格式？',
        'a7': '我们支持 JPG、JPEG、PNG、WEBP、HEIC 和 TIFF 格式。上传的 HEIC 或 TIFF 文件会自动处理和转换。'
    }
}

HOWTO_TRANSLATIONS = {
    'en': {
        'compress_title': 'How to compress images online',
        'convert_title': 'How to convert images online',
        'step1_name': 'Upload Images',
        'step1_text': 'Drag and drop your files into the upload area or click select to browse from your device.',
        'step2_compress_name': 'Select Target Size',
        'step2_compress_text': 'Choose a target size preset (e.g. under 50KB, 100KB) or input a custom limit.',
        'step2_convert_name': 'Select Output Format',
        'step2_convert_text': 'Select your desired output format from the tabs (e.g. JPG, PNG, WEBP, AVIF).',
        'step3_name': 'Download Output',
        'step3_text': 'Click the convert or compress button and download your optimized files instantly.'
    },
    'de': {
        'compress_title': 'Wie man Bilder online komprimiert',
        'convert_title': 'Wie man Bilder online konvertiert',
        'step1_name': 'Bilder hochladen',
        'step1_text': 'Ziehen Sie Ihre Dateien per Drag & Drop in den Upload-Bereich oder klicken Sie auf Auswählen.',
        'step2_compress_name': 'Zielgröße wählen',
        'step2_compress_text': 'Wählen Sie eine Zielgröße (z. B. unter 50KB oder 100KB) oder geben Sie ein eigenes Limit ein.',
        'step2_convert_name': 'Ausgabeformat wählen',
        'step2_convert_text': 'Wählen Sie das gewünschte Ausgabeformat aus den Tabs (z. B. JPG, PNG, WEBP).',
        'step3_name': 'Ergebnis herunterladen',
        'step3_text': 'Klicken Sie auf Konvertieren oder Komprimieren und laden Sie Ihre optimierten Dateien sofort herunter.'
    },
    'es': {
        'compress_title': 'Cómo comprimir imágenes online',
        'convert_title': 'Cómo convertir imágenes online',
        'step1_name': 'Subir imágenes',
        'step1_text': 'Arrastra y suelta tus archivos en el área de carga o haz clic en seleccionar.',
        'step2_compress_name': 'Seleccionar tamaño objetivo',
        'step2_compress_text': 'Elige un ajuste de tamaño (ej. menos de 50KB o 100KB) o ingresa un límite personalizado.',
        'step2_convert_name': 'Seleccionar formato de salida',
        'step2_convert_text': 'Selecciona el formato de salida deseado de las pestañas (ej. JPG, PNG, WEBP).',
        'step3_name': 'Descargar resultado',
        'step3_text': 'Haz clic en el botón de convertir o comprimir y descarga tus archivos optimizados al instante.'
    },
    'fr': {
        'compress_title': 'Comment compresser des images en ligne',
        'convert_title': 'Comment convertir des images en ligne',
        'step1_name': 'Téléverser des images',
        'step1_text': 'Glissez-déposez vos fichiers dans la zone de dépôt ou cliquez sur sélectionner.',
        'step2_compress_name': 'Sélectionner la taille cible',
        'step2_compress_text': 'Choisissez une taille cible prédéfinie (ex. moins de 50Ko ou 100Ko) ou saisissez une limite.',
        'step2_convert_name': 'Sélectionner le format de sortie',
        'step2_convert_text': 'Sélectionnez le format de sortie souhaité dans les onglets (ex. JPG, PNG, WEBP).',
        'step3_name': 'Télécharger le résultat',
        'step3_text': 'Cliquez sur le bouton de conversion ou de compression et téléchargez instantanément vos fichiers.'
    },
    'hi': {
        'compress_title': 'ऑनलाइन इमेज कैसे कंप्रेस करें',
        'convert_title': 'ऑनलाइन इमेज कैसे कनवर्ट करें',
        'step1_name': 'इमेज अपलोड करें',
        'step1_text': 'अपनी फाइलों को अपलोड क्षेत्र में खींचें और छोड़ें या चुनने के लिए क्लिक करें।',
        'step2_compress_name': 'लक्षित आकार चुनें',
        'step2_compress_text': 'एक लक्षित आकार प्रीसेट चुनें (जैसे 50KB या 100KB से कम) या एक कस्टम सीमा डालें।',
        'step2_convert_name': 'आउटपुट प्रारूप चुनें',
        'step2_convert_text': 'टैब से अपना वांछित आउटपुट प्रारूप चुनें (जैसे JPG, PNG, WEBP)।',
        'step3_name': 'आउटपुट डाउनलोड करें',
        'step3_text': 'कनवर्ट या कंप्रेस बटन पर क्लिक करें और अपनी ऑप्टिमाइज़ की गई फाइलों को तुरंत डाउनलोड करें।'
    },
    'zh': {
        'compress_title': '如何在线压缩图片',
        'convert_title': '如何在线转换图片',
        'step1_name': '上传图片',
        'step1_text': '拖放您的文件至上传区域，或点击选择按钮进行浏览。',
        'step2_compress_name': '选择目标大小',
        'step2_compress_text': '选择一个目标大小预设（如 50KB 或 100KB 以下）或输入自定义限制值。',
        'step2_convert_name': '选择输出格式',
        'step2_convert_text': '在选项卡中选择您需要的输出格式（如 JPG、PNG、WEBP）。',
        'step3_name': '下载文件',
        'step3_text': '点击转换或压缩按钮，即可立即下载优化后的文件。'
    }
}

TOOL_TRANSLATIONS = {
    'index.html': {
        'de': {
            'title': 'Kostenloser Bildkonverter Online | Fast, Secure, 100% Client-Side',
            'desc': 'Konvertieren Sie WEBP, HEIC, PNG, JPG und 1500+ Formate online. Unbegrenzte, absolut private Batch-Verarbeitung.',
            'keywords': 'bildkonverter, heic in jpg, webp in jpg, png in jpg, bilder verkleinern',
            'h1': 'Kostenloser Bildkonverter',
            'sub': 'Unser Konverter verarbeitet Ihre Bilddateien direkt in Ihrem Browser. Wir unterstützen PNG, JPG, GIF, WEBP und HEIC. Sie können Auflösung, Qualität und Dateigröße nahtlos steuern.',
            'tabs': {'image/jpeg': 'Zu JPG', 'image/png': 'Zu PNG', 'image/webp': 'Zu WEBP'},
            'article_title': 'Schnelle & sichere Stapel-Bildkonvertierung',
            'article_p1': 'Willkommen beim ultimativen kostenlosen Online-Bildkonverter. Die Optimierung Ihrer Bilder ist entscheidend für Ladezeiten von Websites, Speichereffizienz und den Erhalt der Bildqualität.',
            'article_p2': 'Im Gegensatz zu anderen Cloud-Diensten werden bei unserem Tool alle Bilder vollständig lokal auf Ihrem Gerät verarbeitet. Kein einziges Byte wird über das Internet hochgeladen.',
            'faq_q1': 'Ist dieser Online-Bildkonverter kostenlos?',
            'faq_a1': 'Ja, unser Tool ist zu 100 % kostenlos, ohne Dateigrößenbeschränkungen oder Wasserzeichen.',
            'faq_q2': 'Sind meine Bilder sicher?',
            'faq_a2': 'Absolut. Alles läuft lokal in Ihrem Browser ab. Ihre Bilder werden niemals auf Server hochgeladen.',
            'faq_q3': 'Welche Bildformate werden unterstützt?',
            'faq_a3': 'Wir unterstützen alle gängigen Formate wie JPG, PNG, WEBP und HEIC.'
        },
        'es': {
            'title': 'Convertidor de Imágenes Gratis Online | Rápido, Seguro, Client-Side',
            'desc': 'Convierte WEBP, HEIC, PNG, JPG y más formatos online. Conversión por lotes gratuita y totalmente privada sin subir archivos.',
            'keywords': 'convertidor de imagenes, heic a jpg, webp a jpg, png a jpg, cambiar tamaño imagen',
            'h1': 'Convertidor de Imágenes',
            'sub': 'Nuestro convertidor procesa tus archivos directamente en tu navegador. Soportamos PNG, JPG, GIF, WEBP y HEIC. Puedes controlar la resolución, calidad y tamaño.',
            'tabs': {'image/jpeg': 'A JPG', 'image/png': 'A PNG', 'image/webp': 'A WEBP'},
            'article_title': 'Conversión por lotes rápida y segura',
            'article_p1': 'Optimizar tus imágenes es vital para el rendimiento web, el almacenamiento y la calidad. Nuestro convertidor te ayuda a transformar imágenes al instante.',
            'article_p2': 'A diferencia de otros servicios en la nube, todo se ejecuta en tu propio navegador web, garantizando privacidad absoluta.',
            'faq_q1': '¿Es este convertidor completamente gratis?',
            'faq_a1': 'Sí, es 100% gratuito, sin límites diarios y sin marcas de agua.',
            'faq_q2': '¿Están seguras mis fotos?',
            'faq_a2': 'Totalmente. Al ser procesadas en tu propio dispositivo, las imágenes nunca se transmiten por la red.',
            'faq_q3': '¿Qué formatos son compatibles?',
            'faq_a3': 'Soportamos todos los formatos populares incluyendo JPG, PNG, WEBP y HEIC.'
        },
        'fr': {
            'title': 'Convertisseur d\'Images Gratuit en Ligne | Rapide, Sécurisé',
            'desc': 'Convertissez WEBP, HEIC, PNG, JPG et plus en ligne. Traitement par lots gratuit et entièrement privé sans envoi de fichiers.',
            'keywords': 'convertisseur image, convertir heic en jpg, convertir webp en jpg, png en jpg',
            'h1': 'Convertisseur d\'Images',
            'sub': 'Notre convertisseur traite vos images directement dans votre navigateur. Nous prenons en charge PNG, JPG, GIF, WEBP et HEIC. Ajustez la résolution, la qualité et la taille.',
            'tabs': {'image/jpeg': 'En JPG', 'image/png': 'En PNG', 'image/webp': 'En WEBP'},
            'article_title': 'Conversion d\'images par lots rapide et sécurisée',
            'article_p1': 'L\'optimisation de vos images est cruciale pour la vitesse de votre site et le stockage. Changez de format en un clic.',
            'article_p2': 'Vos images sont traitées localement par votre navigateur web. Aucun fichier n\'est téléchargé sur des serveurs externes.',
            'faq_q1': 'Ce convertisseur d\'images en ligne est-il gratuit ?',
            'faq_a1': 'Oui, notre outil est 100 % gratuit sans limite de taille ni filigranes.',
            'faq_q2': 'Mes images sont-elles en sécurité ?',
            'faq_a2': 'Absolument. Vos photos restent sur votre appareil et sont traitées en local.',
            'faq_q3': 'Quels formats d\'images sont pris en charge ?',
            'faq_a3': 'Nous supportons de nombreux formats populaires, dont JPG, PNG, WEBP et HEIC.'
        },
        'hi': {
            'title': 'मुफ्त ऑनलाइन इमेज कनवर्टर | सुरक्षित और तेज',
            'desc': 'WEBP, HEIC, PNG, JPG प्रारूपों को ऑनलाइन बदलें। पूरी तरह से निजी बैच प्रसंस्करण, फाइलें आपके डिवाइस पर ही रहेंगी।',
            'keywords': 'इमेज कनवर्टर, हीक से जेपीजी, वेबपी से जेपीजी, पीएनजी से जेपीजी',
            'h1': 'इमेज कनवर्टर',
            'sub': 'हमारा कनवर्टर आपके ब्राउज़र में सीधे फाइलों को प्रोसेस करता है। हम PNG, JPG, GIF, WEBP और HEIC को सपोर्ट करते हैं। आप रेजोल्यूशन और क्वालिटी को कंट्रोल कर सकते हैं।',
            'tabs': {'image/jpeg': 'JPG में', 'image/png': 'PNG में', 'image/webp': 'WEBP में'},
            'article_title': 'तेज और सुरक्षित बैच इमेज कनवर्टर',
            'article_p1': 'वेबसाइट के बेहतर प्रदर्शन और फाइल साइज को छोटा करने के लिए इमेज ऑप्टिमाइज़ करना बहुत जरूरी है।',
            'article_p2': 'अन्य टूल्स के विपरीत, यह कनवर्टर क्लाइंट-साइड तकनीक का उपयोग करता है। आपकी फाइलें कभी भी हमारे सर्वर पर अपलोड नहीं होती हैं।',
            'faq_q1': 'क्या यह इमेज कनवर्टर पूरी तरह से मुफ्त है?',
            'faq_a1': 'हाँ, हमारा कनवर्टर बिना किसी फाइल साइज सीमा या वॉटरमार्क के 100% मुफ्त है।',
            'faq_q2': 'क्या मेरी तस्वीरें सुरक्षित हैं?',
            'faq_a2': 'बिल्कुल। सारी प्रक्रिया आपके स्थानीय ब्राउज़र में होती है, जिससे डेटा पूरी तरह सुरक्षित रहता है।',
            'faq_q3': 'कौन-से इमेज प्रारूप समर्थित हैं?',
            'faq_a3': 'हम JPG, PNG, WEBP और HEIC जैसे सभी लोकप्रिय प्रारूपों का समर्थन करते हैं।'
        },
        'zh': {
            'title': '免费在线图片转换器 | 快速、安全、免上传',
            'desc': '在线批量转换 WEBP、HEIC、PNG、JPG 等格式。免费且完全私密，您的文件永远不会离开您的设备。',
            'keywords': '图片转换器, heic转jpg, webp转jpg, png转jpg, 批量图片转换',
            'h1': '图片转换器',
            'sub': '我们的转换器直接在您的浏览器中处理您的图像文件。支持 PNG、JPG、GIF、WEBP 和 HEIC。您可以无缝控制图像的分辨率、质量和文件大小。',
            'tabs': {'image/jpeg': '转为 JPG', 'image/png': '转为 PNG', 'image/webp': '转为 WEBP'},
            'article_title': '快速、安全的批量图片转换器',
            'article_p1': '在当今的数字环境中，优化图像对于网站加载性能、存储效率至关重要。',
            'article_p2': '与传统云端服务不同，本工具采用 HTML5 本地渲染，数据零上传，保证隐私安全。',
            'faq_q1': '这个图片转换器是完全免费的吗？',
            'faq_a1': '是的，我们的转换器 100% 免费，没有文件大小限制，没有每日额度，也没有水印。',
            'faq_q2': '我的图片安全吗？',
            'faq_a2': '绝对安全。所有的处理都发生在您的浏览器中。我们绝不会上传或存储您的任何图像。',
            'faq_q3': '支持哪些图片格式？',
            'faq_a3': '我们支持包括 JPG、PNG、WEBP 和 HEIC 等在内的多种主流图片格式。'
        }
    },
    'compress-image': {
        'de': {
            'title': 'Bilder online komprimieren | Image Converter',
            'desc': 'Komprimieren Sie Bilder online kostenlos. Qualität und Auflösung anpassen, Dateigröße reduzieren.',
            'keywords': 'bilder komprimieren, bildgröße reduzieren, bilder verkleinern',
            'h1': 'Bilder online komprimieren',
            'tabs': 'Bilder komprimieren',
            'article_title': 'So komprimieren Sie Bilder sicher online',
            'article_p1': 'Die Komprimierung von Bildern ist entscheidend für schnelle Ladezeiten von Websites und effiziente Speichernutzung. Unsere App bietet unbegrenzte, sichere Komprimierung direkt in Ihrem Browser.',
            'article_p2': 'Dank modernster Client-Side-Technologie verlassen Ihre Bilder nie Ihr Gerät. Es ist 100 % sicher und schützt Ihre Privatsphäre.',
            'faq_q1': 'Ist dieser Bildkompressor kostenlos?',
            'faq_a1': 'Ja, die Nutzung ist absolut kostenlos und ohne Einschränkungen.',
            'faq_q2': 'Werden meine Bilder auf Server hochgeladen?',
            'faq_a2': 'Nein. Alles wird lokal in Ihrem Browser verarbeitet. Ihre Privatsphäre bleibt geschützt.'
        },
        'es': {
            'title': 'Comprimir imágenes online gratis | Image Converter',
            'desc': 'Comprime imágenes online gratis al instante. Reduce el tamaño de tus fotos PNG, JPG y WEBP con calidad óptima.',
            'keywords': 'comprimir imagen, reducir tamaño de imagen, optimizar imagen',
            'h1': 'Comprimir imágenes online',
            'tabs': 'Comprimir',
            'article_title': 'Cómo comprimir imágenes de forma segura',
            'article_p1': 'Optimizar tus imágenes es vital para la velocidad de la web. Nuestra herramienta te permite reducir el tamaño de tus fotos en segundos sin perder calidad visual.',
            'article_p2': 'Todo se procesa en tu propio dispositivo, lo que significa que tus fotos nunca se envían a ningún servidor externo.',
            'faq_q1': '¿Es gratis este compresor?',
            'faq_a1': 'Sí, es 100% gratuito y no tiene límites de uso ni marcas de agua.',
            'faq_q2': '¿Es seguro para mis fotos privadas?',
            'faq_a2': 'Absolutamente seguro. Al ser 100% del lado del cliente, tus imágenes no se suben a ningún sitio.'
        },
        'fr': {
            'title': 'Compresser des Images en Ligne Gratuitement | Image Converter',
            'desc': 'Compressez vos images en ligne gratuitement. Réduisez le poids de vos fichiers PNG, JPG, WEBP tout en préservant la qualité.',
            'keywords': 'compresser image, réduire taille image, optimiser fichier image',
            'h1': 'Compresser des Images en Ligne',
            'tabs': 'Compresser',
            'article_title': 'Comment compresser vos images en toute sécurité',
            'article_p1': 'La compression des images est essentielle pour accélérer le chargement des pages web. Notre outil vous permet de réduire le poids des fichiers en quelques clics.',
            'article_p2': 'Grâce au traitement 100% local, vos fichiers restent strictement sur votre machine.',
            'faq_q1': 'La compression est-elle gratuite ?',
            'faq_a1': 'Oui, c\'est entièrement gratuit, illimité et sans filigranes.',
            'faq_q2': 'Mes données sont-elles protégées ?',
            'faq_a2': 'Tout à fait. Les images ne quittent jamais votre navigateur.'
        },
        'hi': {
            'title': 'ऑनलाइन इमेज कंप्रेस करें | फ़ाइल का आकार छोटा करें',
            'desc': 'मुफ्त में छवियों को ऑनलाइन कंप्रेस करें। गुणवत्ता को बनाए रखते हुए पीएनजी, जेपीजी और वेबपी फाइलों को छोटा करें।',
            'keywords': 'इमेज कंप्रेस करें, फोटो का साइज छोटा करें, कंप्रेस फोटो',
            'h1': 'ऑनलाइन इमेज कंप्रेस करें',
            'tabs': 'कंप्रेस करें',
            'article_title': 'सुरक्षित रूप से इमेज साइज कैसे कम करें',
            'article_p1': 'वेबसाइट की गति बढ़ाने के लिए छवियों का आकार छोटा करना बहुत आवश्यक है।',
            'article_p2': 'यह टूल पूरी तरह से आपके ब्राउज़र में काम करता है। कोई फ़ाइल अपलोड नहीं होती है।',
            'faq_q1': 'क्या इमेज कंप्रेस करना मुफ्त है?',
            'faq_a1': 'हाँ, यह बिना किसी सीमा के 100% मुफ्त है।',
            'faq_q2': 'क्या मेरी फ़ाइलें सुरक्षित रहेंगी?',
            'faq_a2': 'हाँ, सब कुछ आपके स्थानीय डिवाइस पर प्रोसेस होता है।'
        },
        'zh': {
            'title': '在线图片压缩 | 无损调整大小',
            'desc': '免费在线压缩 PNG、JPG 和 WEBP 图片。在保持清晰度的同时，显著减小图片文件体积。',
            'keywords': '图片压缩, 减小图片大小, 无损压缩图片',
            'h1': '在线图片压缩',
            'tabs': '图片压缩',
            'article_title': '如何在本地安全压缩图片',
            'article_p1': '压缩图片可以提高网页加载速度并节省手机存储空间。我们的工具提供极速且私密的本地压缩。',
            'article_p2': '使用先进的浏览器渲染技术，图片无需传输至外部云端即可快速完成体积缩减。',
            'faq_q1': '这个压缩工具是免费的吗？',
            'faq_a1': '是的，完全免费，且没有任何水印和大小限制。',
            'faq_q2': '压缩后会影响清晰度吗？',
            'faq_a2': '您可以通过滑动滑块自由控制质量，以取得最佳的文件大小与清晰度平衡。'
        }
    },
    'compress-image-to-100kb': {
        'de': {
            'title': 'Bild auf 100KB komprimieren | Image Converter',
            'desc': 'Komprimieren Sie Bilder kostenlos online auf unter 100KB. Optimieren Sie JPG, PNG und WEBP.',
            'keywords': 'bild auf 100kb komprimieren, bilder verkleinern 100kb',
            'h1': 'Bild auf 100KB komprimieren',
            'tabs': 'Auf 100KB komprimieren',
            'article_title': 'Bilder verlustfrei auf unter 100KB verkleinern',
            'article_p1': 'Egal ob für Web-Formulare oder Upload-Portale: Oft dürfen Bilder maximal 100KB groß sein. Unser smarter Kompressor löst dieses Problem perfekt.',
            'article_p2': 'Durch die lokale Ausführung bleiben Ihre sensiblen Daten jederzeit vor Dritten geschützt.',
            'faq_q1': 'Kann ich jedes Bild auf 100KB komprimieren?',
            'faq_a1': 'Ja, das System passt die Dimensionen und Qualität automatisch an, um die 100KB-Grenze einzuhalten.',
            'faq_q2': 'Ist der Konverter sicher?',
            'faq_a2': 'Ja, alle Operationen laufen zu 100% lokal in Ihrem Webbrowser.'
        },
        'es': {
            'title': 'Comprimir imagen a 100KB | Image Converter',
            'desc': 'Comprime tus imágenes a menos de 100KB gratis. Soporta optimización local de JPG, PNG y WEBP.',
            'keywords': 'comprimir imagen a 100kb, reducir foto a 100kb',
            'h1': 'Comprimir imagen a 100KB',
            'tabs': 'Comprimir a 100KB',
            'article_title': 'Cómo reducir tus imágenes a menos de 100KB',
            'article_p1': 'Muchos sitios oficiales y portales requieren archivos de menos de 100KB. Nuestra herramienta automatiza el proceso para ajustar el tamaño con la mejor calidad.',
            'article_p2': 'Tus fotos privadas nunca viajan por internet, lo que garantiza el máximo nivel de seguridad.',
            'faq_q1': '¿Funciona con fotos tomadas desde el móvil?',
            'faq_a1': 'Sí, puedes arrastrar fotos de gran tamaño y el algoritmo las reducirá por debajo de los 100KB.',
            'faq_q2': '¿Es seguro?',
            'faq_a2': 'Sí, es 100% privado y seguro, del lado del cliente.'
        },
        'fr': {
            'title': 'Compresser Image à 100KB | Image Converter',
            'desc': 'Compressez vos images à moins de 100KB gratuitement en ligne. Optimisation locale et ultra-rapide.',
            'keywords': 'compresser image 100kb, réduire taille photo 100kb',
            'h1': 'Compresser Image à 100KB',
            'tabs': 'Compresser à 100KB',
            'article_title': 'Comment optimiser des photos sous le seuil de 100KB',
            'article_p1': 'Notre optimiseur calcule précisément les paramètres de qualité pour réduire vos fichiers sans dépasser la limite de 100KB.',
            'article_p2': 'Tout le processus est client-side, gardant vos documents personnels à l\'abri.',
            'faq_q1': 'Comment le système atteint-il 100KB ?',
            'faq_a1': 'Il ajuste de manière itérative la qualité de compression pour trouver le ratio parfait.',
            'faq_q2': 'Y a-t-il des limites de fichiers ?',
            'faq_a2': 'Aucune limite, traitez autant de fichiers que nécessaire.'
        },
        'hi': {
            'title': 'इमेज साइज 100KB तक कम करें | ऑनलाइन कंप्रेसर',
            'desc': 'अपनी फोटो को मुफ्त में 100KB से कम आकार में बदलें। जेपीजी, पीएनजी और वेबपी ऑप्टिमाइज़र।',
            'keywords': 'फोटो साइज 100kb करें, 100kb में इमेज कंप्रेस करें',
            'h1': 'इमेज साइज 100KB तक कम करें',
            'tabs': '100KB तक कंप्रेस करें',
            'article_title': 'फोटो का आकार 100KB से कम कैसे करें',
            'article_p1': 'कई सरकारी वेबसाइटों पर केवल 100KB से कम की फोटो ही स्वीकार की जाती है।',
            'article_p2': 'यह टूल स्वचालित रूप से आपकी फोटो को 100KB के अंदर सटीक आकार में सहेजता है।',
            'faq_q1': 'क्या फोटो की गुणवत्ता खराब होगी?',
            'faq_a1': 'नहीं, हमारा एल्गोरिथ्म पिक्सेल की स्पष्टता बनाए रखते हुए फाइल का आकार छोटा करता है।',
            'faq_q2': 'क्या यह सुरक्षित है?',
            'faq_a2': 'हाँ, आपकी तस्वीरें पूरी तरह से निजी और सुरक्षित हैं।'
        },
        'zh': {
            'title': '图片压缩至 100KB | 在线本地优化器',
            'desc': '免费在线将图片压缩到 100KB 以下。支持 JPG、PNG 和 WEBP 格式批量本地优化。',
            'keywords': '图片压缩至100kb, 缩小图片到100kb',
            'h1': '图片压缩至 100KB',
            'tabs': '压缩至 100KB',
            'article_title': '如何将图片无损缩减至 100KB 以内',
            'article_p1': '许多在线报考或证件提交系统限制图片在 100KB 以下。该工具会自动调整画质参数以完美适配此要求。',
            'article_p2': '纯本地渲染运行，无需等待云端队列，且绝对保护个人敏感信息隐私。',
            'faq_q1': '可以批量压缩多张图片吗？',
            'faq_a1': '可以，一次性拖入多张图片，系统会全部压缩并提供下载。',
            'faq_q2': '支持苹果的 HEIC 格式吗？',
            'faq_a2': '支持，HEIC 图片会在浏览器中自动转换为符合 100KB 限制的 JPG 格式。'
        }
    },
    'compress-image-to-50kb': {
        'de': {
            'title': 'Bild auf 50KB komprimieren | Image Converter',
            'desc': 'Bilder kostenlos online auf unter 50KB komprimieren. Extrem effizient und 100% privat.',
            'keywords': 'bild auf 50kb komprimieren, bilder verkleinern 50kb',
            'h1': 'Bild auf 50KB komprimieren',
            'tabs': 'Auf 50KB komprimieren',
            'article_title': 'Wie man Bilder extrem auf unter 50KB komprimiert',
            'article_p1': 'Wenn Sie sehr strenge Upload-Limits einhalten müssen, ist die Reduzierung auf 50KB die ideale Lösung.',
            'article_p2': 'Dank Client-Side-Technologie läuft das Ganze blitzschnell und sicher direkt auf Ihrem Computer.',
            'faq_q1': 'Bleibt das Bild erkennbar?',
            'faq_a1': 'Ja, der Algorithmus sorgt dafür, dass wichtige Details trotz der geringen Dateigröße erhalten bleiben.',
            'faq_q2': 'Werden Daten hochgeladen?',
            'faq_a2': 'Nein, es findet kein Datentransfer statt.'
        },
        'es': {
            'title': 'Comprimir imagen a 50KB | Image Converter',
            'desc': 'Comprime imágenes a menos de 50KB online. Rápido, gratuito y con máxima privacidad local.',
            'keywords': 'comprimir imagen a 50kb, reducir foto a 50kb',
            'h1': 'Comprimir imagen a 50KB',
            'tabs': 'Comprimir a 50KB',
            'article_title': 'Optimizar fotos por debajo de 50KB',
            'article_p1': 'Para portales de empleo, perfiles oficiales y firmas de correo, 50KB suele ser el tamaño máximo. Esta herramienta te permite conseguirlo al instante.',
            'article_p2': 'Al realizarse de forma local, puedes procesar documentos confidenciales con total confianza.',
            'faq_q1': '¿Puedo elegir el formato final?',
            'faq_a1': 'Sí, la herramienta mantendrá el formato original o lo optimizará para alcanzar la meta de 50KB.',
            'faq_q2': '¿Es seguro?',
            'faq_a2': 'Absolutamente, funciona en tu navegador sin subir archivos.'
        },
        'fr': {
            'title': 'Compresser Image à 50KB | Image Converter',
            'desc': 'Réduisez vos photos sous les 50KB gratuitement en ligne. Sécurisé, rapide et 100% côté client.',
            'keywords': 'compresser image 50kb, réduire photo 50kb',
            'h1': 'Compresser Image à 50KB',
            'tabs': 'Compresser à 50KB',
            'article_title': 'Réduire efficacement les photos sous 50KB',
            'article_p1': 'Atteindre un fichier de moins de 50KB nécessite un compresseur performant. Notre algorithme réduit l\'encombrement sans détruire l\'image.',
            'article_p2': 'Toutes les manipulations s\'effectuent directement dans le navigateur.',
            'faq_q1': 'Comment le convertisseur fonctionne-t-il sans serveur ?',
            'faq_a1': 'Il exploite les API Canvas HTML5 modernes pour compresser localement.',
            'faq_q2': 'Est-ce payant ?',
            'faq_a2': 'Non, le service est totalement gratuit.'
        },
        'hi': {
            'title': 'फोटो साइज 50KB तक कम करें | ऑनलाइन टूल',
            'desc': 'अपनी फोटो को मुफ्त में 50KB से कम आकार में बदलें। 100% सुरक्षित और स्थानीय रूपांतरण।',
            'keywords': 'फोटो साइज 50kb करें, 50kb में इमेज कंप्रेस करें',
            'h1': 'फोटो साइज 50KB तक कम करें',
            'tabs': '50KB तक कंप्रेस करें',
            'article_title': 'अपनी इमेज का साइज 50KB के अंदर कैसे लाएं',
            'article_p1': 'विभिन्न प्रतियोगी परीक्षाओं के फॉर्म भरने के लिए फोटो को 50KB के अंतर्गत लाना जरूरी होता है।',
            'article_p2': 'यह टूल पिक्सेल के नुकसान को कम करते हुए आकार को बहुत छोटा कर देता है।',
            'faq_q1': 'क्या यह टूल बिल्कुल मुफ्त है?',
            'faq_a1': 'हाँ, आप बिना किसी शुल्क के असीमित बार इसका उपयोग कर सकते हैं।',
            'faq_q2': 'क्या तस्वीरें लीक हो सकती हैं?',
            'faq_a2': 'नहीं, फ़ाइलें कभी भी सर्वर पर अपलोड नहीं की जाती हैं।'
        },
        'zh': {
            'title': '图片压缩至 50KB | 极速证件照压缩',
            'desc': '免费在线将图片压缩至 50KB 以下。最适合公考、考研或社保照片批量快速本地压缩。',
            'keywords': '图片压缩至50kb, 证件照压缩50kb',
            'h1': '图片压缩至 50KB',
            'tabs': '压缩至 50KB',
            'article_title': '证件照快速缩减到 50KB 以内的方法',
            'article_p1': '许多政务平台或考试报名系统的头像图片最大不能超过 50KB。这是专为此类场景优化的工具。',
            'article_p2': '所有计算均在您的手机或电脑本地安全完成，绝对不用担心照片外泄。',
            'faq_q1': '可以调整输出图片的尺寸吗？',
            'faq_a1': '如果需要更精确修改，可以使用我们的“调整大小(Resize)”工具。',
            'faq_q2': '图片会变模糊吗？',
            'faq_a2': '我们会采用智能的高清压缩算法，使图片在 50KB 限制下依然保持清晰可读。'
        }
    },
    'heic-to-jpg': {
        'de': {
            'title': 'HEIC in JPG Konverter | Kostenlos & Sicher',
            'desc': 'Konvertieren Sie HEIC-Bilder von Ihrem iPhone online in JPG. 100% sicher und clientseitig.',
            'keywords': 'heic in jpg, heic to jpg, iphone foto konvertieren',
            'h1': 'HEIC in JPG Konverter',
            'tabs': 'HEIC in JPG konvertieren',
            'article_title': 'iPhone HEIC-Fotos kostenlos in JPG umwandeln',
            'article_p1': 'Apple verwendet das HEIC-Format für Fotos auf dem iPhone, um Speicherplatz zu sparen. Viele Windows- und Android-Geräte können diese Dateien jedoch nicht standardmäßig öffnen. Unser kostenloser Konverter löst dieses Kompatibilitätsproblem sofort.',
            'article_p2': 'Alles läuft lokal ab — die sensiblen Originalfotos verlassen zu keinem Zeitpunkt Ihr Gerät.',
            'faq_q1': 'Warum kann ich HEIC-Bilder nicht überall öffnen?',
            'faq_a1': 'HEIC ist ein neueres Format von Apple und wird von manchen älteren Betriebssystemen und Webseiten nicht unterstützt.',
            'faq_q2': 'Bleiben Live-Fotos oder Metadaten erhalten?',
            'faq_a2': 'Der Konverter extrahiert das hochauflösende Standbild und speichert es als standardkompatibles JPG.'
        },
        'es': {
            'title': 'Convertidor HEIC a JPG Gratis | Image Converter',
            'desc': 'Convierte tus fotos HEIC de iPhone a JPG online. 100% privado y seguro, renderizado local instantáneo.',
            'keywords': 'heic a jpg, convertir heic a jpg, fotos de iphone a jpg',
            'h1': 'Convertidor HEIC a JPG',
            'tabs': 'Convertir a JPG',
            'article_title': 'Cómo convertir archivos HEIC de iPhone a JPG gratis',
            'article_p1': 'Los dispositivos Apple guardan las fotos en formato HEIC de forma predeterminada para ahorrar espacio. Sin embargo, este formato tiene poca compatibilidad en Windows y Android. Con este convertidor local, puedes convertirlos a JPG al instante.',
            'article_p2': 'Las imágenes no se suben a la web, manteniendo la privacidad absoluta de tu galería personal.',
            'faq_q1': '¿Se pierde calidad al convertir HEIC a JPG?',
            'faq_a1': 'Nuestra herramienta utiliza renderizado de alta calidad para conservar toda la fidelidad visual posible.',
            'faq_q2': '¿Es seguro?',
            'faq_a2': 'Totalmente seguro, todo se procesa en tu propio dispositivo.'
        },
        'fr': {
            'title': 'Convertisseur HEIC en JPG Gratuit | Image Converter',
            'desc': 'Convertissez vos photos HEIC iPhone en JPG en ligne. 100% privé, traitement en local ultra-rapide.',
            'keywords': 'heic en jpg, convertir heic en jpg, photo iphone en jpg',
            'h1': 'Convertisseur HEIC en JPG',
            'tabs': 'Convertir en JPG',
            'article_title': 'Convertir les photos HEIC d\'iPhone vers JPG sans risque',
            'article_p1': 'Le format HEIC d\'Apple offre une excellente compression mais pose des problèmes de compatibilité majeurs. Notre convertisseur transforme vos fichiers en JPG standards utilisables partout.',
            'article_p2': 'Grâce au traitement HTML5 local, vos photos privées restent sur votre appareil.',
            'faq_q1': 'Puis-je convertir plusieurs photos HEIC à la fois ?',
            'faq_a1': 'Oui, vous pouvez faire glisser tout un lot de photos HEIC et les convertir simultanément.',
            'faq_q2': 'Est-ce que ça fonctionne sur mobile ?',
            'faq_a2': 'Parfaitement. Cela fonctionne sur iPhone, iPad, Android et ordinateurs de bureau.'
        },
        'hi': {
            'title': 'HEIC से JPG कनवर्टर | iPhone फोटो को JPG में बदलें',
            'desc': 'iPhone की HEIC फोटो को आसानी से JPG में बदलें। 100% सुरक्षित और तेज ऑफलाइन ब्राउज़र कनवर्टर।',
            'keywords': 'हीक से जेपीजी, heic to jpg, आईफोन फोटो कनवर्टर',
            'h1': 'HEIC से JPG कनवर्टर',
            'tabs': 'JPG में बदलें',
            'article_title': 'HEIC फाइलों को JPG में क्यों कनवर्ट करें',
            'article_p1': 'Apple डिवाइस स्टोरेज बचाने के लिए HEIC फॉर्मेट का इस्तेमाल करते हैं, लेकिन विंडोज और एंड्रॉइड डिवाइस पर ये फाइलें आसानी से नहीं खुलती हैं।',
            'article_p2': 'यह मुफ्त टूल आपकी तस्वीरों को बिना सर्वर पर अपलोड किए तुरंत JPG में बदल देता है।',
            'faq_q1': 'क्या यह टूल हीक फाइलों की गुणवत्ता बनाए रखेगा?',
            'faq_a1': 'हाँ, यह बिना किसी गुणवत्ता हानि के उच्च-रिज़ॉल्यूशन स्टैंड-अलोन JPG बनाता है।',
            'faq_q2': 'क्या मैं एक साथ कई फाइलें बदल सकता हूँ?',
            'faq_a2': 'हाँ, बैच रूपांतरण पूरी तरह से समर्थित है।'
        },
        'zh': {
            'title': 'HEIC 转 JPG 转换器 | 苹果手机照片批量转换',
            'desc': '免费在线将 iPhone 的 HEIC 照片转换为 JPG 格式。100% 本地转换，保护您的隐私。',
            'keywords': 'heic转jpg, heic to jpg, 苹果照片转换器, 批量heic转换',
            'h1': 'HEIC 转 JPG 转换器',
            'tabs': '转换为 JPG',
            'article_title': '为什么及如何将苹果 HEIC 照片转换为 JPG',
            'article_p1': '苹果手机默认使用 HEIC 格式以节省空间，但在 Windows 电脑或很多社交平台上无法正常显示。使用我们的转换器可快速恢复兼容性。',
            'article_p2': '我们的解码过程完全在浏览器内进行，绝对不会外泄您的个人照片资产。',
            'faq_q1': '转换速度快吗？',
            'faq_a1': '对于大部分设备，本地转换只需几毫秒。',
            'faq_q2': '转换需要安装插件吗？',
            'faq_a2': '不需要，直接在浏览器里打开网页即可开箱即用。'
        }
    },
    'jpeg-to-webp': {
        'de': {
            'title': 'JPEG in WebP Konverter | Image Converter',
            'desc': 'Konvertieren Sie JPEG in WebP für schnellere Ladezeiten von Websites.',
            'keywords': 'jpeg in webp, jpeg to webp, webp konverter',
            'h1': 'JPEG in WebP Konverter',
            'tabs': 'In WebP konvertieren',
            'article_title': 'JPEG in das moderne WebP-Format umwandeln',
            'article_p1': 'WebP ist das moderne Bildformat von Google, das hervorragende verlustfreie und verlustbehaftete Komprimierung für Bilder im Web bietet.',
            'article_p2': 'Alles läuft sicher lokal in Ihrem Browser ab.',
            'faq_q1': 'Unterstützt WebP Transparenz?',
            'faq_a1': 'Ja, WebP unterstützt Alpha-Transparenz wie PNG.',
            'faq_q2': 'Ist WebP mit allen Browsern kompatibel?',
            'faq_a2': 'Ja, alle modernen Browser unterstützen das WebP-Format vollständig.'
        },
        'es': {
            'title': 'Convertidor JPEG a WebP | Image Converter',
            'desc': 'Convierte JPEG a WebP online gratis. Optimiza el rendimiento de tu sitio web.',
            'keywords': 'jpeg a webp, convertir jpeg a webp, optimizar webp',
            'h1': 'Convertidor JPEG a WebP',
            'tabs': 'Convertir a WebP',
            'article_title': 'Por qué deberías convertir tus imágenes JPEG a WebP',
            'article_p1': 'El formato WebP ofrece archivos mucho más pequeños que el JPG tradicional, manteniendo la misma calidad visual, lo que acelera el tiempo de carga de tu web.',
            'article_p2': 'Nuestra herramienta realiza la conversión localmente, sin intermediarios en la nube.',
            'faq_q1': '¿Es mejor WebP que JPEG?',
            'faq_a1': 'Sí, WebP suele reducir el tamaño del archivo entre un 25% y un 35% en comparación con JPEG.',
            'faq_q2': '¿Es seguro?',
            'faq_a2': 'Totalmente seguro, sin subir imágenes a servidores.'
        },
        'fr': {
            'title': 'Convertisseur JPEG en WebP | Image Converter',
            'desc': 'Convertissez JPEG en WebP en ligne gratuitement pour améliorer le référencement web.',
            'keywords': 'jpeg en webp, convertir jpeg en webp, compression webp',
            'h1': 'Convertisseur JPEG en WebP',
            'tabs': 'Convertir en WebP',
            'article_title': 'Optimiser vos JPEG en images de nouvelle génération WebP',
            'article_p1': 'WebP réduit la taille de vos fichiers JPEG tout en conservant une excellente qualité. Idéal pour optimiser les performances SEO de votre site.',
            'article_p2': 'Traitement ultra-rapide directement dans votre navigateur.',
            'faq_q1': 'WebP est-il supporté par Google ?',
            'faq_a1': 'Oui, c\'est un format créé par Google spécialement recommandé pour les sites web.',
            'faq_q2': 'Puis-je l\'utiliser gratuitement ?',
            'faq_a2': 'Oui, le convertisseur est 100% gratuit.'
        },
        'hi': {
            'title': 'JPEG से WebP कनवर्टर | वेबसाइट इमेज ऑप्टिमाइज़र',
            'desc': 'JPEG फाइलों को आधुनिक WebP फॉर्मेट में बदलें और वेबसाइट की गति बढ़ाएं।',
            'keywords': 'जेपेग से वेबपी, jpeg to webp, वेबपी कनवर्टर',
            'h1': 'JPEG से WebP कनवर्टर',
            'tabs': 'WebP में बदलें',
            'article_title': 'JPEG को WebP में बदलने के लाभ',
            'article_p1': 'WebP फॉर्मेट साधारण JPEG की तुलना में लगभग 30% अधिक कंप्रेस प्रदान करता है, जिससे वेबसाइट तेजी से लोड होती है।',
            'article_p2': 'यह कनवर्टर सुरक्षित और 100% स्थानीय क्लाइंट-साइड रेंडरिंग का उपयोग करता है।',
            'faq_q1': 'क्या सभी ब्राउज़र वेबपी का समर्थन करते हैं?',
            'faq_a1': 'हाँ, क्रोम, सफारी, फ़ायरफ़ॉक्स सहित सभी आधुनिक ब्राउज़र इसका समर्थन करते हैं।',
            'faq_q2': 'क्या यह मुफ़्त है?',
            'faq_a2': 'हाँ, यह बिना किसी सीमा के मुफ़्त है।'
        },
        'zh': {
            'title': 'JPEG 转 WebP 转换器 | 网页速度优化',
            'desc': '免费在线将 JPEG 图片转换为下一代 WebP 格式。大幅缩减图片体积，提升网页加载速率。',
            'keywords': 'jpeg转webp, jpeg to webp, webp转换器, 网页图片优化',
            'h1': 'JPEG 转 WebP 转换器',
            'tabs': '转换为 WebP',
            'article_title': '使用 WebP 替换 JPEG 提升网站性能',
            'article_p1': 'WebP 是由谷歌开发的一种现代图像格式，专门针对网页端进行了极限体积优化。',
            'article_p2': '转换操作完全在您的本地计算设备中安全运行，数据零上传，效率飞速。',
            'faq_q1': '转换后的图片清晰度会变差吗？',
            'faq_a1': '不会，WebP 拥有极高的画质保真度，即使体积缩小清晰度也依然维持高水准。',
            'faq_q2': '转换需要多长时间？',
            'faq_a2': '瞬间完成。本地 JS 解码运行极快。'
        }
    },
    'jpg-to-avif': {
        'de': {
            'title': 'JPG in AVIF Konverter | Image Converter',
            'desc': 'Konvertieren Sie JPG in AVIF für unschlagbare Dateikomprimierung und exzellente Qualität.',
            'keywords': 'jpg in avif, avif konverter, next-gen bilder',
            'h1': 'JPG in AVIF Konverter',
            'tabs': 'In AVIF konvertieren',
            'article_title': 'Warum Sie JPG in das ultra-effiziente AVIF-Format konvertieren sollten',
            'article_p1': 'AVIF ist das modernste Bildformat, das eine noch bessere Komprimierung als WebP bietet. Es reduziert Bildgrößen dramatisch bei gleichbleibender Qualität.',
            'article_p2': 'Unsere Konvertierung schützt Ihre Daten, indem sie vollständig lokal in Ihrem Webbrowser arbeitet.',
            'faq_q1': 'Ist AVIF besser als WebP?',
            'faq_a1': 'Ja, AVIF liefert meist um 20% kleinere Dateien als WebP bei vergleichbarer Bildqualität.',
            'faq_q2': 'Ist der Service privat?',
            'faq_a2': 'Ja. Keine Bilder werden auf Server hochgeladen.'
        },
        'es': {
            'title': 'Convertidor JPG a AVIF | Image Converter',
            'desc': 'Convierte tus imágenes JPG a AVIF online gratis. Disfruta de la mejor compresión de próxima generación.',
            'keywords': 'jpg a avif, convertir jpg a avif, formato avif gratis',
            'h1': 'Convertidor JPG a AVIF',
            'tabs': 'Convertir a AVIF',
            'article_title': 'Beneficios de convertir tus imágenes JPG a AVIF',
            'article_p1': 'AVIF es el formato de imagen del futuro. Supera a WebP y JPG en términos de compresión y fidelidad, reduciendo enormemente el tamaño de las páginas web.',
            'article_p2': 'La conversión se ejecuta localmente mediante tu navegador en HTML5.',
            'faq_q1': '¿Es AVIF compatible con todos los navegadores?',
            'faq_a1': 'La gran mayoría de los navegadores modernos como Chrome, Firefox, Safari y Edge son plenamente compatibles.',
            'faq_q2': '¿Es seguro?',
            'faq_a2': '100% privado y seguro, del lado del cliente.'
        },
        'fr': {
            'title': 'Convertisseur JPG en AVIF | Image Converter',
            'desc': 'Convertissez vos images JPG en AVIF gratuitement en ligne. Format de nouvelle génération.',
            'keywords': 'jpg en avif, convertir jpg en avif, compression avif',
            'h1': 'Convertisseur JPG en AVIF',
            'tabs': 'Convertir en AVIF',
            'article_title': 'Optimiser vos JPG au format ultra-performant AVIF',
            'article_p1': 'Le format AVIF offre le meilleur ratio compression/qualité actuellement disponible sur le web, surpassant même le format WebP.',
            'article_p2': 'Vos images sont converties localement sur votre ordinateur.',
            'faq_q1': 'Qu\'est-ce que l\'AVIF ?',
            'faq_a1': 'C\'est un format ouvert basé sur le codec vidéo AV1 qui révolutionne la compression d\'image.',
            'faq_q2': 'Mes données sont-elles envoyées sur internet ?',
            'faq_a2': 'Non, aucun envoi de fichier n\'est effectué.'
        },
        'hi': {
            'title': 'JPG से AVIF कनवर्टर | नेक्स्ट-जेन इमेज कंप्रेसर',
            'desc': 'JPG को सर्वश्रेष्ठ और आधुनिक AVIF प्रारूप में बदलें। 100% सुरक्षित और स्थानीय ब्राउज़र रूपांतरण।',
            'keywords': 'जेपीजी से एवीआईएफ, jpg to avif, एवीआईएफ कनवर्टर',
            'h1': 'JPG से AVIF कनवर्टर',
            'tabs': 'AVIF में बदलें',
            'article_title': 'JPG को AVIF में क्यों कनवर्ट करें',
            'article_p1': 'AVIF आज के समय का सबसे आधुनिक और शक्तिशाली इमेज प्रारूप है, जो WebP से भी अधिक कंप्रेस प्रदान करता है।',
            'article_p2': 'यह मुफ्त टूल बिना सर्वर पर अपलोड किए सीधे आपके ब्राउज़र में रूपांतरण करता है।',
            'faq_q1': 'क्या AVIF वेबपी से बेहतर है?',
            'faq_a1': 'हाँ, AVIF समान गुणवत्ता पर 20% तक छोटा फाइल आकार प्रदान करता है।',
            'faq_q2': 'क्या यह सुरक्षित है?',
            'faq_a2': 'हाँ, डेटा लीक होने का कोई खतरा नहीं है।'
        },
        'zh': {
            'title': 'JPG 转 AVIF 转换器 | 新一代高效图片格式',
            'desc': '免费在线将 JPG 图片转换为 AVIF 格式。提供超越 WebP 的极致无损和有损压缩比。',
            'keywords': 'jpg转avif, jpg to avif, avif转换器, 新一代图片格式',
            'h1': 'JPG 转 AVIF 转换器',
            'tabs': '转换为 AVIF',
            'article_title': '为什么应该将 JPG 转换为 AVIF 格式',
            'article_p1': 'AVIF 代表了当前最先进的开源图片压缩标准，能在大幅缩小体积的同时保留令人惊叹的画面细节。',
            'article_p2': '完全基于本地设备算力解码与再编码，效率极高，绝对保障数据私密性。',
            'faq_q1': 'AVIF 的兼容性如何？',
            'faq_a1': '各大主流浏览器如 Chrome、Firefox 和 Safari 均已深度兼容并支持 AVIF 图片。',
            'faq_q2': '使用这个转换器收费吗？',
            'faq_a2': '不收费，100% 免费且不设日常限制。'
        }
    },
    'jpg-to-png': {
        'de': {
            'title': 'JPG in PNG Konverter | Verlustfrei mit Transparenz',
            'desc': 'Konvertieren Sie JPG in PNG online kostenlos. Ideal für Grafiken und Web-Assets.',
            'keywords': 'jpg in png, jpg to png, bilder umwandeln png',
            'h1': 'JPG in PNG Konverter',
            'tabs': 'In PNG konvertieren',
            'article_title': 'JPG-Bilder verlustfrei in das PNG-Format konvertieren',
            'article_p1': 'PNG ist der Standard für verlustfreie Grafiken im Web. Durch die Konvertierung wird eine weitere Qualitätsabnutzung bei zukünftigen Bearbeitungen verhindert.',
            'article_p2': 'Ihre Bilder verbleiben zu 100% lokal auf Ihrem System.',
            'faq_q1': 'Kann PNG die Bildqualität verbessern?',
            'faq_a1': 'Nein, es kann verlorene JPEG-Daten nicht zurückholen, aber es verhindert jegliche zukünftige Komprimierungsverluste.',
            'faq_q2': 'Ist der Batch-Uploader kostenlos?',
            'faq_a2': 'Absolut kostenlos und unbegrenzt.'
        },
        'es': {
            'title': 'Convertir JPG a PNG Online Gratis | Image Converter',
            'desc': 'Convierte JPG a PNG online gratis. Soporte de transparencia, 100% privado.',
            'keywords': 'convertir jpg a png, jpg a png online gratis, convertir imagen jpg a png',
            'h1': 'Convertir JPG a PNG',
            'tabs': 'Convertir a PNG',
            'article_title': 'Cómo convertir JPG a PNG online de forma segura',
            'article_p1': 'Convertir una imagen JPEG (JPG) a PNG es una de las operaciones web más comunes. Se necesita cuando quieres preservar detalles sin artefactos de compresión lossy.',
            'article_p2': 'Nuestro conversor para convertir jpg a png funciona completamente en tu navegador.',
            'faq_q1': '¿Convertir JPG a PNG mejora la calidad?',
            'faq_a1': 'No. Un PNG no puede recuperar los datos descartados por la compresión JPG, pero sí evita cualquier pérdida de calidad adicional.',
            'faq_q2': '¿Es seguro este servicio?',
            'faq_a2': 'Absolutamente. Todo se ejecuta en tu navegador. Nunca subimos tus imágenes a ningún servidor.'
        },
        'fr': {
            'title': 'Convertisseur JPG en PNG Gratuit | Image Converter',
            'desc': 'Convertissez JPG en PNG en ligne gratuitement. Idéal pour préserver la transparence.',
            'keywords': 'jpg en png, convertir jpg en png, image transparente',
            'h1': 'Convertisseur JPG en PNG',
            'tabs': 'Convertir en PNG',
            'article_title': 'Comment exporter vos fichiers JPG vers le format sans perte PNG',
            'article_p1': 'Le format PNG préserve la fidélité de chaque pixel. Utile si vous avez besoin d\'importer des graphiques dans des logiciels d\'édition.',
            'article_p2': 'Aucune donnée n\'est envoyée à l\'extérieur.',
            'faq_q1': 'Le format PNG supporte-t-il la transparence ?',
            'faq_a1': 'Oui, le canal Alpha est pleinement supporté dans toutes les variantes PNG.',
            'faq_q2': 'Combien d\'images puis-je charger ?',
            'faq_a2': 'Il n\'y a aucune restriction de volume.'
        },
        'hi': {
            'title': 'JPG से PNG कनवर्टर | पारदर्शिता के साथ दोषरहित',
            'desc': 'JPG इमेज को मुफ्त में PNG में बदलें। 100% सुरक्षित और स्थानीय रूपांतरण।',
            'keywords': 'जेपीजी से पीएनजी, jpg to png, पीएनजी कनवर्टर',
            'h1': 'JPG से PNG कनवर्टर',
            'tabs': 'PNG में बदलें',
            'article_title': 'JPG को PNG में बदलने का सही तरीका',
            'article_p1': 'PNG एक दोषरहित (lossless) प्रारूप है जो पारदर्शिता का समर्थन करता है और ग्राफिक्स के लिए उत्तम माना जाता है।',
            'article_p2': 'यह कनवर्टर 100% क्लाइंट-साइड है, जो आपकी गोपनीयता बनाए रखता है।',
            'faq_q1': 'क्या पीएनजी गुणवत्ता में सुधार करता है?',
            'faq_a1': 'नहीं, यह JPG द्वारा खोई हुई जानकारी वापस नहीं ला सकता, लेकिन आगे गुणवत्ता हानि रोकता है।',
            'faq_q2': 'क्या यह मुफ़्त है?',
            'faq_a2': 'हाँ, यह पूरी तरह से मुफ्त है।'
        },
        'zh': {
            'title': 'JPG 转 PNG 转换器 | 支持透明底色',
            'desc': '免费在线将 JPG/JPEG 转换为无损 PNG 格式。100% 安全的浏览器本地客户端转换器。',
            'keywords': 'jpg转png, jpg to png, png转换器, 透明图转换',
            'h1': 'JPG 转 PNG 转换器',
            'tabs': '转换为 PNG',
            'article_title': '如何在本地无损将 JPG 转换为 PNG',
            'article_p1': 'PNG 是一种优秀的无损图片格式，支持透明通道，是网页设计与标志素材的必备选择。',
            'article_p2': '使用基于您电脑浏览器的运行方案，图片数据永远不会离开您的本地硬盘。',
            'faq_q1': 'JPG 转换成 PNG 会增加大小吗？',
            'faq_a1': '是的，因为 PNG 是无损压缩，体积通常会比有损压缩的 JPG 大。',
            'faq_q2': '转换需要互联网连接吗？',
            'faq_a2': '页面加载完成后，断开网络连接也依然可以完全正常使用。'
        }
    },
    'photo-to-black-and-white': {
        'de': {
            'title': 'Foto in Schwarz-Weiß umwandeln | Kostenloses Tool',
            'desc': 'Wandeln Sie Ihre Farbfotos online sofort in stilvolle Graustufen-Schwarz-Weiß-Bilder um.',
            'keywords': 'foto in schwarz weiß, graustufen konverter, bilder entfärben',
            'h1': 'Foto in Schwarz-Weiß umwandeln',
            'tabs': 'In Schwarz-Weiß umwandeln',
            'article_title': 'So verleihen Sie Ihren Farbfotos einen zeitlosen Schwarz-Weiß-Look',
            'article_p1': 'Verwandeln Sie gewöhnliche Farbbilder in künstlerische Meisterwerke durch unseren lokalen Graustufenfilter.',
            'article_p2': 'Alle Anpassungen geschehen in Echtzeit direkt in Ihrem Browser.',
            'faq_q1': 'Wird das Originalbild verändert?',
            'faq_a1': 'Nein, das Original bleibt unberührt, Sie laden ein neu generiertes Graustufen-Bild herunter.',
            'faq_q2': 'Ist das Tool kostenlos?',
            'faq_a2': 'Ja, die Nutzung ist komplett kostenfrei.'
        },
        'es': {
            'title': 'Convertir foto a blanco y negro | Image Converter',
            'desc': 'Pasa tus fotos en color a blanco y negro (escala de grises) al instante. 100% gratis y privado.',
            'keywords': 'foto a blanco y negro, escala de grises online, filtro de color gratis',
            'h1': 'Convertir foto a blanco y negro',
            'tabs': 'Convertir a Blanco y Negro',
            'article_title': 'Dale un toque artístico a tus imágenes en escala de grises',
            'article_p1': 'Nuestra herramienta aplica un filtro de desaturación preciso para crear hermosos retratos e imágenes artísticas en blanco y negro de forma instantánea.',
            'article_p2': 'Tus fotos se procesan en tu ordenador localmente, garantizando total privacidad.',
            'faq_q1': '¿Puedo elegir el contraste?',
            'faq_a1': 'El filtro aplica una escala de grises estándar de alta fidelidad que equilibra luces y sombras de forma automática.',
            'faq_q2': '¿Es seguro?',
            'faq_a2': '100% privado y seguro, del lado del cliente.'
        },
        'fr': {
            'title': 'Convertir Photo en Noir et Blanc | Image Converter',
            'desc': 'Transformez vos photos couleur en noir et blanc (niveaux de gris) en ligne. 100% sécurisé.',
            'keywords': 'photo en noir et blanc, niveaux de gris en ligne, filtre photo gratuit',
            'h1': 'Convertir Photo en Noir et Blanc',
            'tabs': 'Convertir en Noir et Blanc',
            'article_title': 'Créer de superbes visuels monochromes en ligne',
            'article_p1': 'Donnez une dimension classique à vos clichés en un instant avec notre filtre monochrome intelligent.',
            'article_p2': 'Rendu direct dans votre navigateur web sans transfert réseau.',
            'faq_q1': 'Quels formats puis-je importer ?',
            'faq_a1': 'Nous prenons en charge JPG, PNG, WEBP et HEIC.',
            'faq_q2': 'Mes fichiers sont-ils stockés ?',
            'faq_a2': 'Non, aucun stockage externe n\'est utilisé.'
        },
        'hi': {
            'title': 'रंगीन फोटो को ब्लैक एंड व्हाइट में बदलें | ऑनलाइन टूल',
            'desc': 'अपनी रंगीन तस्वीरों को तुरंत सुंदर ब्लैक एंड व्हाइट (ग्रेस्केल) चित्रों में बदलें।',
            'keywords': 'फोटो ब्लैक एंड व्हाइट करें, ग्रेस्केल कनवर्टर',
            'h1': 'रंगीन फोटो को ब्लैक एंड व्हाइट में बदलें',
            'tabs': 'ब्लैक एंड व्हाइट करें',
            'article_title': 'तस्वीर को शानदार ब्लैक एंड व्हाइट लुक कैसे दें',
            'article_p1': 'कलात्मक और विंटेज लुक के लिए अपनी छवियों से रंगों को हटाकर उन्हें ग्रेस्केल में बदलें।',
            'article_p2': 'यह टूल पूरी तरह से आपके ब्राउज़र में काम करता है और फोटो की स्पष्टता बनाए रखता है।',
            'faq_q1': 'क्या यह टूल बिल्कुल मुफ़्त है?',
            'faq_a1': 'हाँ, यह 100% मुफ़्त और असीमित है।',
            'faq_q2': 'क्या फ़ाइलें लीक हो सकती हैं?',
            'faq_a2': 'नहीं, सब कुछ केवल आपके स्थानीय ब्राउज़र में होता है।'
        },
        'zh': {
            'title': '照片转黑白 | 极简灰度滤镜',
            'desc': '免费在线将您的彩色照片瞬间转换为黑白灰度图像。安全无上传，本地实时滤镜渲染。',
            'keywords': '照片转黑白, 彩色照片变黑白, 灰度图转换',
            'h1': '彩色照片转黑白',
            'tabs': '转换为黑白',
            'article_title': '如何给彩色图片赋予经典的黑白质感',
            'article_p1': '黑白照片以其独特的影调和故事感经久不衰。使用本工具，您能一键祛除色彩，生成高对比度的完美灰度图像。',
            'article_p2': '依靠浏览器本地绘图 API 渲染，绝不浪费您上传图片的网络流量，安全可靠。',
            'faq_q1': '转换速度快吗？',
            'faq_a1': '非常快，几乎在您添加图片的同时就已完成滤镜处理。',
            'faq_q2': '支持哪些格式的照片？',
            'faq_a2': '支持绝大多数主流图像，如 JPG、PNG、WEBP 和 HEIC 格式。'
        }
    },
    'png-to-avif': {
        'de': {
            'title': 'PNG in AVIF Konverter | Verlustfreie Alpha-Transparenz',
            'desc': 'Konvertieren Sie PNG in AVIF online kostenlos. Behalten Sie Transparenz bei unschlagbar kleinen Dateigrößen.',
            'keywords': 'png in avif, png to avif, avif mit transparenz',
            'h1': 'PNG in AVIF Konverter',
            'tabs': 'In AVIF konvertieren',
            'article_title': 'Verlustfreie PNG-Bilder mit Transparenz in AVIF umwandeln',
            'article_p1': 'AVIF bietet die perfekte Option, um transparentes PNG ohne nennenswerten Qualitätsverlust extrem stark zu komprimieren.',
            'article_p2': 'Komplett lokale Bearbeitung garantiert perfekten Datenschutz.',
            'faq_q1': 'Bleibt der transparente Hintergrund erhalten?',
            'faq_a1': 'Ja, AVIF unterstützt den Alpha-Kanal für transparente Bildbereiche vollständig.',
            'faq_q2': 'Ist der Service unbegrenzt kostenlos?',
            'faq_a2': 'Ja, Sie können beliebig viele Dateien konvertieren.'
        },
        'es': {
            'title': 'Convertidor PNG a AVIF | Image Converter',
            'desc': 'Convierte tus imágenes PNG transparentes a AVIF online gratis. Reduce el peso manteniendo la transparencia.',
            'keywords': 'png a avif, convertir png a avif, avif transparente',
            'h1': 'Convertidor PNG a AVIF',
            'tabs': 'Convertir a AVIF',
            'article_title': 'Por qué convertir imágenes PNG transparentes a AVIF',
            'article_p1': 'AVIF es uno de los pocos formatos modernos de nueva generación que hereda el canal alfa de transparencia de PNG pero logrando archivos hasta un 70% más pequeños.',
            'article_p2': 'Tus fotos se procesan al instante dentro de tu navegador web sin salir de tu dispositivo.',
            'faq_q1': '¿Mantiene la transparencia el formato AVIF?',
            'faq_a1': 'Sí, soporta perfectamente bordes suaves y transparencia en transparencias complejas.',
            'faq_q2': '¿Es seguro?',
            'faq_a2': 'Totalmente seguro, todo funciona localmente.'
        },
        'fr': {
            'title': 'Convertisseur PNG en AVIF | Image Converter',
            'desc': 'Convertissez vos PNG en AVIF gratuitement en ligne. Conservez la transparence avec une compression maximale.',
            'keywords': 'png en avif, convertir png en avif, avif transparent',
            'h1': 'Convertisseur PNG en AVIF',
            'tabs': 'Convertir en AVIF',
            'article_title': 'Compacter vos graphiques PNG avec la transparence au format AVIF',
            'article_p1': 'Pour optimiser vos logos et icônes transparents sur le web, la conversion PNG en AVIF est la solution technique la plus performante.',
            'article_p2': 'Pas d\'envoi externe, tout est traité par votre navigateur.',
            'faq_q1': 'Pourquoi choisir l\'AVIF plutôt que le PNG ?',
            'faq_a1': 'AVIF permet d\'alléger le poids de vos pages web tout en conservant la netteté et la transparence.',
            'faq_q2': 'Est-ce gratuit ?',
            'faq_a2': 'Oui, le service est totalement gratuit.'
        },
        'hi': {
            'title': 'PNG से AVIF कनवर्टर | पारदर्शिता बनाए रखें',
            'desc': 'पारदर्शी PNG को मुफ्त में AVIF प्रारूप में बदलें। 100% सुरक्षित और स्थानीय रूपांतरण।',
            'keywords': 'पीएनजी से एवीआईएफ, png to avif, पारदर्शी एवीआईएफ',
            'h1': 'PNG से AVIF कनवर्टर',
            'tabs': 'AVIF में बदलें',
            'article_title': 'पारदर्शी PNG को AVIF में बदलने के फायदे',
            'article_p1': 'AVIF आपके पारदर्शी चित्रों (जैसे लोगो या आइकन) को बिना गुणवत्ता खोए बेहद छोटा कर देता है।',
            'article_p2': 'यह टूल सीधे आपके ब्राउज़र में सुरक्षित और स्थानीय रूप से फाइलें बदलता है।',
            'faq_q1': 'क्या एवीआईएफ में बैकग्राउंड पारदर्शी रहेगा?',
            'faq_a1': 'हाँ, AVIF पूरी तरह से अल्फा चैनल पारदर्शिता का समर्थन करता है।',
            'faq_q2': 'क्या यह टूल मुफ़्त है?',
            'faq_a2': 'हाँ, यह पूर्णतः मुफ़्त है।'
        },
        'zh': {
            'title': 'PNG 转 AVIF 转换器 | 保留透明通道',
            'desc': '免费在线将透明 PNG 转换为无损/有损 AVIF 格式。利用下一代高压缩算法极大精简体积。',
            'keywords': 'png转avif, png to avif, 透明avif转换, 前端资源优化',
            'h1': 'PNG 转 AVIF 转换器',
            'tabs': '转换为 AVIF',
            'article_title': '如何在使用 AVIF 格式时保留 PNG 的透明背景',
            'article_p1': 'AVIF 不仅压缩率极高，而且完美支持 Alpha 透明通道，是网页设计师优化无缝拼接素材的首选。',
            'article_p2': '依靠完全运行在您电脑本地的编码引擎，无需上传图片文件，极致保障隐私安全。',
            'faq_q1': 'AVIF 支持部分透明和边缘羽化吗？',
            'faq_a1': '支持，AVIF 能够完美再现 PNG 所有的半透明效果与边缘细节。',
            'faq_q2': '我需要登录才能使用吗？',
            'faq_a2': '不需要，本站所有工具均开箱即用，无任何登录要求。'
        }
    },
    'png-to-ico': {
        'de': {
            'title': 'PNG in ICO Konverter | Kostenloser Favicon Generator',
            'desc': 'Konvertieren Sie PNG-Bilder online kostenlos in das ICO-Format. Ideal für Website-Favicons.',
            'keywords': 'png in ico, favicon generator, website icon erstellen',
            'h1': 'PNG in ICO Favicon Generator',
            'tabs': 'In ICO konvertieren',
            'article_title': 'Erstellen Sie Ihr eigenes Website-Favicon aus einem PNG-Bild',
            'article_p1': 'Ein Favicon ist das kleine Symbol, das in Browser-Tabs angezeigt wird. Unser Generator konvertiert Ihre PNGs schnell in standardisierte ICO-Dateien.',
            'article_p2': 'Dank lokaler Ausführung müssen Sie sich keine Sorgen um Urheberrechte oder Bilddiebstahl machen.',
            'faq_q1': 'Welche Größe sollte ein Favicon haben?',
            'faq_a1': 'Die empfohlene Standardgröße für klassische ICO-Dateien ist 32x32 oder 16x16 Pixel.',
            'faq_q2': 'Werden Bildhintergründe transparent gehalten?',
            'faq_a2': 'Ja, die Transparenz des Original-PNGs bleibt in der generierten ICO-Datei voll erhalten.'
        },
        'es': {
            'title': 'Convertidor PNG a ICO | Generador de Favicons Gratis',
            'desc': 'Convierte imágenes PNG a archivos ICO online gratis. Ideal para crear favicons de sitios web.',
            'keywords': 'png a ico, generador de favicons gratis, crear icono web',
            'h1': 'PNG a ICO Generador de Favicons',
            'tabs': 'Convertir a ICO',
            'article_title': 'Cómo crear un favicon profesional para tu web desde un PNG',
            'article_p1': 'El icono de pestaña (favicon) es esencial para el branding de cualquier web. Nuestra herramienta te permite rasterizar y transformar tus PNG a ICO con fondos transparentes listos para producción.',
            'article_p2': 'Todo el procesamiento de imágenes es del lado del cliente, garantizando seguridad absoluta.',
            'faq_q1': '¿Qué tamaños contiene la imagen ICO?',
            'faq_a1': 'Nuestra herramienta genera un icono optimizado de hasta 256x256 píxeles, apto para la mayoría de los navegadores.',
            'faq_q2': '¿Es seguro?',
            'faq_a2': 'Sí, el procesamiento ocurre al 100% en tu navegador.'
        },
        'fr': {
            'title': 'Convertisseur PNG en ICO | Générateur de Favicon Gratuit',
            'desc': 'Convertissez des PNG en fichiers ICO en ligne gratuitement. Parfait pour créer les favicons de sites web.',
            'keywords': 'png en ico, générateur favicon, icône site web',
            'h1': 'PNG en ICO Générateur de Favicon',
            'tabs': 'Convertir en ICO',
            'article_title': 'Créer facilement un favicon à partir d\'un fichier PNG',
            'article_p1': 'Pour que votre site web dispose d\'un favicon propre visible dans les onglets, convertissez simplement votre logo PNG au format ICO.',
            'article_p2': 'Conversion ultra-sécurisée locale sans aucun intermédiaire cloud.',
            'faq_q1': 'La transparence est-elle conservée ?',
            'faq_a1': 'Oui, le canal transparent du fichier PNG d\'origine est parfaitement préservé.',
            'faq_q2': 'Puis-je l\'utiliser pour des projets commerciaux ?',
            'faq_a2': 'Oui, l\'outil est libre d\'utilisation sans aucune restriction.'
        },
        'hi': {
            'title': 'PNG से ICO फेविकॉन जनरेटर | मुफ़्त ऑनलाइन कनवर्टर',
            'desc': 'PNG इमेज को वेबसाइट फेविकॉन (ICO) में बदलें। 100% सुरक्षित और स्थानीय फेविकॉन मेकर।',
            'keywords': 'पीएनजी से आईसीओ, favicon generator, फेविकॉन बनाएं',
            'h1': 'PNG से ICO फेविकॉन जनरेटर',
            'tabs': 'ICO में बदलें',
            'article_title': 'वेबसाइट के लिए सुंदर फेविकॉन कैसे बनाएं',
            'article_p1': 'फेविकॉन वह छोटा आइकन होता है जो ब्राउज़र टैब में दिखाई देता है। आप अपने लोगो (PNG) को आसानी से ICO फॉर्मेट में कनवर्ट कर सकते हैं।',
            'article_p2': 'यह टूल बिना सर्वर पर अपलोड किए पूरी सुरक्षा के साथ स्थानीय स्तर पर फेविकॉन बनाता है।',
            'faq_q1': 'क्या फेविकॉन पारदर्शी पृष्ठभूमि का समर्थन करता है?',
            'faq_a1': 'हाँ, यदि मूल PNG पारदर्शी है, तो बनने वाली ICO फ़ाइल भी पारदर्शी होगी।',
            'faq_q2': 'क्या यह मुफ़्त है?',
            'faq_a2': 'हाँ, यह 100% मुफ़्त है।'
        },
        'zh': {
            'title': 'PNG 转 ICO 转换器 | 免费在线 Favicon 生成器',
            'desc': '免费在线将 PNG 图片转换为 ICO 格式。完美制作高保真网页 Favicon 图标。',
            'keywords': 'png转ico, favicon生成器, 网页图标制作',
            'h1': 'PNG 转 ICO 网页图标生成器',
            'tabs': '转换为 ICO',
            'article_title': '如何利用 PNG 轻松制作高保真网页 Favicon 图标',
            'article_p1': '网页小图标（Favicon）是品牌形象的重要体现。我们的在线图标生成器可以将任何透明 PNG 快速转为标准 ICO 文件。',
            'article_p2': '采用端到端的纯本地计算模式，不涉及网络数据发送，绝对保护您的图片创意设计隐私。',
            'faq_q1': '生成的 ICO 图标最大尺寸是多少？',
            'faq_a1': '支持生成 256x256 等多种适配现代浏览器的标准 ICO 规格。',
            'faq_q2': '是否支持保留透明度？',
            'faq_a2': '支持，原 PNG 图的透明和半透明细节在 ICO 中将被完美保留。'
        }
    },
    'png-to-jpg': {
        'de': {
            'title': 'PNG in JPG Konverter | Schnelle Konvertierung',
            'desc': 'Konvertieren Sie PNG online kostenlos in JPG. Rastert Transparenz auf einen festen weißen Hintergrund.',
            'keywords': 'png in jpg, png to jpg, bilder konvertieren',
            'h1': 'PNG in JPG Konverter',
            'tabs': 'In JPG konvertieren',
            'article_title': 'PNG-Bilder schnell und einfach in JPG umwandeln',
            'article_p1': 'PNG-Dateien sind oft sehr groß. Wenn Sie keine Transparenz benötigen, spart die Konvertierung in JPG erheblich Speicherplatz.',
            'article_p2': 'Die Konvertierung findet vollständig auf Ihrem Computer statt.',
            'faq_q1': 'Was passiert mit transparenten Bereichen?',
            'faq_a1': 'Transparente Bereiche werden automatisch mit einem soliden weißen Hintergrund gefüllt.',
            'faq_q2': 'Ist der Service kostenlos?',
            'faq_a2': 'Ja, völlig kostenfrei und unbegrenzt.'
        },
        'es': {
            'title': 'Convertidor PNG a JPG | Image Converter',
            'desc': 'Convierte imágenes PNG a JPG online gratis. Reduce el tamaño fusionando transparencias sobre fondo blanco.',
            'keywords': 'png a jpg, convertir png a jpg, quitar transparencia png',
            'h1': 'Convertidor PNG a JPG',
            'tabs': 'Convertir a JPG',
            'article_title': 'Por qué convertir imágenes PNG a JPG',
            'article_p1': 'Las imágenes PNG pueden llegar a ser muy pesadas. Si no necesitas fondos transparentes, convertirlas a JPG reducirá significativamente su peso sin perder nitidez visible.',
            'article_p2': 'Todo el procesamiento ocurre directamente en tu navegador web local.',
            'faq_q1': '¿Qué sucede con la transparencia de mi PNG?',
            'faq_a1': 'El convertidor rellenará automáticamente los fondos transparentes con un fondo blanco sólido.',
            'faq_q2': '¿Es seguro?',
            'faq_a2': 'Totalmente seguro, sin subir imágenes a la nube.'
        },
        'fr': {
            'title': 'Convertisseur PNG en JPG | Image Converter',
            'desc': 'Convertissez vos images PNG en JPG en ligne gratuitement. Idéal pour réduire le poids des fichiers.',
            'keywords': 'png en jpg, convertir png en jpg, compression image',
            'h1': 'Convertisseur PNG en JPG',
            'tabs': 'Convertir en JPG',
            'article_title': 'Comment exporter vos fichiers PNG vers le format compressé JPG',
            'article_p1': 'Les fichiers JPG sont hautement compressés et compatibles avec tous les systèmes de partage de fichiers et réseaux sociaux.',
            'article_p2': 'Traitement local instantané et totalement privé.',
            'faq_q1': 'Qu\'advient-il des zones transparentes ?',
            'faq_a1': 'Elles sont remplacées par une couleur blanche unie par défaut.',
            'faq_q2': 'Y a-t-il des limites de taille ?',
            'faq_a2': 'Non, traitez vos images en toute liberté.'
        },
        'hi': {
            'title': 'PNG से JPG कनवर्टर | फ़ाइल का आकार छोटा करें',
            'desc': 'PNG इमेज को आसानी से JPG फॉर्मेट में बदलें। 100% सुरक्षित और स्थानीय रूपांतरण।',
            'keywords': 'पीएनजी से जेपीजी, png to jpg, जेपीजी कनवर्टर',
            'h1': 'PNG से JPG कनवर्टर',
            'tabs': 'JPG में बदलें',
            'article_title': 'PNG को JPG में कनवर्ट करने का सही तरीका',
            'article_p1': 'यदि आपकी इमेज में पारदर्शिता की आवश्यकता नहीं है, तो उसे JPG में बदलने से फाइल का आकार बहुत छोटा हो जाता है।',
            'article_p2': 'यह टूल पारदर्शी हिस्सों को सफेद रंग से बदलकर सुरक्षित रूप से स्थानीय स्तर पर प्रोसेस करता है।',
            'faq_q1': 'पारदर्शी हिस्सों का क्या होगा?',
            'faq_a1': 'पारदर्शी हिस्सों में स्वचालित रूप से सफेद बैकग्राउंड आ जाएगा।',
            'faq_q2': 'क्या यह बिल्कुल मुफ़्त है?',
            'faq_a2': 'हाँ, यह बिना किसी छिपे हुए शुल्क के मुफ़्त है।'
        },
        'zh': {
            'title': 'PNG 转 JPG 转换器 | 极限缩小体积',
            'desc': '免费在线将 PNG 转换为通用 JPG 格式。将透明通道栅格化为纯白底色，大幅度压缩文件。',
            'keywords': 'png转jpg, png to jpg, jpg转换器, 去除透明底色',
            'h1': 'PNG 转 JPG 转换器',
            'tabs': '转换为 JPG',
            'article_title': '如何在线快速将透明 PNG 转换为 JPG 格式',
            'article_p1': 'PNG 图片由于无损存储，体积往往非常庞大。若不需要透明通道，转换为 JPG 能够大幅精简服务器存储和网页开销。',
            'article_p2': '所有解析转换过程在您本地设备内飞速完成，保障您的隐私免受云端监测。',
            'faq_q1': '转换后透明底色会变成什么样？',
            'faq_a1': '系统会自动将透明区域填充为纯白色背景。',
            'faq_q2': '一次可以转换几张图片？',
            'faq_a2': '支持无上限的批量拖拽，多张图一次性并发转换。'
        }
    },
    'svg-to-jpg': {
        'de': {
            'title': 'SVG in JPG Konverter | Vektorgrafiken rastern',
            'desc': 'Konvertieren Sie Vektorgrafiken (SVG) online kostenlos in JPG-Bilder.',
            'keywords': 'svg in jpg, svg to jpg, vektoren rastern',
            'h1': 'SVG in JPG Konverter',
            'tabs': 'In JPG konvertieren',
            'article_title': 'SVG-Vektorgrafiken sicher in hochauflösende JPGs konvertieren',
            'article_p1': 'SVG-Dateien sind hervorragend für unendliche Skalierbarkeit, aber nicht immer kompatibel mit Fotogalerien oder Druckern. Rasteren Sie sie hier ganz einfach.',
            'article_p2': '100% sicher durch lokale clientseitige Verarbeitung.',
            'faq_q1': 'Wird das Bild unscharf?',
            'faq_a1': 'Unser Konverter rendert die Vektorgrafiken in einer hohen Auflösung, um die bestmögliche Bildschärfe zu erhalten.',
            'faq_q2': 'Was passiert mit Transparenz?',
            'faq_a2': 'Transparente Bereiche der Vektorgrafik werden mit einem soliden weißen Hintergrund ausgefüllt.'
        },
        'es': {
            'title': 'Convertidor SVG a JPG | Rasterizar Vectores Gratis',
            'desc': 'Convierte gráficos vectoriales SVG a imágenes JPG online gratis. Rasterización local con fondo blanco.',
            'keywords': 'svg a jpg, convertir svg a jpg, rasterizar vectores',
            'h1': 'Convertidor SVG a JPG',
            'tabs': 'Convertir a JPG',
            'article_title': 'Cómo rasterizar gráficos vectoriales SVG a JPG de alta resolución',
            'article_p1': 'Las imágenes vectoriales SVG son perfectas para diseño pero poco prácticas para compartir en redes o imprimir. Con esta herramienta gratuita, puedes transformarlas a JPG al instante.',
            'article_p2': 'Todo el renderizado se efectúa localmente en HTML5, sin enviar tus archivos a internet.',
            'faq_q1': '¿Cómo afecta esto a la calidad?',
            'faq_a1': 'Rasterizamos el vector usando sus dimensiones originales para asegurar que permanezca nítido e impecable.',
            'faq_q2': '¿Qué pasa con el fondo transparente?',
            'faq_a2': 'La transparencia se rellenará automáticamente con un color blanco sólido.'
        },
        'fr': {
            'title': 'Convertisseur SVG en JPG | Image Converter',
            'desc': 'Convertissez vos fichiers vectoriels SVG en images JPG en ligne gratuitement.',
            'keywords': 'svg en jpg, convertir svg en jpg, pixelliser vecteur',
            'h1': 'Convertisseur SVG en JPG',
            'tabs': 'Convertir en JPG',
            'article_title': 'Comment pixelliser vos tracés vectoriels SVG en fichiers JPG',
            'article_p1': 'Pour intégrer vos illustrations SVG dans des présentations ou des portfolios en ligne, la conversion en JPG est idéale.',
            'article_p2': 'Rendu sécurisé et sans perte directement sur votre poste de travail.',
            'faq_q1': 'Le format JPG supporte-t-il les tracés vectoriels ?',
            'faq_a1': 'Non, le JPG est un format de grille de pixels (raster), le fichier final n\'est donc plus librement étirable.',
            'faq_q2': 'Quelle est la couleur de fond par défaut ?',
            'faq_a2': 'La transparence est remplacée par un fond blanc uni.'
        },
        'hi': {
            'title': 'SVG से JPG कनवर्टर | वेक्टर को इमेज में बदलें',
            'desc': 'वेक्टर SVG फाइलों को उच्च गुणवत्ता वाली JPG छवियों में बदलें। 100% सुरक्षित और स्थानीय रूपांतरण।',
            'keywords': 'एसवीजी से जेपीजी, svg to jpg, वेक्टर कनवर्टर',
            'h1': 'SVG से JPG कनवर्टर',
            'tabs': 'JPG में बदलें',
            'article_title': 'SVG वेक्टर को JPG में बदलने का सरल तरीका',
            'article_p1': 'SVG फाइलें असीमित ज़ूम का समर्थन करती हैं, लेकिन सामान्य फोटो व्यूअर में उन्हें देखना मुश्किल होता है। इसलिए उन्हें JPG में बदलना आवश्यक है।',
            'article_p2': 'यह कनवर्टर आपके स्थानीय डिवाइस पर काम करता है और शानदार परिणाम देता है।',
            'faq_q1': 'क्या पारदर्शी बैकग्राउंड बदल जाएगा?',
            'faq_a1': 'हाँ, पारदर्शी हिस्से स्वचालित रूप से सफेद पृष्ठभूमि में बदल जाएंगे।',
            'faq_q2': 'क्या यह टूल मुफ़्त है?',
            'faq_a2': 'हाँ, यह पूरी तरह से मुफ्त है।'
        },
        'zh': {
            'title': 'SVG 转 JPG 转换器 | 矢量图栅格化工具',
            'desc': '免费在线将 SVG 矢量图转换为高分辨率 JPG 格式。本地极速栅格化，提供完美纯白背景。',
            'keywords': 'svg转jpg, svg to jpg, 矢量图转换器, 矢量图转图片',
            'h1': 'SVG 转 JPG 转换器',
            'tabs': '转换为 JPG',
            'article_title': '如何在线安全地将 SVG 矢量图转成高清 JPG',
            'article_p1': 'SVG 拥有无限拉伸不失真的优势，但兼容性较弱，不适合用于主流社交或多媒体平台展示。栅格化为 JPG 是绝佳的解决方案。',
            'article_p2': '在浏览器中直接通过高性能 Canvas 本地渲染，百分百隔离云端监控，安全可靠。',
            'faq_q1': '转换出的 JPG 图片清晰吗？',
            'faq_a1': '我们采用矢量直接绘制渲染，输出分辨率极佳，边缘平滑无毛刺。',
            'faq_q2': '原矢量图的透明背景会如何处理？',
            'faq_a2': '转换过程中，透明像素将自动平滑填充为实心纯白背景。'
        }
    },
    'svg-to-png': {
        'de': {
            'title': 'SVG in PNG Konverter | Vektoren mit Transparenz rastern',
            'desc': 'Konvertieren Sie SVG-Vektordateien online kostenlos in transparente PNGs.',
            'keywords': 'svg in png, svg to png, vektor transparent rastern',
            'h1': 'SVG in PNG Konverter',
            'tabs': 'In PNG konvertieren',
            'article_title': 'SVG-Vektoren unter Beibehaltung der Transparenz in PNG umwandeln',
            'article_p1': 'Konvertieren Sie SVG-Logos und -Icons in PNGs, um sie in allen Webanwendungen mit originalem transparenten Hintergrund einzusetzen.',
            'article_p2': 'Keine Uploads nötig, alles läuft sicher in Ihrem Webbrowser ab.',
            'faq_q1': 'Bleibt der Hintergrund transparent?',
            'faq_a1': 'Ja, die Transparenz des Vektors wird im ausgegebenen PNG-Bild perfekt abgebildet.',
            'faq_q2': 'Kostet dieser Konverter etwas?',
            'faq_a2': 'Nein, es ist völlig gratis.'
        },
        'es': {
            'title': 'Convertidor SVG a PNG | Rasterizar Vectores Transparentes',
            'desc': 'Convierte gráficos vectoriales SVG a imágenes PNG transparentes online gratis. Rasterización local de alta calidad.',
            'keywords': 'svg a png, convertir svg a png, svg transparente gratis',
            'h1': 'Convertidor SVG a PNG',
            'tabs': 'Convertir a PNG',
            'article_title': 'Cómo rasterizar vectores SVG a PNG conservando la transparencia',
            'article_p1': 'A diferencia de JPG, convertir tus SVG a PNG te permite mantener intactos los fondos transparentes y los bordes suaves, ideal para logotipos y activos digitales.',
            'article_p2': 'Tus archivos se procesan de manera privada dentro de tu propio navegador web.',
            'faq_q1': '¿Mantiene la transparencia del vector?',
            'faq_a1': 'Sí, todas las áreas transparentes del diseño SVG original se conservan exactamente iguales en el PNG final.',
            'faq_q2': '¿Es seguro?',
            'faq_a2': 'Absolutamente seguro, no hay cargas a servidores remotos.'
        },
        'fr': {
            'title': 'Convertisseur SVG en PNG | Image Converter',
            'desc': 'Convertissez vos tracés SVG en images PNG transparentes gratuitement en ligne.',
            'keywords': 'svg en png, convertir svg en png, svg transparent',
            'h1': 'Convertisseur SVG en PNG',
            'tabs': 'Convertir en PNG',
            'article_title': 'Pixelliser des illustrations SVG au format PNG avec la transparence',
            'article_p1': 'Idéal pour l\'intégration d\'icônes personnalisées et d\'éléments d\'interface utilisateur sur tous vos sites web.',
            'article_p2': 'Toutes les étapes sont réalisées en local dans le navigateur.',
            'faq_q1': 'La transparence est-elle conservée ?',
            'faq_a1': 'Oui, le canal transparent du fichier vectoriel SVG d\'origine est préservé.',
            'faq_q2': 'Y a-t-il des limites de taille pour le fichier d\'entrée ?',
            'faq_a2': 'L\'outil supporte la majorité des fichiers vectoriels standard sans restrictions.'
        },
        'hi': {
            'title': 'SVG से PNG कनवर्टर | पारदर्शी वेक्टर कनवर्टर',
            'desc': 'वेक्टर SVG को पारदर्शी PNG में बदलें। 100% सुरक्षित और स्थानीय बैच रूपांतरण।',
            'keywords': 'एसवीजी से पीएनजी, svg to png, पारदर्शी पीएनजी कनवर्टर',
            'h1': 'SVG से PNG कनवर्टर',
            'tabs': 'PNG में बदलें',
            'article_title': 'SVG को पारदर्शी PNG में बदलने के फ़ायदे',
            'article_p1': 'जब आप लोगो या वेब आइकन को बदलते हैं, तो पारदर्शिता बनाए रखना बहुत महत्वपूर्ण होता है। PNG इस कार्य के लिए एकदम सही है।',
            'article_p2': 'यह कनवर्टर बिना किसी सर्वर को डेटा भेजे स्थानीय रूप से उत्कृष्ट परिणाम देता है।',
            'faq_q1': 'क्या बैकग्राउंड पारदर्शी रहेगा?',
            'faq_a1': 'हाँ, मूल वेक्टर फ़ाइल की सभी पारदर्शिता PNG में सुरक्षित रहेगी।',
            'faq_q2': 'क्या मैं असीमित फ़ाइलें कनवर्ट कर सकता हूँ?',
            'faq_a2': 'हाँ, उपयोग पर कोई दैनिक सीमा नहीं है।'
        },
        'zh': {
            'title': 'SVG 转 PNG 转换器 | 保留完美透明通道',
            'desc': '免费在线将 SVG 矢量图转换为透明 PNG 格式。完美保存矢量透明和阴影细节。',
            'keywords': 'svg转png, svg to png, 矢量透明转换, favicon素材制作',
            'h1': 'SVG 转 PNG 转换器',
            'tabs': '转换为 PNG',
            'article_title': '如何将 SVG 矢量图标栅格化为透明 PNG 格式',
            'article_p1': '为了能在各类主流办公文档或图片工具中正常粘贴，将 SVG 栅格化为兼容性极佳的透明 PNG 是理想选择。',
            'article_p2': '所有的编译处理都在您本地浏览器线程中进行，无云端中转，隐私安全无虞。',
            'faq_q1': '转换后图片有锯齿吗？',
            'faq_a1': '没有，系统采用矢量矢量原路径插值渲染，边缘过度顺滑无杂音。',
            'faq_q2': '支持复杂的 SVG 特效吗？',
            'faq_a2': '支持大部分符合现代网页 W3C 标准的 SVG 渐变、剪切路径及基本阴影特效。'
        }
    },
    'webp-to-jpg': {
        'de': {
            'title': 'WebP in JPG Konverter | Maximale Kompatibilität',
            'desc': 'Konvertieren Sie WebP-Bilder online kostenlos in JPG-Dateien. Ideal für Offline-Anwendungen.',
            'keywords': 'webp in jpg, webp to jpg, webp umwandeln',
            'h1': 'WebP in JPG Konverter',
            'tabs': 'In JPG konvertieren',
            'article_title': 'WebP-Bilder sicher in kompatible JPGs umwandeln',
            'article_p1': 'WebP ist toll fürs Web, aber nicht alle Fotobetrachter unterstützen es. Konvertieren Sie es hier einfach in das universelle JPG-Format.',
            'article_p2': 'Privat und sicher durch lokale clientseitige Technologie.',
            'faq_q1': 'Geht die Qualität verloren?',
            'faq_a1': 'Wir verwenden hohe Qualitätseinstellungen beim Rendering, um visuelle Detailverluste so gering wie möglich zu halten.',
            'faq_q2': 'Sind meine Bilder privat?',
            'faq_a2': 'Ja, alle Konvertierungen finden ausschließlich in Ihrem Webbrowser statt.'
        },
        'es': {
            'title': 'Convertidor WebP a JPG | Image Converter',
            'desc': 'Convierte imágenes WebP a JPG online gratis. Aumenta la compatibilidad al instante.',
            'keywords': 'webp a jpg, convertir webp a jpg, webp a jpeg',
            'h1': 'Convertidor WebP a JPG',
            'tabs': 'Convertir a JPG',
            'article_title': 'Cómo convertir tus imágenes WebP a JPG gratis',
            'article_p1': 'El formato WebP es ideal para navegar por internet, pero a menudo causa problemas en editores de fotos offline o herramientas antiguas. Convertirlos a JPG soluciona este problema.',
            'article_p2': 'Nuestra herramienta realiza la conversión localmente usando HTML5.',
            'faq_q1': '¿Qué sucede con los fondos transparentes de WebP?',
            'faq_a1': 'Dado que JPG no soporta transparencias, los fondos transparentes se rellenarán con un fondo blanco sólido.',
            'faq_q2': '¿Es seguro?',
            'faq_a2': 'Totalmente seguro, todo funciona localmente.'
        },
        'fr': {
            'title': 'Convertisseur WebP en JPG | Image Converter',
            'desc': 'Convertissez des fichiers WebP en JPG en ligne gratuitement. Compatibilité universelle garantie.',
            'keywords': 'webp en jpg, convertir webp en jpg, image webp',
            'h1': 'Convertisseur WebP en JPG',
            'tabs': 'Convertir en JPG',
            'article_title': 'Comment exporter vos visuels WebP au format JPG classique',
            'article_p1': 'Le format JPG assure que vos photos s\'afficheront de manière identique sur n\'importe quel appareil électronique.',
            'article_p2': 'Conversion locale rapide et 100% anonyme.',
            'faq_q1': 'Le rendu est-il rapide ?',
            'faq_a1': 'Oui, la conversion s\'effectue en une fraction de seconde grâce à notre technologie.',
            'faq_q2': 'Y a-t-il des limites de taille ?',
            'faq_a2': 'Aucune limite n\'est imposée.'
        },
        'hi': {
            'title': 'WebP से JPG कनवर्टर | फ़ोटो को जेपीजी में बदलें',
            'desc': 'WebP छवियों को अत्यधिक अनुकूल JPG फ़ाइलों में बदलें। 100% सुरक्षित और स्थानीय रूपांतरण।',
            'keywords': 'वेबपी से जेपीजी, webp to jpg, जेपीजी कनवर्टर',
            'h1': 'WebP से JPG कनवर्टर',
            'tabs': 'JPG में बदलें',
            'article_title': 'WebP को JPG में कनवर्ट क्यों करें',
            'article_p1': 'WebP वेब के लिए बढ़िया है, लेकिन कई ऑफलाइन एडिटिंग ऐप्स या प्रिंटर इसे सपोर्ट नहीं करते हैं।',
            'article_p2': 'यह मुफ़्त टूल आपकी फ़ाइलों को आपके ही ब्राउज़र में सुरक्षित और स्थानीय रूप से बदलता है।',
            'faq_q1': 'क्या पारदर्शी बैकग्राउंड हट जाएगा?',
            'faq_a1': 'हाँ, क्योंकि JPG पारदर्शिता का समर्थन नहीं करता, इसलिए पृष्ठभूमि सफेद हो जाएगी।',
            'faq_q2': 'क्या यह मुफ़्त है?',
            'faq_a2': 'हाँ, यह बिना किसी शुल्क के पूरी तरह मुफ़्त है।'
        },
        'zh': {
            'title': 'WebP 转 JPG 转换器 | 通用兼容性转换',
            'desc': '免费在线将 WebP 图片转换为兼容性极佳的 JPG 格式。本地快速解码，方便离线编辑。',
            'keywords': 'webp转jpg, webp to jpg, 格式转换, 图片兼容转换',
            'h1': 'WebP 转 JPG 转换器',
            'tabs': '转换为 JPG',
            'article_title': '为什么及如何将网页 WebP 格式图片转为 JPG',
            'article_p1': 'WebP 极度适合网页传输，但许多离线软件（如旧版 PS 或特定看图程序）并不支持它。转为万能的 JPG 是极佳解决方法。',
            'article_p2': '无任何云服务器中转，所有的转换操作均发生在您本机的浏览器内存中，安全可靠。',
            'faq_q1': '原 WebP 图中透明区域会如何处理？',
            'faq_a1': '由于 JPG 不支持透明底色，透明区域将被智能填充为纯实心白色。',
            'faq_q2': '支持苹果手机或安卓平板吗？',
            'faq_a2': '支持，只要设备上装有现代浏览器即可在任意系统使用。'
        }
    },
    'webp-to-png': {
        'de': {
            'title': 'WebP in PNG Konverter | Verlustfreier Qualitäts-Erhalt',
            'desc': 'Konvertieren Sie WebP online kostenlos in transparente PNGs. Clientseitig und absolut sicher.',
            'keywords': 'webp in png, webp to png, webp transparent',
            'h1': 'WebP in PNG Konverter',
            'tabs': 'In PNG konvertieren',
            'article_title': 'WebP-Dateien verlustfrei in das transparente PNG-Format umwandeln',
            'article_p1': 'PNG eignet sich hervorragend, um die volle Bildschärfe von WebP-Bildern ohne erneute Qualitätsverluste bei der Weiterbearbeitung zu bewahren.',
            'article_p2': '100% lokal im Browser ausgeführt.',
            'faq_q1': 'Wird Transparenz unterstützt?',
            'faq_a1': 'Ja, der Alpha-Kanal wird perfekt vom WebP in das ausgegebene PNG übertragen.',
            'faq_q2': 'Kostet der Konverter etwas?',
            'faq_a2': 'Nein, es ist komplett kostenlos.'
        },
        'es': {
            'title': 'Convertidor WebP a PNG | Image Converter',
            'desc': 'Convierte imágenes WebP a PNG transparentes online gratis. 100% privado, sin subir archivos.',
            'keywords': 'webp a png, convertir webp a png, webp transparente gratis',
            'h1': 'Convertidor WebP a PNG',
            'tabs': 'Convertir a PNG',
            'article_title': 'Cómo convertir tus WebP a PNG de forma segura',
            'article_p1': 'El formato PNG te permite editar tus imágenes conservando la transparencia intacta que hereda del archivo WebP original sin aplicar más compresión con pérdida.',
            'article_p2': 'Nuestra herramienta realiza el procesamiento localmente en HTML5.',
            'faq_q1': '¿Conserva la transparencia del WebP?',
            'faq_a1': 'Sí, todas las transparencias y efectos de opacidad se trasladan exactamente iguales al PNG final.',
            'faq_q2': '¿Es seguro?',
            'faq_a2': 'Totalmente seguro, todo funciona localmente.'
        },
        'fr': {
            'title': 'Convertisseur WebP en PNG | Image Converter',
            'desc': 'Convertissez vos fichiers WebP en PNG transparents gratuitement en ligne.',
            'keywords': 'webp en png, convertir webp en png, webp transparent',
            'h1': 'Convertisseur WebP en PNG',
            'tabs': 'Convertir en PNG',
            'article_title': 'Exporter vos graphiques WebP au format sans perte PNG',
            'article_p1': 'Pour retravailler des images WebP dans des éditeurs graphiques en préservant chaque pixel et la transparence.',
            'article_p2': 'Tout se déroule en local sur votre appareil.',
            'faq_q1': 'Le PNG est-il plus lourd ?',
            'faq_a1': 'Oui, car le PNG utilise une compression sans perte, mais il garantit un résultat pixel-perfect.',
            'faq_q2': 'Est-ce gratuit ?',
            'faq_a2': 'Oui, 100% gratuit.'
        },
        'hi': {
            'title': 'WebP से PNG कनवर्टर | पारदर्शिता बनाए रखें',
            'desc': 'WebP छवियों को दोषरहित पारदर्शी PNG में बदलें। 100% सुरक्षित और स्थानीय रूपांतरण।',
            'keywords': 'वेबपी से पीएनजी, webp to png, पीएनजी कनवर्टर',
            'h1': 'WebP से PNG कनवर्टर',
            'tabs': 'PNG में बदलें',
            'article_title': 'WebP को पारदर्शी PNG में बदलने का सही तरीका',
            'article_p1': 'यदि आपकी WebP छवि में पारदर्शी पृष्ठभूमि है, तो उसे PNG में बदलने से गुणवत्ता और पारदर्शिता दोनों सुरक्षित रहती हैं।',
            'article_p2': 'यह कनवर्टर 100% सुरक्षित है, आपकी फ़ाइलें कभी भी हमारे सर्वर पर नहीं जाती हैं।',
            'faq_q1': 'क्या बैकग्राउंड पारदर्शी रहेगा?',
            'faq_a1': 'हाँ, WebP की सभी पारदर्शिता बनने वाली PNG फ़ाइल में बनी रहेगी।',
            'faq_q2': 'क्या उपयोग करने की कोई सीमा है?',
            'faq_a2': 'नहीं, आप जितना चाहें उतना उपयोग कर सकते हैं।'
        },
        'zh': {
            'title': 'WebP 转 PNG 转换器 | 无损透明度转换',
            'desc': '免费在线将 WebP 转换为无损 PNG 格式。完美重现 WebP 原有的透明底色与高保真画质。',
            'keywords': 'webp转png, webp to png, 透明png转换, 无损图片转换',
            'h1': 'WebP 转 PNG 转换器',
            'tabs': '转换为 PNG',
            'article_title': '如何将透明 WebP 转换为无损 PNG 图档',
            'article_p1': '当您需要在不支持 WebP 的设计软件中无损修改图片时，将其转换为透明 PNG 是最佳工作流方案。',
            'article_p2': '依靠 HTML5 前端处理引擎进行直接本地渲染，提供高枕无忧的隐私防泄漏体验。',
            'faq_q1': '可以保留图像透明通道吗？',
            'faq_a1': '可以，原 WebP 所有的透明或半透明边缘像素都将在新 PNG 中完整呈现。',
            'faq_q2': '图片会变大吗？',
            'faq_a2': '会，因为 PNG 是无损格式，所以文件体积相比 WebP 稍大一些，但画质完美不受损。'
        }
    },
    'compress-image-to-10kb': {
        'de': {
            'title': 'Bild auf 10KB komprimieren | 100% Sicher, Schnell & Privat',
            'desc': 'Komprimieren Sie Bilder kostenlos online auf unter 10KB. Optimieren Sie JPG, PNG und WEBP 100% lokal im Browser für absolute Privatsphäre.',
            'keywords': 'bild auf 10kb komprimieren, bilder verkleinern 10kb, bildgröße reduzieren 10kb',
            'h1': 'Bild auf 10KB komprimieren',
            'tabs': 'Auf 10KB komprimieren',
            'article_title': 'Bilder verlustfrei auf unter 10KB verkleinern',
            'article_p1': 'Viele offizielle Formulare und Bewerbungsportale verlangen extrem kleine Dateigrößen von unter 10KB. Unser privater, clientseitiger Kompressor löst dies schnell.',
            'article_p2': 'Ihre sensiblen oder privaten Daten verlassen nie Ihr Gerät — 100% sicher und offline verarbeitet.',
            'faq_q1': 'Wie kann ich ein Bild auf 10KB komprimieren?',
            'faq_a1': 'Laden Sie Ihre Datei per Drag-and-Drop in den Konverter. Unser Tool passt Dimensionen und Kompressionsrate automatisch an, um die 10KB-Grenze einzuhalten.',
            'faq_q2': 'Sind meine hochgeladenen Bilder sicher?',
            'faq_a2': 'Absolut. Alles läuft lokal in Ihrem Browser ab. Ihre Bilder werden niemals auf Server hochgeladen, um absolute Privatsphäre zu garantieren.',
            'faq_q3': 'Kann ich PNG-Dateien ohne Qualitätsverlust auf 10KB komprimieren?',
            'faq_a3': 'Unser Kompressor wendet eine effiziente Kompression an. Bei sehr kleinen Größen wie 10KB wird die Qualität automatisch angepasst, um die Dateigröße optimal zu minimieren.'
        },
        'es': {
            'title': 'Comprimir imagen a 10KB | Gratis, Privado y Seguro',
            'desc': 'Comprime tus imágenes a menos de 10KB gratis online. Optimiza JPG, PNG y WEBP 100% local en tu navegador para total privacidad.',
            'keywords': 'comprimir imagen a 10kb, reducir foto a 10kb, cambiar tamaño imagen a 10kb',
            'h1': 'Comprimir imagen a 10KB',
            'tabs': 'Comprimir a 10KB',
            'article_title': 'Cómo reducir tus imágenes a menos de 10KB',
            'article_p1': 'Muchos trámites gubernamentales y portales en línea exigen archivos de tamaño inferior a 10KB. Nuestra herramienta automatiza el proceso manteniendo la mejor resolución local posible.',
            'article_p2': 'Tus fotos privadas nunca viajan por internet ni se guardan en ningún servidor externo, garantizando el máximo nivel de seguridad.',
            'faq_q1': '¿Cómo comprimir una imagen a 10KB sin perder calidad?',
            'faq_a1': 'Arrastra tus fotos al área de carga y el algoritmo optimizará la calidad y los píxeles para lograr el tamaño objetivo de 10KB.',
            'faq_q2': '¿Es seguro usar este reductor en kb?',
            'faq_a2': 'Sí, es 100% privado y seguro al procesarse en tu propio dispositivo (del lado del cliente).',
            'faq_q3': '¿Puedo comprimir PNG a 10KB?',
            'faq_a3': 'Sí, convertimos o cuantizamos los colores de las imágenes PNG para asegurar que ocupen menos de 10KB de forma rápida y sencilla.'
        },
        'fr': {
            'title': 'Compresser Image à 10KB | Gratuit, Privé et Rapide',
            'desc': 'Compressez vos images à moins de 10KB gratuitement en ligne. Optimisation locale et sécurisée de JPG, PNG et WEBP.',
            'keywords': 'compresser image 10kb, réduire taille photo 10kb, compresser image en ko',
            'h1': 'Compresser Image à 10KB',
            'tabs': 'Compresser à 10KB',
            'article_title': 'Comment réduire le poids d\'une image à 10KB',
            'article_p1': 'Pour les signatures électroniques ou les formulaires administratifs stricts, notre outil réduit rapidement vos images sous les 10KB.',
            'article_p2': 'Tout le processus est client-side, gardant vos documents personnels à l\'abri du réseau.',
            'faq_q1': 'Comment compresser un fichier à 10KB ?',
            'faq_a1': 'Déposez votre image, notre outil de compression ajuste de manière itérative la qualité pour descendre sous 10KB.',
            'faq_q2': 'Les fichiers sont-ils stockés en ligne ?',
            'faq_a2': 'Non. Vos images restent locales et ne sont jamais téléversées sur des serveurs externes.',
            'faq_q3': 'Puis-je compresser un PNG sans perte à 10KB ?',
            'faq_a3': 'Pour atteindre un poids aussi bas, une compression optimisée est requise. L\'outil adapte les paramètres automatiquement.'
        },
        'hi': {
            'title': 'इमेज साइज 10KB तक कम करें | मुफ्त ऑनलाइन कंप्रेसर',
            'desc': 'अपनी फोटो को मुफ्त में 10KB से कम आकार में बदलें। 100% सुरक्षित और स्थानीय जेपीजी, पीएनजी और वेबपी ऑप्टिमाइज़र।',
            'keywords': 'फोटो साइज 10kb करें, 10kb में इमेज कंप्रेस करें, इमेज कंप्रेसर 10kb',
            'h1': 'इमेज साइज 10KB तक कम करें',
            'tabs': '10KB तक कंप्रेस करें',
            'article_title': 'फोटो का आकार 10KB से कम कैसे करें',
            'article_p1': 'हस्ताक्षर, सरकारी आवेदन और ऑनलाइन फॉर्म के लिए 10KB से कम की फोटो की आवश्यकता होती है। हमारा टूल इसे तुरंत प्रोसेस करता है।',
            'article_p2': 'आपकी तस्वीरें कभी भी आपके डिवाइस से बाहर नहीं जाती हैं, जिससे पूर्ण गोपनीयता और सुरक्षा सुनिश्चित होती है।',
            'faq_q1': 'मैं फोटो का साइज 10KB कैसे कर सकता हूँ?',
            'faq_a1': 'अपनी इमेज को अपलोड करें, हमारा सिस्टम पिक्सेल और गुणवत्ता को 10KB से कम करने के लिए स्वचालित रूप से समायोजित करेगा।',
            'faq_q2': 'क्या मेरी तस्वीरें सुरक्षित हैं?',
            'faq_a2': 'हाँ, पूरी प्रक्रिया स्थानीय रूप से आपके ब्राउज़र में होती है, कोई सर्वर अपलोड नहीं होता।',
            'faq_q3': 'क्या PNG को बिना गुणवत्ता नुकसान के 10KB तक कंप्रेस किया जा सकता है?',
            'faq_a3': '10KB के अति-छोटे आकार के लिए गुणवत्ता को थोड़ा अनुकूलित करना पड़ता है, जो हमारा टूल स्वचालित रूप से कुशलता से करता है।'
        },
        'zh': {
            'title': '图片压缩至 10KB | 免费在线本地优化器',
            'desc': '免费在线将图片压缩到 10KB 以下。支持 JPG、PNG 和 WEBP 格式批量本地优化，确保隐私安全。',
            'keywords': '图片压缩至10kb, 缩小图片到10kb, 电子签名压缩',
            'h1': '图片压缩至 10KB',
            'tabs': '压缩至 10KB',
            'article_title': '如何将图片或电子签名缩减至 10KB 以内',
            'article_p1': '电子签名、头像或某些表格系统需要图片绝对小于 10KB。该工具会在本地快速调整画质参数以适应此要求。',
            'article_p2': '纯浏览器本地运行，数据零上传，极力保障您的隐私和安全。',
            'faq_q1': '如何把照片压缩到10KB以下？',
            'faq_a1': '直接拖入图片，系统会通过本地 canvas 压缩算法自动缩减大小至 10KB 以下。',
            'faq_q2': '我的图片安全吗？',
            'faq_a2': '绝对安全。处理均在您本地设备浏览器完成，不向外部服务器传输任何图片字节。',
            'faq_q3': '如何无损压缩 PNG 到 10KB？',
            'faq_a3': '对于 10KB 这样极小的体积，系统会自动进行色彩量化和无损参数的最佳结合，以达到极限缩减。'
        }
    },
    'resize-image': {
        'de': {
            'title': 'Bildgröße online ändern | Kostenloses Batch-Resizer',
            'desc': 'Ändern Sie die Größe von Bildern online kostenlos. Abmessungen in Pixeln 100% lokal im Browser anpassen.',
            'keywords': 'bildgröße ändern, bilder verkleinern, bildabmessungen ändern, batch resizer',
            'h1': 'Bildgröße online ändern',
            'tabs': 'Größe ändern',
            'article_title': 'So ändern Sie die Bildgröße schnell und einfach',
            'article_p1': 'Das Anpassen der Bildabmessungen ist wichtig für das Design und die Ladezeiten von Webseiten. Unser Tool ermöglicht eine schnelle Größenänderung im Batch-Verfahren.',
            'article_p2': 'Alle Berechnungen laufen lokal auf Ihrem Gerät für maximale Datensicherheit.',
            'faq_q1': 'Bleibt das Seitenverhältnis erhalten?',
            'faq_a1': 'Ja, Sie können das Kontrollkästchen "Seitenverhältnis beibehalten" aktivieren, um Verzerrungen zu vermeiden.',
            'faq_q2': 'Gibt es ein Dateigrößen-Limit?',
            'faq_a2': 'Nein, da alles in Ihrem Browser verarbeitet wird, gibt es keine künstlichen Limits für die Dateigröße.'
        },
        'es': {
            'title': 'Redimensionar Imágenes Online Gratis | Image Converter',
            'desc': 'Cambia el tamaño de tus fotos online gratis. Ajusta dimensiones en píxeles de forma local en tu navegador.',
            'keywords': 'redimensionar imagen, cambiar tamaño de foto, redimensionador de imagenes',
            'h1': 'Redimensionar Imágenes Online',
            'tabs': 'Redimensionar',
            'article_title': 'Cómo cambiar el tamaño de tus imágenes online de forma segura',
            'article_p1': 'Ajustar las dimensiones de una imagen es clave para optimizar el rendimiento web. Nuestra herramienta te permite cambiar el tamaño de tus fotos en segundos.',
            'article_p2': 'Todo el procesamiento ocurre de forma local en tu navegador.',
            'faq_q1': '¿Se mantiene la proporción de aspecto?',
            'faq_a1': 'Sí, puedes marcar la opción de mantener la relación de aspecto para evitar deformaciones.',
            'faq_q2': '¿Es seguro?',
            'faq_a2': 'Totalmente seguro, sin subir imágenes a ningún servidor.'
        },
        'fr': {
            'title': 'Redimensionner des Images en Ligne Gratuitement | Image Converter',
            'desc': 'Modifiez la taille et les dimensions de vos images en ligne gratuitement. Traitement local et privé.',
            'keywords': 'redimensionner image, changer taille photo, redimensionneur image gratuit',
            'h1': 'Redimensionner des Images en Ligne',
            'tabs': 'Redimensionner',
            'article_title': 'Comment changer la taille de vos images en toute sécurité',
            'article_p1': 'Ajuster la taille en pixels de vos images est nécessaire pour le web et les réseaux sociaux. Redimensionnez vos fichiers en quelques clics.',
            'article_p2': 'Vos fichiers restent sur votre machine pour une confidentialité totale.',
            'faq_q1': "Le ratio d'aspect est-il préservé ?",
            'faq_a1': 'Oui, vous pouvez verrouiller le ratio pour que vos images ne soient pas étirées.',
            'faq_q2': 'Y a-t-il une limite de taille ?',
            'faq_a2': 'Non, le traitement se fait localement sans aucune limite.'
        },
        'hi': {
            'title': 'ऑनलाइन इमेज का आकार बदलें | मुफ़्त फोटो रिसाइज़र',
            'desc': 'अपनी छवियों का आकार पिक्सेल में मुफ्त में बदलें। 100% सुरक्षित और स्थानीय इमेज रिसाइज़र।',
            'keywords': 'इमेज रिसाइज़र, फोटो का आकार बदलें, इमेज रिसाइज करें, फोटो छोटा करें',
            'h1': 'इमेज का आकार ऑनलाइन बदलें',
            'tabs': 'आकार बदलें',
            'article_title': 'इमेज का आकार बदलने का आसान तरीका',
            'article_p1': 'वेबसाइट के लिए पिक्सेल आयामों को समायोजित करना बहुत आवश्यक है। यह रिसाइज़र बैच में काम करता है।',
            'article_p2': 'यह टूल आपके स्थानीय डिवाइस पर काम करता है और डेटा सुरक्षित रखता है।',
            'faq_q1': 'क्या फोटो का अनुपात बना रहेगा?',
            'faq_a1': 'हाँ, आप "अनुपात बनाए रखें" विकल्प चुन सकते हैं ताकि फोटो खराब न हो।',
            'faq_q2': 'क्या यह सुरक्षित है?',
            'faq_a2': 'हाँ, सभी प्रक्रिया आपके स्थानीय ब्राउज़र में होती है।'
        },
        'zh': {
            'title': '在线调整图片大小 | 免费批量图片缩放工具',
            'desc': '在线免费调整图片尺寸。在本地浏览器中快速修改像素宽高，保护个人隐私。',
            'keywords': '调整图片大小, 修改图片尺寸, 图片缩放, 批量图片改大小',
            'h1': '在线调整图片大小',
            'tabs': '调整大小',
            'article_title': '如何安全地调整图片像素大小',
            'article_p1': '为了适应网页设计或社交媒体的尺寸规范，经常需要调整图像的宽高。该工具提供便捷的批量缩放服务。',
            'article_p2': '依靠浏览器本地 Canvas 渲染，不产生网络流量，彻底保障隐私。',
            'faq_q1': '可以保持纵横比吗？',
            'faq_a1': '可以，勾选“保持比例”选项即可避免图片变形。',
            'faq_q2': '需要付费吗？',
            'faq_a2': '不需要，这是一个 100% 免费的本地实用工具。'
        }
    },
    'watermark-image': {
        'de': {
            'title': 'Bilder online mit Wasserzeichen versehen | Batch-Wasserzeichen',
            'desc': 'Fügen Sie Ihren Bildern online kostenlos Textwasserzeichen hinzu. Schützen Sie Ihre Urheberrechte lokal im Browser.',
            'keywords': 'wasserzeichen hinzufügen, bilder wasserzeichen, urheberrecht schützen',
            'h1': 'Bilder mit Wasserzeichen versehen',
            'tabs': 'Wasserzeichen hinzufügen',
            'article_title': 'So versehen Sie Ihre Bilder mit einem Wasserzeichen',
            'article_p1': 'Wasserzeichen schützen Ihre visuellen Werke vor unbefugter Nutzung. Unser Tool fügt Texte in verschiedenen Positionen und Größen hinzu.',
            'article_p2': 'Keine Uploads nötig, Ihre Urheberrechte bleiben auf Ihrem lokalen System geschützt.',
            'faq_q1': 'Wird die Bildqualität beeinträchtigt?',
            'faq_a1': 'Nein, das Wasserzeichen wird direkt auf das Bild gerendert, wobei die hohe visuelle Qualität erhalten bleibt.',
            'faq_q2': 'Werden meine Bilder irgendwo gespeichert?',
            'faq_a2': 'Absolut nicht. Die Bearbeitung erfolgt vollständig clientseitig in Ihrem Webbrowser.'
        },
        'es': {
            'title': 'Poner Marca de Agua a Imágenes Gratis | Image Converter',
            'desc': 'Añade marcas de agua de texto a tus imágenes online gratis. Protege tus fotos de forma local en tu navegador.',
            'keywords': 'marca de agua gratis, poner marca de agua online, proteger fotos, marca de agua texto',
            'h1': 'Marca de Agua en Imágenes',
            'tabs': 'Añadir marca de agua',
            'article_title': 'Cómo proteger tus imágenes con marcas de agua online',
            'article_p1': 'Las marcas de agua te ayudan a proteger tus derechos de autor en internet. Puedes añadir textos personalizados, ajustar tamaños y posiciones de forma masiva.',
            'article_p2': 'Todo se procesa en tu propio dispositivo para una privacidad garantizada.',
            'faq_q1': '¿Se pueden procesar varias fotos a la vez?',
            'faq_a1': 'Sí, puedes arrastrar y soltar múltiples fotos para aplicarles la marca de agua en un solo lote.',
            'faq_q2': '¿Es seguro?',
            'faq_a2': 'Completamente seguro, las fotos nunca se suben a internet.'
        },
        'fr': {
            'title': 'Ajouter un Filigrane sur vos Images | Image Converter',
            'desc': 'Ajoutez des filigranes textuels à vos photos en ligne gratuitement. Protégez vos droits d\'auteur localement.',
            'keywords': 'ajouter filigrane image, filigrane gratuit en ligne, protection photos',
            'h1': 'Ajouter un Filigrane sur des Images',
            'tabs': 'Ajouter un filigrane',
            'article_title': 'Comment protéger vos images avec un filigrane en ligne',
            'article_p1': 'Le filigrane est idéal pour marquer la propriété de vos clichés avant diffusion. Choisissez le texte, la taille et la position.',
            'article_p2': 'Le traitement est effectué entièrement dans votre navigateur pour une sécurité totale.',
            'faq_q1': 'Puis-je traiter des lots d\'images ?',
            'faq_a1': 'Oui, glissez-déposez plusieurs fichiers pour leur appliquer le filigrane simultanément.',
            'faq_q2': 'Les photos originales sont-elles modifiées ?',
            'faq_a2': 'Non, vous téléchargez de nouveaux fichiers avec le filigrane incrusté.'
        },
        'hi': {
            'title': 'फोटो पर वॉटरमार्क लगाएं | ऑनलाइन वॉटरमार्क टूल',
            'desc': 'अपनी छवियों पर टेक्स्ट वॉटरमार्क मुफ्त में जोड़ें। अपने कॉपीराइट को ब्राउज़र में सुरक्षित रखें।',
            'keywords': 'वॉटरमार्क लगाएं, फोटो वॉटरमार्क, कॉपीराइट सुरक्षित करें',
            'h1': 'छवियों पर वॉटरमार्क लगाएं',
            'tabs': 'वॉटरमार्क लगाएं',
            'article_title': 'अपनी तस्वीरों को वॉटरमार्क से कैसे सुरक्षित करें',
            'article_p1': 'वॉटरमार्क आपके चित्रों को अनधिकृत उपयोग से बचाने का एक शानदार तरीका है। आप कस्टम टेक्स्ट, आकार और स्थिति चुन सकते हैं।',
            'article_p2': 'यह टूल पूरी तरह से आपके ब्राउज़र में काम करता है और डेटा लीक होने का कोई खतरा नहीं है।',
            'faq_q1': 'क्या मैं एक बार में कई छवियों पर वॉटरमार्क लगा सकता हूँ?',
            'faq_a1': 'हाँ, यह टूल बैच मोड का समर्थन करता है ताकि आप कई फाइलों पर एक साथ वॉटरमार्क लगा सकें।',
            'faq_q2': 'क्या यह मुफ़्त है?',
            'faq_a2': 'हाँ, यह बिना किसी शुल्क के 100% मुफ़्त है।'
        },
        'zh': {
            'title': '在线图片加水印 | 批量文字水印工具',
            'desc': '免费在线为图片添加文字水印。本地安全运行，保护图片版权不受侵犯。',
            'keywords': '图片加水印, 在线加水印, 批量水印工具, 保护版权',
            'h1': '在线图片添加水印',
            'tabs': '添加水印',
            'article_title': '如何在线为图片快速批量添加水印',
            'article_p1': '为了防止您的摄影作品或设计被盗用，添加文字水印是极佳的方法。支持自定义大小和五个位置放置。',
            'article_p2': '所有水印合成在浏览器端本地线程进行，绝不上传，确保您的原片安全。',
            'faq_q1': '支持批量添加吗？',
            'faq_a1': '支持，您可以一次拖入多张图片，系统会全部盖上水印并打包下载。',
            'faq_q2': '可以选择哪些位置？',
            'faq_a2': '支持四角（左上、右上、左下、右下）以及正中间五个位置。'
        }
    },
    'jpg-to-pdf': {
        'de': {
            'title': 'JPG in PDF Konverter | Bilder als PDF speichern',
            'desc': 'Konvertieren Sie JPG-Bilder online kostenlos in ein PDF-Dokument. 100% lokal im Browser.',
            'keywords': 'jpg in pdf, bilder in pdf, jpg to pdf, pdf compiler',
            'h1': 'JPG in PDF Konverter',
            'tabs': 'In PDF konvertieren',
            'article_title': 'Bilder in ein PDF-Dokument umwandeln',
            'article_p1': 'Fügen Sie mehrere JPG-Bilder zu einem einzigen PDF-Dokument zusammen. Ideal für Bewerbungsunterlagen, Scans oder Portfolios.',
            'article_p2': 'Die Konvertierung läuft lokal auf Ihrem Gerät und garantiert absolute Datensicherheit.',
            'faq_q1': 'Werden die Bilder komprimiert?',
            'faq_a1': 'Das Tool passt die Bilder an das A4-Format an, um ein optimales Layout ohne unnötigen Qualitätsverlust zu gewährleisten.',
            'faq_q2': 'Wie viele Seiten kann das PDF haben?',
            'faq_a2': 'Es gibt keine Begrenzung der Seitenzahl, da alles lokal im Browser kompiliert wird.'
        },
        'es': {
            'title': 'Convertidor JPG a PDF | Unir Imágenes en PDF Gratis',
            'desc': 'Convierte tus imágenes JPG a un documento PDF online gratis. Proceso local en tu navegador para total privacidad.',
            'keywords': 'jpg a pdf, convertir fotos a pdf, imagenes a pdf gratis, unir pdf',
            'h1': 'Convertidor JPG a PDF',
            'tabs': 'Convertir a PDF',
            'article_title': 'Cómo compilar múltiples imágenes JPG en un solo archivo PDF',
            'article_p1': 'Agrupar tus fotos o documentos escaneados en un solo PDF facilita su envío y organización. Nuestra herramienta escala automáticamente las fotos para ajustarse al formato A4.',
            'article_p2': 'Tus documentos confidenciales nunca viajan por internet, asegurando la máxima privacidad.',
            'faq_q1': '¿Puedo subir otros formatos aparte de JPG?',
            'faq_a1': 'Sí, la herramienta soporta la conversión automática de PNG, WEBP y HEIC directamente al PDF.',
            'faq_q2': '¿Es gratis?',
            'faq_a2': 'Sí, es 100% gratuito y sin límites de páginas.'
        },
        'fr': {
            'title': 'Convertisseur JPG en PDF | Compiler des Images en PDF',
            'desc': 'Convertissez vos images JPG en un seul fichier PDF en ligne gratuitement. Rendu local sécurisé.',
            'keywords': 'jpg en pdf, assembler pdf, images en pdf gratuit, convertisseur image pdf',
            'h1': 'Convertisseur JPG en PDF',
            'tabs': 'Convertir en PDF',
            'article_title': 'Comment assembler vos documents JPG dans un fichier PDF',
            'article_p1': 'Parfait pour regrouper des reçus, des pièces d\'identité ou des portfolios. Vos images sont mises à l\'échelle et centrées automatiquement.',
            'article_p2': 'Tout le processus est client-side, gardant vos documents confidentiels.',
            'faq_q1': 'Quels formats d\'image sont acceptés ?',
            'faq_a1': 'Vous pouvez insérer des fichiers JPG, PNG, WEBP et HEIC.',
            'faq_q2': 'Combien de pages puis-je générer ?',
            'faq_a2': 'Il n\'y a aucune limite du nombre de pages.'
        },
        'hi': {
            'title': 'JPG से PDF कनवर्टर | छवियों को PDF में बदलें',
            'desc': 'JPG इमेज को एक PDF दस्तावेज़ में मुफ्त में बदलें। 100% सुरक्षित और स्थानीय पीडीएफ मेकर।',
            'keywords': 'जेपीजी से पीडीएफ, jpg to pdf, फोटो को पीडीएफ बनाएं',
            'h1': 'JPG से PDF कनवर्टर',
            'tabs': 'PDF में बदलें',
            'article_title': 'कई चित्रों को एक PDF में संकलित कैसे करें',
            'article_p1': 'रसीदें, दस्तावेज़ या तस्वीरें एक ही पीडीएफ में जमा करने के लिए यह टूल छवियों को A4 आकार में स्वचालित रूप से फिट कर देता है।',
            'article_p2': 'यह पीडीएफ कंपाइलर बिना सर्वर के पूरी सुरक्षा के साथ काम करता है।',
            'faq_q1': 'क्या छवियों की गुणवत्ता बनी रहेगी?',
            'faq_a1': 'हाँ, हमारा कनवर्टर छवियों को बिना धुंधला किए उपयुक्त आकार में फिट करता है।',
            'faq_q2': 'क्या इसकी कोई सीमा है?',
            'faq_a2': 'नहीं, आप असीमित पेजों का पीडीएफ दस्तावेज बना सकते हैं।'
        },
        'zh': {
            'title': 'JPG 转 PDF 转换器 | 免费在线合成 PDF 文档',
            'desc': '免费在线将多张 JPG 图片合成一个 PDF 文档。100% 本地浏览器合成，确保敏感文件隐私。',
            'keywords': 'jpg转pdf, 图片转pdf, 批量合成pdf, 多图转pdf',
            'h1': 'JPG 转 PDF 转换器',
            'tabs': '转换为 PDF',
            'article_title': '如何在本地将多张 JPG/PNG 图片合成单个 PDF',
            'article_p1': '将扫描件、发票或作品集整理合成单个 PDF，极大地方便了发送与打印。系统会将图片自动调整并居中适配 A4 页面。',
            'article_p2': '纯前端本地打包技术，无需任何云端处理，全力守护您的证件和敏感隐私。',
            'faq_q1': '支持除 JPG 以外的图片吗？',
            'faq_a1': '支持，您可以把 PNG、WEBP 或 HEIC 等多种格式 of 图片一起放入并排版。',
            'faq_q2': '合成文件有页数限制吗？',
            'faq_a2': '没有，系统在您电脑内存中进行合成，支持无限页数。'
        }
    },
    'jpg-to-tiff': {
        'de': {
            'title': 'JPG in TIFF Konverter | Rasterbilder erstellen',
            'desc': 'Konvertieren Sie JPG-Bilder online kostenlos in das TIFF-Format. Ideal für hochwertigen Druck.',
            'keywords': 'jpg in tiff, jpg to tiff, bilder in tiff',
            'h1': 'JPG in TIFF Konverter',
            'tabs': 'In TIFF konvertieren',
            'article_title': 'JPG-Bilder in das TIFF-Format umwandeln',
            'article_p1': 'TIFF ist ein etabliertes Format in der Druckindustrie und im Grafikdesign, das Rasterdaten in hoher Qualität speichert.',
            'article_p2': 'Der Konverter arbeitet 100% lokal in Ihrem Webbrowser.',
            'faq_q1': 'Warum TIFF statt JPG wählen?',
            'faq_a1': 'TIFF eignet sich besser für die Weiterbearbeitung und den professionellen Druck, da es verlustfrei gespeichert werden kann.',
            'faq_q2': 'Ist dieser Konverter sicher?',
            'faq_a2': 'Ja, Ihre Bilder verlassen Ihr Gerät zu keinem Zeitpunkt.'
        },
        'es': {
            'title': 'Convertidor JPG a TIFF | Crear Imágenes Rasterizadas',
            'desc': 'Convierte imágenes JPG a formato TIFF online gratis. Ideal para diseño profesional e impresión.',
            'keywords': 'jpg a tiff, convertir jpg a tiff, formato tiff gratis',
            'h1': 'Convertidor JPG a TIFF',
            'tabs': 'Convertir a TIFF',
            'article_title': 'Cómo convertir tus imágenes JPG a TIFF de alta calidad',
            'article_p1': 'TIFF es el formato estándar preferido por imprentas y publicaciones profesionales por su capacidad para almacenar datos de mapa de bits sin compresión agresiva.',
            'article_p2': 'Todo el renderizado se realiza localmente en tu navegador sin subidas.',
            'faq_q1': '¿Es seguro?',
            'faq_a1': 'Sí, la conversión ocurre 100% del lado del cliente.',
            'faq_q2': '¿Tiene costo?',
            'faq_a2': 'No, es completamente gratuito y sin límites.'
        },
        'fr': {
            'title': 'Convertisseur JPG en TIFF | Image Converter',
            'desc': 'Convertissez vos images JPG en fichiers TIFF en ligne gratuitement. Idéal pour l\'impression professionnelle.',
            'keywords': 'jpg en tiff, convertir jpg en tiff, image tiff gratuit',
            'h1': 'Convertisseur JPG en TIFF',
            'tabs': 'Convertir en TIFF',
            'article_title': 'Comment exporter vos images JPG vers le format TIFF',
            'article_p1': 'TIFF est largement utilisé dans l\'édition et l\'imprimerie pour sa gestion rigoureuse des données matricielles.',
            'article_p2': 'Traitement sécurisé en local sans transfert cloud.',
            'faq_q1': 'Pourquoi convertir en TIFF ?',
            'faq_a1': 'Le format TIFF évite les pertes de compression lors des sauvegardes successives.',
            'faq_q2': 'Est-ce gratuit ?',
            'faq_a2': 'Oui, l\'outil est totalement gratuit et livre d\'accès.'
        },
        'hi': {
            'title': 'JPG से TIFF कनवर्टर | उच्च गुणवत्ता वाली TIFF इमेज',
            'desc': 'JPG इमेज को मुफ्त में TIFF प्रारूप में बदलें। 100% सुरक्षित और स्थानीय रूपांतरण।',
            'keywords': 'जेपीजी से टिफ, jpg to tiff, टिफ कनवर्टर',
            'h1': 'JPG से TIFF कनवर्टर',
            'tabs': 'TIFF में बदलें',
            'article_title': 'JPG को TIFF में बदलने का आसान तरीका',
            'article_p1': 'TIFF प्रारूप मुख्य रूप से प्रिंटिंग और प्रकाशन उद्योगों में उपयोग किया जाता है क्योंकि यह विवरणों को सुरक्षित रखता है।',
            'article_p2': 'यह कनवर्टर बिना किसी सर्वर को डेटा भेजे स्थानीय रूप से चलता है।',
            'faq_q1': 'क्या यह टूल मुफ़्त है?',
            'faq_a1': 'हाँ, यह 100% मुफ़्त है और इसकी कोई सीमा नहीं है।',
            'faq_q2': 'क्या यह मोबाइल पर काम करता है?',
            'faq_a2': 'हाँ, यह मोबाइल वेब ब्राउज़र के माध्यम से सभी उपकरणों पर आसानी से काम करता है।'
        },
        'zh': {
            'title': 'JPG 转 TIFF 转换器 | 免费在线生成 TIFF',
            'desc': '免费在线将 JPG 图片转换为 TIFF 格式。本地运行，适合印刷和高精度学术出版物。',
            'keywords': 'jpg转tiff, jpg to tiff, tiff转换器, 印刷图片格式',
            'h1': 'JPG 转 TIFF 转换器',
            'tabs': '转换为 TIFF',
            'article_title': '如何安全在本地将 JPG 图片转换为 TIFF 格式',
            'article_p1': 'TIFF 是一种非常成熟的图像格式，广泛应用于出版、印刷和医学影像，以保留最精确的栅格数据。',
            'article_p2': '依托浏览器本地引擎计算，数据无需上传，隐私极其安全。',
            'faq_q1': 'TIFF 格式有什么优势？',
            'faq_a1': 'TIFF 能够进行无损保存，非常方便后续进行多次无损调整和印刷排版。',
            'faq_q2': '有大小限制吗？',
            'faq_a2': '本站纯本地合成，不设网络带宽大小门槛，完全免费使用。'
        }
    },
    'tiff-to-jpg': {
        'de': {
            'title': 'TIFF in JPG Konverter | Tagged-Image-Dateien umwandeln',
            'desc': 'Konvertieren Sie TIFF-Bilder online kostenlos in JPG-Dateien. Erhöhen Sie die Kompatibilität.',
            'keywords': 'tiff in jpg, tiff to jpg, tagged image konvertieren',
            'h1': 'TIFF in JPG Konverter',
            'tabs': 'In JPG konvertieren',
            'article_title': 'TIFF-Dateien sicher in JPGs konvertieren',
            'article_p1': 'TIFF-Dateien sind oft extrem groß und werden von Mobilgeräten oder Webseiten selten nativ unterstützt. Konvertieren Sie sie in JPG für eine einfache Freigabe.',
            'article_p2': 'Alle Konvertierungen geschehen privat in Ihrem Webbrowser.',
            'faq_q1': 'Wird das TIFF-Bild komprimiert?',
            'faq_a1': 'Ja, durch die Konvertierung wird das Bild im komprimierten JPG-Format gespeichert, wodurch die Dateigröße drastisch sinkt.',
            'faq_q2': 'Kostet dieses Tool etwas?',
            'faq_a2': 'Nein, es ist vollkommen kostenlos.'
        },
        'es': {
            'title': 'Convertidor TIFF a JPG | Convertir Archivos Tagged Image',
            'desc': 'Convierte imágenes TIFF a JPG online gratis. Ahorra espacio de forma local en tu navegador.',
            'keywords': 'tiff a jpg, convertir tiff a jpg, formato tiff a jpeg',
            'h1': 'Convertidor TIFF a JPG',
            'tabs': 'Convertir a JPG',
            'article_title': 'Por qué convertir imágenes TIFF a JPG',
            'article_p1': 'Los archivos TIFF suelen ser sumamente pesados y difíciles de compartir. Convertirlos al formato JPG reduce significativamente su peso haciéndolos ideales para la web.',
            'article_p2': 'El motor de renderizado local asegura que no haya riesgos de fugas de datos.',
            'faq_q1': '¿Qué pasa con las capas del TIFF?',
            'faq_a1': 'El convertidor combinará automáticamente todas las capas del archivo TIFF en una sola imagen JPG plana.',
            'faq_q2': '¿Es seguro?',
            'faq_a2': 'Absolutamente, es un convertidor offline del lado del cliente.'
        },
        'fr': {
            'title': 'Convertisseur TIFF en JPG | Image Converter',
            'desc': 'Convertissez vos fichiers TIFF en images JPG en ligne gratuitement. Réduisez le poids des fichiers.',
            'keywords': 'tiff en jpg, convertir tiff en jpg, image matricielle',
            'h1': 'Convertisseur TIFF en JPG',
            'tabs': 'Convertir en JPG',
            'article_title': 'Comment optimiser vos clichés TIFF en fichiers JPG compressés',
            'article_p1': 'Les fichiers TIFF sont lourds et complexes. Les convertir en JPG les rend instantanément compatibles avec la plupart des visionneuses d\'images et réseaux.',
            'article_p2': 'Rendu sécurisé et sans intermédiaire cloud.',
            'faq_q1': 'Les calques TIFF sont-ils conservés ?',
            'faq_a1': 'Non, le format JPG ne gérant pas les calques, l\'image finale est aplatie.',
            'faq_q2': 'Y a-t-il des limites de taille pour le fichier d\'entrée ?',
            'faq_a2': 'L\'outil supporte la majorité des fichiers TIFF standard.'
        },
        'hi': {
            'title': 'TIFF से JPG कनवर्टर | फ़ाइल का आकार छोटा करें',
            'desc': 'भारी TIFF फाइलों को आसानी से JPG फॉर्मेट में बदलें। 100% सुरक्षित और स्थानीय रूपांतरण।',
            'keywords': 'टिफ से जेपीजी, tiff to jpg, इमेज कनवर्टर',
            'h1': 'TIFF से JPG कनवर्टर',
            'tabs': 'JPG में बदलें',
            'article_title': 'TIFF को JPG में बदलने का सबसे आसान तरीका',
            'article_p1': 'TIFF फाइलें बहुत बड़ी होती हैं और उन्हें सोशल मीडिया पर शेयर करना मुश्किल होता है। JPG में बदलने से इनका साइज काफी कम हो जाता है।',
            'article_p2': 'यह कनवर्टर सीधे आपके डिवाइस पर काम करता है और गुणवत्ता सुनिश्चित करता है।',
            'faq_q1': 'क्या यह टूल सुरक्षित है?',
            'faq_a1': 'हाँ, चूंकि कोई भी डेटा बाहर नहीं जाता है, यह 100% सुरक्षित और निजी है।',
            'faq_q2': 'क्या इसके लिए इंटरनेट की आवश्यकता है?',
            'faq_a2': 'नहीं, पेज लोड होने के बाद यह पूरी तरह से ऑफलाइन काम करता है।'
        },
        'zh': {
            'title': 'TIFF 转 JPG 转换器 | 极限缩小体积',
            'desc': '免费在线将 TIFF 图像转换为 JPG 格式。本地运行，大幅度减少印刷级别大图的文件体积。',
            'keywords': 'tiff转jpg, tiff to jpg, tiff图转换, 批量转换大图',
            'h1': 'TIFF 转 JPG 转换器',
            'tabs': '转换为 JPG',
            'article_title': '如何在线快速将大体积 TIFF 转换为 JPG 格式',
            'article_p1': 'TIFF 图片因为常包含高精无损信息，体积动辄数十兆，在网络分发或日常查看时兼容性极差。转换为 JPG 能够立即解决此痛点。',
            'article_p2': '所有转换分析均在您本地设备中进行，安全隔绝，不必担心重要设计稿被泄露。',
            'faq_q1': 'TIFF 中的图层和多页会保留吗？',
            'faq_a1': '系统在转换时，会自动将最上层可见图像图层合并栅格化为扁平的 JPG。',
            'faq_q2': '一次能转换几张？',
            'faq_a2': '支持多张 TIFF 文件批量推入，极速自动按顺序转为 JPG 并输出。'
        }
    }
}

# Programmatically populate translations for target size and format-specific compression landing pages!
more_sizes = [20, 30, 200, 500]
for sz in more_sizes:
    t_name = f"compress-image-to-{sz}kb"
    TOOL_TRANSLATIONS[t_name] = {
        'de': {
            'title': f'Bild auf {sz}KB komprimieren online | Keine Anmeldung',
            'desc': f'Bilder kostenlos online unter {sz}KB komprimieren. JPG, PNG und WEBP 100% lokal im Browser optimieren.',
            'keywords': f'bild auf {sz}kb komprimieren, bilder verkleinern {sz}kb, png komprimieren {sz}kb',
            'h1': f'Bild auf {sz}KB komprimieren online',
            'tabs': f'Auf {sz}KB komprimieren',
            'article_title': f'Wie man Bilder extrem auf unter {sz}KB komprimiert',
            'article_p1': f'Für Online-Formulare oder Bewerbungen müssen Bilder oft unter {sz}KB groß sein. Unser kostenloser Kompressor hilft Ihnen dabei.',
            'article_p2': f'Da die Verarbeitung lokal im Browser erfolgt, sind Ihre privaten Daten absolut sicher.'
        },
        'es': {
            'title': f'Comprimir imagen a {sz}KB gratis online | Sin Registro',
            'desc': f'Comprime tus imágenes a menos de {sz}KB gratis online. Optimización local de JPG, PNG y WEBP para total privacidad.',
            'keywords': f'comprimir imagen a {sz}kb, reducir foto a {sz}kb, comprimir png a {sz}kb',
            'h1': f'Comprimir imagen a {sz}KB online',
            'tabs': f'Comprimir a {sz}KB',
            'article_title': f'Cómo reducir tus imágenes a menos de {sz}KB',
            'article_p1': f'Muchos trámites exigen archivos de tamaño inferior a {sz}KB. Nuestra herramienta automatiza el proceso.',
            'article_p2': f'Tus fotos nunca viajan por internet ni se guardan en ningún servidor, garantizando seguridad total.'
        },
        'fr': {
            'title': f'Compresser Image à {sz}KB en Ligne | Sans Téléchargement',
            'desc': f'Compressez vos images à moins de {sz}KB gratuitement en ligne. Optimisation locale et ultra-rapide de JPG, PNG et WEBP.',
            'keywords': f'compresser image {sz}kb, réduire taille photo {sz}kb, compresser png {sz}kb',
            'h1': f'Compresser Image à {sz}KB en Ligne',
            'tabs': f'Compresser à {sz}KB',
            'article_title': f'Comment optimiser des photos sous le seuil de {sz}KB',
            'article_p1': f'Notre outil calcule précisément les paramètres de qualité pour réduire vos fichiers sans dépasser la limite de {sz}KB.',
            'article_p2': f"Tout le processus est client-side, gardant vos documents personnels à l'abri du réseau."
        },
        'hi': {
            'title': f'इमेज साइज {sz}KB तक कम करें ऑनलाइन | बिना अपलोड किए',
            'desc': f'अपनी फोटो को मुफ्त में {sz}KB से कम आकार में बदलें। 100% सुरक्षित और स्थानीय जेपीजी, पीएनजी और वेबपी कंप्रेसर।',
            'keywords': f'फोटो साइज {sz}kb करें, {sz}kb में इमेज कंप्रेस करें, पीएनजी को {sz}kb करें',
            'h1': f'इमेज साइज {sz}KB तक कम करें ऑनलाइन',
            'tabs': f'{sz}KB तक कंप्रेस करें',
            'article_title': f'फोटो का आकार {sz}KB से कम कैसे करें',
            'article_p1': f'सरकारी आवेदन और ऑनलाइन फॉर्म के लिए {sz}KB से कम की फोटो की आवश्यकता होती है। हमारा टूल इसे तुरंत प्रोसेस करता है।',
            'article_p2': f'आपकी तस्वीरें कभी भी आपके डिवाइस से बाहर नहीं जाती हैं, जिससे पूर्ण गोपनीयता सुनिश्चित होती है।'
        },
        'zh': {
            'title': f'图片压缩至 {sz}KB 在线 | 免费安全本地优化器',
            'desc': f'免费在线将图片压缩至 {sz}KB 以下。支持 JPG、PNG 和 WEBP 格式批量本地优化。',
            'keywords': f'图片压缩至{sz}kb, 缩小图片到{sz}kb, png压缩{sz}kb',
            'h1': f'图片压缩至 {sz}KB 在线',
            'tabs': f'压缩至 {sz}KB',
            'article_title': f'如何将图片缩减至 {sz}KB 以内',
            'article_p1': f'电子签名、头像或某些表格系统需要图片绝对小于 {sz}KB。该工具会在本地快速调整画质以适应要求。',
            'article_p2': f'纯本地运行，数据零上传，极力保障您的隐私和安全。'
        }
    }

format_specific = [("jpg", 100), ("png", 100), ("jpeg", 100)]
for fmt_name, sz in format_specific:
    t_name = f"compress-{fmt_name}-to-{sz}kb"
    fmt_upper = fmt_name.upper()
    TOOL_TRANSLATIONS[t_name] = {
        'de': {
            'title': f'{fmt_upper} auf {sz}KB komprimieren online | Ohne Upload',
            'desc': f'Komprimieren Sie {fmt_upper}-Bilder kostenlos online auf unter {sz}KB. Optimieren Sie Ihre {fmt_upper} 100% lokal.',
            'keywords': f'{fmt_name} auf {sz}kb komprimieren, {fmt_name} verkleinern {sz}kb, png komprimieren {sz}kb',
            'h1': f'{fmt_upper} auf {sz}KB komprimieren online',
            'tabs': f'Auf {sz}KB komprimieren',
            'article_title': f'Wie man {fmt_upper}-Dateien auf unter {sz}KB komprimiert',
            'article_p1': f'Für Online-Formulare oder Bewerbungen müssen {fmt_upper}-Bilder oft unter {sz}KB groß sein. Unser kostenloser Kompressor hilft Ihnen dabei.',
            'article_p2': f'Da die Verarbeitung lokal im Browser erfolgt, sind Ihre privaten Daten absolut sicher.'
        },
        'es': {
            'title': f'Comprimir {fmt_upper} a {sz}KB gratis online | Sin Subida',
            'desc': f'Comprime tus {fmt_upper} a menos de {sz}KB gratis online. Optimización local en tu navegador para total privacidad.',
            'keywords': f'comprimir {fmt_name} a {sz}kb, reducir {fmt_name} a {sz}kb, comprimir png a {sz}kb',
            'h1': f'Comprimir {fmt_upper} a {sz}KB online',
            'tabs': f'Comprimir a {sz}KB',
            'article_title': f'Cómo reducir tus {fmt_upper} a menos de {sz}KB',
            'article_p1': f'Muchos trámites exigen archivos de tamaño inferior a {sz}KB. Nuestra herramienta automatiza el proceso.',
            'article_p2': f'Tus fotos nunca viajan por internet ni se guardan en ningún servidor, garantizando seguridad total.'
        },
        'fr': {
            'title': f'Compresser {fmt_upper} à {sz}KB en Ligne | Sans Serveur',
            'desc': f'Compressez vos {fmt_upper} à moins de {sz}KB gratuitement en ligne. Optimisation locale et ultra-rapide.',
            'keywords': f'compresser {fmt_name} {sz}kb, réduire taille {fmt_name} {sz}kb, compresser png {sz}kb',
            'h1': f'Compresser {fmt_upper} à {sz}KB en Ligne',
            'tabs': f'Compresser à {sz}KB',
            'article_title': f'Comment optimiser des fichiers {fmt_upper} sous le seuil de {sz}KB',
            'article_p1': f'Notre outil calcule précisément les paramètres de qualité pour réduire vos {fmt_upper} sans dépasser la limite de {sz}KB.',
            'article_p2': f"Tout le processus est client-side, gardant vos documents personnels à l'abri du réseau."
        },
        'hi': {
            'title': f'{fmt_upper} साइज {sz}KB तक कम करें online | बिना सर्वर',
            'desc': f'अपनी {fmt_upper} फोटो को मुफ्त में {sz}KB से कम आकार में बदलें। 100% सुरक्षित और स्थानीय कंप्रेसर।',
            'keywords': f'{fmt_name} साइज {sz}kb करें, {sz}kb में {fmt_name} कंप्रेस करें',
            'h1': f'{fmt_upper} साइज {sz}KB तक कम करें ऑनलाइन',
            'tabs': f'{sz}KB तक कंप्रेस करें',
            'article_title': f'{fmt_upper} का आकार {sz}KB से कम कैसे करें',
            'article_p1': f'सरकारी आवेदन और ऑनलाइन फॉर्म के लिए {sz}KB से कम की {fmt_upper} फोटो की आवश्यकता होती है। हमारा टूल इसे तुरंत प्रोसेस करता है।',
            'article_p2': f'आपकी तस्वीरें कभी भी आपके डिवाइस से बाहर नहीं जाती हैं, जिससे पूर्ण गोपनीयता सुनिश्चित होती है।'
        },
        'zh': {
            'title': f'{fmt_upper} 图片压缩至 {sz}KB 在线 | 免费安全本地优化器',
            'desc': f'免费在线将 {fmt_upper} 图片压缩至 {sz}KB 以下。支持批量本地优化，确保隐私安全。',
            'keywords': f'{fmt_name}图片压缩至{sz}kb, 缩小{fmt_name}到{sz}kb, png压缩{sz}kb',
            'h1': f'{fmt_upper} 图片压缩至 {sz}KB 在线',
            'tabs': f'压缩至 {sz}KB',
            'article_title': f'如何将 {fmt_upper} 图片缩减至 {sz}KB 以内',
            'article_p1': f'电子签名、头像或某些表格系统需要 {fmt_upper} 图片绝对小于 {sz}KB。该工具会在本地快速调整画质以适应要求。',
            'article_p2': f'纯浏览器本地运行，数据零上传，极力保障您的隐私和安全。'
        }
    }

def translate_page(filepath, lang, tool_name):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
        
    # Get translated parameters
    # Auto-generate dynamic FAQ translations for all target size and format-specific pages
    match_size = re.match(r'compress-image-to-(\d+)kb', tool_name)
    match_fmt = re.match(r'compress-(jpg|png|jpeg)-to-(\d+)kb', tool_name)
    if (match_size or match_fmt) and tool_name not in TOOL_TRANSLATIONS:
        # Clone translation structure if not pre-defined
        TOOL_TRANSLATIONS[tool_name] = {}
        
    lang_translations = TOOL_TRANSLATIONS.get(tool_name, {}).get(lang, {})
    ui_trans = COMMON_UI.get(lang, {})
    
    if (match_size or match_fmt):
        size = match_size.group(1) if match_size else match_fmt.group(2)
        raw_fmt = "image" if match_size else match_fmt.group(1).upper()
        
        faq_t = FAQ_TEMPLATES.get(lang, FAQ_TEMPLATES['en'])
        translated_fmt = faq_t['format_image'] if raw_fmt == "image" else raw_fmt
        
        # Merge FAQ entries dynamically
        lang_translations["faq_q1"] = faq_t["q1"].format(format=translated_fmt, size=size)
        lang_translations["faq_a1"] = faq_t["a1"].format(format=translated_fmt, size=size)
        lang_translations["faq_q2"] = faq_t["q2"].format(size=size)
        lang_translations["faq_a2"] = faq_t["a2"].format(size=size)
        lang_translations["faq_q3"] = faq_t["q3"]
        lang_translations["faq_a3"] = faq_t["a3"]
        lang_translations["faq_q4"] = faq_t["q4"]
        lang_translations["faq_a4"] = faq_t["a4"]
        lang_translations["faq_q5"] = faq_t["q5"]
        lang_translations["faq_a5"] = faq_t["a5"]
        lang_translations["faq_q6"] = faq_t["q6"]
        lang_translations["faq_a6"] = faq_t["a6"]
        lang_translations["faq_q7"] = faq_t["q7"]
        lang_translations["faq_a7"] = faq_t["a7"]
        
    if not lang_translations:
        print(f"Warning: No translations found for tool '{tool_name}' in language '{lang}'")
        return
        
    # Replace basic headers & layoutlang
    html = html.replace('<html lang="en">', f'<html lang="{lang}">')
    html = html.replace('<html lang="es">', f'<html lang="{lang}">')
    html = html.replace('<html lang="fr">', f'<html lang="{lang}">')
    html = html.replace('<html lang="zh">', f'<html lang="{lang}">')
    html = html.replace('<html lang="hi">', f'<html lang="{lang}">')
    
    # Standard Title & SEO Description
    title_regex = r'<title>(.*?)</title>'
    html = re.sub(title_regex, f'<title>{lang_translations["title"]}</title>', html, flags=re.IGNORECASE)
    
    desc_regex = r'<meta\s+name="description"\s+content="([^"]+)"'
    html = re.sub(desc_regex, f'<meta name="description" content="{lang_translations["desc"]}"', html, flags=re.IGNORECASE)
    
    kw_regex = r'<meta\s+name="keywords"\s+content="([^"]+)"'
    html = re.sub(kw_regex, f'<meta name="keywords" content="{lang_translations["keywords"]}"', html, flags=re.IGNORECASE)
    
    # H1
    h1_regex = r'<h1([^>]*)>.*?</h1>'
    h1_style = ' style="text-align:center; font-size: 28px; margin: 10px 0 20px; background: linear-gradient(135deg, #818cf8, #d8b4fe); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; color: transparent;"'
    if tool_name == 'index.html':
        h1_replacement = f'<h1 class="hero-title">{lang_translations["h1"]}</h1>'
        html = re.sub(r'<h1 class="hero-title">.*?</h1>', h1_replacement, html, flags=re.IGNORECASE)
        # and subtitle
        sub_replacement = f'<p class="hero-subtitle" style="margin: 0 auto;">{lang_translations["sub"]}</p>'
        html = re.sub(r'<p class="hero-subtitle"[^>]*>.*?</p>', sub_replacement, html, flags=re.DOTALL)
    else:
        # Check if the page has style attributes on H1
        html = re.sub(h1_regex, f'<h1\\1>{lang_translations["h1"]}</h1>', html, flags=re.DOTALL)

    # Format Tabs
    if tool_name == 'index.html':
        # replace tab buttons on the main homepage
        tabs_dict = lang_translations["tabs"]
        for target, val in tabs_dict.items():
            html = re.sub(rf'<button class="tab([^>]*)" data-target="{target}">.*?</button>', 
                          f'<button class="tab\\1" data-target="{target}">{val}</button>', html)
    else:
        # replace tab buttons on specialized tool pages dynamically preserving data-target
        html = re.sub(r'<button class="tab active" data-target="([^"]*)">.*?</button>', 
                      lambda m: f'<button class="tab active" data-target="{m.group(1)}">{lang_translations.get("tabs", "")}</button>', html)
                      
    # Drop Zone Translations
    html = re.sub(r'<h2>Select your file here to get started</h2>', f'<h2>{ui_trans["select_file_start"]}</h2>', html)
    html = re.sub(r'<h2>Drop images here</h2>', f'<h2>{ui_trans["drop_images_here"]}</h2>', html)
    html = re.sub(r'<h2>Drop JPG images here</h2>', f'<h2>{ui_trans["drop_images_here"]}</h2>', html)
    html = re.sub(r'<h2>Drop PNG images here</h2>', f'<h2>{ui_trans["drop_images_here"]}</h2>', html)
    html = re.sub(r'<h2>Drop SVG images here</h2>', f'<h2>{ui_trans["drop_images_here"]}</h2>', html)
    html = re.sub(r'<h2>Drop WebP images here</h2>', f'<h2>{ui_trans["drop_images_here"]}</h2>', html)
    
    html = re.sub(r'<p>or drop your file here.</p>', f'<p>{ui_trans["or_drop_here"]}</p>', html)
    html = re.sub(r'<p>Supports formats including.*?</p>', f'<p>{ui_trans["supports_formats"]}</p>', html)
    
    # Drop Zone Select Button
    html = re.sub(r'Select File\s*<svg class="chevron-down"', f'{ui_trans["device"]} <svg class="chevron-down"', html)
    html = re.sub(r'</svg>\s*Device\s*</button>', f'</svg> {ui_trans["device"]} </button>', html)
    html = re.sub(r'</svg>\s*Seleccionar archivo\s*</button>', f'</svg> {ui_trans["device"]} </button>', html)
    
    # Trust Badge
    html = re.sub(r'<div class="trust-badge">(.*?)100% secure — images never leave your device</div>', 
                  f'<div class="trust-badge">\\1{ui_trans["trust_badge"]}</div>', html)
    html = re.sub(r'<div class="trust-badge">(.*?)100% seguro — las imágenes nunca salen de tu dispositivo</div>', 
                  f'<div class="trust-badge">\\1{ui_trans["trust_badge"]}</div>', html)

    # Convert Button Action Text
    html = re.sub(r'<span id="convertBtnText">Convert Images</span>', f'<span id="convertBtnText">{ui_trans["convert_images"]}</span>', html)
    html = re.sub(r'<span id="convertBtnText">Convert to PNG</span>', f'<span id="convertBtnText">{ui_trans["convert_images"]}</span>', html)
    html = re.sub(r'<span id="convertBtnText">Convert to JPG</span>', f'<span id="convertBtnText">{ui_trans["convert_images"]}</span>', html)
    html = re.sub(r'<span id="convertBtnText">Convert to WEBP</span>', f'<span id="convertBtnText">{ui_trans["convert_images"]}</span>', html)
    html = re.sub(r'<span id="convertBtnText">Convert to AVIF</span>', f'<span id="convertBtnText">{ui_trans["convert_images"]}</span>', html)
    html = re.sub(r'<span id="convertBtnText">Convert to ICO</span>', f'<span id="convertBtnText">{ui_trans["convert_images"]}</span>', html)
    html = re.sub(r'<span id="convertBtnText">Convert Photo</span>', f'<span id="convertBtnText">{ui_trans["convert_images"]}</span>', html)
    html = re.sub(r'<span id="convertBtnText">Compress Images</span>', f'<span id="convertBtnText">{ui_trans["convert_images"]}</span>', html)
    
    # Result Card successfully header
    html = re.sub(r'<div class="result-header">[^<]*Converted successfully!</div>', f'<div class="result-header">{ui_trans["converted_successfully"]}</div>', html)
    html = re.sub(r'<div class="result-header">[^<]*Converted to PNG successfully!</div>', f'<div class="result-header">{ui_trans["converted_successfully"]}</div>', html)
    html = re.sub(r'<div class="result-header">[^<]*Converted to JPG successfully!</div>', f'<div class="result-header">{ui_trans["converted_successfully"]}</div>', html)
    html = re.sub(r'<div class="result-header">[^<]*Converted to WEBP successfully!</div>', f'<div class="result-header">{ui_trans["converted_successfully"]}</div>', html)
    html = re.sub(r'<div class="result-header">[^<]*Converted to AVIF successfully!</div>', f'<div class="result-header">{ui_trans["converted_successfully"]}</div>', html)
    html = re.sub(r'<div class="result-header">[^<]*Converted to ICO successfully!</div>', f'<div class="result-header">{ui_trans["converted_successfully"]}</div>', html)
    html = re.sub(r'<div class="result-header">[^<]*Compressed successfully!</div>', f'<div class="result-header">{ui_trans["converted_successfully"]}</div>', html)
    
    # Download Button Action Text
    html = re.sub(r'<span id="downloadText">Download</span>', f'<span id="downloadText">{ui_trans["download"]}</span>', html)
    html = re.sub(r'<span id="downloadText">Download PNG</span>', f'<span id="downloadText">{ui_trans["download"]}</span>', html)
    html = re.sub(r'<span id="downloadText">Download JPG</span>', f'<span id="downloadText">{ui_trans["download"]}</span>', html)
    html = re.sub(r'<span id="downloadText">Download WEBP</span>', f'<span id="downloadText">{ui_trans["download"]}</span>', html)
    html = re.sub(r'<span id="downloadText">Download AVIF</span>', f'<span id="downloadText">{ui_trans["download"]}</span>', html)
    html = re.sub(r'<span id="downloadText">Download ICO</span>', f'<span id="downloadText">{ui_trans["download"]}</span>', html)
    
    # Related Tools Header
    html = re.sub(r'<h3>Related Free Tools</h3>', f'<h3>{ui_trans["related_free_tools"]}</h3>', html)
    html = re.sub(r'<h3>Herramientas gratuitas relacionadas</h3>', f'<h3>{ui_trans["related_free_tools"]}</h3>', html)
    
    # Convert Related Tool anchor HREFs to include language prefix!
    def route_related_anchors(match):
        anchor_body = match.group(1)
        # if the href doesn't already have language prefix, inject it
        if f'href="/{lang}/' not in anchor_body and 'href="/' in anchor_body:
            anchor_body = anchor_body.replace('href="/', f'href="/{lang}/')
        return f'<a {anchor_body}>'
        
    html = re.sub(r'<a\s+([^>]*class="related-tools"[^>]*)>', route_related_anchors, html)
    # also standard links inside section.related-tools
    def route_section_anchors(match):
        section_content = match.group(1)
        # convert <a href="/something"> to <a href="/lang/something">
        new_section = re.sub(r'href="/(?!de|es|fr|hi|zh|privacy-policy|terms|about|contact|blog)([a-zA-Z0-9_-]+)"', rf'href="/{lang}/\1"', section_content)
        new_section = re.sub(r'href="/"', rf'href="/{lang}/"', new_section)
        return f'<section class="related-tools glass-panel">{new_section}</section>'
        
    html = re.sub(r'<section class="related-tools glass-panel">(.*?)</section>', route_section_anchors, html, flags=re.DOTALL)
    
    # Footer UI translation
    html = re.sub(r'<div class="footer-copy">(.*?)Your files never leave your device(.*?)</div>', 
                  f'<div class="footer-copy">\\1{ui_trans["footer_copy"]}\\2</div>', html)
    html = re.sub(r'<div class="footer-copy">(.*?)Tus archivos nunca salen de tu dispositivo(.*?)</div>', 
                  f'<div class="footer-copy">\\1{ui_trans["footer_copy"]}\\2</div>', html)
                  
    # Policy links translation
    html = html.replace('Privacy Policy</a>', f'{ui_trans["privacy_policy"]}</a>')
    html = html.replace('Terms of Service</a>', f'{ui_trans["terms_of_service"]}</a>')
    html = html.replace('About Us</a>', f'{ui_trans["about_us"]}</a>')
    html = html.replace('Contact</a>', f'{ui_trans["contact"]}</a>')
    html = html.replace('Política de Privacidad</a>', f'{ui_trans["privacy_policy"]}</a>')
    html = html.replace('Términos de Servicio</a>', f'{ui_trans["terms_of_service"]}</a>')
    html = html.replace('Sobre Nosotros</a>', f'{ui_trans["about_us"]}</a>')

    # Related tools names translations
    tools_names = {
        'de': {
            'Convert Multiple Formats': 'Mehrere Formate konvertieren',
            'Convert JPG to PNG': 'JPG in PNG umwandeln',
            'Convert WebP to JPG': 'WebP in JPG umwandeln',
            'Convert PNG to JPG': 'PNG in JPG umwandeln',
            'Compress Image Files': 'Bilddateien komprimieren',
            'Convert Multiple': 'Mehrere Formate konvertieren',
            'Compress Image (Custom Size)': 'Bild komprimieren (Custom)',
            'Compress Image to 10KB': 'Bild auf 10KB komprimieren',
            'Compress Image to 20KB': 'Bild auf 20KB komprimieren',
            'Compress Image to 30KB': 'Bild auf 30KB komprimieren',
            'Compress Image to 50KB': 'Bild auf 50KB komprimieren',
            'Compress Image to 100KB': 'Bild auf 100KB komprimieren',
            'Compress Image to 200KB': 'Bild auf 200KB komprimieren',
            'Compress Image to 500KB': 'Bild auf 500KB komprimieren',
            'Compress JPG to 100KB': 'JPG auf 100KB komprimieren',
            'Compress PNG to 100KB': 'PNG auf 100KB komprimieren',
            'Compress JPEG to 100KB': 'JPEG auf 100KB komprimieren'
        },
        'es': {
            'Convert Multiple Formats': 'Convertir múltiples formatos',
            'Convert JPG to PNG': 'Convertir JPG a PNG',
            'Convert WebP to JPG': 'Convertir WebP a JPG',
            'Convert PNG to JPG': 'Convertir PNG a JPG',
            'Compress Image Files': 'Comprimir imágenes',
            'Convert Multiple': 'Convertir múltiples formatos',
            'Compress Image (Custom Size)': 'Comprimir imagen (Personalizado)',
            'Compress Image to 10KB': 'Comprimir imagen a 10KB',
            'Compress Image to 20KB': 'Comprimir imagen a 20KB',
            'Compress Image to 30KB': 'Comprimir imagen a 30KB',
            'Compress Image to 50KB': 'Comprimir imagen a 50KB',
            'Compress Image to 100KB': 'Comprimir imagen a 100KB',
            'Compress Image to 200KB': 'Comprimir imagen a 200KB',
            'Compress Image to 500KB': 'Comprimir imagen a 500KB',
            'Compress JPG to 100KB': 'Comprimir JPG a 100KB',
            'Compress PNG to 100KB': 'Comprimir PNG a 100KB',
            'Compress JPEG to 100KB': 'Comprimir JPEG a 100KB'
        },
        'fr': {
            'Convert Multiple Formats': 'Convertir plusieurs formats',
            'Convert JPG to PNG': 'Convertir JPG en PNG',
            'Convert WebP to JPG': 'Convertir WebP en JPG',
            'Convert PNG to JPG': 'Convertir PNG en JPG',
            'Compress Image Files': 'Compresser des images',
            'Convert Multiple': 'Convertir plusieurs formats',
            'Compress Image (Custom Size)': 'Compresser image (Personnalisé)',
            'Compress Image to 10KB': 'Compresser Image à 10KB',
            'Compress Image to 20KB': 'Compresser Image à 20KB',
            'Compress Image to 30KB': 'Compresser Image à 30KB',
            'Compress Image to 50KB': 'Compresser Image à 50KB',
            'Compress Image to 100KB': 'Compresser Image à 100KB',
            'Compress Image to 200KB': 'Compresser Image à 200KB',
            'Compress Image to 500KB': 'Compresser Image à 500KB',
            'Compress JPG to 100KB': 'Compresser JPG à 100KB',
            'Compress PNG to 100KB': 'Compresser PNG à 100KB',
            'Compress JPEG to 100KB': 'Compresser JPEG à 100KB'
        },
        'hi': {
            'Convert Multiple Formats': 'कई प्रारूप बदलें',
            'Convert JPG to PNG': 'JPG से PNG बदलें',
            'Convert WebP to JPG': 'WebP से JPG बदलें',
            'Convert PNG to JPG': 'PNG से JPG बदलें',
            'Compress Image Files': 'इमेज फाइल कंप्रेस करें',
            'Convert Multiple': 'कई प्रारूप बदलें',
            'Compress Image (Custom Size)': 'इमेज कंप्रेस करें (कस्टम)',
            'Compress Image to 10KB': 'इमेज साइज 10KB करें',
            'Compress Image to 20KB': 'इमेज साइज 20KB करें',
            'Compress Image to 30KB': 'इमेज साइज 30KB करें',
            'Compress Image to 50KB': 'इमेज साइज 50KB करें',
            'Compress Image to 100KB': 'इमेज साइज 100KB करें',
            'Compress Image to 200KB': 'इमेज साइज 200KB करें',
            'Compress Image to 500KB': 'इमेज साइज 500KB करें',
            'Compress JPG to 100KB': 'JPG को 100KB कंप्रेस करें',
            'Compress PNG to 100KB': 'PNG को 100KB कंप्रेस करें',
            'Compress JPEG to 100KB': 'JPEG को 100KB कंप्रेस करें'
        },
        'zh': {
            'Convert Multiple Formats': '转换多种格式',
            'Convert JPG to PNG': 'JPG 转 PNG 转换',
            'Convert WebP to JPG': 'WebP 转 JPG 转换',
            'Convert PNG to JPG': 'PNG 转 JPG 转换',
            'Compress Image Files': '压缩图片文件',
            'Convert Multiple': '转换多种格式',
            'Compress Image (Custom Size)': '压缩图片（自定义大小）',
            'Compress Image to 10KB': '图片压缩至 10KB',
            'Compress Image to 20KB': '图片压缩至 20KB',
            'Compress Image to 30KB': '图片压缩至 30KB',
            'Compress Image to 50KB': '图片压缩至 50KB',
            'Compress Image to 100KB': '图片压缩至 100KB',
            'Compress Image to 200KB': '图片压缩至 200KB',
            'Compress Image to 500KB': '图片压缩至 500KB',
            'Compress JPG to 100KB': 'JPG 图片压缩至 100KB',
            'Compress PNG to 100KB': 'PNG 图片压缩至 100KB',
            'Compress JPEG to 100KB': 'JPEG 图片压缩至 100KB'
        }
    }
    
    trans_map = tools_names.get(lang, {})
    for eng, local in trans_map.items():
        html = html.replace(f'>{eng}</a>', f'>{local}</a>')

    # Compile dynamic SEO Article & FAQs!
    seo_article = f"""<h2>{lang_translations["article_title"]}</h2>
    <p>{lang_translations["article_p1"]}</p>
    <p>{lang_translations["article_p2"]}</p>
    
    <div class="faq-section">
      <h3>{ 'Häufig gestellte Fragen' if lang=='de' else 'Preguntas frecuentes' if lang=='es' else 'Foire aux questions' if lang=='fr' else 'अक्सर पूछे जाने वाले प्रश्न' if lang=='hi' else '常见问题解答' }</h3>
      <div class="faq-item">
        <div class="faq-question">{lang_translations["faq_q1"]}</div>
        <div class="faq-answer">{lang_translations["faq_a1"]}</div>
      </div>
      <div class="faq-item">
        <div class="faq-question">{lang_translations["faq_q2"]}</div>
        <div class="faq-answer">{lang_translations["faq_a2"]}</div>
      </div>"""
      
    for idx in range(3, 9):
        q_key = f"faq_q{idx}"
        a_key = f"faq_a{idx}"
        if q_key in lang_translations:
            seo_article += f"""
      <div class="faq-item">
        <div class="faq-question">{lang_translations[q_key]}</div>
        <div class="faq-answer">{lang_translations[a_key]}</div>
      </div>"""
      
    seo_article += "\n    </div>"
    
    # replace the entire article.seo-article block
    html = re.sub(r'<article class="seo-article glass-panel">.*?</article>', 
                  f'<article class="seo-article glass-panel">\n      {seo_article}\n    </article>', html, flags=re.DOTALL)

    # Build and inject the JSON-LD FAQ schema matching the translated questions!
    faq_entities = [
        {
            "@type": "Question",
            "name": lang_translations["faq_q1"],
            "acceptedAnswer": {"@type": "Answer", "text": lang_translations["faq_a1"]}
        },
        {
            "@type": "Question",
            "name": lang_translations["faq_q2"],
            "acceptedAnswer": {"@type": "Answer", "text": lang_translations["faq_a2"]}
        }
    ]
    for idx in range(3, 9):
        q_key = f"faq_q{idx}"
        a_key = f"faq_a{idx}"
        if q_key in lang_translations:
            faq_entities.append({
                "@type": "Question",
                "name": lang_translations[q_key],
                "acceptedAnswer": {"@type": "Answer", "text": lang_translations[a_key]}
            })
        
    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": faq_entities
    }
    
    # Build and inject the JSON-LD HowTo schema!
    is_compress_tool = "compress" in tool_name or tool_name == "index.html"
    ht_trans = HOWTO_TRANSLATIONS.get(lang, HOWTO_TRANSLATIONS['en'])
    
    ht_title = ht_trans['compress_title'] if is_compress_tool else ht_trans['convert_title']
    step2_name = ht_trans['step2_compress_name'] if is_compress_tool else ht_trans['step2_convert_name']
    step2_text = ht_trans['step2_compress_text'] if is_compress_tool else ht_trans['step2_convert_text']
    
    tool_suffix = "" if tool_name == "index.html" else tool_name.strip('/')
    if tool_suffix:
        page_url = f"https://www.imglabconverter.com/{lang}/{tool_suffix}" if lang != 'en' else f"https://www.imglabconverter.com/{tool_suffix}"
    else:
        page_url = f"https://www.imglabconverter.com/{lang}" if lang != 'en' else "https://www.imglabconverter.com/"
    
    howto_schema = {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": ht_title,
        "step": [
            {
                "@type": "HowToStep",
                "name": ht_trans['step1_name'],
                "text": ht_trans['step1_text'],
                "url": page_url
            },
            {
                "@type": "HowToStep",
                "name": step2_name,
                "text": step2_text,
                "url": page_url
            },
            {
                "@type": "HowToStep",
                "name": ht_trans['step3_name'],
                "text": ht_trans['step3_text'],
                "url": page_url
            }
        ]
    }
    
    faq_schema_str = json.dumps(faq_schema, ensure_ascii=False, indent=2)
    howto_schema_str = json.dumps(howto_schema, ensure_ascii=False, indent=2)
    
    schema_script_block = f'''<script type="application/ld+json">
{faq_schema_str}
</script>
<script type="application/ld+json">
{howto_schema_str}
</script>'''
  
    # Strip any existing ld+json schemas
    html = re.sub(r'<script type="application/ld\+json">.*?</script>', '', html, flags=re.DOTALL)
    # inject the new translated JSON-LD schema right before </head>
    html = html.replace('</head>', schema_script_block + '\n</head>')

    # Translate custom UI settings for resize-image
    if tool_name == 'resize-image':
        resize_trans = {
            'de': {
                'Target Dimensions': 'Zielabmessungen',
                'Width (px)': 'Breite (px)',
                'Height (px)': 'Höhe (px)',
                'Maintain aspect ratio (enter one value to auto-calculate the other)': 'Seitenverhältnis beibehalten (einen Wert eingeben, um den anderen automatisch zu berechnen)'
            },
            'es': {
                'Target Dimensions': 'Dimensiones de Destino',
                'Width (px)': 'Ancho (px)',
                'Height (px)': 'Alto (px)',
                'Maintain aspect ratio (enter one value to auto-calculate the other)': 'Mantener relación de aspecto (ingrese un valor para calcular automáticamente el otro)'
            },
            'fr': {
                'Target Dimensions': 'Dimensions Cibles',
                'Width (px)': 'Largeur (px)',
                'Height (px)': 'Hauteur (px)',
                'Maintain aspect ratio (enter one value to auto-calculate the other)': "Conserver le ratio d'aspect (entrer une valeur pour calculer l'autre automatiquement)"
            },
            'hi': {
                'Target Dimensions': 'लक्षित आयाम',
                'Width (px)': 'चौड़ाई (px)',
                'Height (px)': 'ऊंचाई (px)',
                'Maintain aspect ratio (enter one value to auto-calculate the other)': 'आस्पेक्ट रेशियो बनाए रखें (दूसरा ऑटो-कैलकुलेट करने के लिए एक वैल्यू डालें)'
            },
            'zh': {
                'Target Dimensions': '目标尺寸',
                'Width (px)': '宽度 (px)',
                'Height (px)': '高度 (px)',
                'Maintain aspect ratio (enter one value to auto-calculate the other)': '保持比例（输入一个值，另一个将自动计算）'
            }
        }
        if lang in resize_trans:
            for eng_txt, lang_txt in resize_trans[lang].items():
                html = html.replace(eng_txt, lang_txt)

    # Translate custom UI settings for watermark-image
    if tool_name == 'watermark-image':
        watermark_trans = {
            'de': {
                'Watermark Settings': 'Wasserzeichen-Einstellungen',
                'Watermark Text (Leave empty for none)': 'Wasserzeichen-Text (Leer lassen für keins)',
                'Text Size (px)': 'Textgröße (px)',
                'Position': 'Position',
                'Bottom Right': 'Unten rechts',
                'Bottom Left': 'Unten links',
                'Top Right': 'Oben rechts',
                'Top Left': 'Oben links',
                'Center': 'Mitte'
            },
            'es': {
                'Watermark Settings': 'Ajustes de Marca de Agua',
                'Watermark Text (Leave empty for none)': 'Texto de la marca de agua (dejar vacío para ninguno)',
                'Text Size (px)': 'Tamaño del texto (px)',
                'Position': 'Posición',
                'Bottom Right': 'Abajo a la derecha',
                'Bottom Left': 'Abajo a la izquierda',
                'Top Right': 'Arriba a la derecha',
                'Top Left': 'Arriba a la izquierda',
                'Center': 'Centro'
            },
            'fr': {
                'Watermark Settings': 'Paramètres du Filigrane',
                'Watermark Text (Leave empty for none)': 'Texte du filigrane (laisser vide pour aucun)',
                'Text Size (px)': 'Taille du texte (px)',
                'Position': 'Position',
                'Bottom Right': 'En bas à droite',
                'Bottom Left': 'En bas à gauche',
                'Top Right': 'En haut à droite',
                'Top Left': 'En haut à gauche',
                'Center': 'Centre'
            },
            'hi': {
                'Watermark Settings': 'वॉटरमार्क सेटिंग्स',
                'Watermark Text (Leave empty for none)': 'वॉटरमार्क टेक्स्ट (हटाने के लिए खाली छोड़ें)',
                'Text Size (px)': 'टेक्स्ट का आकार (px)',
                'Position': 'स्थिति',
                'Bottom Right': 'नीचे दाईं ओर',
                'Bottom Left': 'नीचे बाईं ओर',
                'Top Right': 'ऊपर दाईं ओर',
                'Top Left': 'ऊपर बाईं ओर',
                'Center': 'केंद्र'
            },
            'zh': {
                'Watermark Settings': '水印设置',
                'Watermark Text (Leave empty for none)': '水印文字（留空表示不添加）',
                'Text Size (px)': '文字大小 (px)',
                'Position': '位置',
                'Bottom Right': '右下角',
                'Bottom Left': '左下角',
                'Top Right': '右上角',
                'Top Left': '左上角',
                'Center': '正中间'
            }
        }
        if lang in watermark_trans:
            for eng_txt, lang_txt in watermark_trans[lang].items():
                html = html.replace(eng_txt, lang_txt)

    return html

def main():
    all_tools = [
        "compress-image",
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
        "heic-to-jpg",
        "jpeg-to-webp",
        "jpg-to-avif",
        "jpg-to-png",
        "photo-to-black-and-white",
        "png-to-avif",
        "png-to-ico",
        "png-to-jpg",
        "svg-to-jpg",
        "svg-to-png",
        "webp-to-jpg",
        "webp-to-png",
        "resize-image",
        "watermark-image",
        "jpg-to-pdf",
        "jpg-to-tiff",
        "tiff-to-jpg"
    ]
    
    # 1. Translate Root Homepages
    for lang in languages:
        src_path = os.path.join(base_dir, "index.html")
        dest_dir = os.path.join(base_dir, lang)
        os.makedirs(dest_dir, exist_ok=True)
        dest_path = os.path.join(dest_dir, "index.html")
        
        translated_html = translate_page(src_path, lang, "index.html")
        if translated_html:
            # fix canonical URL for the translated homepage
            translated_html = re.sub(r'<link rel="canonical" href="https://www.imglabconverter.com/"', 
                                     f'<link rel="canonical" href="https://www.imglabconverter.com/{lang}"', translated_html)
            with open(dest_path, 'w', encoding='utf-8') as f:
                f.write(translated_html)
            print(f"Compiled translated homepage: {lang}/index.html")
            
    # 2. Translate all 15 sub-tool converter pages
    for tool in all_tools:
        src_path = os.path.join(base_dir, tool, "index.html")
        if not os.path.exists(src_path):
            print(f"Warning: Root tool index.html not found for '{tool}' at {src_path}")
            continue
            
        for lang in languages:
            dest_dir = os.path.join(base_dir, lang, tool)
            os.makedirs(dest_dir, exist_ok=True)
            dest_path = os.path.join(dest_dir, "index.html")
            
            translated_html = translate_page(src_path, lang, tool)
            if translated_html:
                # fix canonical URL for the translated subpage
                # support matching both with and without trailing slash in the template's canonical tag
                translated_html = re.sub(rf'<link rel="canonical" href="https://www.imglabconverter.com/{tool}/?"', 
                                         f'<link rel="canonical" href="https://www.imglabconverter.com/{lang}/{tool}"', translated_html)
                # fix form actions or data target attributes if any
                with open(dest_path, 'w', encoding='utf-8') as f:
                    f.write(translated_html)
                print(f"Compiled translated page: {lang}/{tool}/index.html")

if __name__ == "__main__":
    main()
