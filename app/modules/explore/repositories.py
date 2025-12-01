import re

import unidecode
<<<<<<< HEAD
from sqlalchemy import or_

from app.modules.dataset.models import Author, DataSet, DSMetaData, PublicationType
=======
from sqlalchemy import any_, or_

from app.modules.dataset.models import Author, DataSet, DSMetaData, PublicationType, Community
<<<<<<< HEAD

=======
>>>>>>> origin/trunk
from app.modules.featuremodel.models import FeatureModel, FMMetaData
>>>>>>> 60e60f3715d5b2d66af5f212768c480611e6dcdb
from core.repositories.BaseRepository import BaseRepository


class ExploreRepository(BaseRepository):
    def __init__(self):
        super().__init__(DataSet)

<<<<<<< HEAD
    def filter(
        self,
        query="",
        sorting="newest",
        publication_type="any",
        tags=None,
        description="",
        authors="",
        affiliation="",
        orcid="",
        csv_filename="",
        csv_title="",
        publication_doi="",
        **kwargs,
    ):
=======
    def filter(self, query="", sorting="newest", publication_type="any", tags=[], community_id=None, **kwargs):
        # Normalize and remove unwanted characters
        normalized_query = unidecode.unidecode(query).lower()
        cleaned_query = re.sub(r'[,.":\'()\[\]^;!¡¿?]', "", normalized_query)

        filters = []
        for word in cleaned_query.split():
            filters.append(DSMetaData.title.ilike(f"%{word}%"))
            filters.append(DSMetaData.description.ilike(f"%{word}%"))
            filters.append(Author.name.ilike(f"%{word}%"))
            filters.append(Author.affiliation.ilike(f"%{word}%"))
            filters.append(Author.orcid.ilike(f"%{word}%"))
            filters.append(DSMetaData.tags.ilike(f"%{word}%"))
>>>>>>> origin/trunk

        datasets = (
            self.model.query.join(DataSet.ds_meta_data)
            .join(DSMetaData.authors)
<<<<<<< HEAD
=======
            .join(DataSet.feature_models)
            .join(FeatureModel.fm_meta_data)
<<<<<<< HEAD
        )

        normalized_query = unidecode.unidecode(query).lower()
        cleaned_query = re.sub(r'[,.":\'()\[\]^;!¡¿?]', "", normalized_query)
        datasets = datasets.filter(DSMetaData.dataset_doi.isnot(None))
        if query:
            datasets = datasets.filter(DSMetaData.title.ilike(f"%{cleaned_query}%"))

        if description:
            datasets = datasets.filter(DSMetaData.description.ilike(f"%{description}%"))
        if authors:
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
        if tags:
            datasets = datasets.filter(or_(FMMetaData.tags.ilike(f"%{tags}%"), DSMetaData.tags.ilike(f"%{tags}%")))

        if publication_type != "any":
            for member in PublicationType:
                if member.value.lower() == publication_type:
                    datasets = datasets.filter(DSMetaData.publication_type == member.name)
                    break

        # Orden
        datasets = datasets.order_by(
            self.model.created_at.asc() if sorting == "oldest" else self.model.created_at.desc()
        )
=======
>>>>>>> 60e60f3715d5b2d66af5f212768c480611e6dcdb
            .filter(or_(*filters))
            .filter(DSMetaData.dataset_doi.isnot(None))  # Exclude datasets with empty dataset_doi
        )

        if community_id is not None and community_id != "":
            try:
                community_id_int = int(community_id)
                
                if community_id_int > 0: 
                    datasets = datasets.filter(
                        DataSet.communities.any(Community.id == community_id_int)
                    )
            except ValueError:
                pass

        if publication_type != "any":
            matching_type = None
            for member in PublicationType:
                if member.value.lower() == publication_type:
                    matching_type = member
                    break

            if matching_type is not None:
                datasets = datasets.filter(DSMetaData.publication_type == matching_type.name)

        if tags:
            datasets = datasets.filter(DSMetaData.tags.ilike(any_(f"%{tag}%" for tag in tags)))

        # Order by created_at
        if sorting == "oldest":
            datasets = datasets.order_by(self.model.created_at.asc())
        else:
            datasets = datasets.order_by(self.model.created_at.desc())
>>>>>>> origin/trunk

        return datasets.all()
