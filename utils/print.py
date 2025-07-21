from typing import Literal, Union, Sequence
from collections.abc import Iterable
from langchain_core.documents import Document


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