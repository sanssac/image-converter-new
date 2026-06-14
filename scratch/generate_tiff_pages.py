import os
import re

langs = ['en', 'de', 'es', 'fr', 'hi', 'zh']
base_dir = r"c:\image converter new"

# Translations for tiff-to-jpg
tiff_to_jpg_trans = {
    'en': {
        'title': 'Convert TIFF to JPG Online Free | Image Converter',
        'desc': 'Instantly convert TIFF or TIF files to JPG format. Free, 100% private, client-side TIFF conversion — no uploads needed, works on any browser.',
        'keywords': 'tiff to jpg, convert tiff, tiff to jpeg, free tiff converter online',
        'h1': 'Convert TIFF to JPG Online Free',
        'tab_active': 'Converting to JPG',
        'drop_h2': 'Drop TIFF images here',
        'drop_p': 'Supports formats including JPG, WEBP, PNG, TIFF, HEIC',
        'btn_convert': 'Convert to JPG',
        'res_header': 'Converted to JPG successfully!',
        'res_download': 'Download JPG',
        'related_h3': 'Related Free Tools',
        'related_links': [
            ('<a href="/">Convert Multiple Formats</a>', '<a href="/">Convert Multiple Formats</a>'),
            ('<a href="/heic-to-jpg">Convert HEIC to JPG</a>', '<a href="/heic-to-jpg">Convert HEIC to JPG</a>'),
            ('<a href="/png-to-jpg">Convert PNG to JPG</a>', '<a href="/png-to-jpg">Convert PNG to JPG</a>'),
            ('<a href="/jpg-to-tiff">Convert JPG to TIFF</a>', '<a href="/jpg-to-tiff">Convert JPG to TIFF</a>'),
        ],
        'article_h2': 'How to Convert TIFF to JPG Online Securely',
        'article_p1': 'TIFF (Tagged Image File Format) is widely used in publishing, graphic design, and medical imaging due to its ability to store high-quality raster graphics. However, TIFF files are often extremely large and unsupported by web browsers or social media platforms. Converting TIFF to JPG is the easiest way to make these images easy to share and view on any device.',
        'article_p2': 'Our converter processes your images entirely in the browser using HTML5 technologies. Your files never touch a remote server, ensuring complete confidentiality for your private files and professional projects.',
        'faq_h3': 'Frequently Asked Questions',
        'faq1_q': 'Will I lose image quality during conversion?',
        'faq1_a': 'Converting a TIFF to a JPG uses lossy JPEG compression, which might slightly reduce quality in exchange for a significantly smaller file size. Our converter uses high-quality settings to ensure the visual difference is minimal.',
        'faq2_q': 'Can I convert multiple TIFF files at once?',
        'faq2_a': 'Yes! You can drag and drop multiple TIFF files at once. They will be processed in a batch, and you can download them all as a single ZIP file.',
        'faq3_q': 'Are my TIFF files uploaded to a server?',
        'faq3_a': 'No. This tool runs 100% inside your browser. All decoding and encoding happen locally on your device, ensuring complete privacy and security.',
        'footer_copy': 'Your files never leave your device — 100% client-side rendering.'
    },
    'de': {
        'title': 'TIFF in JPG Konverter | Kostenlos & Online',
        'desc': 'Konvertieren Sie TIFF- oder TIF-Bilder online in JPG. 100% sicher und clientseitig - keine Uploads erforderlich.',
        'keywords': 'tiff in jpg, tiff to jpg, tiff konvertieren, tiff dateien umwandeln',
        'h1': 'TIFF in JPG Konverter',
        'tab_active': 'TIFF in JPG konvertieren',
        'drop_h2': 'TIFF-Bilder hierher ziehen',
        'drop_p': 'Unterstützt JPG, PNG, WEBP, HEIC, TIFF, SVG',
        'btn_convert': 'In JPG konvertieren',
        'res_header': 'Erfolgreich konvertiert!',
        'res_download': 'Herunterladen',
        'related_h3': 'Verwandte kostenlose Werkzeuge',
        'related_links': [
            ('<a href="/de/">Mehrere Formate konvertieren</a>', '<a href="/de/">Mehrere Formate konvertieren</a>'),
            ('<a href="/de/heic-to-jpg">HEIC in JPG umwandeln</a>', '<a href="/de/heic-to-jpg">HEIC in JPG umwandeln</a>'),
            ('<a href="/de/png-to-jpg">PNG in JPG umwandeln</a>', '<a href="/de/png-to-jpg">PNG in JPG umwandeln</a>'),
            ('<a href="/de/jpg-to-tiff">JPG in TIFF umwandeln</a>', '<a href="/de/jpg-to-tiff">JPG in TIFF umwandeln</a>'),
        ],
        'article_h2': 'So konvertieren Sie TIFF sicher online in JPG',
        'article_p1': 'TIFF (Tagged Image File Format) wird aufgrund seiner hohen Qualität häufig im Druck und Grafikdesign verwendet. Diese Dateien sind jedoch oft riesig und werden von Browsern oder sozialen Medien nicht standardmäßig unterstützt. Die Konvertierung in JPG ist der einfachste Weg, um diese Bilder auf jedem Gerät kompatibel zu machen.',
        'article_p2': 'Unser Konverter läuft komplett lokal in Ihrem Browser. Ihre sensiblen Fotos werden nicht an Server übertragen, sodass Ihre Privatsphäre vollständig geschützt bleibt.',
        'faq_h3': 'Häufig gestellte Fragen',
        'faq1_q': 'Verliere ich beim Konvertieren an Qualität?',
        'faq1_a': 'JPG verwendet eine verlustbehaftete Komprimierung, um kleinere Dateigrößen zu erzielen. Unser Konverter verwendet jedoch hohe Qualitätseinstellungen, damit der visuelle Unterschied minimal bleibt.',
        'faq2_q': 'Kann ich mehrere TIFF-Dateien gleichzeitig konvertieren?',
        'faq2_a': 'Ja, unser Konverter unterstützt die Stapelkonvertierung. Ziehen Sie einfach mehrere TIFF-Dateien hinein und laden Sie sie als ZIP-Datei herunter.',
        'faq3_q': 'Werden meine Bilder auf einen Server hochgeladen?',
        'faq3_a': 'Nein, die Konvertierung findet vollständig lokal in Ihrem Browser statt. Ihre Dateien verlassen Ihr Gerät nicht.',
        'footer_copy': 'Ihre Dateien verlassen Ihr Gerät nie — 100% clientseitige Verarbeitung.'
    },
    'es': {
        'title': 'Convertidor de TIFF a JPG Gratis | En Línea',
        'desc': 'Convierta archivos TIFF o TIF a formato JPG al instante. Gratis, 100% privado y en su navegador, sin necesidad de subir archivos.',
        'keywords': 'tiff a jpg, convertir tiff, tiff a jpeg, convertidor tiff en linea',
        'h1': 'Convertidor de TIFF a JPG',
        'tab_active': 'Convertir a JPG',
        'drop_h2': 'Arrastre imágenes TIFF aquí',
        'drop_p': 'Soporta formatos como JPG, PNG, WEBP, HEIC, TIFF, SVG',
        'btn_convert': 'Convertir a JPG',
        'res_header': '¡Convertido con éxito!',
        'res_download': 'Descargar',
        'related_h3': 'Herramientas Relacionadas',
        'related_links': [
            ('<a href="/es/">Convertir múltiples formatos</a>', '<a href="/es/">Convertir múltiples formatos</a>'),
            ('<a href="/es/heic-to-jpg">Convertir HEIC a JPG</a>', '<a href="/es/heic-to-jpg">Convertir HEIC a JPG</a>'),
            ('<a href="/es/png-to-jpg">Convertir PNG a JPG</a>', '<a href="/es/png-to-jpg">Convertir PNG a JPG</a>'),
            ('<a href="/es/jpg-to-tiff">Convertir JPG a TIFF</a>', '<a href="/es/jpg-to-tiff">Convertir JPG a TIFF</a>'),
        ],
        'article_h2': 'Cómo convertir TIFF a JPG en línea de forma segura',
        'article_p1': 'El formato TIFF (Tagged Image File Format) es muy utilizado en diseño gráfico y publicaciones debido a su alta calidad. Sin embargo, suelen ser archivos muy pesados y no son compatibles con navegadores web o redes sociales. Convertir TIFF a JPG es la forma más rápida y fácil de compartirlos y verlos en cualquier dispositivo.',
        'article_p2': 'La conversión se procesa localmente en su dispositivo. Garantizamos la máxima privacidad para sus imágenes y archivos.',
        'faq_h3': 'Preguntas Frecuentes',
        'faq1_q': '¿Perderé calidad de imagen al convertir?',
        'faq1_a': 'La conversión a JPG utiliza compresión con pérdida, lo que reduce el tamaño del archivo a cambio de una pequeña pérdida de detalles. Nuestro convertidor utiliza una configuración de alta calidad para garantizar que el cambio visual sea imperceptible.',
        'faq2_q': '¿Puedo convertir varios archivos TIFF a la vez?',
        'faq2_a': 'Sí, nuestro convertidor admite la conversión por lotes. Simplemente arrastre varios archivos TIFF y descárguelos todos en un único archivo ZIP.',
        'faq3_q': '¿Se suben mis archivos TIFF a algún servidor?',
        'faq3_a': 'No. Esta herramienta se ejecuta al 100% en su navegador local. Todos los procesos se realizan en su dispositivo, garantizando total privacidad.',
        'footer_copy': 'Sus archivos nunca salen de su dispositivo — 100% local en su navegador.'
    },
    'fr': {
        'title': 'Convertisseur TIFF en JPG Gratuit | En Ligne',
        'desc': 'Convertissez instantanément vos fichiers TIFF ou TIF en JPG. Gratuit, 100% privé et local dans votre navigateur — aucun envoi requis.',
        'keywords': 'tiff en jpg, convertir tiff, tiff en jpeg, convertisseur tiff gratuit',
        'h1': 'Convertisseur TIFF en JPG',
        'tab_active': 'Convertir en JPG',
        'drop_h2': 'Déposez les images TIFF ici',
        'drop_p': 'Prend en charge les formats JPG, PNG, WEBP, HEIC, TIFF, SVG',
        'btn_convert': 'Convertir en JPG',
        'res_header': 'Converti avec succès !',
        'res_download': 'Télécharger',
        'related_h3': 'Outils Connexes',
        'related_links': [
            ('<a href="/fr/">Convertir plusieurs formats</a>', '<a href="/fr/">Convertir plusieurs formats</a>'),
            ('<a href="/fr/heic-to-jpg">Convertir HEIC en JPG</a>', '<a href="/fr/heic-to-jpg">Convertir HEIC en JPG</a>'),
            ('<a href="/fr/png-to-jpg">Convertir PNG en JPG</a>', '<a href="/fr/png-to-jpg">Convertir PNG en JPG</a>'),
            ('<a href="/fr/jpg-to-tiff">Convertir JPG en TIFF</a>', '<a href="/fr/jpg-to-tiff">Convertir JPG en TIFF</a>'),
        ],
        'article_h2': 'Comment convertir TIFF en JPG en ligne en toute sécurité',
        'article_p1': "Le format TIFF (Tagged Image File Format) est largement utilisé dans l'édition et le graphisme pour sa qualité exceptionnelle. Cependant, les fichiers TIFF sont volumineux et incompatibles avec la plupart des navigateurs web ou des réseaux sociaux. Les convertir en JPG permet de les partager facilement et de les lire sur n'importe quel appareil.",
        'article_p2': 'Toutes les opérations de décodage et de compression ont lieu localement dans votre navigateur sans transfert de données externe.',
        'faq_h3': 'Foire Aux Questions',
        'faq1_q': 'Vais-je perdre en qualité lors de la conversion ?',
        'faq1_a': 'La conversion vers le format JPG applique une compression avec perte, ce qui réduit considérablement la taille du fichier. Notre outil utilise des paramètres de haute qualité pour minimiser la perte visuelle.',
        'faq2_q': 'Puis-je convertir plusieurs fichiers TIFF à la fois ?',
        'faq2_a': 'Oui, notre outil gère la conversion par lots. Déposez plusieurs fichiers TIFF et téléchargez-les instantanément sous forme d\'archive ZIP.',
        'faq3_q': 'Mes fichiers sont-ils envoyés sur un serveur ?',
        'faq3_a': 'Non. Ce convertisseur fonctionne à 100% dans votre navigateur. Le traitement s\'effectue localement, protégeant ainsi votre vie privée.',
        'footer_copy': 'Vos fichiers ne quittent jamais votre appareil — 100% traitement client.'
    },
    'hi': {
        'title': 'TIFF से JPG कनवर्टर ऑनलाइन | मुफ्त और सुरक्षित',
        'desc': 'मुफ़्त में TIFF या TIF फ़ाइलों को JPG फॉर्मेट में तुरंत बदलें। 100% सुरक्षित और स्थानीय ब्राउज़र कनवर्टर, कोई अपलोड नहीं।',
        'keywords': 'tiff to jpg, tiff से jpg, tiff कनवर्टर, tiff फ़ाइल बदलें',
        'h1': 'TIFF से JPG कनवर्टर',
        'tab_active': 'TIFF से JPG में बदलें',
        'drop_h2': 'TIFF इमेज यहाँ ड्राप करें',
        'drop_p': 'JPG, PNG, WEBP, HEIC, TIFF, SVG फॉर्मेट समर्थित हैं',
        'btn_convert': 'JPG में बदलें',
        'res_header': 'सफलतापूर्वक बदला गया!',
        'res_download': 'डाउनलोड करें',
        'related_h3': 'संबंधित मुफ्त उपकरण',
        'related_links': [
            ('<a href="/hi/">कई प्रारूपों को बदलें</a>', '<a href="/hi/">कई प्रारूपों को बदलें</a>'),
            ('<a href="/hi/heic-to-jpg">HEIC से JPG कनवर्ट करें</a>', '<a href="/hi/heic-to-jpg">HEIC से JPG कनवर्ट करें</a>'),
            ('<a href="/hi/png-to-jpg">PNG से JPG कनवर्ट करें</a>', '<a href="/hi/png-to-jpg">PNG से JPG कनवर्ट करें</a>'),
            ('<a href="/hi/jpg-to-tiff">JPG से TIFF कनवर्ट करें</a>', '<a href="/hi/jpg-to-tiff">JPG से TIFF कनवर्ट करें</a>'),
        ],
        'article_h2': 'TIFF को JPG में सुरक्षित रूप से ऑनलाइन कैसे बदलें',
        'article_p1': 'TIFF (Tagged Image File Format) का उपयोग प्रकाशन और ग्राफिक डिज़ाइन में उच्च गुणवत्ता वाली छवियों के लिए किया जाता है। हालाँकि, ये फाइलें अक्सर बहुत बड़ी होती हैं और वेब ब्राउज़र या सोशल मीडिया पर प्रदर्शित नहीं हो पाती हैं। TIFF को JPG में बदलना इन्हें किसी भी डिवाइस पर देखने योग्य बनाने का सबसे आसान तरीका है।',
        'article_p2': 'यह रूपांतरण पूरी तरह से आपके ब्राउज़र में होता है, जो आपकी व्यक्तिगत और व्यावसायिक फ़ाइलों के लिए पूर्ण गोपनीयता सुनिश्चित करता है।',
        'faq_h3': 'अक्सर पूछे जाने वाले प्रश्न',
        'faq1_q': 'क्या कनवर्ट करने से गुणवत्ता कम हो जाएगी?',
        'faq1_a': 'JPG कंप्रेशन से फ़ाइल का आकार बहुत छोटा हो जाता है लेकिन गुणवत्ता में मामूली कमी आ सकती है। हमारा कनवर्टर सर्वोत्तम सेटिंग्स का उपयोग करता है ताकि अंतर पता न चले।',
        'faq2_q': 'क्या मैं एक साथ कई TIFF फाइलें कनवर्ट कर सकता हूँ?',
        'faq2_a': 'हाँ! आप एक साथ कई TIFF फ़ाइलों को खींचकर छोड़ सकते हैं। वे बैच में प्रोसेस होंगी और आप उन्हें एक ZIP फ़ाइल में डाउनलोड कर सकते हैं।',
        'faq3_q': 'क्या मेरी फाइलें किसी सर्वर पर अपलोड की जाती हैं?',
        'faq3_a': 'नहीं। यह टूल पूरी तरह से आपके ब्राउज़र में काम करता है। आपका डेटा आपके डिवाइस पर ही सुरक्षित रहता है।',
        'footer_copy': 'आपकी फाइलें कभी आपके डिवाइस से बाहर नहीं जातीं — 100% स्थानीय कनवर्टर।'
    },
    'zh': {
        'title': 'TIFF 转 JPG 转换器 | 免费在线 TIFF 图像转换',
        'desc': '在线免费将 TIFF 或 TIF 文件转换为 JPG 格式。100% 本地隐私保护，无需上传，可在任何浏览器中使用。',
        'keywords': 'tiff转jpg, tiff to jpg, tiff转换器, 免费在线tiff转换',
        'h1': 'TIFF 转 JPG 转换器',
        'tab_active': '转换为 JPG',
        'drop_h2': '将 TIFF 图片拖到此处',
        'drop_p': '支持 JPG、PNG、WEBP、HEIC、TIFF、SVG 等格式',
        'btn_convert': '转换为 JPG',
        'res_header': '转换成功！',
        'res_download': '下载',
        'related_h3': '相关免费工具',
        'related_links': [
            ('<a href="/zh/">转换多种格式</a>', '<a href="/zh/">转换多种格式</a>'),
            ('<a href="/zh/heic-to-jpg">HEIC 转 JPG 转换</a>', '<a href="/zh/heic-to-jpg">HEIC 转 JPG 转换</a>'),
            ('<a href="/zh/png-to-jpg">PNG 转 JPG 转换</a>', '<a href="/zh/png-to-jpg">PNG 转 JPG 转换</a>'),
            ('<a href="/zh/jpg-to-tiff">JPG 转 TIFF 转换</a>', '<a href="/zh/jpg-to-tiff">JPG 转 TIFF 转换</a>'),
        ],
        'article_h2': '如何安全地在线将 TIFF 转换为 JPG',
        'article_p1': 'TIFF（标签图像文件格式）因能够存储高质量的光栅图像而广泛用于印刷和设计领域。然而，TIFF 文件体积庞大，通常无法在浏览器或社交媒体上直接查看。将其转换为 JPG 是在任何设备上分享 and 查看图片的最简便方式。',
        'article_p2': '我们的转换程序完全在浏览器内运行。您的敏感或私人图片永远不会发送到云端。',
        'faq_h3': '常见问题解答',
        'faq1_q': '转换会降低画质吗？',
        'faq1_a': 'JPG 使用有损压缩以大幅减小文件大小。我们的转换器采用高画质设置，确保视觉上的差异几乎不可察觉。',
        'faq2_q': '我可以一次性批量转换多个 TIFF 文件吗？',
        'faq2_a': '可以，本工具支持批量转换。您可以直接拖入多个 TIFF 文件并一键下载 ZIP 压缩包。',
        'faq3_q': '我的文件会被上传到服务器吗？',
        'faq3_a': '不会。转换完全在您的本地浏览器中完成，图片数据永远不会离开您的设备，绝对安全。',
        'footer_copy': '您的文件永远不会离开您的设备 — 100% 浏览器客户端本地转换。'
    }
}

