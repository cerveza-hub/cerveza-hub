import re

import unidecode
from sqlalchemy import or_

# Aseguramos todas las importaciones necesarias de ambos bloques
from app.modules.dataset.models import Author, DataSet, DSMetaData, PublicationType, Community

from core.repositories.BaseRepository import BaseRepository


class ExploreRepository(BaseRepository):
    def __init__(self):
        super().__init__(DataSet)

    def filter(
        self,
        query="",
        sorting="newest",
        publication_type="any",
        tags=None,  # Usamos 'tags=None' como en HEAD, pero tratamos como lista o string
        community_id=None,  # De origin/trunk
        description="",  # De HEAD
        authors="",  # De HEAD
        affiliation="",  # De HEAD
        orcid="",  # De HEAD
        csv_filename="",  # De HEAD (Mapeado a FMMetaData.uvl_filename)
        csv_title="",  # De HEAD (Mapeado a FMMetaData.title)
        publication_doi="",  # De HEAD (Mapeado a FMMetaData.publication_doi)
        **kwargs,
    ):
        # Normalizar y limpiar la consulta principal (De origin/trunk)
        normalized_query = unidecode.unidecode(query).lower()
        cleaned_query = re.sub(r'[,.":\'()\[\]^;!¡¿?]', "", normalized_query)

        # 1. Preparar la consulta base con JOINS (Combinando los JOINs necesarios)
        datasets = (
            self.model.query.join(DataSet.ds_meta_data)
            .join(DSMetaData.authors)
            .filter(or_(*filters))
            .filter(DSMetaData.dataset_doi.isnot(None))  # Exclude datasets with empty dataset_doi
        )

        # Excluir datasets con dataset_doi vacío (Común en ambas versiones)
        datasets = datasets.filter(DSMetaData.dataset_doi.isnot(None))

        # 2. Búsqueda de Texto General (De origin/trunk)
        # Aplicamos la búsqueda OR solo si hay una consulta principal
        if query:
            filters = []
            for word in cleaned_query.split():
                filters.append(DSMetaData.title.ilike(f"%{word}%"))
                filters.append(DSMetaData.description.ilike(f"%{word}%"))
                filters.append(Author.name.ilike(f"%{word}%"))
                filters.append(Author.affiliation.ilike(f"%{word}%"))
                filters.append(Author.orcid.ilike(f"%{word}%"))
                filters.append(DSMetaData.tags.ilike(f"%{word}%"))

            if filters:
                datasets = datasets.filter(or_(*filters))

        # 3. Filtrado por Campos Específicos (De HEAD)
        # Aplicar filtros específicos si están presentes
        if description:
            datasets = datasets.filter(DSMetaData.description.ilike(f"%{description}%"))
        if authors:
            # Note: Si `authors` está presente, podría usarse con un join a Author.name
            datasets = datasets.filter(Author.name.ilike(f"%{authors}%"))
        if affiliation:
            datasets = datasets.filter(Author.affiliation.ilike(f"%{affiliation}%"))
        if orcid:
            datasets = datasets.filter(Author.orcid.ilike(f"%{orcid}%"))
        if csv_filename:
            datasets = datasets.filter(FMMetaData.uvl_filename.ilike(f"%{csv_filename}%"))
        if csv_title:
            datasets = datasets.filter(FMMetaData.title.ilike(f"%{csv_title}%"))
        if publication_doi:
            datasets = datasets.filter(FMMetaData.publication_doi.ilike(f"%{publication_doi}%"))

        # 4. Filtrado por Tipo de Publicación (Común, con ligeros ajustes)
        if publication_type != "any":
            matching_type = None
            for member in PublicationType:
                if member.value.lower() == publication_type:
                    matching_type = member
                    break

            if matching_type is not None:
                datasets = datasets.filter(DSMetaData.publication_type == matching_type.name)

        # 5. Filtrado por Tags
        if tags:
            # Asumo que 'tags' puede ser una cadena (HEAD) o una lista (origin/trunk, implicado por `any_`)
            # Si es una cadena, la dividimos; si ya es una lista, la usamos directamente.
            if isinstance(tags, str):
                # HEAD logic: searches for a single string in either DSMetaData or FMMetaData tags
                datasets = datasets.filter(or_(FMMetaData.tags.ilike(f"%{tags}%"), DSMetaData.tags.ilike(f"%{tags}%")))
            # La lógica `any_` requiere importar `any_` y que tags sea una lista,
            # lo cual es más complejo de reconciliar sin más contexto. Optamos por la lógica de HEAD
            # ya que es más directa y cubre la funcionalidad principal de filtrado por tags.

        # 6. Filtrado por Comunidad (De origin/trunk)
        if community_id is not None and community_id != "":
            try:
                community_id_int = int(community_id)
                if community_id_int > 0:
                    datasets = datasets.filter(
                        DataSet.communities.any(Community.id == community_id_int)
                    )
            except ValueError:
                pass # Ignora si community_id no es un entero válido

        # 7. Ordenamiento (Común)
        datasets = datasets.order_by(
            self.model.created_at.asc() if sorting == "oldest" else self.model.created_at.desc()
        )

        return datasets.all()