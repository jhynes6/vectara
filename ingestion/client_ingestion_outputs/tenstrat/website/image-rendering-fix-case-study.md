---
source: "website"
content_type: "case_studies"
url: "https://tenstrat.com/image-rendering-fix-case-study/"
title: "Image Rendering Fix Case Study"
domain: "tenstrat.com"
path: "/image-rendering-fix-case-study/"
scraped_time: "2025-10-05T01:40:46.780011"
url_depth: 1
word_count: 321
client_name: "tenstrat"
---

# Image Rendering Fix Case Study

#### By TenStrat

**Client:** Ecommerce Website in the Toys Industry

**Situation:**  
Our client, an ecommerce website in the toys industry, was experiencing inconsistent display of relevant image thumbnails in Google search results for their Product Listing Pages (PLPs) and landing pages. When image thumbnails were displayed, they were often irrelevant icons or country flags, as the site was both international and multi-lingual.

**Challenge:**  
While all images appeared normally to front-end users on the PLPs and landing pages, they weren’t being rendered by Google in tests conducted using tools like the URL Inspection tool or JS-rendering crawlers such as Screaming Frog. The image resources weren’t blocked via robots.txt or any other means that would prevent Google or crawlers from rendering them.

**Solution:**  
After reviewing Google’s documentation on image SEO best practices and experimenting with multiple approaches alongside the client’s development team, we identified the root cause of the rendering issue. The client was using the data-src attribute for HTML <img> elements with responsive sizes, rather than the src attribute, which is what search engine crawlers use to render images.

**Implementation:**  
The client’s development team added a fallback src attribute for all images used on product tiles and landing pages, ensuring crawler accessibility while preserving the responsive data-src implementation.

**Results:**  
The impact of these changes was both immediate and substantial. Shortly after implementing the updates, Google began displaying the expected image thumbnails—showing accurate product thumbnails and above-the-fold landing page images consistently:

*   **SEO Clicks:** Increased by 9.6%
*   **Keywords Ranked on Page #1:** Increased by 33%

**Conclusion:**  
This was a complex issue to diagnose because the front-end user experience showed no apparent problems, yet crawlers couldn’t properly render images. By taking a first-principles approach, we were able to identify the root cause and partner with the client’s development team to implement an effective solution. This improved the client’s SEO traffic and brand perception significantly in search results.