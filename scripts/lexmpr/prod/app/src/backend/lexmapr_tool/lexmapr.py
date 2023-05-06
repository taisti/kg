# IMPORTANT: Below codes uses parts of LexMapr tool to fit into our project needs

import re
from collections import OrderedDict
from itertools import permutations
from typing import Any

import lexmapr.pipeline_resources as pipeline_resources
import lexmapr.pipeline_helpers as helpers
import pandas as pd
from nltk import word_tokenize


class LexMaprTool:
    def __init__(self, config_path: str):
        # To contain all resources, and their variations, that samples are
        # matched to.  Start by adding pre-defined resources from
        # lexmapr.predefined_resources.
        self.lookup_table = pipeline_resources.get_predefined_resources()

        # Scientific names dictionary fetched from lookup tables.
        self.scientific_names_dict = pipeline_resources.get_resource_dict("foodon_ncbi_synonyms.csv")

        # Fetch online ontology terms specified in config file.
        self.ontology_lookup_table = pipeline_resources.get_config_resources(config_path, no_cache=True)

        # Merge ``ontology_lookup_table`` into ``lookup_table``
        self.lookup_table = helpers.merge_lookup_tables(self.lookup_table, self.ontology_lookup_table)

    def run(self, text: str) -> pd.Series:
        original_sample = text.strip()
        cleaned_sample = ""
        cleaned_sample_scientific_name = ""
        matched_components = []
        macro_status = "No Match"
        micro_status: Any = []
        sample_conversion_status = {}

        # Standardize sample to lowercase and with punctuation
        # treatment.
        sample = original_sample.lower()
        sample = helpers.punctuation_treatment(sample)

        sample_tokens = word_tokenize(sample)

        # Get ``cleaned_sample``
        for token in sample_tokens:
            # Ignore dates
            if helpers.is_date(token) or helpers.is_number(token):
                continue
            # Some preprocessing
            token = helpers.preprocess(token)

            lemma = helpers.singularize_token(token, self.lookup_table, micro_status)
            lemma = helpers.spelling_correction(lemma, self.lookup_table, micro_status)
            lemma = helpers.abbreviation_normalization_token(lemma, self.lookup_table, micro_status)
            lemma = helpers.non_English_normalization_token(lemma, self.lookup_table, micro_status)
            if not token == lemma:
                sample_conversion_status[token] = lemma
            cleaned_sample = helpers.get_cleaned_sample(cleaned_sample, lemma, self.lookup_table)
            cleaned_sample = re.sub(' +', ' ', cleaned_sample)
            cleaned_sample = helpers.abbreviation_normalization_phrase(cleaned_sample,
                                                                       self.lookup_table, micro_status)
            cleaned_sample = helpers.non_English_normalization_phrase(cleaned_sample, self.lookup_table,
                                                                      micro_status)
            cleaned_sample_scientific_name = helpers.get_annotated_sample(
                cleaned_sample_scientific_name, lemma, self.scientific_names_dict)
            cleaned_sample_scientific_name = re.sub(' +', ' ', cleaned_sample_scientific_name)

        cleaned_sample = helpers.remove_duplicate_tokens(cleaned_sample)

        # Attempt full term match
        full_term_match = helpers.map_term(sample, self.lookup_table)

        if not full_term_match:
            # Attempt full term match with cleaned sample
            full_term_match = helpers.map_term(cleaned_sample, self.lookup_table)
            if full_term_match:
                micro_status.insert(0, "Used Cleaned Sample")

        if not full_term_match:
            # Attempt full term match using suffixes
            full_term_match = helpers.map_term(sample, self.lookup_table, consider_suffixes=True)

        if not full_term_match:
            # Attempt full term match with cleaned sample using suffixes
            full_term_match = \
                helpers.map_term(cleaned_sample, self.lookup_table, consider_suffixes=True)
            if full_term_match:
                micro_status.insert(0, "Used Cleaned Sample")

        if full_term_match:
            matched_components.append(full_term_match["term"] + ":" + full_term_match["id"])
            macro_status = "Full Term Match"
            micro_status += full_term_match["status"]
        else:
            # Attempt various component matches
            component_matches = []
            covered_tokens = set()

            for i in range(5, 0, -1):
                for gram_chunk in helpers.get_gram_chunks(cleaned_sample, i):
                    concat_gram_chunk = " ".join(gram_chunk)
                    gram_tokens = word_tokenize(concat_gram_chunk)
                    gram_permutations = \
                        list(OrderedDict.fromkeys(permutations(concat_gram_chunk.split())))

                    # gram_tokens covered in prior component match
                    if set(gram_tokens) <= covered_tokens:
                        continue

                    for gram_permutation in gram_permutations:
                        gram_permutation_str = " ".join(gram_permutation)
                        component_match = helpers.map_term(gram_permutation_str, self.lookup_table)

                        if not component_match:
                            # Try again with suffixes
                            component_match = helpers.map_term(gram_permutation_str, self.lookup_table,
                                                               consider_suffixes=True)

                        if component_match:
                            component_matches.append(component_match)
                            covered_tokens.update(gram_tokens)
                            break

            # We need should not consider component matches that are
            # ancestral to other component matches.
            ancestors = set()
            for component_match in component_matches:
                component_match_hierarchies = \
                    helpers.get_term_parent_hierarchies(component_match["id"], self.lookup_table)

                for component_match_hierarchy in component_match_hierarchies:
                    # We do not need the first element
                    component_match_hierarchy.pop(0)

                    ancestors |= set(component_match_hierarchy)

            for component_match in component_matches:
                if component_match["id"] not in ancestors:
                    matched_component = component_match["term"] + ":" + component_match["id"]
                    matched_components.append(matched_component)

            # We do need it, but perhaps the function could be
            #  simplified?
            if len(matched_components):
                matched_components = helpers.retain_phrase(matched_components)

            # Finalize micro_status
            micro_status_covered_matches = set()
            for component_match in component_matches:
                possible_matched_component = component_match["term"] + ":" + component_match["id"]
                if possible_matched_component in matched_components:
                    if possible_matched_component not in micro_status_covered_matches:
                        micro_status_covered_matches.add(possible_matched_component)
                        micro_status.append("{%s: %s}"
                                            % (component_match["term"], component_match["status"]))

            if matched_components:
                macro_status = "Component Match"

        # Write to row
        matched_components = helpers.get_matched_component_standardized(matched_components)

        results = pd.Series({
            "Matched_Components": str(matched_components),
            "Match_Status(Macro Level)": macro_status
        })
        return results
