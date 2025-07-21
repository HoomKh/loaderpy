from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document

from collections.abc import Iterable
from typing import Union
from pathlib import Path


def pypdf_loader(
    path: Union[str, Path, list[str], list[Path]],
) -> list[Document]:
    if isinstance(path, Iterable):
        output = []
        for p in path:
            loader = PyPDFLoader(p)
            docs = list(loader.load())
            for doc in docs:
                output.append(doc)
        return output

    elif isinstance(path, str):
        try:
            loader = PyPDFLoader(path)
            output = list(loader.lazy_load())
        except Exception as e:
            raise ValueError(f"error while loading file : \n{e}")
        return output
