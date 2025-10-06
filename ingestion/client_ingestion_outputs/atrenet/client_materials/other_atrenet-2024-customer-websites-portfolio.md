<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AtreNet Customer Websites 2024</title>
    <style>
        body, html {
            margin: 0;
            padding: 0;
            height: 100%;
            font-family: Arial, sans-serif;
        }
        #controls {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: rgba(255, 255, 255, 0.8);
            padding: 10px;
            z-index: 1000;
        }
        #urlInput, #fallbackUrlInput {
            width: calc(50% - 65px);
            padding: 5px;
            margin-right: 10px;
        }
        #createButton {
            width: 100px;
            padding: 5px;
        }
	#grid {
    display: grid;
    gap: 10px;
    padding: 10px;
    box-sizing: border-box;
    margin-top: 50px;
}
        .grid-item {
            position: relative;
            border: 3px solid #3498db;
            border-radius: 15px;
            overflow: hidden;
            transition: all 0.3s ease;
	    min-height: 150px;
            aspect-ratio: 1 / 1;
        }
        .grid-item:hover {
            border-width: 6px;
            transform: scale(1.02);
        }

	.pdf-button:hover {
	border-width: 6px;
            transform: scale(1.02);
	}

	.grid-item img, .grid-item iframe {
    	width: 100%;
    	height: 100%;
    	object-fit: cover;
	}
        
        .site-name {
            position: absolute;
            bottom: 10px;
            right: 10px;
            background: rgba(0, 0, 0, 0.7);
            color: white;
            padding: 5px 10px;
            border-radius: 5px;
            font-size: 14px;
            text-decoration: none;
            z-index: 10;
        }
        .site-name:hover {
            background: rgba(0, 0, 0, 0.9);
        }

@media (min-width: 400px) and (max-width: 768px) {
    #grid {
        grid-template-columns: repeat(2, 1fr);
    }
}
 @media (max-width: 400px) {
    #grid {
           grid-template-columns: repeat(1, 1fr);
    }
    .grid-item {
        aspect-ratio: 4 / 3; /* Slightly wider aspect ratio for mobile */
        min-height: auto;
    }
}


    </style>
</head>
<body>
	<div id="pdf-viewer-section" style="margin-bottom: 20px; text-align: center;">
          <button id="close-pdf-viewer" style="position: absolute; top: 10px; right: 10px; z-index: 10; display:none" onclick="closePDFViewer()">Close</button>
      		<div id="pdf-viewer-container" style="margin-top: 10px; display: none;">
            <iframe id="pdf-viewer" width="100%" height="1000px" style="border: 1px solid #3498db;"></iframe>
        </div>
    </div>
    <div id="grid"></div>
 <div style="text-align: center; margin-top: 20px; ">
	<img class="pdf-button" src="https://epicscore.ai/AtreNet-Overview-2024-cover.jpg" style="border-radius: 20px; border: 3px solid #3498db;" alt="View PDF" style="cursor: pointer;" onclick="loadPDF('https://epicscore.ai/AtreNet-Overview-2024.pdf')">
       </div>
<script>
        function createGrid() {
            // Hardcoded URLs and fallback image URLs
            const urls = [
                "https://rapyd.net", 
                "https://tenable.com", 
                "https://sonatus.com", 
                "https://arable.com", 
                "https://igel.com", 
                "https://vitechinc.com", 
                "https://oxio.com",
		"https://sdvi.com",
		"https://scalevp.com",
		"https://na.itron.com"
            ];
            const fallbackUrls = [
                "https://epicscore.ai/rapyd-screenshot.png", 
                "", 
                "", 
                "", 
                "", 
                "https://epicscore.ai/vitech-screenshot.png", 
                "https://epicscore.ai/oxio-screenshot.png",
		"",
		"",
		"https://epicscore.ai/itron-screenshot.png"
            ];

            const grid = document.getElementById('grid');
            grid.innerHTML = '';

		const isMobile = window.innerWidth <= 768;

    // Only set columns dynamically if not on mobile
    if (!isMobile) {
        const columns = Math.ceil(Math.sqrt(urls.length));
        grid.style.gridTemplateColumns = `repeat(${columns}, 1fr)`;
    }

//            const columns = Math.ceil(Math.sqrt(urls.length));
//            grid.style.gridTemplateColumns = `repeat(${columns}, 1fr)`;

            urls.forEach((url, index) => {
                if (!/^https?:\/\//i.test(url)) {
                    url = 'https://' + url;
                }

                const fallbackUrl = fallbackUrls[index] || '';  // Use the fallback URL if provided, otherwise empty

                const item = document.createElement('div');
                item.className = 'grid-item';
                
                // Create and add fallback image if specified
                if (fallbackUrl) {
                    const img = document.createElement('img');
                    img.src = fallbackUrl;
                    img.alt = 'Fallback image';
                    item.appendChild(img);
                } else {
                    // Create and add iframe on top of the fallback image
                    const iframe = document.createElement('iframe');
                    iframe.src = url;
                    iframe.sandbox = 'allow-scripts allow-same-origin';
                    iframe.onload = () => handleIframeLoad(iframe);
                    iframe.onerror = () => handleIframeError(item, iframe);
                    item.appendChild(iframe);
                }

                const siteLink = document.createElement('a');
                siteLink.className = 'site-name';
                siteLink.href = url;
                siteLink.target = '_blank';
                try {
                    siteLink.textContent = new URL(url).hostname;
                } catch (e) {
                    siteLink.textContent = url;
                }
                item.appendChild(siteLink);
                
                grid.appendChild(item);
            });
        }

        function handleIframeLoad(iframe) {
            // If the iframe loads successfully, it will stay on top of the fallback image
        }

        function handleIframeError(item, iframe) {
            // Remove the iframe if it fails to load
            if (iframe && iframe.parentNode) {
                iframe.parentNode.removeChild(iframe);
            }
        }
	
	function loadPDF(pdfUrl) {
	const isMobile = window.innerWidth <= 400;

    	if (isMobile) {
        // Redirect to the PDF on mobile devices
        window.location.href = pdfUrl;
    	} else {
	
            const pdfViewerContainer = document.getElementById('pdf-viewer-container');
            const pdfViewer = document.getElementById('pdf-viewer');
            const pdfViewerClose = document.getElementById('close-pdf-viewer');
            pdfViewerClose.style.display = 'block';
            pdfViewer.src = pdfUrl;
            pdfViewerContainer.style.display = 'block';

            window.scrollTo({ top: 0, behavior: 'smooth' });
		}
        }

	function closePDFViewer() {
            const pdfViewerSection = document.getElementById('pdf-viewer-section');
            const pdfViewer = document.getElementById('pdf-viewer');
		const pdfViewerClose = document.getElementById('close-pdf-viewer');
    // Clear the src attribute to force reload on next open
    pdfViewer.src = '';

		pdfViewer.style.display = 'none';
                pdfViewerClose.style.display = 'none';
        }
        // Initialize the grid on page load
        window.onload = createGrid;
    </script>
</body>
</html>
