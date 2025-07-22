from typing import Union, Sequence
from collections.abc import Iterable
from PIL import Image
from IPython.display import HTML, display
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import fitz
from langchain_core.documents import Document


# Unstructured print/plot
def print_unstructured_page(
    docs: list[Document],
    *,
    pages: Union[int, Sequence[int], None] = None,
    start_page: int | None = None,
    end_page: int | None = None,
    show_metadata: bool = False,
    ignore_metadata_keys: Sequence[str] | None = ("coordinates", "bbox"),
) -> None:

    # Resolve which page numbers we want
    if pages is not None:
        if isinstance(pages, int):
            page_number = [pages]
        elif isinstance(pages, Iterable):
            page_number = sorted(set(int(p) for p in pages))
        else:
            raise TypeError("pages must be int or iterable of ints")

    else:
        if start_page is None or end_page is None:
            raise ValueError(
                "Provide either `pages` or both `start_page` and `end_page`"
            )
        if start_page < 1 or end_page < start_page:
            raise ValueError("1 <= start_page <= end_page is required!")
        page_number = list(range(start_page, end_page + 1))

    # Print each requested page
    for page in page_number:
        page_docs = [d for d in docs if d.metadata.get("page_number") == page]

        if not page_docs:
            print(f"⚠️  No content found for page {page}\n")
            continue

        print(f"\n📄 Page {page} content\n" + "-" * 30)
        for idx, doc in enumerate(page_docs, 1):
            print(f"[{idx}] {doc.page_content}\n")

        if show_metadata:
            meta = _unstructured_page_metadata(
                page_docs=page_docs, ignore_keys=ignore_metadata_keys
            )
            print("📑 Page Level Metadata: ")
            print(meta, "\n")
            print("📑 Metadata (first chunk):")
            print(page_docs[0].metadata, "\n")


def _unstructured_page_metadata(
    page_docs: list[Document],
    ignore_keys: tuple[str, ...] | None = None,
) -> dict[str, object]:
    if not page_docs:
        return {}

    ignore_keys = tuple(ignore_keys or ())
    first_meta = page_docs[0].metadata
    common: dict[str, object] = {}

    for key, first_val in first_meta.items():
        if key in ignore_keys:
            continue
        if all(doc.metadata.get(key) == first_val for doc in page_docs):
            common[key] = first_val

    return common


def plot_pdf_with_boxes(pdf_page: fitz.Page, segments: list[dict]):
    pix = pdf_page.get_pixmap()
    pil_image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    fig, ax = plt.subplots(1, figsize=(10, 10))
    ax.imshow(pil_image)
    categories = set()
    category_to_color = {
        "Title": "orchid",
        "Image": "forestgreen",
        "Table": "tomato",
    }
    for segment in segments:
        points = segment["coordinates"]["points"]
        layout_width = segment["coordinates"]["layout_width"]
        layout_height = segment["coordinates"]["layout_height"]
        scaled_points = [
            (x * pix.width / layout_width, y * pix.height / layout_height)
            for x, y in points
        ]
        box_color = category_to_color.get(segment["category"], "deepskyblue")
        categories.add(segment["category"])
        rect = patches.Polygon(
            scaled_points, linewidth=1, edgecolor=box_color, facecolor="none"
        )
        ax.add_patch(rect)

    # Make legend
    legend_handles = [patches.Patch(color="deepskyblue", label="Text")]
    for category in ["Title", "Image", "Table"]:
        if category in categories:
            legend_handles.append(
                patches.Patch(color=category_to_color[category], label=category)
            )
    ax.axis("off")
    ax.legend(handles=legend_handles, loc="upper right")
    plt.tight_layout()
    plt.show()


# Pypdf print
def print_pypdf_page(
    docs: list[Document],
    *,
    pages: Union[int, Sequence[int], None] = None,
    start_page: int | None = None,
    end_page: int | None = None,
    show_metadata: bool = False,
) -> None:

    if pages is not None:
        if isinstance(pages, int):
            page_number = [pages]
        if isinstance(pages, Iterable):
            page_number = sorted(set(int(p) for p in pages))
        else:
            raise TypeError("pages must be int or iterable of ints")
    else:
        if start_page is None or end_page is None:
            raise ValueError(
                "Provide either `pages` or both `start_page` and `end_page`"
            )
        if start_page < 1 or end_page < start_page:
            raise ValueError("1 <= start_page <= end_page is required!")
        page_number = list(range(start_page, end_page + 1))

    for page in page_number:
        page_docs = docs[page]

        if not page_docs:
            print(f"⚠️  No content found for page {page}\n")
            continue

        print(f"\n📄 Page {page} content\n" + "-" * 30)
        print(f"{page_docs.page_content}\n")

        if show_metadata:
            print(f"📑 Metadata ({page}):")
            print(page_docs.metadata, "\n")
