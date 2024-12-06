import asyncio
from playwright.async_api import async_playwright

LANGUAGES = ["es", "en-US"]

async def download_pdf(language: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="chrome", headless=False, args=["--start-maximized"])
        #context = await browser.new_context() #español
        # english context
        context = await browser.new_context(locale=language)
        page = await context.new_page()
        await page.set_viewport_size({"width": 1920, "height": 1080})
        await page.goto("http://juanfrilla.github.io", wait_until="load")
        
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(3000)
        await page.evaluate(
            """
                            function modifyClasses() {
    const elements = document.querySelectorAll("h4, div, section");
    elements.forEach((element) => {
      if (!element.originalClasses) {
        element.originalClasses = [...element.classList];
      }
  
      const classesToRemove = [];
      const classesToReplace = [];
  
      switch (element.tagName) {
        case "H4":
          element.classList.forEach((className) => {
            if (className.startsWith("card-title")) {
              classesToRemove.push(className);
            }
            // if (className.startsWith("mt-4")) {
            //   classesToReplace.push({ old: className, new: "ml-3" });
            // }
          });
          break;
  
        case "DIV":
          element.classList.forEach((className) => {
            if (className.startsWith("card-body")) {
              classesToRemove.push(className);
              classesToReplace.push("card-body", "p-0"); // Add classes separately
            }
            if (element.id === "personal_data") {
              classesToReplace.push({ old: className, new: "mb-3" });
            }
          });
          const aboutText = element.querySelector("p#about_text");
          if (aboutText) {
            aboutText.classList.add("pl-3");
          }
          break;
  
        case "SECTION":
          element.classList.forEach((className) => {
            if (className.includes("p-") && !className.includes("p-3")) {
              classesToRemove.push(className);
            }
            if (className.includes("p-3")) {
              //classesToReplace.push({ old: className, new: "pr-3" });
              classesToRemove.push(className);
            }
            if (className.includes("border-dark")) {
              classesToReplace.push({ old: className, new: "border-0" });
            }
            if (className.includes("mt-")) {
              classesToRemove.push(className);
            }
            if (className.includes("mb-")) {
              classesToRemove.push(className);
            }
          });
          break;
  
        default:
          break;
      }
  
      element.classList.remove(...classesToRemove);
      classesToReplace.forEach(({ old, new: newClass }) => {
        element.classList.replace(old, newClass);
      });
    });
  }
                            """
        )

        await page.evaluate(
            """
                              function modifyH4() {
    const h4Elements = document.querySelectorAll("h4");
    const replacedElements = [];
  
    h4Elements.forEach((h4) => {
      const div = document.createElement("div");
      div.innerHTML = h4.innerHTML;
      div.style.fontSize = "12px";
      div.style.fontWeight = "bold";
      div.className = h4.className;
      div.id = h4.id;
      div.classList.add("ml-3");
      h4.replaceWith(div);
      replacedElements.push({ original: h4, new: div });
    });
  }
                            """
        )
        await page.evaluate(
        """
                              function modifyImg() {
    const img = document.querySelector("img");
    if (img) {
      img.style.width = "150px";
      img.style.height = "auto";
    }
  }
                            """
    )
        
        await page.evaluate(
            """
                              function modifyHR() {
    const hrElements = document.querySelectorAll("hr");
    hrElements.forEach((hr) => {
      hr.style.marginTop = "0px";
      hr.style.marginBottom = "1px";
      hr.style.width = "100%";
      //hr.style.border = "none";
      hr.style.borderTop = "1px solid black";
    });
  }
                            """
        )
        
        await page.evaluate(
            """
        const content = document.getElementById("content-to-download");
        content.classList.remove("border-dark");
        content.style.margin = "0";
        //content.style.padding = "0";
        document.body.style.fontSize = "11px";
        document.body.style.fontFamily = "Arial";
                """
        )
        await page.emulate_media(media="print")
        await page.evaluate("""
            // Remove navbar (example: using class or id selector)
            const navbar = document.querySelector('nav');  // Adjust selector as needed
            if (navbar) {
                navbar.remove();
            }

            // Remove footer (example: using class or id selector)
            const footer = document.querySelector('footer');  // Adjust selector as needed
            if (footer) {
                footer.remove();
            }
            // remove download_cv button
            const download_cv = document.querySelector('#download_cv');  // Adjust selector as needed
            if (download_cv) {
                download_cv.remove();
            }
        """)
        await page.pdf(
            path=f"CV_DEV_{language.upper()}.pdf",
            format="A3",
            margin=None,
            print_background=True
        )
        await browser.close()


if __name__ == "__main__":
  for language in LANGUAGES:
      asyncio.run(download_pdf(language))
