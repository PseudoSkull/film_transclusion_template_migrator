import pywikibot

from edit_mw import get_category_items, save_page

# Define the site
site = pywikibot.Site('en', 'wikisource')

# Define the category

category_items = get_category_items(site, "film")

for page_title in category_items:

    page = pywikibot.Page(site, page_title)
    page_text = page.text
    div_in_page_text = "<div" in page_text
    page_tag_in_page_text = "{{page|" in page_text.lower()

    # if div_in_page_text and not "</div>" in page_text:
    #     print(page_title)
    

    if not div_in_page_text or not page_tag_in_page_text:
        print(page_title)
        print(f"Has <div: ", div_in_page_text)
        print(f"Has {{{{page|: ", page_tag_in_page_text)

    if page_tag_in_page_text and "{{Film transclusion" not in page_text:
        if div_in_page_text:
            
            page_text = page_text.replace(">{{", ">\n{{")
            page_text = page_text.replace("}}</div>", "}}\n</div>")
            
            # replace div with Film transcription template
            page_text_lines = page_text.split("\n")

            new_text_lines = []

            for line in page_text_lines:
                if line.startswith("<div"):
                    line = "{{Film transclusion|"
                new_text_lines.append(line)
            
            page_text = "\n".join(new_text_lines)

            # end template
            page_text = page_text.replace("</div>", "}}")
        
        else:
            # replace first instance of {{page| with {{Film transclusion

            page_text = page_text.replace("{{page|", "{{Film transclusion|\n{{page|", 1)
            page_text = page_text.replace("{{Page|", "{{Film transclusion|\n{{Page|", 1)


            # replace last {{page| with end template of film transclusion
            page_text_lines = page_text.split("\n")

            counting_page_templates = False
            new_text_lines = []

            for line in page_text_lines:
                page_template_in_line = "{{page|" in line.lower()
                if page_template_in_line:
                    counting_page_templates = True
                if counting_page_templates and not page_template_in_line:
                    line = f"}}}}\n{line}"
                    counting_page_templates = False
                new_text_lines.append(line)
            
            page_text = "\n".join(new_text_lines)
        
        save_page(page, site, page_text, "Wrapping film pages into {{tl|Film transclusion}}, a new template that standardizes film transcription styling")



    # if page_tag_in_page_text and not div_in_page_text:
    #     page = page.replace("{{page|", "{{")
    #     page = page.replace("{{page|", "{{")

    # print(page.text)