# Translations for jpg-to-tiff
jpg_to_tiff_trans = {
    'en': {
        'title': 'Convert JPG to TIFF Online Free | Image Converter',
        'desc': 'Instantly convert JPG images to high-quality TIFF format. Free, secure, client-side browser conversion — perfect for print and publishing.',
        'keywords': 'jpg to tiff, convert jpg to tiff, jpeg to tiff, free online tiff converter',
        'h1': 'Convert JPG to TIFF Online Free',
        'tab_active': 'Converting to TIFF',
        'drop_h2': 'Drop JPG images here',
        'drop_p': 'Supports formats including JPG, WEBP, PNG, TIFF, HEIC',
        'btn_convert': 'Convert to TIFF',
        'res_header': 'Converted to TIFF successfully!',
        'res_download': 'Download TIFF',
        'related_h3': 'Related Free Tools',
        'related_links': [
            ('<a href="/">Convert Multiple Formats</a>', '<a href="/">Convert Multiple Formats</a>'),
            ('<a href="/jpg-to-png">Convert JPG to PNG</a>', '<a href="/jpg-to-png">Convert JPG to PNG</a>'),
            ('<a href="/tiff-to-jpg">Convert TIFF to JPG</a>', '<a href="/tiff-to-jpg">Convert TIFF to JPG</a>'),
            ('<a href="/png-to-jpg">Convert PNG to JPG</a>', '<a href="/png-to-jpg">Convert PNG to JPG</a>'),
        ],
        'article_h2': 'How to Convert JPG to TIFF Online Securely',
        'article_p1': 'JPG is the most common format for photos on the web, but it relies on lossy compression. If you need to prepare an image for high-quality printing, publication, or archiving, converting it to TIFF (Tagged Image File Format) is an excellent choice. TIFF preserves image layers and metadata, making it the industry standard for print design.',
        'article_p2': 'Using standard web canvas and client-side encoding libraries, our tool runs 100% offline inside your web browser. Your private file contents are never exposed or transferred.',
        'faq_h3': 'Frequently Asked Questions',
        'faq1_q': 'Why convert JPG to TIFF?',
        'faq1_a': 'Converting to TIFF is useful if you are importing photos into software that requires TIFF format (like certain publishing tools) or if you want to store the image in an uncompressed format for future edits.',
        'faq2_q': 'Does converting JPG to TIFF restore lost quality?',
        'faq2_a': 'No. Since JPG compression is lossy and has already discarded some data, converting to TIFF cannot restore that quality. However, it prevents further loss during subsequent saves.',
        'faq3_q': 'Is there a file size limit?',
        'faq3_a': 'No. Since conversion is processed entirely on your local device within the browser, there are no file size limits or server restrictions.',
        'footer_copy': 'Your files never leave your device — 100% client-side rendering.'
    },
    'de': {
        'title': 'JPG in TIFF Konverter | Kostenlos & Online',
        'desc': 'Konvertieren Sie JPG-Bilder online in das hochwertige TIFF-Format. 100% kostenlos und sicher im Browser.',
        'keywords': 'jpg in tiff, jpg to tiff, jpeg in tiff, tiff erstellen',
        'h1': 'JPG in TIFF Konverter',
        'tab_active': 'JPG in TIFF konvertieren',
        'drop_h2': 'JPG-Bilder hierher ziehen',
        'drop_p': 'Unterstützt JPG, PNG, WEBP, HEIC, TIFF, SVG',
        'btn_convert': 'In TIFF konvertieren',
        'res_header': 'Erfolgreich konvertiert!',
        'res_download': 'Herunterladen',
        'related_h3': 'Verwandte kostenlose Werkzeuge',
        'related_links': [
            ('<a href="/de/">Mehrere Formate konvertieren</a>', '<a href="/de/">Mehrere Formate konvertieren</a>'),
            ('<a href="/de/jpg-to-png">JPG in PNG umwandeln</a>', '<a href="/de/jpg-to-png">JPG in PNG umwandeln</a>'),
            ('<a href="/de/tiff-to-jpg">TIFF in JPG umwandeln</a>', '<a href="/de/tiff-to-jpg">TIFF in JPG umwandeln</a>'),
            ('<a href="/de/png-to-jpg">PNG in JPG umwandeln</a>', '<a href="/de/png-to-jpg">PNG in JPG umwandeln</a>'),
        ],
        'article_h2': 'So konvertieren Sie JPG sicher online in TIFF',
        'article_p1': 'JPG ist das am häufigsten verwendete Bildformat im Web, verliert jedoch bei jedem Speichervorgang an Qualität. Wenn Sie ein Bild für den professionellen Druck oder die Archivierung vorbereiten möchten, ist die Konvertierung in TIFF eine hervorragende Wahl. TIFF ist der Standard im Druckdesign.',
        'article_p2': 'Dank unserer HTML5-basierten Architektur erfolgt der gesamte Bildkodierungsprozess direkt im Browser, ohne Uploads und unter Wahrung der vollen Vertraulichkeit.',
        'faq_h3': 'Häufig gestellte Fragen',
        'faq1_q': 'Warum sollte ich JPG in TIFF konvertieren?',
        'faq1_a': 'Die Konvertierung in TIFF is nützlich für Layout- und Druckprogramme, die dieses Format erfordern, oder um weitere Qualitätsverluste bei der Bearbeitung zu vermeiden.',
        'faq2_q': 'Stellt die Konvertierung die verlorene Qualität wieder her?',
        'faq2_a': 'Nein, da JPG bereits Bildinformationen verworfen hat. Die Konvertierung verhindert jedoch weiteren Qualitätsverlust bei zukünftigen Speichervorgängen.',
        'faq3_q': 'Gibt es eine Dateigrößenbeschränkung?',
        'faq3_a': 'Nein, da die Verarbeitung komplett lokal auf Ihrem Gerät erfolgt, gibt es keine Größen- oder Mengenbeschränkungen.',
        'footer_copy': 'Ihre Dateien verlassen Ihr Gerät nie — 100% clientseitige Verarbeitung.'
    },
    'es': {
        'title': 'Convertidor de JPG a TIFF Gratis | En Línea',
        'desc': 'Convierta imágenes JPG a formato TIFF de alta calidad. Gratis, seguro y 100% local en su navegador.',
        'keywords': 'jpg a tiff, convertir jpg a tiff, jpeg a tiff, convertidor tiff gratis',
        'h1': 'Convertidor de JPG a TIFF',
        'tab_active': 'Convertir a TIFF',
        'drop_h2': 'Arrastre imágenes JPG aquí',
        'drop_p': 'Soporta formatos como JPG, PNG, WEBP, HEIC, TIFF, SVG',
        'btn_convert': 'Convertir a TIFF',
        'res_header': '¡Convertido con éxito!',
        'res_download': 'Descargar',
        'related_h3': 'Herramientas Relacionadas',
        'related_links': [
            ('<a href="/es/">Convertir múltiples formatos</a>', '<a href="/es/">Convertir múltiples formatos</a>'),
            ('<a href="/es/jpg-to-png">Convertir JPG a PNG</a>', '<a href="/es/jpg-to-png">Convertir JPG a PNG</a>'),
            ('<a href="/es/tiff-to-jpg">Convertir TIFF a JPG</a>', '<a href="/es/tiff-to-jpg">Convertir TIFF a JPG</a>'),
            ('<a href="/es/png-to-jpg">Convertir PNG a JPG</a>', '<a href="/es/png-to-jpg">Convertir PNG a JPG</a>'),
        ],
        'article_h2': 'Cómo convertir JPG a TIFF en línea de forma segura',
        'article_p1': 'El formato JPG es muy popular pero utiliza compresión con pérdida. Si necesita preparar una imagen para impresión profesional o archivado, convertirla a TIFF (Tagged Image File Format) es la mejor opción, ya que es el estándar de la industria gráfica.',
        'article_p2': 'Toda la conversión de imágenes se lleva a cabo directamente en su navegador web. Garantizamos que no se envían datos a ningún servidor externo.',
        'faq_h3': 'Preguntas Frecuentes',
        'faq1_q': '¿Por qué convertir JPG a TIFF?',
        'faq1_a': 'Es útil para importar fotos en programas de maquetación e imprenta que requieren TIFF, o para editar la imagen sin seguir perdiendo calidad.',
        'faq2_q': '¿La conversión restaura la calidad perdida del JPG?',
        'faq2_a': 'No. La información descartada por el JPG ya no se puede recuperar, pero la conversión evita que se pierda más calidad al editar y guardar de nuevo.',
        'faq3_q': '¿Hay límite de tamaño de archivo?',
        'faq3_a': 'No hay límites. La conversión se procesa localmente en su navegador, sin restricciones de servidor.',
        'footer_copy': 'Sus archivos nunca salen de su dispositivo — 100% local en su navegador.'
    },
    'fr': {
        'title': 'Convertisseur JPG en TIFF Gratuit | En Ligne',
        'desc': 'Convertissez des images JPG au format TIFF de haute qualité. Gratuit, sécurisé et 100% local dans votre navigateur.',
        'keywords': 'jpg en tiff, convertir jpg en tiff, jpeg en tiff, convertisseur tiff gratuit',
        'h1': 'Convertisseur JPG en TIFF',
        'tab_active': 'Convertir en TIFF',
        'drop_h2': 'Déposez les images JPG ici',
        'drop_p': 'Prend en charge les formats JPG, PNG, WEBP, HEIC, TIFF, SVG',
        'btn_convert': 'Convertir en TIFF',
        'res_header': 'Converti avec succès !',
        'res_download': 'Télécharger',
        'related_h3': 'Outils Connexes',
        'related_links': [
            ('<a href="/fr/">Convertir plusieurs formats</a>', '<a href="/fr/">Convertir plusieurs formats</a>'),
            ('<a href="/fr/jpg-to-png">Convertir JPG en PNG</a>', '<a href="/fr/jpg-to-png">Convertir JPG en PNG</a>'),
            ('<a href="/fr/tiff-to-jpg">Convertir TIFF en JPG</a>', '<a href="/fr/tiff-to-jpg">Convertir TIFF en JPG</a>'),
            ('<a href="/fr/png-to-jpg">Convertir PNG en JPG</a>', '<a href="/fr/png-to-jpg">Convertir PNG en JPG</a>'),
        ],
        'article_h2': 'Comment convertir JPG en TIFF en toute sécurité',
        'article_p1': 'Le format JPG est idéal pour le web mais utilise une compression avec perte. Si vous devez préparer une image pour une impression professionnelle, une publication ou un archivage, la conversion en TIFF (Tagged Image File Format) est recommandée car c\'est le standard de l\'industrie de l\'impression.',
        'article_p2': 'Toutes les opérations d\'encodage s\'exécutent localement sur votre ordinateur. Vos documents et photos sensibles sont à l\'abri.',
        'faq_h3': 'Foire Aux Questions',
        'faq1_q': 'Pourquoi convertir un JPG en TIFF?',
        'faq1_a': 'Le TIFF est requis par de nombreux logiciels de mise en page professionnels pour l\'impression, et il évite de dégrader l\'image lors des sauvegardes successives.',
        'faq2_q': 'La conversion restaure-t-elle la qualité perdue du JPG?',
        'faq2_a': 'Non, les données perdues lors de la compression JPG ne peuvent pas être restaurées. Cependant, la conversion empêche toute perte supplémentaire lors de futures modifications.',
        'faq3_q': 'Y a-t-il une limite de taille de fichier?',
        'faq3_a': 'Aucune. Le traitement étant entièrement local dans votre navigateur, il n\'y a pas de limites liées à un serveur.',
        'footer_copy': 'Vos fichiers ne quittent jamais votre appareil — 100% traitement client.'
    },
    'hi': {
        'title': 'JPG से TIFF कनवर्टर ऑनलाइन | मुफ्त और सुरक्षित',
        'desc': 'JPG छवियों को उच्च गुणवत्ता वाले TIFF फॉर्मेट में ऑनलाइन बदलें। 100% मुफ़्त, सुरक्षित और स्थानीय ब्राउज़र रूपांतरण।',
        'keywords': 'jpg to tiff, jpg से tiff, jpeg to tiff, tiff फ़ाइल बनाएं',
        'h1': 'JPG से TIFF कनवर्टर',
        'tab_active': 'TIFF में बदलें',
        'drop_h2': 'JPG इमेज यहाँ ड्राप करें',
        'drop_p': 'JPG, PNG, WEBP, HEIC, TIFF, SVG फॉर्मेट समर्थित हैं',
        'btn_convert': 'TIFF में बदलें',
        'res_header': 'सफलतापूर्वक बदला गया!',
        'res_download': 'डाउनलोड करें',
        'related_h3': 'संबंधित मुफ्त उपकरण',
        'related_links': [
            ('<a href="/hi/">कई प्रारूपों को बदलें</a>', '<a href="/hi/">कई प्रारूपों को बदलें</a>'),
            ('<a href="/hi/jpg-to-png">JPG से PNG कनवर्ट करें</a>', '<a href="/hi/jpg-to-png">JPG से PNG कनवर्ट करें</a>'),
            ('<a href="/hi/tiff-to-jpg">TIFF से JPG कनवर्ट करें</a>', '<a href="/hi/tiff-to-jpg">TIFF से JPG कनवर्ट करें</a>'),
            ('<a href="/hi/png-to-jpg">PNG से JPG कनवर्ट करें</a>', '<a href="/hi/png-to-jpg">PNG से JPG कनवर्ट करें</a>'),
        ],
        'article_h2': 'JPG को TIFF में सुरक्षित रूप से ऑनलाइन कैसे बदलें',
        'article_p1': 'JPG वेब पर सबसे लोकप्रिय फॉर्मेट है, लेकिन यह कंप्रेस्ड होता है। यदि आप छवि को प्रिंटिंग, प्रकाशन या भविष्य के संपादन के लिए तैयार करना चाहते हैं, तो इसे TIFF (Tagged Image File Format) में बदलना एक बेहतरीन विकल्प है, जो प्रिंट उद्योग का मानक है।',
        'article_p2': 'कनवर्टर पूरी तरह से आपके ब्राउज़र में काम करता है, ताकि आपकी फाइलें कहीं बाहर न भेजी जाएं।',
        'faq_h3': 'अक्सर पूछे जाने वाले प्रश्न',
        'faq1_q': 'JPG को TIFF में क्यों बदलें?',
        'faq1_a': 'TIFF प्रिंटिंग और प्रकाशन सॉफ्टवेयर में अधिक संगत है और संपादन के दौरान गुणवत्ता को सुरक्षित रखता है।',
        'faq2_q': 'क्या TIFF में बदलने से पुरानी खोई गुणवत्ता वापस मिल जाएगी?',
        'faq2_a': 'नहीं। JPG में खोई हुई जानकारी वापस नहीं लाई जा सकती, लेकिन यह आगे और गुणवत्ता खराब होने से बचाएगा।',
        'faq3_q': 'क्या फ़ाइल आकार की कोई सीमा है?',
        'faq3_a': 'नहीं। चूंकि रूपांतरण आपके स्थानीय डिवाइस पर ही होता है, इसलिए कोई आकार सीमा नहीं है।',
        'footer_copy': 'आपकी फाइलें कभी आपके डिवाइस से बाहर नहीं जातीं — 100% स्थानीय कनवर्टर।'
    },
    'zh': {
        'title': 'JPG 转 TIFF 转换器 | 免费在线高画质 TIFF 转换',
        'desc': '将 JPG 图像在线转换为高画质的 TIFF 格式。100% 免费、安全且完全在浏览器本地进行。',
        'keywords': 'jpg转tiff, jpg to tiff, jpeg转tiff, 免费tiff转换',
        'h1': 'JPG 转 TIFF 转换器',
        'tab_active': '转换为 TIFF',
        'drop_h2': '将 JPG 图片拖到此处',
        'drop_p': '支持 JPG、PNG、WEBP、HEIC、TIFF、SVG 等格式',
        'btn_convert': '转换为 TIFF',
        'res_header': '转换成功！',
        'res_download': '下载',
        'related_h3': '相关免费工具',
        'related_links': [
            ('<a href="/zh/">转换多种格式</a>', '<a href="/zh/">转换多种格式</a>'),
            ('<a href="/zh/jpg-to-png">JPG 转 PNG 转换</a>', '<a href="/zh/jpg-to-png">JPG 转 PNG 转换</a>'),
            ('<a href="/zh/tiff-to-jpg">TIFF 转 JPG 转换</a>', '<a href="/zh/tiff-to-jpg">TIFF 转 JPG 转换</a>'),
            ('<a href="/zh/png-to-jpg">PNG 转 JPG 转换</a>', '<a href="/zh/png-to-jpg">PNG 转 JPG 转换</a>'),
        ],
        'article_h2': '如何安全地在线将 JPG 转换为 TIFF',
        'article_p1': 'JPG 是网络上最常见的文件格式，但它是有损压缩的。如果您需要为高质量印刷、出版或长期存档准备图片，将其转换为 TIFF（标签图像文件格式）是极佳的选择，因为 TIFF 是印刷设计界的行业标准。',
        'article_p2': '在客户端本地完成编码，确保您照片或机密图纸的私密权。',
        'faq_h3': '常见问题解答',
        'faq1_q': '为什么要将 JPG 转换为 TIFF？',
        'faq1_a': 'TIFF 格式在排版和印刷软件中兼容性更好，且可以作为无损图片保存，便于未来的二次编辑。',
        'faq2_q': '将 JPG 转换为 TIFF 能恢复画质吗？',
        'faq2_a': '不能。JPG 已经丢弃的信息无法通过转换恢复。但转换为 TIFF 可以防止未来重复保存时画质进一步降低。',
        'faq3_q': '有文件大小限制吗？',
        'faq3_a': '没有限制。因为所有转换逻辑均在本地浏览器运行，不存在服务器文件大小或流量限制。',
        'footer_copy': '您的文件永远不会离开您的设备 — 100% 浏览器客户端本地转换。'
    }
}

