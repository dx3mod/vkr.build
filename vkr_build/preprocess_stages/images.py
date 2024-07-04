from bs4 import BeautifulSoup

from vkr_build.preprocess_stages.stage import PreprocessStage


class ImagesPreprocessStage(PreprocessStage):
    def process(self, soup: BeautifulSoup):
        for image_tag in soup.select("img"):
            image_tag["style"] = image_tag.get("style") or ""

            if image_tag.has_attr("width"):
                width = image_tag.attrs["width"]
                width = f"{width}px" if not width.endswith(("px", "%")) else width

                image_tag["style"] += f"width: {width};"