def generate_page(tool_type, lang):
    """Generates index.html for a given tool_type (tiff-to-jpg or jpg-to-tiff) and language code."""
    # 1. Paths setup
    is_en = (lang == 'en')
    
    # Source path
    src_folder = 'heic-to-jpg' if tool_type == 'tiff-to-jpg' else 'jpg-to-png'
    src_file_path = os.path.join(base_dir, src_folder, 'index.html') if is_en else os.path.join(base_dir, lang, src_folder, 'index.html')
    
    # Target folder and path
    target_folder = tool_type if is_en else os.path.join(lang, tool_type)
    target_dir_abs = os.path.join(base_dir, target_folder)
    os.makedirs(target_dir_abs, exist_ok=True)
    target_file_path = os.path.join(target_dir_abs, 'index.html')
    
    with open(src_file_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 2. Select translations dictionary
    trans_dict = tiff_to_jpg_trans[lang] if tool_type == 'tiff-to-jpg' else jpg_to_tiff_trans[lang]
    
    # 3. Process URL references (replaces heic-to-jpg/jpg-to-png in links)
    if tool_type == 'tiff-to-jpg':
        html = html.replace('heic-to-jpg', 'tiff-to-jpg')
    else:
        html = html.replace('jpg-to-png', 'jpg-to-tiff')
        
    # 4. Replace meta keywords, descriptions and titles in head
    title_pattern = re.compile(r'<title>.*?</title>', re.IGNORECASE)
    html = title_pattern.sub(f"<title>{trans_dict['title']}</title>", html)
    
    desc_pattern = re.compile(r'<meta name="description" content="[^"]*"', re.IGNORECASE)
    html = desc_pattern.sub(f'<meta name="description" content="{trans_dict["desc"]}"', html)
    
    key_pattern = re.compile(r'<meta name="keywords" content="[^"]*"', re.IGNORECASE)
    html = key_pattern.sub(f'<meta name="keywords" content="{trans_dict["keywords"]}"', html)
    
    og_title_pattern = re.compile(r'<meta property="og:title" content="[^"]*"', re.IGNORECASE)
    html = og_title_pattern.sub(f'<meta property="og:title" content="{trans_dict["title"]}"', html)
    
    og_desc_pattern = re.compile(r'<meta property="og:description" content="[^"]*"', re.IGNORECASE)
    html = og_desc_pattern.sub(f'<meta property="og:description" content="{trans_dict["desc"]}"', html)
    
    tw_title_pattern = re.compile(r'<meta name="twitter:title" content="[^"]*"', re.IGNORECASE)
    html = tw_title_pattern.sub(f'<meta name="twitter:title" content="{trans_dict["title"]}"', html)
    
    tw_desc_pattern = re.compile(r'<meta name="twitter:description" content="[^"]*"', re.IGNORECASE)
    html = tw_desc_pattern.sub(f'<meta name="twitter:description" content="{trans_dict["desc"]}"', html)
    
    # 5. Replace structural page tags / attributes
    if tool_type == 'tiff-to-jpg':
        # input accept tags and data-target-mime
        html = re.sub(r'data-target-mime="[^"]*"', 'data-target-mime="image/jpeg"', html)
        html = html.replace('accept="image/*,.heic"', 'accept="image/*,.heic,.tiff,.tif"')
    else:
        html = re.sub(r'data-target-mime="[^"]*"', 'data-target-mime="image/tiff"', html)
        html = html.replace('accept="image/*,.heic"', 'accept="image/*,.heic,.tiff,.tif"')
        
    # 6. Replace tab buttons, headings and upload zones
    page_title_pattern = re.compile(r'<h1 class="page-title">.*?</h1>', re.IGNORECASE)
    html = page_title_pattern.sub(f'<h1 class="page-title">{trans_dict["h1"]}</h1>', html)
    
    # Format tabs replacement
    if tool_type == 'tiff-to-jpg':
        tabs_html = f'<div class="format-tabs glass-panel" id="formatTabs">\n        <button class="tab active" data-target="image/jpeg">{trans_dict["tab_active"]}</button>\n      </div>'
    else:
        tabs_html = f'<div class="format-tabs glass-panel" id="formatTabs">\n        <button class="tab active" data-target="image/tiff">{trans_dict["tab_active"]}</button>\n      </div>'
    html = re.sub(r'<div class="format-tabs glass-panel" id="formatTabs">.*?</div>', tabs_html, html, flags=re.DOTALL)
    
    # Drop zone texts
    html = re.sub(r'<h2>Drop HEIC images here</h2>|<h2>Drop JPG images here</h2>|<h2>.*?图片拖到此处</h2>|<h2>.*?images here</h2>', f'<h2>{trans_dict["drop_h2"]}</h2>', html)
    html = re.sub(r'<p>Supports formats including JPG, WEBP, HEIC</p>|<p>Supports formats including JPG, WEBP, PNG, TIFF, HEIC</p>|<p>支持.*?</p>|<p>Unterstützt.*?</p>|<p>Soporta.*?</p>|<p>Prend en charge.*?</p>|<p>.* समर्थित हैं</p>', f'<p>{trans_dict["drop_p"]}</p>', html)
    
    # Convert button and download texts
    html = re.sub(r'<span id="convertBtnText">.*?</span>', f'<span id="convertBtnText">{trans_dict["btn_convert"]}</span>', html)
    html = re.sub(r'<div class="result-header">.*?</div>', f'<div class="result-header">{trans_dict["res_header"]}</div>', html)
    html = re.sub(r'<span id="downloadText">.*?</span>', f'<span id="downloadText">{trans_dict["res_download"]}</span>', html)
    
    # 7. Related Tools links replacement
    related_sec_pattern = re.compile(r'<section class="related-tools glass-panel">.*?</section>', re.DOTALL)
    links_html = "\n        ".join([l[0] for l in trans_dict['related_links']])
    new_related = f'<section class="related-tools glass-panel">\n        <h3>{trans_dict["related_h3"]}</h3>\n        {links_html}\n      </section>'
    html = related_sec_pattern.sub(new_related, html)
    
    # 8. Article content replacement (including FAQs)
    article_sec_pattern = re.compile(r'<article class="seo-article glass-panel">.*?</article>', re.DOTALL)
    
    faq_ld_pattern = re.compile(r'<script type="application/ld\+json">\s*\{\s*"@context":\s*"https://schema\.org",\s*"@type":\s*"FAQPage",.*?\}\s*</script>', re.DOTALL)
    
    # Build JSON-LD FAQ Schema
    faq_ld = f'''<script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {{
        "@type": "Question",
        "name": "{trans_dict['faq1_q']}",
        "acceptedAnswer": {{
          "@type": "Answer",
          "text": "{trans_dict['faq1_a']}"
        }}
      }},
      {{
        "@type": "Question",
        "name": "{trans_dict['faq2_q']}",
        "acceptedAnswer": {{
          "@type": "Answer",
          "text": "{trans_dict['faq2_a']}"
        }}
      }},
      {{
        "@type": "Question",
        "name": "{trans_dict['faq3_q']}",
        "acceptedAnswer": {{
          "@type": "Answer",
          "text": "{trans_dict['faq3_a']}"
        }}
      }}
    ]
  }}
  </script>'''
    
    # Replace FAQ LD inside head
    html = faq_ld_pattern.sub(faq_ld, html)
    
    # Build Article markup
    new_article = f'''<article class="seo-article glass-panel">
        <h2>{trans_dict['article_h2']}</h2>
        <p>{trans_dict['article_p1']}</p>
        <p>{trans_dict['article_p2']}</p>
        <div class="faq-section">
          <h3>{trans_dict['faq_h3']}</h3>
          <div class="faq-item">
            <div class="faq-question">{trans_dict['faq1_q']}</div>
            <div class="faq-answer">{trans_dict['faq1_a']}</div>
          </div>
          <div class="faq-item">
            <div class="faq-question">{trans_dict['faq2_q']}</div>
            <div class="faq-answer">{trans_dict['faq2_a']}</div>
          </div>
          <div class="faq-item">
            <div class="faq-question">{trans_dict['faq3_q']}</div>
            <div class="faq-answer">{trans_dict['faq3_a']}</div>
          </div>
        </div>
      </article>'''
    
    html = article_sec_pattern.sub(new_article, html)
    
    # Footer copy
    html = re.sub(r'<div class="footer-copy">.*?</div>', f'<div class="footer-copy">{trans_dict["footer_copy"]}</div>', html)
    
    # Write output file
    with open(target_file_path, 'w', encoding='utf-8') as f:
        f.write(html)
        
    print(f"Generated {target_file_path}")

def main():
    for lang in langs:
        generate_page('tiff-to-jpg', lang)
        generate_page('jpg-to-tiff', lang)
    print("Done generating pages!")

if __name__ == "__main__":
    main()
